import os
from pathlib import Path
import py_compile
import shutil
import subprocess
import sys
import unittest
from unittest.mock import MagicMock

ROOT = Path(__file__).resolve().parents[1]


if "pya" not in sys.modules:
    sys.modules["pya"] = MagicMock()
if "klayout" not in sys.modules:
    mock_klayout = MagicMock()
    sys.modules["klayout"] = mock_klayout
    sys.modules["klayout.db"] = mock_klayout.db

from scripts.hierarchical import (
    REPO_ROOT,
    parse_sch_paths,
    sch_to_gds_candidates,
    autoload_reuse_gds,
    main as hierarchical_main,
)


class TestHierarchicalPaths(unittest.TestCase):
    def test_scripts_compile(self):
        scripts_to_compile = [
            ROOT / "scripts" / "hierarchical.py",
            ROOT / "scripts" / "extract_comparison.py",
            ROOT / "scripts" / "check_xschem_paths.py",
            ROOT / "scripts" / "notebook_data.py",
        ]
        for script in scripts_to_compile:
            self.assertTrue(script.is_file(), f"{script} should exist")
            py_compile.compile(str(script), doraise=True)

    def test_parse_sch_paths_basic_unquoted(self):
        netlist = (
            "** sch_path: CDR4176-main/schematic/xschem/psdiff/psdiff.sch\n"
            ".subckt psdiff A B\n"
            ".ends\n"
        )
        paths = parse_sch_paths(netlist)
        self.assertEqual(paths, ["CDR4176-main/schematic/xschem/psdiff/psdiff.sch"])

    def test_parse_sch_paths_with_spaces_unquoted(self):
        netlist = (
            "** sch_path: CDR4176-main/schematic/xschem/my cell name/my cell name.sch\n"
        )
        paths = parse_sch_paths(netlist)
        self.assertEqual(
            paths,
            ["CDR4176-main/schematic/xschem/my cell name/my cell name.sch"],
        )

    def test_parse_sch_paths_quoted_double(self):
        netlist = (
            '** sch_path: "CDR4176-main/schematic/xschem/my cell/my cell.sch"\n'
        )
        paths = parse_sch_paths(netlist)
        self.assertEqual(
            paths,
            ["CDR4176-main/schematic/xschem/my cell/my cell.sch"],
        )

    def test_parse_sch_paths_quoted_single(self):
        netlist = (
            "** sch_path: 'CDR4176-main/schematic/xschem/my cell/my cell.sch'\n"
        )
        paths = parse_sch_paths(netlist)
        self.assertEqual(
            paths,
            ["CDR4176-main/schematic/xschem/my cell/my cell.sch"],
        )

    def test_parse_sch_paths_multiple(self):
        netlist = (
            "** sch_path: CDR4176-main/schematic/xschem/psdiff/psdiff.sch\n"
            "X1 A B psdiff\n"
            "** sch_path: \"CDR4176-main/schematic/xschem/inv_PI_d2/inv_PI_d2.sch\"\n"
            "X2 C D inv_PI_d2\n"
        )
        paths = parse_sch_paths(netlist)
        self.assertEqual(
            paths,
            [
                "CDR4176-main/schematic/xschem/psdiff/psdiff.sch",
                "CDR4176-main/schematic/xschem/inv_PI_d2/inv_PI_d2.sch",
            ],
        )

    def test_parse_sch_paths_empty(self):
        self.assertEqual(parse_sch_paths(""), [])
        self.assertEqual(parse_sch_paths("* no schematic path here\n.subckt foo\n"), [])

    def test_sch_to_gds_candidates_sibling_support(self):
        sch = "Custom_std_cells/inv_PI_d2.sch"
        cands = sch_to_gds_candidates(sch)
        self.assertIn("Custom_std_cells/inv_PI_d2.gds", cands)

    def test_sch_to_gds_candidates_new_cell_path(self):
        sch = "CDR4176-main/schematic/xschem/psdiff/psdiff.sch"
        cands = sch_to_gds_candidates(sch)
        expected_anchored = str(
            REPO_ROOT / "CDR4176-main" / "layout" / "klayout" / "psdiff" / "psdiff.gds"
        )
        self.assertIn(expected_anchored, cands)
        expected_rel = str(
            Path("CDR4176-main") / "layout" / "klayout" / "psdiff" / "psdiff.gds"
        )
        self.assertIn(expected_rel, cands)
        expected_layout_rel = str(
            Path("layout") / "klayout" / "psdiff" / "psdiff.gds"
        )
        self.assertIn(expected_layout_rel, cands)

        self.assertTrue(
            Path(expected_anchored).exists(),
            f"Expected actual layout file to exist: {expected_anchored}",
        )

    def test_sch_to_gds_candidates_with_reuse_dir(self):
        sch = "CDR4176-main/schematic/xschem/psdiff/psdiff.sch"
        reuse = "CDR4176-main/layout/klayout"
        cands = sch_to_gds_candidates(sch, reuse_dir=reuse)

        self.assertIn(
            str(Path(reuse) / "psdiff" / "psdiff.gds"),
            cands,
        )

        self.assertIn(
            str(Path(reuse) / "psdiff.gds"),
            cands,
        )

    def test_sch_to_gds_candidates_avoids_legacy(self):
        sch = "CDR4176-main/layout/klayout/8xPI_top/legacy/8xPI_top.sch"
        cands = sch_to_gds_candidates(sch)
        for c in cands:
            self.assertNotIn("legacy", Path(c).parts)

    def test_sch_to_gds_candidates_repo_anchoring(self):
        sch = "CDR4176-main/schematic/xschem/inv/inv.sch"
        cands = sch_to_gds_candidates(sch)
        anchored_path = REPO_ROOT / "CDR4176-main" / "layout" / "klayout" / "inv" / "inv.gds"
        self.assertIn(str(anchored_path), cands)
        self.assertTrue(anchored_path.is_file())

    def test_main_guard_missing_rd_exits_cleanly(self):

        import io
        from contextlib import redirect_stdout
        with redirect_stdout(io.StringIO()):
            with self.assertRaises(SystemExit) as ctx:
                hierarchical_main()
        self.assertEqual(ctx.exception.code, 1)

    def test_distrobox_klayout_execution(self):
        if not shutil.which("distrobox"):
            self.skipTest("distrobox not installed")
        proc = subprocess.run(
            ["distrobox", "list"],
            capture_output=True,
            text=True,
        )
        if "iic-osic-tools2" not in proc.stdout:
            self.skipTest("iic-osic-tools2 container not running")


        cmd = [
            "distrobox",
            "enter",
            "iic-osic-tools2",
            "--",
            "klayout",
            "-zz",
            "-r",
            "scripts/hierarchical.py",
        ]
        res = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(res.returncode, 1)
        self.assertIn("Missing -rd netlist=<path>", res.stdout + res.stderr)

    def test_distrobox_klayout_import(self):
        if not shutil.which("distrobox"):
            self.skipTest("distrobox not installed")
        proc = subprocess.run(
            ["distrobox", "list"],
            capture_output=True,
            text=True,
        )
        if "iic-osic-tools2" not in proc.stdout:
            self.skipTest("iic-osic-tools2 container not running")

        cmd = [
            "distrobox",
            "enter",
            "iic-osic-tools2",
            "--",
            "python3",
            "-c",
            "import pya, klayout.db, scripts.hierarchical; assert scripts.hierarchical.pya is not None",
        ]
        res = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, res.stderr)

    def test_distrobox_klayout_execution_success(self):
        if not shutil.which("distrobox"):
            self.skipTest("distrobox not installed")
        proc = subprocess.run(
            ["distrobox", "list"],
            capture_output=True,
            text=True,
        )
        if "iic-osic-tools2" not in proc.stdout:
            self.skipTest("iic-osic-tools2 container not running")

        out_tmp = ROOT / "tests" / "_test_inv_out.gds"
        try:
            cmd = [
                "distrobox",
                "enter",
                "iic-osic-tools2",
                "--",
                "klayout",
                "-zz",
                "-r",
                "scripts/hierarchical.py",
                "-rd",
                "netlist=CDR4176-main/schematic/xschem/inv/inv.spice",
                "-rd",
                f"output={out_tmp}",
            ]
            res = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(res.returncode, 0, res.stderr)
            self.assertIn("GDS created:", res.stdout)
            self.assertTrue(out_tmp.is_file())
        finally:
            if out_tmp.exists():
                out_tmp.unlink()


if __name__ == "__main__":
    unittest.main()
