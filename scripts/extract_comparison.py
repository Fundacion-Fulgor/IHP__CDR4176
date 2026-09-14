#!/usr/bin/env python3
# extract_comparison.py
#
# Uso:
#   python3 extract_comparison.py a.raw b.raw
#   python3 extract_comparison.py a.raw b.raw time v(vout) v(vin)
#   python3 extract_comparison.py a.raw b.raw frequency v(out) --complex mag
#
# Requisitos: numpy, matplotlib

import argparse
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt


# -------------------- RAW READER (ngspice/xschem) --------------------

def _read_header(f):
    header = {}
    variables = []
    data_start_offset = None
    is_binary = False

    while True:
        line = f.readline()
        if not line:
            raise ValueError("EOF inesperado leyendo el header. ¿.raw válido?")
        s = line.decode("utf-8", errors="replace").strip()

        if s.startswith("Title:"):
            header["Title"] = s.split(":", 1)[1].strip()
        elif s.startswith("Date:"):
            header["Date"] = s.split(":", 1)[1].strip()
        elif s.startswith("Plotname:"):
            header["Plotname"] = s.split(":", 1)[1].strip()
        elif s.startswith("Flags:"):
            header["Flags"] = s.split(":", 1)[1].strip()
        elif s.startswith("No. Variables:"):
            header["No. Variables"] = int(s.split(":", 1)[1].strip())
        elif s.startswith("No. Points:"):
            header["No. Points"] = int(s.split(":", 1)[1].strip())
        elif s == "Variables:":
            while True:
                pos = f.tell()
                line2 = f.readline()
                if not line2:
                    raise ValueError("EOF inesperado en sección Variables:")
                s2 = line2.decode("utf-8", errors="replace").strip()
                if s2 in ("Values:", "Binary:"):
                    f.seek(pos)
                    break
                if not s2:
                    continue
                parts = s2.split()
                if len(parts) >= 3:
                    variables.append({"index": int(parts[0]), "name": parts[1], "type": parts[2]})
        elif s == "Values:":
            data_start_offset = f.tell()
            is_binary = False
            break
        elif s == "Binary:":
            data_start_offset = f.tell()
            is_binary = True
            break

    if "No. Variables" not in header or "No. Points" not in header:
        raise ValueError("Header incompleto: faltan 'No. Variables' o 'No. Points'.")
    if len(variables) == 0:
        raise ValueError("No pude leer la lista de Variables del .raw.")

    return header, variables, data_start_offset, is_binary


def _parse_ascii_data(f, nvars, npts):
    text = f.read().decode("utf-8", errors="replace")
    tokens = text.replace(",", " ").split()

    # Intento 1: bloques (1 + nvars) por punto: idx + valores
    block = 1 + nvars
    if len(tokens) >= npts * block:
        arr = np.array(tokens[: npts * block], dtype=np.float64).reshape(npts, block)
        return arr[:, 1:]

    # Intento 2: solo valores (npts * nvars)
    if len(tokens) >= npts * nvars:
        return np.array(tokens[: npts * nvars], dtype=np.float64).reshape(npts, nvars)

    raise ValueError("No pude parsear datos ASCII: tokens insuficientes.")


def _parse_binary_data(f, header, nvars, npts):
    flags = header.get("Flags", "").lower()
    is_complex = ("complex" in flags)

    per_value = 16 if is_complex else 8
    total_bytes = npts * nvars * per_value
    blob = f.read(total_bytes)

    if len(blob) < total_bytes:
        raise ValueError(f"Datos binarios incompletos: esperaba {total_bytes} bytes, tengo {len(blob)}.")

    if not is_complex:
        return np.frombuffer(blob, dtype=np.float64).reshape(npts, nvars)

    raw = np.frombuffer(blob, dtype=np.float64).reshape(npts, nvars, 2)
    return raw[..., 0] + 1j * raw[..., 1]


def read_ngspice_raw(raw_path: str):
    with open(raw_path, "rb") as f:
        header, variables, data_offset, is_binary = _read_header(f)
        f.seek(data_offset)
        nvars = header["No. Variables"]
        npts = header["No. Points"]

        if is_binary:
            data = _parse_binary_data(f, header, nvars, npts)
        else:
            data = _parse_ascii_data(f, nvars, npts)

    return header, variables, data


def normalize_name(s: str) -> str:
    return s.strip().lower()


