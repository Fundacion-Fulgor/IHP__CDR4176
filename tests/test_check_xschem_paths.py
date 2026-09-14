import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

from scripts.check_xschem_paths import (
    Violation,
    parse_content,
    run_checker,
)

ROOT = Path(__file__).resolve().parents[1]


class TestCheckXschemPaths(unittest.TestCase):
    def setUp(self):
        self.temp_dir_obj = tempfile.TemporaryDirectory()
        self.temp_dir = Path(self.temp_dir_obj.name)

    def tearDown(self):
        self.temp_dir_obj.cleanup()

    def _init_git_repo(self, repo_dir: Path) -> None:
        subprocess.run(["git", "init"], cwd=repo_dir, check=True, stdout=subprocess.PIPE)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=repo_dir, check=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=repo_dir, check=True)

    def test_ngspice_assigned_simul_variable_in_control_allowed(self):
        content = (
            ".control\n"
            "let simul = 0\n"
            "while simul < 32\n"
            "  write tran_io_fase{$&simul}.raw\n"
            "  let simul = simul + 1\n"
            ".endc\n"
        )
        violations = parse_content(content, "test.spice", repo_root=None)
        self.assertEqual(violations, [])

    def test_ngspice_assigned_output_path_variable_in_control_allowed(self):
        content = (
            ".control\n"
            "set output_path = tb_bin2thermo_tran/\n"
            "write {$output_path}out1.raw V(vo_st7)\n"
            "wrdata $output_path/data.raw V(vo_st7)\n"
            ".endc\n"
        )
        violations = parse_content(content, "test.spice", repo_root=None)
        self.assertEqual(violations, [])

    def test_ngspice_unassigned_variable_in_control_rejected(self):
        content = (
            ".control\n"
            "write tran_io_fase{$&unassigned_simul}.raw\n"
            ".endc\n"
        )
        violations = parse_content(content, "test.spice", repo_root=None)
        self.assertTrue(any("unassigned ngspice variable" in v.message for v in violations))

    def test_ngspice_unassigned_output_path_in_control_rejected(self):
        content = (
            ".control\n"
            "write {$unassigned_path}out.raw\n"
            ".endc\n"
        )
        violations = parse_content(content, "test.spice", repo_root=None)
        self.assertTrue(any("unassigned ngspice variable" in v.message for v in violations))

    def test_ngspice_variable_outside_control_rejected(self):
        content = "write tran_io_fase{$&simul}.raw\n"
        violations = parse_content(content, "test.spice", repo_root=None)
        self.assertTrue(any("used outside .control" in v.message for v in violations))

    def test_runtime_raw_outputs_do_not_require_file_on_disk(self):
        content = (
            ".control\n"
            "let simul = 0\n"
            "write non_existent_runtime_output_{$&simul}.raw\n"
            "wrdata non_existent_data.raw V(1)\n"
            ".endc\n"
        )
        violations = parse_content(content, "test.spice", repo_root=ROOT)
        self.assertEqual(violations, [])

    def test_detect_actual_missing_local_symbol(self):
        sch_content = (
            "v {xschem version=3.4.8RC file_version=1.3}\n"
            "C {completely_missing_custom_block_xyz.sym} 0 0 0 0 {name=x1}\n"
        )
        violations = parse_content(sch_content, "CDR4176-main/schematic/xschem/test/test.sch", repo_root=ROOT)
        self.assertTrue(any("completely_missing_custom_block_xyz.sym" in v.offending_reference for v in violations))

    def test_detect_actual_missing_dependency(self):
        spice_content = (
            ".include \"missing_subcircuit_pex_extracted.cir\"\n"
        )
        violations = parse_content(spice_content, "test.spice", repo_root=ROOT)
        self.assertTrue(any("missing_subcircuit_pex_extracted.cir" in v.offending_reference for v in violations))

    def test_bare_corner_pdk_lib_allowed(self):
        spice_content = (
            ".lib cornerMOSlv.lib mos_tt\n"
        )
        violations = parse_content(spice_content, "test.spice", repo_root=ROOT)
        self.assertEqual(violations, [])

    def test_bare_missing_lib_fails(self):
        spice_content = (
            ".lib nonexistent_random_library.lib mos_tt\n"
        )
        violations = parse_content(spice_content, "test.spice", repo_root=ROOT)
        self.assertTrue(any("nonexistent_random_library.lib" in v.offending_reference for v in violations))

    def test_namespaced_project_io_symbol(self):
        valid_sch = (
            "v {xschem version=3.4.8RC file_version=1.3}\n"
            "C {project_io/sg13g2_IOPadIn/sg13g2_IOPadIn.sym} 0 0 0 0 {name=p1}\n"
        )
        violations = parse_content(valid_sch, "CDR4176-main/schematic/xschem/CDR4176/CDR4176.sch", repo_root=ROOT)
        self.assertEqual(violations, [])

    def test_colocated_views(self):
        cell_dir = ROOT / "CDR4176-main" / "schematic" / "xschem" / "CDR4176"
        if cell_dir.is_dir():
            expected_files = [
                cell_dir / "CDR4176.sch",
                cell_dir / "CDR4176.sym",
                cell_dir / "CDR4176.spice",
                cell_dir / "CDR4176_extracted.cir",
            ]
            for f in expected_files:
                self.assertTrue(f.exists(), f"Colocated view missing: {f}")

    def test_working_tree_includes_untracked_and_excludes_deleted(self):
        repo_dir = self.temp_dir / "repo_wt_test"
        repo_dir.mkdir()
        self._init_git_repo(repo_dir)

        tracked_file = repo_dir / "tracked.sch"
        tracked_file.write_text("v {xschem version=3.4.8RC file_version=1.3}\nC {devices/lab_pin.sym} 0 0 0 0 {}\n")
        subprocess.run(["git", "add", "tracked.sch"], cwd=repo_dir, check=True)
        subprocess.run(["git", "commit", "-m", "initial"], cwd=repo_dir, check=True, stdout=subprocess.PIPE)

        tracked_file.unlink()

        untracked_file = repo_dir / "untracked_moved.sch"
        untracked_file.write_text(
            "v {xschem version=3.4.8RC file_version=1.3}\n"
            "C {/absolute/bad/path.sym} 0 0 0 0 {}\n"
        )

        code, violations, count = run_checker(staged=False, repo_root_arg=str(repo_dir))
        self.assertEqual(code, 1)
        self.assertEqual(count, 1)
        self.assertEqual(len(violations), 1)
        self.assertIn("/absolute/bad/path.sym", violations[0].offending_reference)
        self.assertFalse(any("tracked.sch" in v.file_path for v in violations))

    def test_staged_mode(self):
        repo_dir = self.temp_dir / "repo_staged_test"
        repo_dir.mkdir()
        self._init_git_repo(repo_dir)

        initial = repo_dir / "initial.sch"
        initial.write_text("v {xschem version=3.4.8RC file_version=1.3}\n")
        subprocess.run(["git", "add", "initial.sch"], cwd=repo_dir, check=True)
        subprocess.run(["git", "commit", "-m", "init"], cwd=repo_dir, check=True, stdout=subprocess.PIPE)

        bad_staged = repo_dir / "bad_staged.sch"
        bad_staged.write_text(
            "v {xschem version=3.4.8RC file_version=1.3}\n"
            "C {/absolute/path/viol.sym} 0 0 0 0 {}\n"
        )
        subprocess.run(["git", "add", "bad_staged.sch"], cwd=repo_dir, check=True)

        bad_staged.write_text(
            "v {xschem version=3.4.8RC file_version=1.3}\n"
            "C {devices/lab_pin.sym} 0 0 0 0 {}\n"
        )

        code, violations, count = run_checker(staged=True, repo_root_arg=str(repo_dir))
        self.assertEqual(code, 1)
        self.assertEqual(count, 1)
        self.assertEqual(len(violations), 1)
        self.assertIn("/absolute/path/viol.sym", violations[0].offending_reference)

    def test_staged_untracked_dependency_fails(self):
        repo_dir = self.temp_dir / "repo_staged_untracked"
        repo_dir.mkdir()
        self._init_git_repo(repo_dir)

        top_sch = repo_dir / "top.sch"
        top_sch.write_text(
            "v {xschem version=3.4.8RC file_version=1.3}\n"
            "C {my_local_block.sym} 0 0 0 0 {}\n"
        )
        subprocess.run(["git", "add", "top.sch"], cwd=repo_dir, check=True)

        local_sym = repo_dir / "my_local_block.sym"
        local_sym.write_text("v {xschem version=3.4.8RC}\n")

        code, violations, count = run_checker(staged=True, repo_root_arg=str(repo_dir))
        self.assertEqual(code, 1)
        self.assertTrue(any("my_local_block.sym" in v.offending_reference for v in violations))

    def test_staged_missing_working_tree_file_passes(self):
        repo_dir = self.temp_dir / "repo_staged_missing_wt"
        repo_dir.mkdir()
        self._init_git_repo(repo_dir)

        top_sch = repo_dir / "top.sch"
        top_sch.write_text(
            "v {xschem version=3.4.8RC file_version=1.3}\n"
            "C {my_local_block.sym} 0 0 0 0 {}\n"
        )
        local_sym = repo_dir / "my_local_block.sym"
        local_sym.write_text("v {xschem version=3.4.8RC}\n")

        subprocess.run(["git", "add", "top.sch", "my_local_block.sym"], cwd=repo_dir, check=True)
        local_sym.unlink()

        code, violations, count = run_checker(staged=True, repo_root_arg=str(repo_dir))
        self.assertEqual(code, 0, f"Expected 0 violations but got: {violations}")

    def test_staged_scans_consumers_on_dependency_deletion(self):
        repo_dir = self.temp_dir / "repo_staged_dep_deletion"
        repo_dir.mkdir()
        self._init_git_repo(repo_dir)

        top_sch = repo_dir / "top.sch"
        top_sch.write_text(
            "v {xschem version=3.4.8RC file_version=1.3}\n"
            "C {child.sym} 0 0 0 0 {}\n"
        )
        child_sym = repo_dir / "child.sym"
        child_sym.write_text("v {xschem version=3.4.8RC}\n")

        subprocess.run(["git", "add", "top.sch", "child.sym"], cwd=repo_dir, check=True)
        subprocess.run(["git", "commit", "-m", "init"], cwd=repo_dir, check=True, stdout=subprocess.PIPE)

        subprocess.run(["git", "rm", "child.sym"], cwd=repo_dir, check=True, stdout=subprocess.PIPE)

        code, violations, count = run_checker(staged=True, repo_root_arg=str(repo_dir))
        self.assertEqual(code, 1)
        self.assertTrue(any("child.sym" in v.offending_reference for v in violations))

    def test_staged_scans_consumers_on_dependency_rename(self):
        repo_dir = self.temp_dir / "repo_staged_dep_rename"
        repo_dir.mkdir()
        self._init_git_repo(repo_dir)

        top_sch = repo_dir / "top.sch"
        top_sch.write_text(
            "v {xschem version=3.4.8RC file_version=1.3}\n"
            "C {old_child.sym} 0 0 0 0 {}\n"
        )
        old_sym = repo_dir / "old_child.sym"
        old_sym.write_text("v {xschem version=3.4.8RC}\n")

        subprocess.run(["git", "add", "top.sch", "old_child.sym"], cwd=repo_dir, check=True)
        subprocess.run(["git", "commit", "-m", "init"], cwd=repo_dir, check=True, stdout=subprocess.PIPE)

        subprocess.run(["git", "mv", "old_child.sym", "new_child.sym"], cwd=repo_dir, check=True)

        code, violations, count = run_checker(staged=True, repo_root_arg=str(repo_dir))
        self.assertEqual(code, 1)
        self.assertTrue(any("old_child.sym" in v.offending_reference for v in violations))

    def test_script_dir_root_traversal_prevention(self):
        content_direct = ".include \"$SCRIPT_DIR/../../secret.cir\"\n"
        v1 = parse_content(content_direct, "sub/test.spice", repo_root=None)
        self.assertTrue(any("traverses outside" in v.message for v in v1))

        content_file_join = "[file join $SCRIPT_DIR .. .. secret.cir]"
        v2 = parse_content(f"K {{type=code\ntclcommand=\"source {content_file_join}\"\n}}\n", "sub/test.sch", repo_root=None)
        self.assertTrue(any("traverses outside" in v.message for v in v2))

    def test_static_script_dir_resolution_and_existence(self):
        repo_dir = self.temp_dir / "repo_script_dir"
        repo_dir.mkdir()
        valid_sub = repo_dir / "valid_sub.cir"
        valid_sub.write_text(".param x=1\n")

        valid_content = ".include \"$SCRIPT_DIR/valid_sub.cir\"\n"
        v_ok = parse_content(valid_content, "sub/test.spice", repo_root=repo_dir)
        self.assertEqual(v_ok, [])

        missing_content = ".include \"$SCRIPT_DIR/missing_sub.cir\"\n"
        v_missing = parse_content(missing_content, "sub/test.spice", repo_root=repo_dir)
        self.assertTrue(any("missing_sub.cir" in v.offending_reference for v in v_missing))

    def test_file_join_containment_and_resolution(self):
        repo_dir = self.temp_dir / "repo_file_join"
        repo_dir.mkdir()
        valid_file = repo_dir / "valid.spice"
        valid_file.write_text("* ok\n")

        valid_tcl = "K {type=code\ntclcommand=\"source [file join $SCRIPT_DIR valid.spice]\"\n}\n"
        v_ok = parse_content(valid_tcl, "sub/test.sch", repo_root=repo_dir)
        self.assertEqual(v_ok, [])

        missing_tcl = "K {type=code\ntclcommand=\"source [file join $SCRIPT_DIR missing.spice]\"\n}\n"
        v_missing = parse_content(missing_tcl, "sub/test.sch", repo_root=repo_dir)
        self.assertTrue(any("missing.spice" in v.offending_reference for v in v_missing))

        escaped_tcl = "K {type=code\ntclcommand=\"source [file join $SCRIPT_DIR .. .. escaped.spice]\"\n}\n"
        v_escaped = parse_content(escaped_tcl, "sub/test.sch", repo_root=repo_dir)
        self.assertTrue(any("traverses outside" in v.message for v in v_escaped))

    def test_file_join_suffix_attached_root_containment_and_resolution(self):
        v_join_escape = parse_content(
            "K {type=code\ntclcommand=\"source [file join $SCRIPT_DIR/../outside child.cir]\"\n}\n",
            "sub/test.sch",
            repo_root=None,
        )
        self.assertTrue(any("traverses outside" in v.message for v in v_join_escape))

        v_join_nested_escape = parse_content(
            "K {type=code\ntclcommand=\"source [file join $SCRIPT_DIR/nested/../../outside child.cir]\"\n}\n",
            "sub/test.sch",
            repo_root=None,
        )
        self.assertTrue(any("traverses outside" in v.message for v in v_join_nested_escape))

        v_direct_escape = parse_content(".include \"$SCRIPT_DIR/../outside/child.cir\"\n", "sub/test.spice", repo_root=None)
        self.assertTrue(any("traverses outside" in v.message for v in v_direct_escape))

        v_direct_tcl_escape = parse_content(
            "K {type=code\ntclcommand=\"source $SCRIPT_DIR/../outside/child.cir\"\n}\n",
            "sub/test.sch",
            repo_root=None,
        )
        self.assertTrue(any("traverses outside" in v.message for v in v_direct_tcl_escape))

        repo_dir = self.temp_dir / "repo_suffix_attached"
        repo_dir.mkdir()
        (repo_dir / "sub").mkdir()
        (repo_dir / "sub" / "child.cir").write_text(".param x=1\n")

        valid_join = "K {type=code\ntclcommand=\"source [file join $SCRIPT_DIR/sub child.cir]\"\n}\n"
        self.assertEqual(parse_content(valid_join, "top.sch", repo_root=repo_dir), [])

        valid_join_rel = "K {type=code\ntclcommand=\"source [file join $SCRIPT_DIR/sub/nested/.. child.cir]\"\n}\n"
        self.assertEqual(parse_content(valid_join_rel, "top.sch", repo_root=repo_dir), [])

        missing_join = "K {type=code\ntclcommand=\"source [file join $SCRIPT_DIR/sub missing.cir]\"\n}\n"
        v_missing = parse_content(missing_join, "top.sch", repo_root=repo_dir)
        self.assertTrue(any("missing.cir" in v.offending_reference for v in v_missing))

    def test_script_dir_wrong_location_dependency_rejected(self):
        staged = {"sub/child.cir"}
        v_staged_inc = parse_content(".include \"$SCRIPT_DIR/child.cir\"\n", "top.spice", repo_root=None, staged_paths=staged)
        self.assertTrue(any("child.cir" in v.offending_reference for v in v_staged_inc))

        v_staged_tcl_dir = parse_content(
            "K {type=code\ntclcommand=\"source $SCRIPT_DIR/child.cir\"\n}\n",
            "top.sch",
            repo_root=None,
            staged_paths=staged,
        )
        self.assertTrue(any("child.cir" in v.offending_reference for v in v_staged_tcl_dir))

        v_staged_join = parse_content(
            "K {type=code\ntclcommand=\"source [file join $SCRIPT_DIR child.cir]\"\n}\n",
            "top.sch",
            repo_root=None,
            staged_paths=staged,
        )
        self.assertTrue(any("child.cir" in v.offending_reference for v in v_staged_join))

        v_staged_ok_inc = parse_content(".include \"$SCRIPT_DIR/sub/child.cir\"\n", "top.spice", repo_root=None, staged_paths=staged)
        self.assertEqual(v_staged_ok_inc, [])

        v_staged_ok_join = parse_content(
            "K {type=code\ntclcommand=\"source [file join $SCRIPT_DIR sub child.cir]\"\n}\n",
            "top.sch",
            repo_root=None,
            staged_paths=staged,
        )
        self.assertEqual(v_staged_ok_join, [])

        v_staged_ok_join_pfx = parse_content(
            "K {type=code\ntclcommand=\"source [file join $SCRIPT_DIR/sub child.cir]\"\n}\n",
            "top.sch",
            repo_root=None,
            staged_paths=staged,
        )
        self.assertEqual(v_staged_ok_join_pfx, [])

        repo_dir = self.temp_dir / "repo_wt_wrong_location"
        repo_dir.mkdir()
        (repo_dir / "sub").mkdir()
        (repo_dir / "sub" / "child.cir").write_text(".param x=1\n")

        v_wt_inc = parse_content(".include \"$SCRIPT_DIR/child.cir\"\n", "sub/test.spice", repo_root=repo_dir)
        self.assertTrue(any("child.cir" in v.offending_reference for v in v_wt_inc))

        v_wt_tcl_dir = parse_content(
            "K {type=code\ntclcommand=\"source \\\"$SCRIPT_DIR/child.cir\\\"\"\n}\n",
            "sub/test.sch",
            repo_root=repo_dir,
        )
        self.assertTrue(any("child.cir" in v.offending_reference for v in v_wt_tcl_dir))

        v_wt_join = parse_content(
            "K {type=code\ntclcommand=\"source [file join $SCRIPT_DIR child.cir]\"\n}\n",
            "sub/test.sch",
            repo_root=repo_dir,
        )
        self.assertTrue(any("child.cir" in v.offending_reference for v in v_wt_join))

        (repo_dir / "child.cir").write_text(".param x=1\n")
        self.assertEqual(parse_content(".include \"$SCRIPT_DIR/child.cir\"\n", "sub/test.spice", repo_root=repo_dir), [])
        self.assertEqual(
            parse_content(
                "K {type=code\ntclcommand=\"source \\\"$SCRIPT_DIR/child.cir\\\"\"\n}\n",
                "sub/test.sch",
                repo_root=repo_dir,
            ),
            [],
        )
        self.assertEqual(
            parse_content(
                "K {type=code\ntclcommand=\"source [file join $SCRIPT_DIR child.cir]\"\n}\n",
                "sub/test.sch",
                repo_root=repo_dir,
            ),
            [],
        )

    def test_script_dir_paths_with_spaces(self):
        repo_dir = self.temp_dir / "repo_spaces"
        repo_dir.mkdir()
        folder = repo_dir / "my folder"
        folder.mkdir()
        (folder / "my test.cir").write_text(".param x=1\n")
        (folder / "my script.tcl").write_text("# ok\n")

        v_inc_ok = parse_content(".include \"$SCRIPT_DIR/my folder/my test.cir\"\n", "test.spice", repo_root=repo_dir)
        self.assertEqual(v_inc_ok, [])

        v_inc_miss = parse_content(".include \"$SCRIPT_DIR/my folder/missing.cir\"\n", "test.spice", repo_root=repo_dir)
        self.assertTrue(any("missing.cir" in v.offending_reference for v in v_inc_miss))

        v_tcl_ok = parse_content(
            "K {type=code\ntclcommand=\"source \\\"$SCRIPT_DIR/my folder/my script.tcl\\\"\"\n}\n",
            "test.sch",
            repo_root=repo_dir,
        )
        self.assertEqual(v_tcl_ok, [])

        v_tcl_miss = parse_content(
            "K {type=code\ntclcommand=\"source \\\"$SCRIPT_DIR/my folder/missing.tcl\\\"\"\n}\n",
            "test.sch",
            repo_root=repo_dir,
        )
        self.assertTrue(any("missing.tcl" in v.offending_reference for v in v_tcl_miss))

        v_join_att = parse_content(
            "K {type=code\ntclcommand=\"source [file join \\\"$SCRIPT_DIR/my folder\\\" \\\"my script.tcl\\\"]\"\n}\n",
            "test.sch",
            repo_root=repo_dir,
        )
        self.assertEqual(v_join_att, [])

        v_join_sep = parse_content(
            "K {type=code\ntclcommand=\"source [file join $SCRIPT_DIR \\\"my folder\\\" \\\"my script.tcl\\\"]\"\n}\n",
            "test.sch",
            repo_root=repo_dir,
        )
        self.assertEqual(v_join_sep, [])

        v_join_space_esc = parse_content(
            "K {type=code\ntclcommand=\"source [file join \\\"$SCRIPT_DIR/../outside folder\\\" \\\"my script.tcl\\\"]\"\n}\n",
            "test.sch",
            repo_root=repo_dir,
        )
        self.assertTrue(any("traverses outside" in v.message for v in v_join_space_esc))

    def test_staged_script_dir_wrong_location_and_untracked(self):
        repo_dir = self.temp_dir / "repo_staged_script_dir"
        repo_dir.mkdir()
        self._init_git_repo(repo_dir)

        (repo_dir / "sub").mkdir()
        (repo_dir / "sub" / "child.cir").write_text(".param x=1\n")
        top_sch = repo_dir / "top.sch"
        top_sch.write_text("K {type=code\ntclcommand=\"source [file join $SCRIPT_DIR child.cir]\"\n}\n")
        top_spice = repo_dir / "top.spice"
        top_spice.write_text(".include \"$SCRIPT_DIR/child.cir\"\n")

        subprocess.run(["git", "add", "sub/child.cir", "top.sch", "top.spice"], cwd=repo_dir, check=True)

        code1, viols1, count1 = run_checker(staged=True, repo_root_arg=str(repo_dir))
        self.assertEqual(code1, 1)
        self.assertTrue(any("[file join $SCRIPT_DIR child.cir]" in v.offending_reference for v in viols1))
        self.assertTrue(any("$SCRIPT_DIR/child.cir" in v.offending_reference for v in viols1))

        (repo_dir / "child.cir").write_text(".param x=1\n")
        code2, viols2, count2 = run_checker(staged=True, repo_root_arg=str(repo_dir))
        self.assertEqual(code2, 1)
        self.assertTrue(any("[file join $SCRIPT_DIR child.cir]" in v.offending_reference for v in viols2))
        self.assertTrue(any("$SCRIPT_DIR/child.cir" in v.offending_reference for v in viols2))

        subprocess.run(["git", "add", "child.cir"], cwd=repo_dir, check=True)
        code3, viols3, count3 = run_checker(staged=True, repo_root_arg=str(repo_dir))
        self.assertEqual(code3, 0, f"Expected 0 violations but got: {viols3}")

    def test_bare_symbol_preserves_library_and_submodule_search(self):
        sch = "C {my_sub_cell.sym} 0 0 0 0 {}\n"
        self.assertEqual(parse_content(sch, "test.sch", repo_root=None, staged_paths={"sub/my_sub_cell.sym"}), [])

        v_miss_staged = parse_content(sch, "test.sch", repo_root=None, staged_paths={"sub/other.sym"})
        self.assertTrue(any("my_sub_cell.sym" in v.offending_reference for v in v_miss_staged))

        repo_dir = self.temp_dir / "repo_bare_search"
        repo_dir.mkdir()
        cell_dir = repo_dir / "CDR4176-main" / "schematic" / "xschem" / "sub"
        cell_dir.mkdir(parents=True)
        (cell_dir / "my_sub_cell.sym").write_text("v {xschem version=3.4.8RC}\n")

        self.assertEqual(parse_content(sch, "test.sch", repo_root=repo_dir), [])

        sch_missing = "C {missing_block.sym} 0 0 0 0 {}\n"
        v_miss_wt = parse_content(sch_missing, "test.sch", repo_root=repo_dir)
        self.assertTrue(any("missing_block.sym" in v.offending_reference for v in v_miss_wt))

    def test_whitelist_symbols_without_submodules(self):
        sch_pdk_bare = "C {sg13_hv_pmos.sym} 0 0 0 0 {}\n"
        self.assertEqual(parse_content(sch_pdk_bare, "test.sch", repo_root=self.temp_dir), [])

        sch_pdk_prefix = "C {sg13g2_pr/sg13_hv_pmos.sym} 0 0 0 0 {}\n"
        self.assertEqual(parse_content(sch_pdk_prefix, "test.sch", repo_root=self.temp_dir), [])

        sch_io_bare = "C {sg13g2_IOPadIn.sym} 0 0 0 0 {}\n"
        self.assertEqual(parse_content(sch_io_bare, "test.sch", repo_root=self.temp_dir), [])

        sch_device_bare = "C {lab_pin.sym} 0 0 0 0 {}\n"
        self.assertEqual(parse_content(sch_device_bare, "test.sch", repo_root=self.temp_dir), [])

        sch_device_prefix = "C {devices/lab_pin.sym} 0 0 0 0 {}\n"
        self.assertEqual(parse_content(sch_device_prefix, "test.sch", repo_root=self.temp_dir), [])

        sch_arbitrary_bare = "C {unknown_arbitrary_cell.sym} 0 0 0 0 {}\n"
        v_arb = parse_content(sch_arbitrary_bare, "test.sch", repo_root=self.temp_dir)
        self.assertTrue(any("unknown_arbitrary_cell.sym" in v.offending_reference for v in v_arb))

        sch_arbitrary_prefix = "C {sg13g2_pr/unknown_arbitrary_cell.sym} 0 0 0 0 {}\n"
        v_arb_pdk = parse_content(sch_arbitrary_prefix, "test.sch", repo_root=self.temp_dir)
        self.assertTrue(any("unknown_arbitrary_cell.sym" in v.offending_reference for v in v_arb_pdk))

    def test_pdk_external_models_without_checkout(self):
        spice_known = ".lib $PDK_ROOT/$PDK/libs.tech/ngspice/models/cornerMOSlv.lib mos_tt\n"
        self.assertEqual(parse_content(spice_known, "test.spice", repo_root=self.temp_dir), [])

        spice_unknown = ".lib $PDK_ROOT/$PDK/libs.tech/ngspice/models/fake_unknown_model.lib mos_tt\n"
        v_unk = parse_content(spice_unknown, "test.spice", repo_root=self.temp_dir)
        self.assertTrue(any("fake_unknown_model.lib" in v.offending_reference for v in v_unk))


if __name__ == "__main__":
    unittest.main()
