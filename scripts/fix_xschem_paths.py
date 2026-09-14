#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
from pathlib import Path
import posixpath
import re
import stat
import subprocess
import sys
from urllib.parse import unquote, urlsplit

SOURCE_EXTENSIONS = {".sch", ".sym"}


def git(repo_root: Path, *args: str, data: bytes | None = None) -> bytes:
    return subprocess.run(
        ["git", *args], cwd=repo_root, input=data, check=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    ).stdout


def component_spans(content: bytes):
    depth = 0
    pos = 0
    line_start = True
    while pos < len(content):
        if depth == 0 and line_start:
            match = re.match(rb"[ \t]*C\s+\{", content[pos:])
            if match:
                start = pos + match.end()
                end = start
                nested = 1
                while end < len(content):
                    char = content[end]
                    if char == 92 and end + 1 < len(content) and content[end + 1] in (123, 125):
                        end += 2
                        continue
                    if char == 123:
                        nested += 1
                    elif char == 125:
                        nested -= 1
                        if not nested:
                            break
                    end += 1
                if nested:
                    raise ValueError("unterminated component symbol path")
                yield start, end
                pos = end + 1
                line_start = False
                continue
        char = content[pos]
        if char == 92 and pos + 1 < len(content):
            pos += 2
            line_start = False
            continue
        if char == 123:
            depth += 1
        elif char == 125:
            depth -= 1
            if depth < 0:
                raise ValueError("unbalanced braces")
        line_start = char == 10
        pos += 1
    if depth:
        raise ValueError("unbalanced braces")


def regular_path(root: Path, relative: str) -> bool:
    current = root
    parts = Path(relative).parts
    if not parts or Path(relative).is_absolute() or ".." in parts:
        return False
    for index, part in enumerate(parts):
        current = current / part
        try:
            mode = current.lstat().st_mode
        except OSError:
            return False
        if index == len(parts) - 1:
            return stat.S_ISREG(mode)
        if not stat.S_ISDIR(mode):
            return False
    return False


def file_uri_path(reference: str) -> str:
    if not reference.lower().startswith("file:///"):
        raise ValueError(f"unsupported file URI symbol reference {reference!r}")
    parsed = urlsplit(reference)
    if parsed.scheme.lower() != "file" or parsed.netloc or parsed.query or parsed.fragment:
        raise ValueError(f"unsupported file URI symbol reference {reference!r}")
    path = unquote(parsed.path)
    if not path or path.startswith("//"):
        raise ValueError(f"unsupported file URI symbol reference {reference!r}")
    return path


def resolve_symbol(reference: str, source: str, root: Path,
                   entries: dict, libraries: list[Path]) -> str:
    file_uri = reference.lower().startswith("file:")
    without_scheme = file_uri_path(reference) if file_uri else reference
    normalized = without_scheme.replace("\\", "/")
    obsolete = re.search(r"IHP-Open-PDK/.*/libs\.ref/sg13g2_io/xschem/(.+)$", normalized)
    if not (normalized.startswith(("/", "~")) or re.match(r"^[A-Za-z]:", normalized) is not None
            or file_uri or obsolete):
        return reference
    if normalized.startswith("~"):
        raise ValueError(f"unresolved literal tilde symbol reference {reference!r}")
    if file_uri and not obsolete and not (normalized.startswith("/") or re.match(r"^[A-Za-z]:", normalized)):
        stripped = without_scheme.replace("\\", "/")
        if not (stripped.startswith(("/", "~")) or re.match(r"^[A-Za-z]:", stripped)):
            return stripped
    symbols = {p for p, (mode, oid, stage) in entries.items()
               if mode in ("100644", "100755") and stage == "0" and p.endswith(".sym")}
    candidates = set()

    def local_candidate(relative):
        portable = posixpath.relpath(relative, posixpath.dirname(source) or ".")
        norm = posixpath.normpath(portable)
        contained = not (norm == ".." or norm.startswith("../")
                         or posixpath.isabs(norm) or re.match(r"^[A-Za-z]:", norm) is not None)
        if contained:
            for library in libraries:
                target = Path(os.path.abspath(library / norm))
                try:
                    local_target = target.relative_to(root).as_posix()
                except ValueError:
                    local_target = None
                if local_target is not None:
                    exists = local_target in entries
                else:
                    exists = regular_path(library, norm)
                if target != root / relative and exists:
                    raise ValueError(f"ambiguous symbol reference {reference!r}")
        return portable

    prefix = root.as_posix() + "/"
    if normalized.startswith(prefix):
        relative = normalized[len(prefix):]
        if relative in symbols:
            candidates.add(local_candidate(relative))
    for library in libraries:
        library_prefix = library.as_posix() + "/"
        relative = None
        if normalized.startswith(library_prefix):
            relative = normalized[len(library_prefix):]
        elif obsolete and library.name == "xschem" and library.parent.name == "sg13g2_io":
            relative = obsolete[1]
        if not relative:
            continue
        try:
            repo_relative = (library / relative).relative_to(root).as_posix()
        except ValueError:
            repo_relative = None
        if repo_relative is not None and repo_relative not in symbols:
            continue
        if repo_relative is None and not regular_path(library, relative):
            continue
        local = posixpath.normpath(posixpath.join(posixpath.dirname(source), relative))
        if local in symbols:
            raise ValueError(f"ambiguous symbol reference {reference!r}")
        destinations = set()
        for search_root in libraries:
            target = search_root / relative
            try:
                tracked = target.relative_to(root).as_posix()
            except ValueError:
                tracked = None
            if tracked is not None:
                if tracked in entries:
                    destinations.add(str(target))
            elif regular_path(search_root, relative):
                destinations.add(str(target))
        if len(destinations) != 1:
            raise ValueError(f"ambiguous symbol reference {reference!r}")
        candidates.add(relative)
    if len(candidates) == 1:
        result = candidates.pop()
        if any(char in result for char in "{}\\\r\n"):
            raise ValueError(f"unsupported symbol filename {reference!r}")
        return result
    same_name = sorted(p for p in symbols if posixpath.basename(p) == posixpath.basename(normalized))
    if len(candidates) > 1 or len(same_name) > 1:
        reason = "ambiguous"
    else:
        reason = "unresolved"
    message = f"{reason} symbol reference {reference!r}; supply an exact tracked path or --library-root"
    if reason == "unresolved" and len(same_name) == 1:
        message += f"; did you mean {same_name[0]!r}?"
    raise ValueError(message)


