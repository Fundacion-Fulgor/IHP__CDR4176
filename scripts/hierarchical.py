"""
Created by Phase Interpolator team (Victor Muñoz & Agustina Trabichet)

hierarchical.py

- Construye jerarquía Layout desde SPICE (xschem) leyendo el TEXTO del netlist.
- Reusa celdas de GDS existentes por nombre (autoload desde sch_path o reuse_dir, y/o reuse manual).
- FIX: NO interpreta XM1/XM2 como instancias jerárquicas: solo instancia subckts reales.
- Opcional: genera PCells de tecnología (MOS/R/C/antennas) cuando el netlist NO tiene jerarquía interna
  o cuando un subckt NO tiene layout reusado (celda vacía).

Flags (klayout -rd ...)
- netlist=<path>   (requerido)
- output=<path>    (requerido)
- reuse=<path.gds> (opcional)
- autoload=0/1     (opcional)  carga gds candidatos desde sch_path (.sch->.gds) y/o reuse_dir
- reuse_dir=<dir>  (opcional)  dir para buscar <cell>.gds
- leaf=0/1         (opcional)  1 = generar PCells para leaf devices (como tu script original)
- gallery=0/1      (opcional)  1 = crea una celda "gallery" con los leaf PCells generados
"""

from __future__ import annotations

import pathlib
import sys
import re
from typing import Dict, List, Tuple, Set, Optional

try:
    import pya
except ImportError:
    pya = None

try:
    import klayout.db
except ImportError:
    klayout = None

try:
    _file_path = pathlib.Path(__file__).resolve()
    if _file_path.parent.name == "scripts":
        REPO_ROOT = _file_path.parent.parent
    else:
        REPO_ROOT = _file_path.parent
except Exception:
    REPO_ROOT = pathlib.Path.cwd()


# -----------------------------
# Config
# -----------------------------
PCELL_LIB = "SG13_dev"  # librería PCells (IHP SG13G2)

# Modelos de netlist -> nombre PCell en SG13_dev
MOS_PCELLS = {
    "sg13_lv_nmos": "nmos",
    "sg13_hv_nmos": "nmosHV",
    "sg13_lv_pmos": "pmos",
    "sg13_hv_pmos": "pmosHV",
}

RES_PCELLS = {
    "rppd": "rppd",
    "rhigh": "rhigh",
    "rsil": "rsil",
}

CAP_PCELLS = {
    "cap_cmim": "cmim",
}

ANT_PCELLS = {
    "dantenna": "dantenna",
    "dpantenna": "dpantenna",
}


# -----------------------------
# Helpers
# -----------------------------
def _rd_bool(v, default: bool = False) -> bool:
    if v is None:
        return default
    s = str(v).strip().lower()
    return s in ("1", "true", "yes", "y", "on")


def _basename_noext(path: str) -> str:
    return pathlib.Path(path).stem


