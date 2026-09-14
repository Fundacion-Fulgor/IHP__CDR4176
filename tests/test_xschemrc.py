import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
XSCHEMRC_FILE = ROOT / "xschemrc"


class TestXschemrc(unittest.TestCase):
    def setUp(self):
        self.temp_dir_obj = tempfile.TemporaryDirectory()
        self.temp_dir = Path(self.temp_dir_obj.name)

    def tearDown(self):
        self.temp_dir_obj.cleanup()

    def _create_mock_repo(self, path: Path) -> Path:
        pdk_dir = path / "IHP-Open-PDK" / "ihp-sg13g2"
        xschem_tech = pdk_dir / "libs.tech" / "xschem"
        ngspice_models = pdk_dir / "libs.tech" / "ngspice" / "models"
        stdcell_sym = pdk_dir / "libs.ref" / "sg13g2_stdcell" / "sym" / "xschem"
        pr_sym = pdk_dir / "libs.ref" / "sg13g2_pr" / "xschem"
        io_dir = path / "openpdk-libraries" / "ihp-sg13g2" / "sg13g2_io" / "xschem"
        main_sch = path / "CDR4176-main" / "schematic" / "xschem" / "cell1"
        tb_sch = path / "CDR4176-main" / "testbenches" / "tran" / "xschem"

        xschem_tech.mkdir(parents=True, exist_ok=True)
        ngspice_models.mkdir(parents=True, exist_ok=True)
        stdcell_sym.mkdir(parents=True, exist_ok=True)
        pr_sym.mkdir(parents=True, exist_ok=True)
        io_dir.mkdir(parents=True, exist_ok=True)
        main_sch.mkdir(parents=True, exist_ok=True)
        tb_sch.mkdir(parents=True, exist_ok=True)

        pdk_rc = xschem_tech / "xschemrc"
        pdk_rc.write_text(
            "set MODELS_NGSPICE [file join $PDK_ROOT $PDK libs.tech ngspice models]\n"
            "set SG13G2_MODELS $MODELS_NGSPICE\n"
        )
        (path / "xschemrc").write_text(XSCHEMRC_FILE.read_text(encoding="utf-8"))
        shutil.copy2(ROOT / "eda", path / "eda")
        (path / "eda").chmod(0o755)
        return path

    def _run_tcl(self, script: str, cwd: Path | None = None, env: dict | None = None) -> subprocess.CompletedProcess[str]:
        run_env = os.environ.copy()
        if env:
            run_env.update(env)
        return subprocess.run(
            ["tclsh"],
            input=script,
            cwd=str(cwd or ROOT),
            env=run_env,
            capture_output=True,
            text=True,
        )

    def test_xschemrc_loads_cleanly(self):
        repo = self._create_mock_repo(self.temp_dir / "repo")
        script = f"""
        source "{str(repo / 'xschemrc')}"
        puts "LOADED_OK"
        """
        res = self._run_tcl(script, cwd=repo)
        self.assertEqual(res.returncode, 0, msg=res.stderr)
        self.assertIn("LOADED_OK", res.stdout)

    def test_default_netlist_dir(self):
        repo = self._create_mock_repo(self.temp_dir / "repo")
        script = f"""
        source "{str(repo / 'xschemrc')}"
        puts "NETLIST_DIR=$netlist_dir"
        """
        res = self._run_tcl(script, cwd=repo)
        self.assertEqual(res.returncode, 0, msg=res.stderr)
        expected = str((repo / "CDR4176-main" / "simulation").resolve())
        self.assertIn(f"NETLIST_DIR={expected}", res.stdout)

    def test_preserves_explicit_netlist_dir_override(self):
        repo = self._create_mock_repo(self.temp_dir / "repo")
        custom_out = str((self.temp_dir / "custom_simulation").resolve())
        script = f"""
        set netlist_dir "{custom_out}"
        source "{str(repo / 'xschemrc')}"
        puts "NETLIST_DIR=$netlist_dir"
        """
        res = self._run_tcl(script, cwd=repo)
        self.assertEqual(res.returncode, 0, msg=res.stderr)
        self.assertIn(f"NETLIST_DIR={custom_out}", res.stdout)

    def test_spice_scripts_never_assigned_to_models(self):
        repo = self._create_mock_repo(self.temp_dir / "repo")
        script = f"""
        source "{str(repo / 'xschemrc')}"
        if {{[info exists env(SPICE_SCRIPTS)]}} {{
            puts "ENV_SPICE_SCRIPTS=$env(SPICE_SCRIPTS)"
        }} else {{
            puts "ENV_SPICE_SCRIPTS=UNSET"
        }}
        if {{[info exists SPICE_SCRIPTS]}} {{
            puts "VAR_SPICE_SCRIPTS=$SPICE_SCRIPTS"
        }} else {{
            puts "VAR_SPICE_SCRIPTS=UNSET"
        }}
        """
        res = self._run_tcl(script, cwd=repo)
        self.assertEqual(res.returncode, 0, msg=res.stderr)
        self.assertIn("ENV_SPICE_SCRIPTS=UNSET", res.stdout)
        self.assertIn("VAR_SPICE_SCRIPTS=UNSET", res.stdout)

        script_with_prior = f"""
        source "{str(repo / 'xschemrc')}"
        puts "ENV_SPICE_SCRIPTS=$env(SPICE_SCRIPTS)"
        """
        res_prior = self._run_tcl(script_with_prior, cwd=repo, env={"SPICE_SCRIPTS": "/custom/spinit_dir"})
        self.assertEqual(res_prior.returncode, 0, msg=res_prior.stderr)
        self.assertIn("ENV_SPICE_SCRIPTS=/custom/spinit_dir", res_prior.stdout)

    def test_local_simulation_spiceinit_created(self):
        repo = self._create_mock_repo(self.temp_dir / "repo")
        script = f"""
        source "{str(repo / 'xschemrc')}"
        """
        res = self._run_tcl(script, cwd=repo)
        self.assertEqual(res.returncode, 0, msg=res.stderr)
        sim_dir = repo / "CDR4176-main" / "simulation"
        spiceinit = sim_dir / ".spiceinit"
        self.assertTrue(spiceinit.is_file(), ".spiceinit must be initialized in netlist_dir")
        content = spiceinit.read_text(encoding="utf-8")
        self.assertIn("setcs sourcepath = ( $sourcepath .pdk-models", content)
        self.assertNotIn("*", content)
        self.assertTrue((sim_dir / ".pdk-models").is_symlink())

    def test_library_paths_excludes_project_io(self):
        repo = self._create_mock_repo(self.temp_dir / "repo")
        script = f"""
        source "{str(repo / 'xschemrc')}"
        puts "XSCHEM_LIBRARY_PATH=$XSCHEM_LIBRARY_PATH"
        """
        res = self._run_tcl(script, cwd=repo)
        self.assertEqual(res.returncode, 0, msg=res.stderr)
        lib_path = ""
        for line in res.stdout.splitlines():
            if line.startswith("XSCHEM_LIBRARY_PATH="):
                lib_path = line.split("=", 1)[1]
        self.assertTrue(lib_path, "XSCHEM_LIBRARY_PATH was not printed")
        dirs = [d for d in lib_path.split(":") if d]
        for d in dirs:
            self.assertFalse(
                Path(d).name == "project_io",
                f"project_io must not be a bare search path, found in {d}",
            )

    def test_no_legacy_design_dir_in_library_paths(self):
        repo = self._create_mock_repo(self.temp_dir / "repo")
        legacy_dir = repo / "design"
        legacy_dir.mkdir(parents=True, exist_ok=True)
        script = f"""
        source "{str(repo / 'xschemrc')}"
        puts "XSCHEM_LIBRARY_PATH=$XSCHEM_LIBRARY_PATH"
        """
        res = self._run_tcl(script, cwd=repo)
        self.assertEqual(res.returncode, 0, msg=res.stderr)
        lib_path = ""
        for line in res.stdout.splitlines():
            if line.startswith("XSCHEM_LIBRARY_PATH="):
                lib_path = line.split("=", 1)[1]
        dirs = [d for d in lib_path.split(":") if d]
        for d in dirs:
            self.assertFalse(
                Path(d) == legacy_dir.resolve(),
                f"legacy design dir must not be in XSCHEM_LIBRARY_PATH, found {d}",
            )

    def test_external_pdk_respected_in_xschemrc(self):
        repo = self._create_mock_repo(self.temp_dir / "repo")
        ext_pdk_root = self.temp_dir / "external_pdk"
        ext_ihp = ext_pdk_root / "ihp-sg13g2"
        ext_xschem = ext_ihp / "libs.tech" / "xschem"
        ext_ngspice = ext_ihp / "libs.tech" / "ngspice" / "models"
        ext_xschem.mkdir(parents=True, exist_ok=True)
        ext_ngspice.mkdir(parents=True, exist_ok=True)
        (ext_xschem / "xschemrc").write_text("set MODELS_NGSPICE [file join $PDK_ROOT $PDK libs.tech ngspice models]\n")

        script = f"""
        set env(PDK_ROOT) "{str(ext_pdk_root)}"
        source "{str(repo / 'xschemrc')}"
        puts "PDK_ROOT=$PDK_ROOT"
        puts "MODELS_NGSPICE=$MODELS_NGSPICE"
        """
        res = self._run_tcl(script, cwd=repo)
        self.assertEqual(res.returncode, 0, msg=res.stderr)
        self.assertIn(f"PDK_ROOT={str(ext_pdk_root.resolve())}", res.stdout)
        self.assertIn(f"MODELS_NGSPICE={str(ext_ngspice.resolve())}", res.stdout)


if __name__ == "__main__":
    unittest.main()