def make_getter(variables, data):
    name_to_idx = {normalize_name(v["name"]): v["index"] for v in variables}

    def get(sig: str):
        s = normalize_name(sig)
        if s in name_to_idx:
            return data[:, name_to_idx[s]]

        # Alias útil: "vout" -> "v(vout)" si existe
        alt = f"v({s})"
        if alt in name_to_idx:
            return data[:, name_to_idx[alt]]

        raise KeyError(f"No encuentro '{sig}' en el .raw")

    return get, name_to_idx


def apply_complex_mode(y, mode: str):
    if not np.iscomplexobj(y):
        return y
    if mode == "real":
        return np.real(y)
    if mode == "imag":
        return np.imag(y)
    if mode == "mag":
        return np.abs(y)
    if mode == "phase":
        return np.angle(y)
    return np.real(y)


# -------------------- PLOT TWO RAWS --------------------

def plot_two_raws(raw1, raw2, signals, x_name=None, labels=None, complex_mode="real", title=None):
    h1, v1, d1 = read_ngspice_raw(raw1)
    h2, v2, d2 = read_ngspice_raw(raw2)

    get1, map1 = make_getter(v1, d1)
    get2, map2 = make_getter(v2, d2)

    if labels is None:
        labels = (Path(raw1).stem, Path(raw2).stem)

    # Eje X: por defecto 'time' si existe en ambos; si no, primera variable
    if x_name is None:
        if "time" in map1 and "time" in map2:
            x_name = "time"
        elif "frequency" in map1 and "frequency" in map2:
            x_name = "frequency"
        else:
            x_name = v1[0]["name"]  # fallback

    x1 = get1(x_name) if normalize_name(x_name) in map1 else d1[:, 0]
    x2 = get2(x_name) if normalize_name(x_name) in map2 else d2[:, 0]

    # Si el usuario incluyó el eje X dentro de signals, lo removemos de Y
    ysignals = [s for s in signals if normalize_name(s) != normalize_name(x_name)]
    if len(ysignals) == 0:
        raise ValueError("No hay señales Y para plotear (solo quedó el eje X).")

    plt.figure()
    for s in ysignals:
        y1 = apply_complex_mode(get1(s), complex_mode)
        y2 = apply_complex_mode(get2(s), complex_mode)

        plt.plot(x1, y1, label=f"{s} ({labels[0]})")
        plt.plot(x2, y2, label=f"{s} ({labels[1]})")

    plt.xlabel(x_name)
    plt.grid(True)
    plt.legend()

    if title is None:
        t1 = h1.get("Title", Path(raw1).name)
        t2 = h2.get("Title", Path(raw2).name)
        title = f"Compare: {t1}  vs  {t2}"
    plt.title(title)

    plt.tight_layout()
    plt.show()


def main():
    ap = argparse.ArgumentParser(prog="extract_comparison.py", description="Comparar 2 .raw de ngspice/xschem en un solo plot")
    ap.add_argument("raw1", help="Primer .raw")
    ap.add_argument("raw2", help="Segundo .raw")
    ap.add_argument("signals", nargs="*", help="Señales a plotear (ej: time v(vout) v(vin))")
    ap.add_argument("--x", default=None, help="Señal para eje X (default: time o frequency si existen)")
    ap.add_argument("--label1", default=None, help="Label para raw1")
    ap.add_argument("--label2", default=None, help="Label para raw2")
    ap.add_argument("--complex", default="real", choices=["real", "imag", "mag", "phase"],
                    help="Cómo plotear señales complejas (default: real)")
    ap.add_argument("--title", default=None, help="Título del plot")
    args = ap.parse_args()

    # Si no pidieron señales, listamos variables de ambos raws y salimos
    if len(args.signals) == 0:
        for i, rp in enumerate([args.raw1, args.raw2], start=1):
            h, vars_, _ = read_ngspice_raw(rp)
            print(f"\nRAW {i}: {rp}")
            print(f"  Title: {h.get('Title','')}")
            print("  Variables:")
            for v in vars_:
                print(f"    [{v['index']:>3}] {v['name']:<20} {v['type']}")
        print("\nEjemplo:")
        print(f"  python3 {Path(__file__).name} {args.raw1} {args.raw2} time v(vout) v(vin)")
        return

    labels = (args.label1, args.label2)
    if labels[0] is None or labels[1] is None:
        labels = None  # usa nombres de archivo

    plot_two_raws(
        args.raw1,
        args.raw2,
        args.signals,
        x_name=args.x,
        labels=labels,
        complex_mode=args.complex,
        title=args.title
    )


if __name__ == "__main__":
    main()