def _norm_name(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", str(s).lower()) if s is not None else ""


def _maybe_uncomment_spice_directive(line: str) -> Optional[str]:
    """
    - directivas comentadas tipo **.subckt, *.ends, *.ipin, etc => las "descomenta"
    - comentario normal => None
    - línea normal => limpia
    """
    s = line.strip()
    if not s:
        return None
    if s.startswith("*"):
        if re.match(r"^\*+\.((subckt)|(ends)|(ipin)|(opin)|(iopin))\b", s, re.IGNORECASE):
            return s.lstrip("*").strip()
        return None
    return s


def _parse_params(tokens: List[str]) -> Dict[str, str]:
    out: Dict[str, str] = {}
    for t in tokens:
        if "=" in t:
            k, v = t.split("=", 1)
            out[k.strip().lower()] = v.strip()
    return out


_SPICE_SUFFIX = {
    "t": 1e12,
    "g": 1e9,
    "meg": 1e6,
    "k": 1e3,
    "m": 1e-3,
    "u": 1e-6,
    "n": 1e-9,
    "p": 1e-12,
    "f": 1e-15,
}


def _to_float_spice(x: str) -> float:
    """
    Parse de número SPICE con sufijos (u,n,p,m,k,meg,...) o notación científica.
    Devuelve valor en unidades base (sin asumir um/m).
    """
    s = str(x).strip().lower()

    # meg (3 letras)
    if s.endswith("meg"):
        return float(s[:-3]) * _SPICE_SUFFIX["meg"]

    # sufijo 1 letra
    m = re.match(r"^([+-]?\d*\.?\d+(?:e[+-]?\d+)?)\s*([a-z])?$", s)
    if m:
        num = float(m.group(1))
        suf = m.group(2)
        if suf and suf in _SPICE_SUFFIX:
            return num * _SPICE_SUFFIX[suf]
        return num

    # fallback
    return float(s)


def _len_to_um(x: str) -> float:
    """
    Convierte a micrómetros.
    Heurística:
      - si trae sufijo (u,n,...) se interpreta como SI y se convierte a um
      - si no trae sufijo:
           si valor < 1e-3 -> asumimos metros
           else -> asumimos ya está en um
    """
    s = str(x).strip().lower()
    has_suffix = bool(re.search(r"(meg|[a-z])$", s)) and not bool(re.search(r"e[+-]?\d+$", s))
    val = _to_float_spice(s)

    if has_suffix:
        # val está en SI (metros si el parámetro era longitud con u/n/etc)
        return val * 1e6

    # sin sufijo: heurística
    if abs(val) < 1e-3:
        return val * 1e6  # metros -> um
    return val  # ya um


# -----------------------------
# Reuse / Cells
# -----------------------------
def build_existing_cell_map(layout: klayout.db.Layout) -> Dict[str, int]:
    m: Dict[str, int] = {}
    for cell in layout.each_cell():
        m[_norm_name(cell.name)] = cell.cell_index()
    return m


def get_or_create_cell_index(layout: klayout.db.Layout, name: str, existing_map: Dict[str, int]) -> int:
    nn = _norm_name(name)
    if nn in existing_map:
        return existing_map[nn]

    c = layout.cell(name)
    if c is None:
        c = layout.create_cell(name)

    existing_map[nn] = c.cell_index()
    return c.cell_index()


def _cell_has_content(cell: klayout.db.Cell) -> bool:
    """
    True si la celda ya tiene algo (instancias o shapes).
    Útil para no "reconstruir" una celda que ya vino de un reuse.gds/autoload.
    """
    try:
        if cell.each_inst().at_end() is False:
            return True
    except Exception:
        # fallback si API cambia
        pass

    try:
        # revisa shapes en cualquier layer
        for li in cell.layout().layer_indices():
            if not cell.shapes(li).is_empty():
                return True
    except Exception:
        pass

    return False


# -----------------------------
# Netlist reader (validación)
# -----------------------------
def read_hierarchical_netlist(spice_path: str) -> klayout.db.Netlist:
    nl = klayout.db.Netlist()
    reader = klayout.db.NetlistSpiceReader()
    nl.read(spice_path, reader)
    return nl


# -----------------------------
# Autoload de GDS desde netlist
# -----------------------------
def parse_sch_paths(netlist_text: str) -> List[str]:
    out: List[str] = []
    for raw in netlist_text.splitlines():
        m = re.search(r"\bsch_path:\s*(.+)", raw)
        if m:
            val = m.group(1).strip()
            if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                val = val[1:-1].strip()
            if val:
                out.append(val)
    return out


def sch_to_gds_candidates(sch_path: str, reuse_dir: Optional[str] = None) -> List[str]:
    p = pathlib.Path(sch_path)
    cell = p.stem
    candidates: List[str] = []
    if p.suffix.lower() == ".sch":
        candidates.append(str(p.with_suffix(".gds")))
        if not p.is_absolute():
            candidates.append(str(REPO_ROOT / p.with_suffix(".gds")))

    candidates.append(str(REPO_ROOT / "CDR4176-main" / "layout" / "klayout" / cell / f"{cell}.gds"))
    candidates.append(str(pathlib.Path("CDR4176-main") / "layout" / "klayout" / cell / f"{cell}.gds"))
    candidates.append(str(pathlib.Path("layout") / "klayout" / cell / f"{cell}.gds"))

    if "schematic/xschem" in sch_path:
        cand = sch_path.replace("schematic/xschem", "layout/klayout")
        if cand.endswith(".sch"):
            cand = cand[:-4] + ".gds"
        candidates.append(cand)
        cand_p = pathlib.Path(cand)
        if not cand_p.is_absolute():
            candidates.append(str(REPO_ROOT / cand_p))

    if reuse_dir:
        r = pathlib.Path(reuse_dir)
        candidates.append(str(r / cell / f"{cell}.gds"))
        candidates.append(str(r / f"{cell}.gds"))
        if not r.is_absolute():
            candidates.append(str(REPO_ROOT / r / cell / f"{cell}.gds"))
            candidates.append(str(REPO_ROOT / r / f"{cell}.gds"))

    out: List[str] = []
    seen = set()
    for c in candidates:
        if "legacy" in pathlib.Path(c).parts:
            continue
        if c not in seen:
            seen.add(c)
            out.append(c)
    return out


def autoload_reuse_gds(layout: klayout.db.Layout, netlist_text: str, reuse_dir: Optional[str] = None):
    sch_paths = parse_sch_paths(netlist_text)
    seen = set()
    for sch in sch_paths:
        for gds in sch_to_gds_candidates(sch, reuse_dir=reuse_dir):
            if "legacy" in pathlib.Path(gds).parts:
                continue
            if gds in seen:
                continue
            seen.add(gds)
            if pathlib.Path(gds).exists():
                try:
                    layout.read(gds)
                    break
                except Exception:
                    pass


# -----------------------------
# Parse SPICE: subckts + instancias
# -----------------------------
def parse_spice(netlist_text: str) -> Tuple[List[str], Set[str], Dict[str, List[Dict]]]:
    """
    Retorna:
      subckts_order: lista subckts en orden
      subckts_set: set subckts
      inst_map: parent -> list of instances dict:
          {"kind":"subckt","child":"inv"}
          {"kind":"leaf","model":"sg13_lv_nmos","params":{...}}
    """
    cooked_lines: List[str] = []
    for raw in netlist_text.splitlines():
        line = _maybe_uncomment_spice_directive(raw)
        if line is not None:
            cooked_lines.append(line)

    # primer pase: subckts
    subckts_order: List[str] = []
    subckts_set: Set[str] = set()
    for line in cooked_lines:
        m = re.match(r"\.subckt\s+(\S+)", line, re.IGNORECASE)
        if m:
            name = m.group(1)
            subckts_order.append(name)
            subckts_set.add(name)

    # segundo pase: instancias
    inst_map: Dict[str, List[Dict]] = {}
    current: Optional[str] = None

    for line in cooked_lines:
        m = re.match(r"\.subckt\s+(\S+)", line, re.IGNORECASE)
        if m:
            current = m.group(1)
            inst_map.setdefault(current, [])
            continue

        if re.match(r"\.ends\b", line, re.IGNORECASE):
            current = None
            continue

        if current and (line[0] == "X" or line[0] == "x"):
            toks = line.split()
            if len(toks) < 2:
                continue

            # child/model: último token que NO sea key=val
            child = None
            child_pos = None
            for i in range(len(toks) - 1, 0, -1):
                if "=" in toks[i]:
                    continue
                child = toks[i]
                child_pos = i
                break
            if not child:
                continue

            params = _parse_params(toks[child_pos + 1 :]) if child_pos is not None else {}

            # FIX: solo es jerárquico si child es subckt definido
            if child in subckts_set:
                inst_map[current].append({"kind": "subckt", "child": child})
            else:
                inst_map[current].append({"kind": "leaf", "model": child, "params": params})

    return subckts_order, subckts_set, inst_map


# -----------------------------
# PCell factory + cache
# -----------------------------
class PCellFactory:
    def __init__(self, layout: klayout.db.Layout, lib: pya.Library):
        self.layout = layout
        self.lib = lib
        self.cache: Dict[Tuple[str, Tuple[Tuple[str, str], ...]], int] = {}  # (pcell_name, sorted_params) -> cell_index

    def _get_variant(self, pcell_name: str, params: Dict[str, str]) -> Optional[int]:
        decl = self.lib.layout().pcell_declaration(pcell_name)
        if decl is None:
            return None
        key = (pcell_name, tuple(sorted((str(k), str(v)) for k, v in params.items())))
        if key in self.cache:
            return self.cache[key]

        idx = self.layout.add_pcell_variant(self.lib, decl.id(), params)
        self.cache[key] = idx
        return idx

    def create_mos(self, model: str, params: Dict[str, str]) -> Optional[int]:
        mkey = model.strip()
        if mkey not in MOS_PCELLS:
            return None
        pcell_name = MOS_PCELLS[mkey]

        w_um = _len_to_um(params.get("w", "0.15u"))
        l_um = _len_to_um(params.get("l", "0.13u"))
        ng = params.get("ng", "1")

        return self._get_variant(
            pcell_name,
            {"w": f"{w_um}u", "l": f"{l_um}u", "ng": f"{int(float(ng))}"},
        )

    def create_res(self, model: str, params: Dict[str, str]) -> Optional[int]:
        mkey = model.strip()
        if mkey not in RES_PCELLS:
            return None
        pcell_name = RES_PCELLS[mkey]

        w_um = _len_to_um(params.get("w", "1e-6"))
        l_um = _len_to_um(params.get("l", "1e-6"))
        b = params.get("b", "0")

        return self._get_variant(
            pcell_name,
            {"w": f"{w_um}u", "l": f"{l_um}u", "b": f"{int(float(b))}"},
        )

    def create_cap(self, model: str, params: Dict[str, str]) -> Optional[int]:
        mkey = model.strip()
        if mkey not in CAP_PCELLS:
            return None
        pcell_name = CAP_PCELLS[mkey]

        w_um = _len_to_um(params.get("w", "1e-6"))
        l_um = _len_to_um(params.get("l", "1e-6"))

        return self._get_variant(
            pcell_name,
            {"w": f"{w_um}u", "l": f"{l_um}u"},
        )

    def create_ant(self, model: str, params: Dict[str, str]) -> Optional[int]:
        mkey = model.strip()
        if mkey not in ANT_PCELLS:
            return None
        pcell_name = ANT_PCELLS[mkey]

        w_um = _len_to_um(params.get("w", "0.3u"))
        l_um = _len_to_um(params.get("l", "0.3u"))

        return self._get_variant(
            pcell_name,
            {"w": f"{w_um}u", "l": f"{l_um}u"},
        )

    def create_leaf(self, model: str, params: Dict[str, str]) -> Optional[int]:
        # intenta en orden (como tu script original)
        idx = self.create_res(model, params)
        if idx is not None:
            return idx
        idx = self.create_mos(model, params)
        if idx is not None:
            return idx
        idx = self.create_cap(model, params)
        if idx is not None:
            return idx
        idx = self.create_ant(model, params)
        if idx is not None:
            return idx
        return None

    def all_cached_cells(self) -> List[int]:
        return list(set(self.cache.values()))


# -----------------------------
# Construcción Layout: jerarquía + leaf PCells
# -----------------------------
def build_layout(
    layout: klayout.db.Layout,
    netlist_text: str,
    desired_top_name: str,
    existing_map: Dict[str, int],
    leaf_enable: bool,
    margin_um: float = 5.0,
    fallback_step_um: float = 20.0,
) -> List[int]:
    """
    Devuelve lista de cell_indices de PCells leaf creadas (para gallery opcional).
    """
    subckts_order, subckts_set, inst_map = parse_spice(netlist_text)
    if not subckts_order:
        raise RuntimeError("No se encontraron .subckt en el netlist (ni comentados como **.subckt).")

    top_subckt = subckts_order[0]

    # crear/reusar celdas para subckts
    cell_map: Dict[str, int] = {}
    for s in subckts_set:
        cell_map[s] = get_or_create_cell_index(layout, s, existing_map)

    margin = int(margin_um / layout.dbu)
    fallback_step = int(fallback_step_um / layout.dbu)

    # PCell factory
    factory = None
    if leaf_enable:
        lib = pya.Library.library_by_name(PCELL_LIB)
        if lib is not None:
            factory = PCellFactory(layout, lib)

    # poblar cada subckt SOLO si está vacío (si vino de reuse/autoload, lo dejamos tal cual)
    for parent, insts in inst_map.items():
        parent_id = cell_map.get(parent)
        if parent_id is None:
            parent_id = get_or_create_cell_index(layout, parent, existing_map)
            cell_map[parent] = parent_id

        parent_cell = layout.cell(parent_id)

        if _cell_has_content(parent_cell):
            # ya tiene layout (reuse/autoload). No reconstruir.
            continue

        x = 0
        y = 0

        for inst in insts:
            if inst["kind"] == "subckt":
                child = inst["child"]
                child_id = cell_map.get(child)
                if child_id is None:
                    child_id = get_or_create_cell_index(layout, child, existing_map)
                    cell_map[child] = child_id

                parent_cell.insert(
                    klayout.db.CellInstArray(
                        child_id,
                        klayout.db.Trans(klayout.db.Point(x, y)),
                    )
                )

                child_bbox = layout.cell(child_id).bbox()
                step = child_bbox.width() + margin
                if step <= margin:
                    step = fallback_step
                x += step

            else:
                # leaf device -> PCell
                if not leaf_enable or factory is None:
                    continue

                model = inst["model"]
                params = inst["params"]

                # multiplicidad m=...
                m_str = params.get("m", "1")
                try:
                    mult = int(float(m_str))
                except Exception:
                    mult = 1
                mult = max(1, mult)

                for _ in range(mult):
                    pcell_idx = factory.create_leaf(model, params)
                    if pcell_idx is None:
                        # modelo leaf no soportado -> skip
                        x += fallback_step
                        continue

                    parent_cell.insert(
                        klayout.db.CellInstArray(
                            pcell_idx,
                            klayout.db.Trans(klayout.db.Point(x, y)),
                        )
                    )
                    bb = layout.cell(pcell_idx).bbox()
                    step = bb.width() + margin
                    if step <= margin:
                        step = fallback_step
                    x += step

    # wrapper top (evitar ciclos)
    if _norm_name(desired_top_name) != _norm_name(top_subckt):
        wrapper_id = get_or_create_cell_index(layout, desired_top_name, existing_map)
        wrapper_cell = layout.cell(wrapper_id)
        if _cell_has_content(wrapper_cell) is False:
            wrapper_cell.insert(
                klayout.db.CellInstArray(
                    cell_map[top_subckt],
                    klayout.db.Trans(klayout.db.Point(0, 0)),
                )
            )

    return factory.all_cached_cells() if factory is not None else []


# -----------------------------
# Gallery opcional
# -----------------------------
def build_gallery(layout: klayout.db.Layout, leaf_cells: List[int], name: str = "gallery"):
    """
    Crea una celda "gallery" y pone una instancia de cada PCell leaf generado.
    """
    if not leaf_cells:
        return

    gid = layout.add_cell(name)
    gcell = layout.cell(gid)

    margin = int(5.0 / layout.dbu)
    x = 0
    y = 0
    row_h = 0

    for idx in leaf_cells:
        bb = layout.cell(idx).bbox()
        if x > 0 and x + bb.width() > int(2000 / layout.dbu):  # wrap a la siguiente fila
            x = 0
            y += row_h + margin
            row_h = 0

        gcell.insert(klayout.db.CellInstArray(idx, klayout.db.Trans(klayout.db.Point(x, y))))
        x += bb.width() + margin
        row_h = max(row_h, bb.height())


# -----------------------------
# RD args
# -----------------------------

# -----------------------------
# main
# -----------------------------
def main():
    try:
        netlist_val = netlist
    except NameError:
        print("Missing -rd netlist=<path>")
        sys.exit(1)

    try:
        output_val = output
    except NameError:
        print("Missing -rd output=<path>")
        sys.exit(1)

    try:
        reuse_val = reuse
    except NameError:
        reuse_val = None

    try:
        autoload_val = autoload
    except NameError:
        autoload_val = "0"

    try:
        reuse_dir_val = reuse_dir
    except NameError:
        reuse_dir_val = None

    try:
        leaf_val = leaf
    except NameError:
        leaf_val = "0"

    try:
        gallery_val = gallery
    except NameError:
        gallery_val = "0"

    with open(netlist_val, "r") as f:
        netlist_text = f.read()

    layout = klayout.db.Layout(True)
    layout.dbu = 0.001

    # reuse manual
    if reuse_val:
        layout.read(reuse_val)

    # autoload gds (sch->gds y/o reuse_dir)
    if _rd_bool(autoload_val, default=False):
        autoload_reuse_gds(layout, netlist_text, reuse_dir=reuse_dir_val)

    existing_map = build_existing_cell_map(layout)

    # validación opcional (si falla, KLayout no puede leer el netlist)
    _ = read_hierarchical_netlist(netlist_val)

    desired_top_name = _basename_noext(output_val)

    leaf_cells = build_layout(
        layout=layout,
        netlist_text=netlist_text,
        desired_top_name=desired_top_name,
        existing_map=existing_map,
        leaf_enable=_rd_bool(leaf_val, default=False),
        margin_um=5.0,
        fallback_step_um=20.0,
    )

    if _rd_bool(gallery_val, default=False):
        build_gallery(layout, leaf_cells, name="gallery")

    pathlib.Path(output_val).parent.mkdir(parents=True, exist_ok=True)
    layout.write(output_val)
    print(f"GDS created: {output_val}")


if __name__ == "__main__":
    main()
