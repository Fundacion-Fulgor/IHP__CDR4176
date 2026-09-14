from __future__ import annotations

import os
from pathlib import Path
import sys

NOTEBOOK_DATA_MAPPING: dict[str, str] = {
    "verification/scripts/result_simulation_3to7thermo_V2.ipynb": "legacy/tb_bin2thermo_tran",
    "verification/scripts/results_simulations_3to7thermo_deco_tran.ipynb": "legacy/tb_bin2thermo_tran",
    "verification/scripts/results_tb_linearity_integration.ipynb": "legacy/simulation",
    "verification/scripts/results_tb_linearity_ring_integration.ipynb": "legacy/simulations",
    "verification/scripts/results_tb_linearity_termoless.ipynb": "legacy/simulation",
    "simulations/simulation/results_tb_linearity_integration.ipynb": "legacy/simulation",
    "simulations/simulation/results_tb_linearity_termoless.ipynb": "legacy/simulation",
    "simulations/simulations/results_tb_linearity_ring_integration.ipynb": "legacy/simulations",
    "simulations/tb_bin2thermo_tran/results_tran.ipynb": "legacy/tb_bin2thermo_tran",
    "simulations/tb_linearity_8xpi/results_tb_linearity_termoless.ipynb": "legacy/tb_linearity_8xpi",
}


def find_repo_root(start: Path | str | None = None) -> Path:
    if "CDR4176_ROOT" in os.environ and os.environ["CDR4176_ROOT"].strip():
        return Path(os.environ["CDR4176_ROOT"]).expanduser().resolve()
    target = Path(start).resolve() if start is not None else Path(__file__).resolve().parent
    curr = target
    while curr != curr.parent:
        if (curr / "project.yml").exists() or (curr / "CDR4176-main").is_dir():
            return curr
        curr = curr.parent
    if (curr / "project.yml").exists() or (curr / "CDR4176-main").is_dir():
        return curr
    return Path(__file__).resolve().parents[1]


def normalize_notebook_id(notebook_id: str | Path) -> str:
    val = str(notebook_id).replace("\\", "/").strip()
    prefix = "CDR4176-main/verification/python/"
    if prefix in val:
        val = val.split(prefix, 1)[1]
    if val.startswith("./"):
        val = val[2:]
    for k in NOTEBOOK_DATA_MAPPING:
        if val == k or val == k.rsplit(".ipynb", 1)[0] or val.endswith("/" + k):
            return k
    return val


def get_data_dir(
    notebook_id: str | Path,
    repo_root: Path | str | None = None,
    results_root: Path | str | None = None,
) -> Path:
    norm_id = normalize_notebook_id(notebook_id)
    if norm_id in NOTEBOOK_DATA_MAPPING:
        mapped_rel = NOTEBOOK_DATA_MAPPING[norm_id]
    elif norm_id.startswith("legacy/") or f"legacy/{norm_id}" in NOTEBOOK_DATA_MAPPING.values():
        mapped_rel = norm_id if norm_id.startswith("legacy/") else f"legacy/{norm_id}"
    else:
        raise KeyError(f"Unknown notebook or dataset identifier: {notebook_id!r}")

    env_results = os.environ.get("CDR4176_RESULTS")
    if results_root is not None or (env_results and env_results.strip()):
        base_results = Path(results_root).resolve() if results_root is not None else Path(env_results).expanduser().resolve()
        sub = mapped_rel[len("legacy/"):] if mapped_rel.startswith("legacy/") else mapped_rel
        for cand in [base_results / mapped_rel, base_results / sub, base_results]:
            if cand.is_dir():
                return cand.resolve()
        return (base_results / mapped_rel).resolve()

    root = Path(repo_root).resolve() if repo_root is not None else find_repo_root()
    return (root / "CDR4176-main" / "verification" / "results" / mapped_rel).resolve()