def fix_content(content: bytes, source: str, root: Path, entries: dict,
                libraries: list[Path]) -> bytes:
    replacements = []
    for start, end in component_spans(content):
        span = content[start:end]
        trimmed = span.strip()
        reference = os.fsdecode(trimmed)
        fixed = resolve_symbol(reference, source, root, entries, libraries)
        if fixed != reference:
            leading = len(span) - len(span.lstrip())
            replacements.append((start + leading, start + leading + len(trimmed), os.fsencode(fixed)))
    for start, end, replacement in reversed(replacements):
        content = content[:start] + replacement + content[end:]
    return content


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Safely normalize staged Xschem component paths")
    parser.add_argument("--staged", action="store_true", help="inspect the index (default)")
    parser.add_argument("--check", action="store_true", help="read-only; fail if fixes are needed")
    parser.add_argument("--all", action="store_true", help="scan all index sources; requires --check")
    parser.add_argument("--library-root", action="append", default=[], metavar="PATH",
                        help="explicit installed Xschem search root (repeatable)")
    args = parser.parse_args(argv)
    if args.all and not args.check:
        parser.error("--all requires --check")
    try:
        root = Path(os.fsdecode(git(Path.cwd(), "rev-parse", "--show-toplevel").rstrip(b"\n")))
        libraries = []
        for value in args.library_root:
            library = Path(os.path.abspath(value))
            if library.resolve() != library or not library.is_dir():
                raise ValueError(f"library root must be an existing non-symlink directory: {value!r}")
            libraries.append(library)
        entries = {}
        for record in git(root, "ls-files", "--stage", "-z").split(b"\0"):
            if not record:
                continue
            metadata, raw_path = record.split(b"\t", 1)
            mode, oid, stage = metadata.decode("ascii").split()
            path = os.fsdecode(raw_path)
            if stage != "0" and Path(path).suffix.lower() in SOURCE_EXTENSIONS:
                raise ValueError(f"{path!r}: unmerged Xschem source")
            entries[path] = (mode, oid, stage)
        paths = (b"\0".join(os.fsencode(path) for path in entries) if args.all else
                 git(root, "diff", "--cached", "--name-only", "--no-renames", "--diff-filter=ACMT", "-z"))
        plans = []
        for raw_path in paths.split(b"\0"):
            if not raw_path:
                continue
            path = os.fsdecode(raw_path)
            if Path(path).suffix.lower() not in SOURCE_EXTENSIONS:
                continue
            mode, oid, stage = entries[path]
            if mode not in ("100644", "100755") or stage != "0":
                raise ValueError(f"{path!r}: source is not a regular staged file")
            content = git(root, "cat-file", "blob", oid)
            try:
                fixed = fix_content(content, path, root, entries, libraries)
            except ValueError as error:
                raise ValueError(f"{path!r}: {error}") from error
            if fixed == content:
                continue
            if args.check:
                plans.append((path, mode, fixed))
                continue
            full_path = root / path
            if not regular_path(root, path):
                raise ValueError(f"{path!r}: missing or non-regular worktree source")
            work_mode = "100755" if full_path.stat().st_mode & 0o111 else "100644"
            if full_path.read_bytes() != content or work_mode != mode:
                raise ValueError(f"{path!r}: unstaged content or mode changes; refusing to overwrite")
            plans.append((path, mode, fixed))
        if args.check:
            for path, mode, fixed in plans:
                print(f"Needs fix: {path!r}")
            return int(bool(plans))
        updates = bytearray()
        for path, mode, fixed in plans:
            oid = git(root, "hash-object", "-w", "--stdin", data=fixed).strip()
            updates.extend(mode.encode() + b" " + oid + b"\t" + os.fsencode(path) + b"\0")
        for path, mode, fixed in plans:
            (root / path).write_bytes(fixed)
        if updates:
            git(root, "update-index", "-z", "--index-info", data=bytes(updates))
        for path, mode, fixed in plans:
            print(f"Fixed: {path!r}")
        return 0
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        print(f"Xschem path fixer: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
