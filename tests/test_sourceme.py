import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SOURCEME_FILE = ROOT / "SOURCEME"


def has_shell(shell_name: str) -> bool:
    return shutil.which(shell_name) is not None


class TestSourceme(unittest.TestCase):
    def setUp(self):
        self.temp_dir_obj = tempfile.TemporaryDirectory()
        self.temp_dir = Path(self.temp_dir_obj.name)

    def tearDown(self):
        self.temp_dir_obj.cleanup()

    def _create_mock_repo(self, path: Path) -> Path:
        pdk_ihp = path / "IHP-Open-PDK" / "ihp-sg13g2"
        tech_dir = pdk_ihp / "libs.tech" / "klayout" / "tech"
        gds_dir = pdk_ihp / "libs.ref" / "sg13g2_stdcell" / "gds"
        models_dir = pdk_ihp / "libs.tech" / "ngspice" / "models"
        lib_dir = path / "klayout" / "libraries"

        tech_dir.mkdir(parents=True, exist_ok=True)
        gds_dir.mkdir(parents=True, exist_ok=True)
        models_dir.mkdir(parents=True, exist_ok=True)
        lib_dir.mkdir(parents=True, exist_ok=True)

        (tech_dir / "sg13g2.lyt").write_text("mock_lyt")
        (gds_dir / "sg13g2_stdcell.gds").write_bytes(b"mock_gds")
        (models_dir / "cornerMOSlv.lib").write_text("mock_corner")

        rel_gds = os.path.relpath(gds_dir / "sg13g2_stdcell.gds", lib_dir)
        os.symlink(rel_gds, lib_dir / "sg13g2_stdcell.gds")

        shutil.copy(SOURCEME_FILE, path / "SOURCEME")
        return path / "SOURCEME"

    def _run_shell(self, shell: str, command: str, cwd: Path | None = None, env: dict | None = None):
        clean_env = os.environ.copy()
        for var in ("PDK_ROOT", "PDK", "KLAYOUT_PATH", "SPICE_SCRIPTS", "BASH_ENV", "ENV"):
            clean_env.pop(var, None)
        if env:
            clean_env.update(env)

        if shell == "bash":
            cmd_args = ["bash", "--noprofile", "--norc", "-c", command]
        elif shell == "zsh":
            cmd_args = ["zsh", "-f", "-c", command]
        else:
            cmd_args = [shell, "-c", command]

        return subprocess.run(
            cmd_args,
            cwd=cwd or ROOT,
            env=clean_env,
            capture_output=True,
            text=True,
        )

    def test_repo_symlink_static(self):
        symlink_path = ROOT / "klayout" / "libraries" / "sg13g2_stdcell.gds"
        self.assertTrue(
            symlink_path.is_symlink(),
            "klayout/libraries/sg13g2_stdcell.gds must exist and be a symlink",
        )
        target = os.readlink(symlink_path)
        self.assertFalse(os.path.isabs(target), "Symlink must be relative, not absolute")
        self.assertIn("IHP-Open-PDK", target)
        self.assertIn("sg13g2_stdcell.gds", target)
        expected_target = (
            ROOT
            / "IHP-Open-PDK"
            / "ihp-sg13g2"
            / "libs.ref"
            / "sg13g2_stdcell"
            / "gds"
            / "sg13g2_stdcell.gds"
        ).resolve(strict=False)
        self.assertEqual(symlink_path.resolve(strict=False), expected_target)

    def test_export_pinned_values(self):
        repo_sourceme = self._create_mock_repo(self.temp_dir / "repo")
        expected_pdk_root = str((repo_sourceme.parent / "IHP-Open-PDK").resolve())
        expected_klayout = ":".join([
            str((repo_sourceme.parent / "klayout").resolve()),
            str((repo_sourceme.parent / "IHP-Open-PDK" / "ihp-sg13g2" / "libs.tech" / "klayout").resolve()),
            str((repo_sourceme.parent / "IHP-Open-PDK" / "ihp-sg13g2" / "libs.tech" / "klayout" / "tech").resolve()),
        ])

        shells = ["bash"]
        if has_shell("zsh"):
            shells.append("zsh")

        for shell in shells:
            with self.subTest(shell=shell):
                cmd = (
                    f'source "{repo_sourceme}"\n'
                    f'printf "%s\\n%s\\n%s\\n%s\\n" "$PDK_ROOT" "$PDK" "$KLAYOUT_PATH" "${{SPICE_SCRIPTS:-UNSET}}"\n'
                )
                res = self._run_shell(shell, cmd, cwd=ROOT)
                self.assertEqual(res.returncode, 0, msg=res.stderr)
                lines = res.stdout.strip().splitlines()
                self.assertEqual(lines[0], expected_pdk_root)
                self.assertEqual(lines[1], "ihp-sg13g2")
                self.assertEqual(lines[2], expected_klayout)
                self.assertEqual(lines[3], "UNSET", "SPICE_SCRIPTS must not be exported to model directory")

    def test_external_pdk_respected(self):
        repo_sourceme = self._create_mock_repo(self.temp_dir / "repo")
        ext_pdk_root = self.temp_dir / "external_pdk"
        ext_ihp = ext_pdk_root / "ihp-sg13g2"
        ext_tech = ext_ihp / "libs.tech" / "klayout" / "tech"
        ext_gds = ext_ihp / "libs.ref" / "sg13g2_stdcell" / "gds"
        ext_models = ext_ihp / "libs.tech" / "ngspice" / "models"

        ext_tech.mkdir(parents=True, exist_ok=True)
        ext_gds.mkdir(parents=True, exist_ok=True)
        ext_models.mkdir(parents=True, exist_ok=True)
        (ext_tech / "sg13g2.lyt").write_text("ext_lyt")
        (ext_gds / "sg13g2_stdcell.gds").write_bytes(b"ext_gds")

        expected_pdk_root = str(ext_pdk_root.resolve())

        shells = ["bash"]
        if has_shell("zsh"):
            shells.append("zsh")

        for shell in shells:
            with self.subTest(shell=shell):
                cmd = (
                    f'source "{repo_sourceme}"\n'
                    f'printf "%s\\n%s\\n%s\\n" "$PDK_ROOT" "$PDK" "$KLAYOUT_PATH"\n'
                )
                res = self._run_shell(shell, cmd, env={"PDK_ROOT": str(ext_pdk_root)})
                self.assertEqual(res.returncode, 0, msg=res.stderr)
                lines = res.stdout.strip().splitlines()
                self.assertEqual(lines[0], expected_pdk_root)
                self.assertEqual(lines[1], "ihp-sg13g2")
                klayout_parts = lines[2].split(":")
                self.assertNotIn(
                    str((repo_sourceme.parent / "klayout").resolve()),
                    klayout_parts,
                    "Pinned klayout repo directory must not be loaded when using external PDK",
                )
                self.assertIn(str(ext_tech.resolve()), klayout_parts)
                self.assertIn(str((ext_ihp / "libs.tech" / "klayout").resolve()), klayout_parts)
                ext_entry = [p for p in klayout_parts if "klayout-external" in p]
                self.assertTrue(ext_entry, "External klayout directory must be in KLAYOUT_PATH")
                ext_gds_link = Path(ext_entry[0]) / "libraries" / "sg13g2_stdcell.gds"
                self.assertTrue(ext_gds_link.is_symlink())
                self.assertEqual(ext_gds_link.resolve(), (ext_gds / "sg13g2_stdcell.gds").resolve())

    def test_repeated_sourcing_and_pdk_change_cleans_klayout_path(self):
        repo_sourceme = self._create_mock_repo(self.temp_dir / "repo_repeat")
        ext_pdk_root = self.temp_dir / "external_pdk_repeat"
        ext_ihp = ext_pdk_root / "ihp-sg13g2"
        ext_tech = ext_ihp / "libs.tech" / "klayout" / "tech"
        ext_gds = ext_ihp / "libs.ref" / "sg13g2_stdcell" / "gds"

        ext_tech.mkdir(parents=True, exist_ok=True)
        ext_gds.mkdir(parents=True, exist_ok=True)
        (ext_tech / "sg13g2.lyt").write_text("ext_lyt")
        (ext_gds / "sg13g2_stdcell.gds").write_bytes(b"ext_gds")

        shells = ["bash"]
        if has_shell("zsh"):
            shells.append("zsh")

        for shell in shells:
            with self.subTest(shell=shell):
                cmd = (
                    f'source "{repo_sourceme}"\n'
                    f'export PDK_ROOT="{str(ext_pdk_root)}"\n'
                    f'source "{repo_sourceme}"\n'
                    f'after_ext="$KLAYOUT_PATH"\n'
                    f'unset PDK_ROOT\n'
                    f'source "{repo_sourceme}"\n'
                    f'after_pinned="$KLAYOUT_PATH"\n'
                    f'printf "%s\\n---\\n%s\\n" "$after_ext" "$after_pinned"\n'
                )
                res = self._run_shell(shell, cmd, env={"KLAYOUT_PATH": "/opt/custom/plugin"})
                self.assertEqual(res.returncode, 0, msg=res.stderr)
                parts = res.stdout.strip().split("\n---\n")
                ext_parts = parts[0].split(":")
                pinned_parts = parts[1].split(":")

                self.assertNotIn(str((repo_sourceme.parent / "klayout").resolve()), ext_parts)
                self.assertIn("/opt/custom/plugin", ext_parts)

                self.assertNotIn(str((ext_ihp / "libs.tech" / "klayout").resolve()), pinned_parts)
                self.assertIn(str((repo_sourceme.parent / "klayout").resolve()), pinned_parts)
                self.assertIn("/opt/custom/plugin", pinned_parts)

    def test_spice_scripts_preserved_never_assigned_to_models(self):
        repo_sourceme = self._create_mock_repo(self.temp_dir / "repo")
        shells = ["bash"]
        if has_shell("zsh"):
            shells.append("zsh")

        for shell in shells:
            with self.subTest(shell=shell, case="preset"):
                cmd = (
                    f'source "{repo_sourceme}"\n'
                    f'echo "$SPICE_SCRIPTS"\n'
                )
                res = self._run_shell(shell, cmd, env={"SPICE_SCRIPTS": "/system/spinit/dir"})
                self.assertEqual(res.returncode, 0, msg=res.stderr)
                self.assertEqual(res.stdout.strip(), "/system/spinit/dir")

            with self.subTest(shell=shell, case="unset"):
                cmd = (
                    f'source "{repo_sourceme}"\n'
                    f'echo "${{SPICE_SCRIPTS:-UNSET}}"\n'
                )
                res = self._run_shell(shell, cmd)
                self.assertEqual(res.returncode, 0, msg=res.stderr)
                self.assertEqual(res.stdout.strip(), "UNSET")

    def test_external_pdk_works_without_pinned_symlink(self):
        repo_sourceme = self._create_mock_repo(self.temp_dir / "repo_no_submodule")
        pinned_symlink = repo_sourceme.parent / "klayout" / "libraries" / "sg13g2_stdcell.gds"
        pinned_symlink.unlink()

        ext_pdk_root = self.temp_dir / "external_pdk2"
        ext_ihp = ext_pdk_root / "ihp-sg13g2"
        ext_tech = ext_ihp / "libs.tech" / "klayout" / "tech"
        ext_gds = ext_ihp / "libs.ref" / "sg13g2_stdcell" / "gds"

        ext_tech.mkdir(parents=True, exist_ok=True)
        ext_gds.mkdir(parents=True, exist_ok=True)
        (ext_tech / "sg13g2.lyt").write_text("ext_lyt")
        (ext_gds / "sg13g2_stdcell.gds").write_bytes(b"ext_gds")

        shells = ["bash"]
        if has_shell("zsh"):
            shells.append("zsh")

        for shell in shells:
            with self.subTest(shell=shell):
                cmd = (
                    f'source "{repo_sourceme}"\n'
                    f'echo "$PDK_ROOT"\n'
                )
                res = self._run_shell(shell, cmd, env={"PDK_ROOT": str(ext_pdk_root)})
                self.assertEqual(res.returncode, 0, msg=res.stderr)
                self.assertEqual(res.stdout.strip(), str(ext_pdk_root.resolve()))

    def test_arbitrary_working_directory(self):
        repo_sourceme = self._create_mock_repo(self.temp_dir / "repo")
        outside_dir = self.temp_dir / "outside"
        outside_dir.mkdir()
        expected_pdk_root = str((repo_sourceme.parent / "IHP-Open-PDK").resolve())

        shells = ["bash"]
        if has_shell("zsh"):
            shells.append("zsh")

        for shell in shells:
            with self.subTest(shell=shell):
                cmd = f'source "{repo_sourceme}"\necho "$PDK_ROOT"\n'
                res = self._run_shell(shell, cmd, cwd=outside_dir)
                self.assertEqual(res.returncode, 0, msg=res.stderr)
                self.assertEqual(res.stdout.strip(), expected_pdk_root)

    def test_paths_with_spaces(self):
        repo_with_spaces = self.temp_dir / "repo with spaces in name"
        repo_with_spaces.mkdir()
        repo_sourceme = self._create_mock_repo(repo_with_spaces)
        expected_pdk_root = str((repo_with_spaces / "IHP-Open-PDK").resolve())

        shells = ["bash"]
        if has_shell("zsh"):
            shells.append("zsh")

        for shell in shells:
            with self.subTest(shell=shell):
                cmd = f'source "{repo_sourceme}"\necho "$PDK_ROOT"\n'
                res = self._run_shell(shell, cmd)
                self.assertEqual(res.returncode, 0, msg=res.stderr)
                self.assertEqual(res.stdout.strip(), expected_pdk_root)

    def test_inherited_klayout_path_preserved_and_idempotent(self):
        repo_sourceme = self._create_mock_repo(self.temp_dir / "repo")
        inherited = "/custom/klayout/path:/opt/other/klayout"
        shells = ["bash"]
        if has_shell("zsh"):
            shells.append("zsh")

        for shell in shells:
            with self.subTest(shell=shell):
                cmd = (
                    f'source "{repo_sourceme}"\n'
                    f'first="$KLAYOUT_PATH"\n'
                    f'source "{repo_sourceme}"\n'
                    f'second="$KLAYOUT_PATH"\n'
                    f'printf "%s\\n%s\\n" "$first" "$second"\n'
                )
                res = self._run_shell(shell, cmd, env={"KLAYOUT_PATH": inherited})
                self.assertEqual(res.returncode, 0, msg=res.stderr)
                lines = res.stdout.strip().splitlines()
                self.assertEqual(lines[0], lines[1])
                self.assertTrue(lines[0].endswith(f":{inherited}"))

    def test_shell_options_and_cwd_unchanged(self):
        repo_sourceme = self._create_mock_repo(self.temp_dir / "repo")
        outside_dir = self.temp_dir / "outside"
        outside_dir.mkdir()

        shells = ["bash"]
        if has_shell("zsh"):
            shells.append("zsh")

        for shell in shells:
            with self.subTest(shell=shell):
                cmd = (
                    f'opt_before="$-"; cwd_before="$PWD"\n'
                    f'source "{repo_sourceme}"\n'
                    f'opt_after="$-"; cwd_after="$PWD"\n'
                    f'printf "%s|%s|%s|%s\\n" "$opt_before" "$opt_after" "$cwd_before" "$cwd_after"\n'
                )
                res = self._run_shell(shell, cmd, cwd=outside_dir)
                self.assertEqual(res.returncode, 0, msg=res.stderr)
                parts = res.stdout.strip().split("|")
                self.assertEqual(parts[0], parts[1], "Shell options changed")
                self.assertEqual(parts[2], parts[3], "Working directory changed")

    def test_compatible_with_set_eu(self):
        repo_sourceme = self._create_mock_repo(self.temp_dir / "repo")
        shells = ["bash"]
        if has_shell("zsh"):
            shells.append("zsh")

        for shell in shells:
            with self.subTest(shell=shell):
                cmd = (
                    "set -eu\n"
                    f'source "{repo_sourceme}"\n'
                    "echo success\n"
                )
                res = self._run_shell(shell, cmd)
                self.assertEqual(res.returncode, 0, msg=res.stderr)
                self.assertEqual(res.stdout.strip(), "success")

    def test_incomplete_pdk_fails_cleanly(self):
        empty_repo = self.temp_dir / "incomplete_repo"
        empty_repo.mkdir()
        shutil.copy(SOURCEME_FILE, empty_repo / "SOURCEME")
        incomplete_sourceme = empty_repo / "SOURCEME"

        prior_env = {
            "PDK_ROOT": "/prior/pdk/root",
            "PDK": "prior-pdk",
            "KLAYOUT_PATH": "/prior/klayout/path",
        }

        shells = ["bash"]
        if has_shell("zsh"):
            shells.append("zsh")

        for shell in shells:
            with self.subTest(shell=shell):
                cmd = (
                    f'source "{incomplete_sourceme}"; ret=$?\n'
                    'printf "ret=%s|pdk_root=%s|pdk=%s|klayout=%s|alive\\n" '
                    '"$ret" "$PDK_ROOT" "$PDK" "$KLAYOUT_PATH"\n'
                )
                res = self._run_shell(shell, cmd, env=prior_env)
                self.assertEqual(res.returncode, 0)
                parts = res.stdout.strip().split("|")
                self.assertEqual(parts[0], "ret=1")
                self.assertEqual(parts[1], "pdk_root=/prior/pdk/root")
                self.assertEqual(parts[2], "pdk=prior-pdk")
                self.assertEqual(parts[3], "klayout=/prior/klayout/path")
                self.assertEqual(parts[4], "alive")
                self.assertIn("git submodule update --init --recursive", res.stderr)

    def test_missing_symlink_fails_cleanly(self):
        repo_path = self.temp_dir / "missing_symlink_repo"
        repo_sourceme = self._create_mock_repo(repo_path)
        symlink = repo_path / "klayout" / "libraries" / "sg13g2_stdcell.gds"
        symlink.unlink()

        prior_env = {
            "PDK_ROOT": "/prior/pdk/root",
            "PDK": "prior-pdk",
            "KLAYOUT_PATH": "/prior/klayout/path",
        }

        shells = ["bash"]
        if has_shell("zsh"):
            shells.append("zsh")

        for shell in shells:
            with self.subTest(shell=shell):
                cmd = (
                    f'source "{repo_sourceme}"; ret=$?\n'
                    'printf "ret=%s|pdk_root=%s|pdk=%s|klayout=%s|alive\\n" '
                    '"$ret" "$PDK_ROOT" "$PDK" "$KLAYOUT_PATH"\n'
                )
                res = self._run_shell(shell, cmd, env=prior_env)
                self.assertEqual(res.returncode, 0)
                parts = res.stdout.strip().split("|")
                self.assertEqual(parts[0], "ret=1")
                self.assertEqual(parts[1], "pdk_root=/prior/pdk/root")
                self.assertEqual(parts[2], "pdk=prior-pdk")
                self.assertEqual(parts[3], "klayout=/prior/klayout/path")
                self.assertEqual(parts[4], "alive")

    def test_missing_lyt_fails_cleanly(self):
        repo_path = self.temp_dir / "missing_lyt_repo"
        repo_sourceme = self._create_mock_repo(repo_path)
        lyt_file = repo_path / "IHP-Open-PDK" / "ihp-sg13g2" / "libs.tech" / "klayout" / "tech" / "sg13g2.lyt"
        lyt_file.unlink()

        prior_env = {
            "PDK_ROOT": "/prior/pdk/root",
            "PDK": "prior-pdk",
            "KLAYOUT_PATH": "/prior/klayout/path",
        }

        shells = ["bash"]
        if has_shell("zsh"):
            shells.append("zsh")

        for shell in shells:
            with self.subTest(shell=shell):
                cmd = (
                    f'source "{repo_sourceme}"; ret=$?\n'
                    'printf "ret=%s|pdk_root=%s|pdk=%s|klayout=%s|alive\\n" '
                    '"$ret" "$PDK_ROOT" "$PDK" "$KLAYOUT_PATH"\n'
                )
                res = self._run_shell(shell, cmd, env=prior_env)
                self.assertEqual(res.returncode, 0)
                parts = res.stdout.strip().split("|")
                self.assertEqual(parts[0], "ret=1")
                self.assertEqual(parts[1], "pdk_root=/prior/pdk/root")
                self.assertEqual(parts[2], "pdk=prior-pdk")
                self.assertEqual(parts[3], "klayout=/prior/klayout/path")
                self.assertEqual(parts[4], "alive")

    def test_direct_execution_detection(self):
        repo_sourceme = self._create_mock_repo(self.temp_dir / "repo")
        shells = ["bash"]
        if has_shell("zsh"):
            shells.append("zsh")

        for shell in shells:
            with self.subTest(shell=shell):
                cmd = (
                    ["bash", "--noprofile", "--norc", str(repo_sourceme)]
                    if shell == "bash"
                    else ["zsh", "-f", str(repo_sourceme)]
                )
                res = subprocess.run(cmd, capture_output=True, text=True)
                self.assertNotEqual(res.returncode, 0)
                self.assertIn("must be sourced", res.stderr)

    def test_cleanup_helpers_on_success_and_failure(self):
        repo_sourceme = self._create_mock_repo(self.temp_dir / "repo")
        shells = ["bash"]
        if has_shell("zsh"):
            shells.append("zsh")

        for shell in shells:
            with self.subTest(shell=shell, case="success"):
                cmd = (
                    f'source "{repo_sourceme}"\n'
                    'typeset -f _sourceme_main >/dev/null && echo "func_main_exists"\n'
                    'typeset -f _sourceme_add_path >/dev/null && echo "func_add_exists"\n'
                    'echo "done"\n'
                )
                res = self._run_shell(shell, cmd)
                self.assertEqual(res.returncode, 0, msg=res.stderr)
                self.assertNotIn("func_main_exists", res.stdout)
                self.assertNotIn("func_add_exists", res.stdout)
                self.assertIn("done", res.stdout)

            with self.subTest(shell=shell, case="failure"):
                fail_dir = self.temp_dir / f"fail_{shell}"
                fail_dir.mkdir()
                shutil.copy(SOURCEME_FILE, fail_dir / "SOURCEME")
                fail_sourceme = fail_dir / "SOURCEME"
                cmd = (
                    f'source "{fail_sourceme}"; ret=$?\n'
                    'typeset -f _sourceme_main >/dev/null && echo "func_main_exists"\n'
                    'typeset -f _sourceme_add_path >/dev/null && echo "func_add_exists"\n'
                    'echo "ret=$ret"\n'
                )
                res = self._run_shell(shell, cmd)
                self.assertEqual(res.returncode, 0)
                self.assertNotIn("func_main_exists", res.stdout)
                self.assertNotIn("func_add_exists", res.stdout)
                self.assertIn("ret=1", res.stdout)


if __name__ == "__main__":
    unittest.main()
