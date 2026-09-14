import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "fix_xschem_paths.py"
CHECKER = ROOT / "scripts" / "check_xschem_paths.py"
HOOK = ROOT / ".githooks" / "pre-commit"


class FixPathsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.git("init", "-q")
        self.git("config", "user.email", "test@example.invalid")
        self.git("config", "user.name", "Test")

    def git(self, *args, data=None):
        return subprocess.run(["git", *args], cwd=self.root, input=data,
                              check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout

    def put(self, path, data, stage=True):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        if stage:
            self.git("add", "--", path)

    def run_fixer(self, *args, env=None):
        return subprocess.run([sys.executable, str(SCRIPT), *args], cwd=self.root,
                              env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def absolute(self, name="part with space.sym"):
        return os.fsencode(self.root / name)

    def prepare(self):
        self.put("part with space.sym", b"v {}\n")
        original = b"C {" + self.absolute() + b"} 0 0 0 0 {name=x\r\nvalue={a b}}\r\n"
        self.put("main.sch", original)
        return original

    def test_initial_fix_crlf_and_index(self):
        original = self.prepare()
        result = self.run_fixer()
        self.assertEqual(result.returncode, 0, result.stderr)
        expected = original.replace(self.absolute(), b"part with space.sym")
        self.assertEqual((self.root / "main.sch").read_bytes(), expected)
        self.assertEqual(self.git("show", ":main.sch"), expected)
        self.assertIn(b"main.sch", result.stdout)

    def test_portable_multiline_noop(self):
        data = b'C\r\n{devices/res.sym} 0 0 0 0 {\r\nC {/not/a/symbol.sym}\r\nvalue={nested}}\r\n'
        self.put("main.sch", data)
        self.assertEqual(self.run_fixer().returncode, 0)
        self.assertEqual(self.git("show", ":main.sch"), data)
        self.assertEqual((self.root / "main.sch").read_bytes(), data)

    def test_check_readonly(self):
        original = self.prepare()
        self.assertEqual(self.run_fixer("--check").returncode, 1)
        self.assertEqual(self.git("show", ":main.sch"), original)
        self.assertEqual((self.root / "main.sch").read_bytes(), original)

    def test_partial_staging_preflight(self):
        original = self.prepare()
        self.put("z.sch", original)
        self.put("z.sch", original + b"\n", stage=False)
        result = self.run_fixer()
        self.assertEqual(result.returncode, 1)
        self.assertIn(b"unstaged", result.stderr)
        self.assertEqual((self.root / "main.sch").read_bytes(), original)
        self.assertEqual(self.git("show", ":z.sch"), original)
        self.assertEqual((self.root / "z.sch").read_bytes(), original + b"\n")

    def test_unknown_does_not_guess(self):
        original = b"C {/old/part.sym} 0 0 0 0 {}\n"
        self.put("main.sch", original)
        result = self.run_fixer("--check")
        self.assertEqual(result.returncode, 1)
        self.assertIn(b"unresolved", result.stderr)
        self.assertEqual(self.git("show", ":main.sch"), original)

    def test_unknown_windows_drive_does_not_guess(self):
        original = b"C {C:\\old\\part.sym} 0 0 0 0 {}\n"
        self.put("main.sch", original)
        result = self.run_fixer()
        self.assertEqual(result.returncode, 1)
        self.assertIn(b"unresolved", result.stderr)

    def test_unknown_unc_does_not_guess(self):
        original = b"C {\\\\server\\share\\part.sym} 0 0 0 0 {}\n"
        self.put("main.sch", original)
        result = self.run_fixer()
        self.assertEqual(result.returncode, 1)
        self.assertIn(b"unresolved", result.stderr)

    def test_unique_tracked_target_is_hint_only(self):
        self.put("symbols/part.sym", b"v {}\n")
        original = b"C {/old/part.sym} 0 0 0 0 {}\n"
        self.put("main.sch", original)
        result = self.run_fixer("--check")
        self.assertEqual(result.returncode, 1)
        self.assertIn(b"unresolved", result.stderr)
        self.assertIn(b"symbols/part.sym", result.stderr)

    def test_duplicate_symbols_are_ambiguous(self):
        self.put("a/part.sym", b"v {}\n")
        self.put("b/part.sym", b"v {}\n")
        self.put("main.sch", b"C {/old/part.sym} 0 0 0 0 {}\n")
        self.assertIn(b"ambiguous", self.run_fixer().stderr)

    def test_file_uri_exact_repository_path_is_fixed(self):
        self.put("symbols/part.sym", b"v {}\n")
        encoded = os.fsencode((self.root / "symbols/part.sym").as_posix())
        original = b"C {file://" + encoded + b"} 0 0 0 0 {}\n"
        self.put("circuits/main.sch", original)
        result = self.run_fixer()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.git("show", ":circuits/main.sch"),
                         original.replace(b"file://" + encoded, b"../symbols/part.sym"))

    def test_untracked_destination(self):
        self.put("part with space.sym", b"v {}\n", stage=False)
        self.put("main.sch", b"C {" + self.absolute() + b"} 0 0 0 0 {}\n")
        self.assertIn(b"unresolved", self.run_fixer().stderr)

    def test_symlink_sources_and_destinations(self):
        original = self.prepare()
        (self.root / "main.sch").unlink()
        (self.root / "main.sch").symlink_to("part with space.sym")
        self.assertEqual(self.run_fixer().returncode, 1)
        self.assertEqual(self.git("show", ":main.sch"), original)
        self.git("add", "main.sch")
        self.assertIn(b"not a regular", self.run_fixer().stderr)
        (self.root / "main.sch").unlink()
        self.put("main.sch", original)
        (self.root / "part with space.sym").unlink()
        self.put("target", b"v {}\n")
        (self.root / "part with space.sym").symlink_to("target")
        self.git("add", "part with space.sym")
        self.assertIn(b"unresolved", self.run_fixer().stderr)

    def test_missing_and_mode_changes(self):
        original = self.prepare()
        (self.root / "main.sch").chmod(0o755)
        self.assertIn(b"mode changes", self.run_fixer().stderr)
        (self.root / "main.sch").unlink()
        self.assertEqual(self.run_fixer().returncode, 1)
        self.assertEqual(self.git("show", ":main.sch"), original)

    def test_rename_and_delete(self):
        self.prepare()
        self.git("commit", "-qm", "initial")
        self.git("mv", "main.sch", "renamed.sch")
        self.assertEqual(self.run_fixer().returncode, 0)
        self.assertIn(b"C {part with space.sym}", self.git("show", ":renamed.sch"))
        self.git("rm", "-f", "renamed.sch")
        self.assertEqual(self.run_fixer().returncode, 0)

    def test_unmerged_preflight(self):
        original = self.prepare()
        oid = self.git("hash-object", "-w", "--stdin", data=b"v {}\n").strip()
        self.git("update-index", "--index-info", data=b"100644 " + oid + b" 2\tconflict.sch\n")
        self.assertIn(b"unmerged", self.run_fixer().stderr)
        self.assertEqual((self.root / "main.sch").read_bytes(), original)

    def test_gitlink_destination_not_traversed(self):
        self.put("seed", b"seed")
        self.git("commit", "-qm", "initial")
        oid = self.git("rev-parse", "HEAD").strip()
        self.git("update-index", "--add", "--cacheinfo", "160000," + oid.decode() + ",sub")
        self.put("sub/part.sym", b"v {}\n", stage=False)
        self.put("main.sch", b"C {" + self.absolute("sub/part.sym") + b"} 0 0 0 0 {}\n")
        self.assertIn(b"unresolved", self.run_fixer().stderr)

    def test_explicit_library_and_ambiguity(self):
        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            (Path(first) / "part.sym").write_bytes(b"v {}\n")
            reference = os.fsencode(Path(first) / "part.sym")
            original = b"C {" + reference + b"} 0 0 0 0 {}\n"
            self.put("main.sch", original)
            (Path(second) / "part.sym").write_bytes(b"v {}\n")
            result = self.run_fixer("--library-root", first, "--library-root", second)
            self.assertIn(b"ambiguous", result.stderr)
            self.assertEqual(self.git("show", ":main.sch"), original)
            self.assertEqual(self.run_fixer("--library-root", first).returncode, 0)
            self.assertEqual(self.git("show", ":main.sch"), original.replace(reference, b"part.sym"))

    def test_legacy_io_requires_proven_library(self):
        self.put("io/sg13g2_io/xschem/pad.sym", b"v {}\n")
        original = b"C {IHP-Open-PDK/old/libs.ref/sg13g2_io/xschem/pad.sym} 0 0 0 0 {}\n"
        self.put("main.sch", original)
        self.assertEqual(self.run_fixer().returncode, 1)
        result = self.run_fixer("--library-root", str(self.root / "io/sg13g2_io/xschem"))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.git("show", ":main.sch"), b"C {pad.sym} 0 0 0 0 {}\n")

    def test_legacy_multiline_path_is_preserved_and_flagged(self):
        self.put("symbols/FF_D.sym", b"v {}\n")
        for reference in (b"/home/eamtastudent/GROTDC marzo/Esquematicos/FF_D.sym",
                          b"C:\\old machine\\FF_D.sym", b"\\\\server\\share\\FF_D.sym"):
            with self.subTest(reference=reference):
                original = b"C {\r\n  " + reference + b" \t\r\n} 0 0 0 0 {name=x}\r\n"
                self.put("circuits/main.sch", original)
                result = self.run_fixer("--check")
                self.assertEqual(result.returncode, 1)
                self.assertIn(b"unresolved", result.stderr)
                self.assertEqual(self.git("show", ":circuits/main.sch"), original)

    def test_resolver_excludes_untracked_symlink_and_submodule(self):
        self.put("symbols/part.sym", b"v {}\n", stage=False)
        self.put("main.sch", b"C {/old/part.sym} 0 0 0 0 {}\n")
        self.assertIn(b"unresolved", self.run_fixer().stderr)
        (self.root / "symbols/part.sym").unlink()
        (self.root / "symbols/part.sym").symlink_to("../target")
        self.put("target", b"v {}\n")
        self.git("add", "symbols/part.sym")
        self.assertEqual(self.run_fixer().returncode, 1)
        self.git("rm", "-f", "symbols/part.sym")
        self.git("commit", "-qm", "initial")
        oid = self.git("rev-parse", "HEAD").strip().decode()
        self.git("update-index", "--add", "--cacheinfo", "160000," + oid + ",sub")
        self.put("sub/part.sym", b"v {}\n", stage=False)
        self.assertIn(b"unresolved", self.run_fixer("--all", "--check").stderr)

    def test_library_local_coexistence_prefers_local_and_checks_root(self):
        self.put("part.sym", b"v {}\n")
        original = b"C {/old/part.sym} 0 0 0 0 {}\n"
        self.put("main.sch", original)
        with tempfile.TemporaryDirectory() as library:
            (Path(library) / "part.sym").write_bytes(b"v {}\n")
            result = self.run_fixer("--library-root", library)
            self.assertIn(b"unresolved", result.stderr)
            self.assertEqual(self.git("show", ":main.sch"), original)

    def test_tilde_not_guessed(self):
        self.put("part.sym", b"v {}\n")
        self.put("main.sch", b"C {~/part.sym} 0 0 0 0 {}\n")
        self.assertIn(b"tilde", self.run_fixer().stderr)

    def test_check_all_index_only(self):
        original = self.prepare()
        self.git("commit", "-qm", "initial")
        index = (self.root / ".git/index").read_bytes()
        self.assertEqual(self.run_fixer("--check").returncode, 0)
        self.assertEqual(self.run_fixer("--all").returncode, 2)
        self.put("main.sch", b"dirty", stage=False)
        for state in ("dirty", "missing", "symlink"):
            with self.subTest(state=state):
                if state == "missing":
                    (self.root / "main.sch").unlink()
                    (self.root / "part with space.sym").unlink()
                elif state == "symlink":
                    (self.root / "main.sch").symlink_to("missing")
                result = self.run_fixer("--all", "--check")
                self.assertEqual(result.returncode, 1, result.stderr)
                self.assertIn(b"Needs fix", result.stdout)
                self.assertEqual(result.stderr, b"")
                self.assertEqual(self.git("show", ":main.sch"), original)
                self.assertEqual((self.root / ".git/index").read_bytes(), index)
        self.assertTrue((self.root / "main.sch").is_symlink())

    def test_installed_hook_fixes_staged_content_only(self):
        (self.root / "scripts").mkdir()
        (self.root / ".githooks").mkdir()
        (self.root / "scripts/fix_xschem_paths.py").symlink_to(SCRIPT)
        (self.root / "scripts/check_xschem_paths.py").symlink_to(CHECKER)
        (self.root / ".githooks/pre-commit").symlink_to(HOOK)
        self.git("config", "core.hooksPath", ".githooks")
        self.put("part.sym", b"v {}\n")
        original = b"C {" + self.absolute("part.sym") + b"} 0 0 0 0 {}\r\n"
        self.put("main.sch", original)
        self.put("other.bin", b"other bytes\x00\r\n")
        self.git("commit", "-qm", "hook test")
        self.assertEqual(self.git("show", "HEAD:main.sch"),
                         original.replace(self.absolute("part.sym"), b"part.sym"))
        self.assertEqual(self.git("show", "HEAD:other.bin"), b"other bytes\x00\r\n")

    def test_alternate_index_and_pathspec_characters(self):
        original = self.prepare()
        self.git("mv", "main.sch", ":special.sch")
        alternate = self.root / "alternate-index"
        alternate.write_bytes((self.root / ".git/index").read_bytes())
        env = dict(os.environ, GIT_INDEX_FILE=str(alternate))
        result = self.run_fixer(env=env)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.git("show", "::special.sch"), original)
        staged = subprocess.check_output(["git", "show", "::special.sch"], cwd=self.root, env=env)
        self.assertEqual(staged, original.replace(self.absolute(), b"part with space.sym"))


if __name__ == "__main__":
    unittest.main()
