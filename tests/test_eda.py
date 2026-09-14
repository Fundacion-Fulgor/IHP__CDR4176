from importlib.machinery import SourceFileLoader
import importlib.util
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile
import unittest
import unittest.mock
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]

loader = SourceFileLoader("eda", str(ROOT / "eda"))
spec = importlib.util.spec_from_loader("eda", loader)
assert spec is not None
eda = importlib.util.module_from_spec(spec)
sys.modules["eda"] = eda
loader.exec_module(eda)


class TestEda(unittest.TestCase):
    def setUp(self):
        self.temp_dir_obj = tempfile.TemporaryDirectory()
        self.temp_dir = Path(self.temp_dir_obj.name)
        self.env_patcher = unittest.mock.patch.dict(os.environ)
        self.env_patcher.start()

    def tearDown(self):
        self.env_patcher.stop()
        self.temp_dir_obj.cleanup()

    def test_default_schematic(self):
        self.assertEqual(
            eda.DEFAULT_SCHEMATIC,
            "CDR4176-main/schematic/xschem/CDR4176/CDR4176.sch",
        )

    def test_no_cace_in_eda(self):
        eda_source = (ROOT / "eda").read_text(encoding="utf-8")
        self.assertNotIn("cace", eda_source.lower(), "EDA tool must not reference CACE")

    def test_pdk_root_resolution_pinned_and_external(self):
        os.environ.pop("PDK_ROOT", None)
        pinned = eda.get_pdk_root(ROOT)
        self.assertEqual(pinned, (ROOT / "IHP-Open-PDK").resolve())

        mock_ext_pdk = self.temp_dir / "custom_pdk"
        rc = mock_ext_pdk / "ihp-sg13g2" / "libs.tech" / "xschem" / "xschemrc"
        rc.parent.mkdir(parents=True, exist_ok=True)
        rc.write_text("mock rc")

        os.environ["PDK_ROOT"] = str(mock_ext_pdk)
        resolved = eda.get_pdk_root(ROOT)
        self.assertEqual(resolved, mock_ext_pdk.resolve())

    def test_netlist_destination_uses_cdr4176_main_simulation(self):
        eda_source = (ROOT / "eda").read_text(encoding="utf-8")
        self.assertIn('"CDR4176-main"', eda_source)
        self.assertIn('"simulation"', eda_source)
        self.assertNotIn('"runs"', eda_source)

    def test_resolve_schematic(self):
        mock_repo = self.temp_dir / "mock_repo_sch"
        mock_sch = mock_repo / "CDR4176-main" / "schematic" / "xschem" / "CDR4176" / "CDR4176.sch"
        mock_sch.parent.mkdir(parents=True, exist_ok=True)
        mock_sch.write_text("v {xschem}\n")
        resolved, err = eda.resolve_schematic(str(mock_sch), mock_repo)
        self.assertEqual(err, "")
        self.assertEqual(resolved, mock_sch.resolve())

        invalid_ext = mock_repo / "CDR4176-main" / "schematic" / "xschem" / "CDR4176" / "CDR4176.sym"
        resolved, err = eda.resolve_schematic(str(invalid_ext), mock_repo)
        self.assertIsNone(resolved)
        self.assertIn(".sch", err)

        outside = self.temp_dir / "outside.sch"
        outside.write_text("v {xschem}\n")
        resolved, err = eda.resolve_schematic(str(outside), mock_repo)
        self.assertIsNone(resolved)
        self.assertIn("Solo se permiten esquemáticos dentro de", err)

        legacy = mock_repo / "design" / "blocks" / "old.sch"
        resolved, err = eda.resolve_schematic(str(legacy), mock_repo)
        self.assertIsNone(resolved)

    def test_spice_scripts_never_assigned_to_models(self):
        os.environ.pop("SPICE_SCRIPTS", None)
        env = eda.get_eda_env(ROOT)
        self.assertNotIn("SPICE_SCRIPTS", env, "SPICE_SCRIPTS must not be assigned to model directory")

        os.environ["SPICE_SCRIPTS"] = "/system/ngspice/scripts"
        env_preserved = eda.get_eda_env(ROOT)
        self.assertEqual(env_preserved.get("SPICE_SCRIPTS"), "/system/ngspice/scripts")

    def test_init_simulation_directory(self):
        sim_dir = self.temp_dir / "sim_out"
        pdk_dir = self.temp_dir / "pdk"
        models_dir = pdk_dir / "ihp-sg13g2" / "libs.tech" / "ngspice" / "models"
        models_dir.mkdir(parents=True, exist_ok=True)
        rc = pdk_dir / "ihp-sg13g2" / "libs.tech" / "xschem" / "xschemrc"
        rc.parent.mkdir(parents=True, exist_ok=True)
        rc.write_text("rc")

        mock_userinit_dir = self.temp_dir / "user_home"
        mock_userinit_dir.mkdir(parents=True, exist_ok=True)
        mock_userinit = mock_userinit_dir / ".spiceinit"
        mock_userinit.write_text("echo user_custom\n")

        os.environ["PDK_ROOT"] = str(pdk_dir)
        os.environ["SPICE_USERINIT_DIR"] = str(mock_userinit_dir)
        spiceinit_file = eda.init_simulation_directory(sim_dir, ROOT)
        self.assertTrue(spiceinit_file.is_file())
        content = spiceinit_file.read_text(encoding="utf-8")
        self.assertIn("source .user-spiceinit", content)
        self.assertIn("setcs sourcepath = ( $sourcepath .pdk-models", content)
        self.assertNotIn("*", content)
        self.assertTrue((sim_dir / ".pdk-models").is_symlink())
        self.assertTrue((sim_dir / ".user-spiceinit").is_symlink())

    def test_init_simulation_directory_preserves_existing_spiceinit(self):
        sim_dir = self.temp_dir / "sim_existing"
        sim_dir.mkdir(parents=True, exist_ok=True)
        existing_spiceinit = sim_dir / ".spiceinit"
        existing_spiceinit.write_text("echo PRE_EXISTING\n")

        ret = eda.init_simulation_directory(sim_dir, ROOT)
        self.assertEqual(ret, existing_spiceinit)
        self.assertEqual(existing_spiceinit.read_text(encoding="utf-8"), "echo PRE_EXISTING\n")
        self.assertFalse((sim_dir / ".spiceinit.managed").exists())

    def test_osdi_lifecycle_refresh_and_stale_removal(self):
        sim_dir = self.temp_dir / "sim_osdi"
        pdk1_dir = self.temp_dir / "pdk1"
        osdi1_dir = pdk1_dir / "ihp-sg13g2" / "libs.tech" / "ngspice" / "osdi"
        models1_dir = pdk1_dir / "ihp-sg13g2" / "libs.tech" / "ngspice" / "models"
        rc1 = pdk1_dir / "ihp-sg13g2" / "libs.tech" / "xschem" / "xschemrc"
        rc1.parent.mkdir(parents=True, exist_ok=True)
        rc1.write_text("rc1")
        models1_dir.mkdir(parents=True, exist_ok=True)
        osdi1_dir.mkdir(parents=True, exist_ok=True)

        os.environ["PDK_ROOT"] = str(pdk1_dir)
        eda.init_simulation_directory(sim_dir, ROOT)
        init_content = (sim_dir / ".spiceinit").read_text(encoding="utf-8")
        self.assertNotIn("osdi", init_content)
        self.assertTrue((sim_dir / ".spiceinit.managed").is_file())

        machine = 0x3E if platform.machine().lower() in ("x86_64", "amd64") else 0xB7
        elf_data = b"\x7fELF\x02" + b"\x00" * 13 + machine.to_bytes(2, "little") + b"\x00" * 40
        (osdi1_dir / "modelA.osdi").write_bytes(elf_data)

        eda.init_simulation_directory(sim_dir, ROOT)
        refreshed_content = (sim_dir / ".spiceinit").read_text(encoding="utf-8")
        self.assertIn("osdi .osdi/modelA.osdi", refreshed_content)
        self.assertTrue((sim_dir / ".osdi" / "modelA.osdi").is_symlink())

        user_file = sim_dir / ".osdi" / "user_keep.txt"
        user_file.write_text("user content")

        pdk2_dir = self.temp_dir / "pdk2"
        osdi2_dir = pdk2_dir / "ihp-sg13g2" / "libs.tech" / "ngspice" / "osdi"
        models2_dir = pdk2_dir / "ihp-sg13g2" / "libs.tech" / "ngspice" / "models"
        rc2 = pdk2_dir / "ihp-sg13g2" / "libs.tech" / "xschem" / "xschemrc"
        rc2.parent.mkdir(parents=True, exist_ok=True)
        rc2.write_text("rc2")
        models2_dir.mkdir(parents=True, exist_ok=True)
        osdi2_dir.mkdir(parents=True, exist_ok=True)
        (osdi2_dir / "modelB.osdi").write_bytes(elf_data)

        os.environ["PDK_ROOT"] = str(pdk2_dir)
        eda.init_simulation_directory(sim_dir, ROOT)

        switched_content = (sim_dir / ".spiceinit").read_text(encoding="utf-8")
        self.assertIn("osdi .osdi/modelB.osdi", switched_content)
        self.assertNotIn("modelA.osdi", switched_content)
        self.assertFalse((sim_dir / ".osdi" / "modelA.osdi").exists())
        self.assertTrue((sim_dir / ".osdi" / "modelB.osdi").is_symlink())
        self.assertTrue(user_file.is_file())
        self.assertEqual(user_file.read_text(), "user content")

    def test_cmd_netlist_inits_output_for_non_lvs_and_skips_lvs(self):
        mock_repo = self.temp_dir / "mock_repo"
        mock_repo.mkdir(parents=True, exist_ok=True)
        (mock_repo / "xschemrc").write_text("mock rc\n")

        pdk_dir = mock_repo / "IHP-Open-PDK"
        pdk_models = pdk_dir / "ihp-sg13g2" / "libs.tech" / "ngspice" / "models"
        pdk_models.mkdir(parents=True, exist_ok=True)
        pdk_rc = pdk_dir / "ihp-sg13g2" / "libs.tech" / "xschem" / "xschemrc"
        pdk_rc.parent.mkdir(parents=True, exist_ok=True)
        pdk_rc.write_text("mock pdk rc\n")

        sch = mock_repo / "CDR4176-main" / "schematic" / "xschem" / "CDR4176" / "CDR4176.sch"
        sch.parent.mkdir(parents=True, exist_ok=True)
        sch.write_text("v {xschem}\n")

        out_sim_dir = mock_repo / "CDR4176-main" / "simulation" / "CDR4176"

        real_subprocess_run = subprocess.run

        def mock_subprocess_run(cmd, *args, **kwargs):
            if cmd and cmd[0] == "xschem":
                out_spice = out_sim_dir / "CDR4176.spice"
                out_spice.write_text("mock spice content\n")
                return subprocess.CompletedProcess(cmd, returncode=0, stdout="", stderr="")
            return real_subprocess_run(cmd, *args, **kwargs)

        os.environ.pop("PDK_ROOT", None)
        with patch.object(eda, "check_submodules_clean_and_aligned", return_value=(True, "")):
            with patch("subprocess.run", side_effect=mock_subprocess_run):
                ret = eda.cmd_netlist(str(sch), lvs=False, repo_root=mock_repo)
                self.assertEqual(ret, 0)
                self.assertTrue((out_sim_dir / ".spiceinit").is_file())
                self.assertTrue((out_sim_dir / ".spiceinit.managed").is_file())
                self.assertTrue((out_sim_dir / ".pdk-models").is_symlink())

                shutil.rmtree(out_sim_dir)
                ret_lvs = eda.cmd_netlist(str(sch), lvs=True, repo_root=mock_repo)
                self.assertEqual(ret_lvs, 0)
                self.assertFalse((out_sim_dir / ".spiceinit").exists())
                self.assertFalse((out_sim_dir / ".spiceinit.managed").exists())

    def test_init_simulation_directory_paths_with_spaces_and_smoke_ngspice(self):
        if shutil.which("ngspice") is None:
            self.skipTest("ngspice executable not found")

        base_test_dir = self.temp_dir / "spaces test"
        base_test_dir.mkdir(parents=True, exist_ok=True)

        pdk_dir = base_test_dir / "pdk with spaces"
        models_dir = pdk_dir / "ihp-sg13g2" / "libs.tech" / "ngspice" / "models"
        models_dir.mkdir(parents=True, exist_ok=True)
        rc = pdk_dir / "ihp-sg13g2" / "libs.tech" / "xschem" / "xschemrc"
        rc.parent.mkdir(parents=True, exist_ok=True)
        rc.write_text("rc")

        corner_file = models_dir / "cornerMOSlv.lib"
        corner_file.write_text(".lib mos_tt\n.endl mos_tt\n")

        sim_dir = base_test_dir / "sim dir with spaces"
        sim_dir.mkdir(parents=True, exist_ok=True)

        os.environ["PDK_ROOT"] = str(pdk_dir)
        eda.init_simulation_directory(sim_dir, self.temp_dir)

        circuit_file = sim_dir / "test.sp"
        circuit_file.write_text(
            "* circuit title\n"
            ".lib cornerMOSlv.lib mos_tt\n"
            "v1 1 0 1\n"
            "r1 1 0 1k\n"
            ".op\n"
            ".control\n"
            "run\n"
            ".endc\n"
            ".end\n"
        )

        res = subprocess.run(
            ["ngspice", "-b", str(circuit_file.name)],
            cwd=str(sim_dir),
            capture_output=True,
            text=True,
        )
        self.assertEqual(res.returncode, 0, msg=res.stderr)
        self.assertNotIn("Could not find library", res.stderr + res.stdout)
        self.assertNotIn("fatal error", res.stderr + res.stdout)

    def test_simulation_init_preserves_custom_files_and_links(self):
        pdk = self.temp_dir / "pdk"
        base = pdk / "ihp-sg13g2"
        for name in ("libs.tech/ngspice/models", "libs.ref/sg13g2_stdcell/spice", "libs.ref/sg13g2_io/spice", "libs.tech/ngspice/osdi", "libs.tech/xschem"):
            (base / name).mkdir(parents=True)
        (base / "libs.tech/xschem/xschemrc").write_text("rc")
        (base / "libs.tech/ngspice/osdi/model.osdi").write_bytes(b"fixture")
        user_dir = self.temp_dir / "user"
        user_dir.mkdir()
        (user_dir / ".spiceinit").write_text("set custom\n")
        os.environ["PDK_ROOT"] = str(pdk)
        os.environ["SPICE_USERINIT_DIR"] = str(user_dir)
        for managed in (False, True):
            for name in (".pdk-models", ".pdk-stdcell", ".pdk-io", ".user-spiceinit", ".osdi/model.osdi"):
                for as_link in (False, True):
                    with self.subTest(managed=managed, name=name, symlink=as_link):
                        sim = Path(tempfile.mkdtemp(dir=self.temp_dir))
                        if managed:
                            eda.init_simulation_directory(sim, ROOT)
                        custom = sim / name
                        custom.parent.mkdir(parents=True, exist_ok=True)
                        if custom.is_symlink():
                            custom.unlink()
                        target = sim / "user-data"
                        target.write_text("preserve me")
                        if as_link:
                            custom.symlink_to(target)
                        else:
                            custom.write_text("preserve me")
                        with self.assertRaises(FileExistsError):
                            eda.init_simulation_directory(sim, ROOT)
                        self.assertEqual(custom.read_text(), "preserve me")
                        self.assertEqual(custom.is_symlink(), as_link)

    def test_simulation_init_preserves_manual_edits(self):
        sim = self.temp_dir / "managed"
        eda.init_simulation_directory(sim, ROOT)
        init = sim / ".spiceinit"
        init.write_text("set custom\n")
        with self.assertRaises(FileExistsError):
            eda.init_simulation_directory(sim, ROOT)
        self.assertEqual(init.read_text(), "set custom\n")

    def test_quoting_and_spaces_robustness(self):
        repo_spaces = self.temp_dir / "repo with spaces"
        repo_spaces.mkdir()
        eda_link = repo_spaces / "eda"
        shutil_copy = (ROOT / "eda").read_text(encoding="utf-8")
        eda_link.write_text(shutil_copy)
        eda_link.chmod(0o755)

        res = subprocess.run(
            [sys.executable, str(eda_link), "--help"],
            cwd=str(repo_spaces),
            capture_output=True,
            text=True,
        )
        self.assertEqual(res.returncode, 0, msg=res.stderr)
        self.assertIn("CDR4176", res.stdout)


if __name__ == "__main__":
    unittest.main()