def resolve_raw_path(
    filename: str | Path,
    notebook_id: str | Path | None = None,
    repo_root: Path | str | None = None,
    results_root: Path | str | None = None,
) -> Path:
    if isinstance(filename, Path):
        if filename.is_file():
            return filename.resolve()
        filename_str = str(filename)
    else:
        filename_str = str(filename)
        if os.path.isfile(filename_str) and (os.path.isabs(filename_str) or "/" in filename_str or "\\" in filename_str):
            return Path(filename_str).resolve()

    filename_name = Path(filename_str).name
    root = Path(repo_root).resolve() if repo_root is not None else find_repo_root()

    if notebook_id is None:
        for depth in (1, 2, 3):
            try:
                frame = sys._getframe(depth)
                if "NOTEBOOK_ID" in frame.f_globals:
                    notebook_id = frame.f_globals["NOTEBOOK_ID"]
                    break
                if "NOTEBOOK_ID" in frame.f_locals:
                    notebook_id = frame.f_locals["NOTEBOOK_ID"]
                    break
            except Exception:
                pass

    if notebook_id is None:
        raise ValueError(f"notebook_id must be provided to resolve {filename_name}")

    norm_id = normalize_notebook_id(notebook_id)
    if norm_id in NOTEBOOK_DATA_MAPPING:
        mapped_rel = NOTEBOOK_DATA_MAPPING[norm_id]
    elif norm_id.startswith("legacy/") or f"legacy/{norm_id}" in NOTEBOOK_DATA_MAPPING.values():
        mapped_rel = norm_id if norm_id.startswith("legacy/") else f"legacy/{norm_id}"
    else:
        raise KeyError(f"Unknown notebook or dataset identifier: {notebook_id!r}")

    env_results = os.environ.get("CDR4176_RESULTS")
    if results_root is not None or (env_results and env_results.strip()):
        base_results = Path(results_root).resolve() if results_root is not None else Path(env_results).expanduser().resolve()
        sub = mapped_rel[len("legacy/"):] if mapped_rel.startswith("legacy/") else mapped_rel
        candidates = [
            base_results / mapped_rel / filename_name,
            base_results / sub / filename_name,
            base_results / filename_name,
        ]
        for cand in candidates:
            if cand.is_file():
                return cand.resolve()
        checked_str = ", ".join(str(c) for c in candidates)
        raise FileNotFoundError(
            f"Raw simulation dataset not found for '{notebook_id}': '{filename_name}' under CDR4176_RESULTS ('{base_results}'). "
            f"Checked: [{checked_str}]. Raw dumps are no longer tracked in repository; regenerate/export or override with CDR4176_RESULTS."
        )

    expected_path = root / "CDR4176-main" / "verification" / "results" / mapped_rel / filename_name
    if expected_path.is_file():
        return expected_path.resolve()

    raise FileNotFoundError(
        f"Raw simulation dataset not found for notebook '{notebook_id}': '{filename_name}' (expected at '{expected_path}'). "
        f"Raw dumps are no longer tracked in repository; regenerate/export or override with CDR4176_RESULTS."
    )


def read_raw(
    rawfile: str | Path,
    variables: list[str],
    notebook_id: str | Path | None = None,
    repo_root: Path | str | None = None,
    results_root: Path | str | None = None,
) -> dict[str, list[float]]:
    raw_path = resolve_raw_path(rawfile, notebook_id=notebook_id, repo_root=repo_root, results_root=results_root)
    out_dict: dict[str, list[float]] = {}
    aux_dict: dict[int, str] = {}
    head: bool | None = None
    offset = 0

    with open(raw_path, "r") as f:
        for line in f:
            linea = line.strip()
            if linea == "Variables:":
                head = True
            elif linea == "Values:":
                head = False

            if head is True and linea != "Variables:":
                lin_split = linea.split()
                if len(lin_split) >= 2 and lin_split[1] in variables:
                    aux_dict[int(lin_split[0])] = lin_split[1]
                    out_dict[lin_split[1]] = []
            elif head is False and linea != "Values:":
                if len(linea.split()) > 1:
                    offset = 0
                if offset in aux_dict:
                    if offset != 0:
                        label = aux_dict[offset]
                        out_dict[label].append(float(linea))
                    else:
                        label = aux_dict[offset]
                        out_dict[label].append(float(linea.split()[1]))
                offset += 1

    return out_dict


readRaw = read_raw
