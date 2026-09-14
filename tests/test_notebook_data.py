from __future__ import annotations

import os
from pathlib import Path
import tempfile
import unittest

from scripts.notebook_data import (
    NOTEBOOK_DATA_MAPPING,
    find_repo_root,
    get_data_dir,
    normalize_notebook_id,
    read_raw,
    readRaw,
    resolve_raw_path,
)


class TestNotebookData(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir_obj = tempfile.TemporaryDirectory()
        self.temp_dir = Path(self.temp_dir_obj.name)
        self.orig_root = os.environ.get("CDR4176_ROOT")
        self.orig_results = os.environ.get("CDR4176_RESULTS")
        os.environ.pop("CDR4176_ROOT", None)
        os.environ.pop("CDR4176_RESULTS", None)

    def tearDown(self) -> None:
        if self.orig_root is not None:
            os.environ["CDR4176_ROOT"] = self.orig_root
        else:
            os.environ.pop("CDR4176_ROOT", None)

        if self.orig_results is not None:
            os.environ["CDR4176_RESULTS"] = self.orig_results
        else:
            os.environ.pop("CDR4176_RESULTS", None)

        self.temp_dir_obj.cleanup()

    def test_find_repo_root_default(self) -> None:
        root = find_repo_root()
        self.assertTrue((root / "project.yml").is_file() or (root / "CDR4176-main").is_dir())

    def test_find_repo_root_with_env_override(self) -> None:
        custom_dir = self.temp_dir / "custom_root"
        custom_dir.mkdir(parents=True, exist_ok=True)
        os.environ["CDR4176_ROOT"] = str(custom_dir)
        self.assertEqual(find_repo_root(), custom_dir.resolve())

    def test_find_repo_root_from_cwd_ancestry(self) -> None:
        mock_root = self.temp_dir / "mock_project"
        mock_root.mkdir(parents=True, exist_ok=True)
        (mock_root / "project.yml").write_text("title: test\n")
        nested_dir = mock_root / "CDR4176-main" / "verification" / "python" / "simulations"
        nested_dir.mkdir(parents=True, exist_ok=True)
        found = find_repo_root(start=nested_dir)
        self.assertEqual(found, mock_root.resolve())

    def test_temp_root_with_spaces_and_absent_data(self) -> None:
        repo_with_spaces = self.temp_dir / "repo path with spaces"
        nested = repo_with_spaces / "CDR4176-main" / "verification" / "python"
        nested.mkdir(parents=True, exist_ok=True)
        (repo_with_spaces / "project.yml").write_text("title: test with spaces\n")

        os.environ["CDR4176_ROOT"] = str(repo_with_spaces)
        self.assertEqual(find_repo_root(start=nested), repo_with_spaces.resolve())

        with self.assertRaises(FileNotFoundError) as ctx:
            resolve_raw_path("tran_linearity_integration.raw", "verification/scripts/results_tb_linearity_integration.ipynb")
        msg = str(ctx.exception)
        self.assertIn("Raw dumps are no longer tracked in repository", msg)
        self.assertIn("CDR4176_RESULTS", msg)
        self.assertIn("tran_linearity_integration.raw", msg)

    def test_notebook_mapping_keys(self) -> None:
        expected_mappings = {
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
        self.assertEqual(NOTEBOOK_DATA_MAPPING, expected_mappings)

    def test_normalize_notebook_id(self) -> None:
        norm1 = normalize_notebook_id("CDR4176-main/verification/python/verification/scripts/result_simulation_3to7thermo_V2.ipynb")
        self.assertEqual(norm1, "verification/scripts/result_simulation_3to7thermo_V2.ipynb")
        norm2 = normalize_notebook_id("verification/scripts/result_simulation_3to7thermo_V2")
        self.assertEqual(norm2, "verification/scripts/result_simulation_3to7thermo_V2.ipynb")

    def test_tb_linearity_8xpi_missing_error(self) -> None:
        with self.assertRaises(FileNotFoundError) as ctx:
            resolve_raw_path(
                "tran_linearity_termoless.raw",
                "simulations/tb_linearity_8xpi/results_tb_linearity_termoless.ipynb",
                repo_root=self.temp_dir,
            )
        msg = str(ctx.exception)
        self.assertIn("Raw dumps are no longer tracked in repository", msg)
        self.assertIn("legacy/tb_linearity_8xpi", msg)

    def test_legacy_datasets_resolve(self) -> None:
        for notebook_id, relative_dir in NOTEBOOK_DATA_MAPPING.items():
            with self.subTest(notebook=notebook_id):
                dataset = self.temp_dir / "CDR4176-main/verification/results" / relative_dir / "wave.raw"
                dataset.parent.mkdir(parents=True, exist_ok=True)
                dataset.write_text("Title: fixture\n", encoding="utf-8")
                resolved = resolve_raw_path("wave.raw", notebook_id, repo_root=self.temp_dir)
                self.assertEqual(resolved, dataset.resolve())

    def test_cdr4176_results_env_override(self) -> None:
        fresh_dir = self.temp_dir / "fresh_results" / "tb_linearity_8xpi"
        fresh_dir.mkdir(parents=True, exist_ok=True)
        fresh_file = fresh_dir / "tran_linearity_termoless.raw"
        fresh_file.write_text("Title: fresh\nVariables:\n0 time time\n1 v(out) voltage\nValues:\n 0 0.0\n 1.0\n")

        os.environ["CDR4176_RESULTS"] = str(self.temp_dir / "fresh_results")
        resolved = resolve_raw_path(
            "tran_linearity_termoless.raw",
            "simulations/tb_linearity_8xpi/results_tb_linearity_termoless.ipynb",
        )
        self.assertEqual(resolved, fresh_file.resolve())

    def test_cdr4176_results_override_missing_file_raises_actionable_error(self) -> None:
        empty_dir = self.temp_dir / "empty_results"
        empty_dir.mkdir(parents=True, exist_ok=True)
        os.environ["CDR4176_RESULTS"] = str(empty_dir)

        with self.assertRaises(FileNotFoundError) as ctx:
            resolve_raw_path(
                "tran_linearity_integration.raw",
                "simulations/simulation/results_tb_linearity_integration.ipynb",
            )
        msg = str(ctx.exception)
        self.assertIn("CDR4176_RESULTS", msg)
        self.assertIn("Raw dumps are no longer tracked in repository", msg)

    def test_get_data_dir(self) -> None:
        d1 = get_data_dir("simulations/simulation/results_tb_linearity_integration.ipynb")
        self.assertTrue(str(d1).endswith("CDR4176-main/verification/results/legacy/simulation"))

    def test_read_raw_fixture(self) -> None:
        notebook_id = "simulations/simulation/results_tb_linearity_integration.ipynb"
        dataset = get_data_dir(notebook_id, repo_root=self.temp_dir) / "wave.raw"
        dataset.parent.mkdir(parents=True, exist_ok=True)
        dataset.write_text(
            "Title: fixture\nVariables:\n0 time time\n1 v(vout) voltage\n"
            "Values:\n0 0.0\n1.2\n1 1e-9\n0.0\n", encoding="utf-8",
        )
        data = read_raw("wave.raw", ["time", "v(vout)"], notebook_id, repo_root=self.temp_dir)
        self.assertEqual(data, {"time": [0.0, 1e-9], "v(vout)": [1.2, 0.0]})


if __name__ == "__main__":
    unittest.main()
