#!/usr/bin/env python3
"""Tests for commitz_ui.

Phase 1 scope: help/raw-help contract only.

Usage:
    commitz_ui_test.py [-v]

Exit codes:
  0  all tests passed
  1  one or more tests failed
"""

from __future__ import annotations

import argparse
import os
import re
import tempfile
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "commitz_ui"
PYTHON = "/usr/bin/python3"


def strip_ansi(text: str) -> str:
    return re.sub(r"\x1b\[[0-9;]*[A-Za-z]", "", text)


def run(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run([PYTHON, str(SCRIPT), *args], capture_output=True, text=True)


def run_in_repo(repo: Path, args: list[str] | None = None) -> subprocess.CompletedProcess:
    if args is None:
        args = []
    return subprocess.run([PYTHON, str(SCRIPT), *args], capture_output=True, text=True, cwd=str(repo))


def git(repo: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=str(repo), capture_output=True, text=True)


def init_repo() -> Path:
    repo = Path(tempfile.mkdtemp(prefix="commitz_ui_repo_"))
    git(repo, "init")
    git(repo, "config", "user.email", "test@example.com")
    git(repo, "config", "user.name", "Test User")
    return repo


def write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def test_script_exists() -> tuple[bool, str]:
    ok = SCRIPT.exists()
    return ok, f"exists={ok} path={SCRIPT}"


def test_raw_help_exits_0() -> tuple[bool, str]:
    r = run(["-H"])
    ok = r.returncode == 0 and len(r.stdout) > 0
    return ok, f"rc={r.returncode} out_len={len(r.stdout)} err={r.stderr!r}"


def test_help_exits_0() -> tuple[bool, str]:
    r = run(["-h"])
    ok = r.returncode == 0 and len(r.stdout) > 0
    return ok, f"rc={r.returncode} out_len={len(r.stdout)} err={r.stderr!r}"


def test_raw_matches_color_stripped_help() -> tuple[bool, str]:
    raw = run(["-H"])
    help_out = run(["-h"])
    if raw.returncode != 0 or help_out.returncode != 0:
        return False, f"raw_rc={raw.returncode} help_rc={help_out.returncode}"
    ok = raw.stdout == strip_ansi(help_out.stdout)
    return ok, f"raw_len={len(raw.stdout)} help_len={len(help_out.stdout)}"


def test_dirty_repo_renders_pending_menu() -> tuple[bool, str]:
    repo = init_repo()
    try:
        a = repo / "alpha.txt"
        write(a, "base\n")
        git(repo, "add", "alpha.txt")
        git(repo, "commit", "-m", "init")

        # unstaged delete marker candidate
        b = repo / "beta.txt"
        write(b, "to be deleted\n")
        git(repo, "add", "beta.txt")
        git(repo, "commit", "-m", "add beta")

        # modified tracked file (unstaged)
        write(a, "base\nchanged\n")
        os.remove(b)

        # untracked file
        write(repo / "new_notes.md", "hello\n")

        r = run_in_repo(repo)
        out = r.stdout
        ok = (
            r.returncode == 0
            and "2 files to commit." in out
            and "Select buckets with e.g." in out
            and re.search(r"^\d+\. alpha\.txt \+\d+/-\d+", out, re.M)
            and re.search(r"^\d+\. \[del\] beta\.txt", out, re.M)
            and re.search(r"^1 untracked file \(not staged\)\.", out, re.M)
            and re.search(r"^C: commit\.", out, re.M)
            and "P: commit+push" in out
        )
        return ok, f"rc={r.returncode}\n{out}"
    finally:
        subprocess.run(["rm", "-rf", str(repo)], check=False)


def test_unpushed_only_mode() -> tuple[bool, str]:
    repo = init_repo()
    remote = Path(tempfile.mkdtemp(prefix="commitz_ui_remote_"))
    try:
        git(remote, "init", "--bare")

        f = repo / "tracked.txt"
        write(f, "v1\n")
        git(repo, "add", "tracked.txt")
        git(repo, "commit", "-m", "init")
        git(repo, "remote", "add", "origin", str(remote))
        git(repo, "push", "-u", "origin", "HEAD")

        # local commit not pushed
        write(f, "v2\n")
        git(repo, "add", "tracked.txt")
        git(repo, "commit", "-m", "local only")

        r = run_in_repo(repo)
        out = r.stdout
        ok = (
            r.returncode == 0
            and re.search(r"^1 commit already in next push\.$", out, re.M)
            and "file to commit" not in out.lower()
            and re.search(r"^P: push(\+mirror)?\.", out, re.M)
            and "C: commit." not in out
        )
        return ok, f"rc={r.returncode}\n{out}"
    finally:
        subprocess.run(["rm", "-rf", str(repo)], check=False)
        subprocess.run(["rm", "-rf", str(remote)], check=False)


def test_cta_is_flush_left() -> tuple[bool, str]:
    repo = init_repo()
    try:
        f = repo / "a.txt"
        write(f, "v1\n")
        git(repo, "add", "a.txt")
        git(repo, "commit", "-m", "init")

        write(f, "v2\n")
        r = run_in_repo(repo)
        lines = r.stdout.splitlines()
        cta_lines = [ln for ln in lines if ln.startswith("C:") or ln.startswith("P:")]
        indented_bad = [ln for ln in lines if re.match(r"^\s+(C:|P:)", ln)]
        ok = r.returncode == 0 and len(cta_lines) >= 1 and len(indented_bad) == 0
        return ok, f"cta={cta_lines} indented={indented_bad}"
    finally:
        subprocess.run(["rm", "-rf", str(repo)], check=False)


def test_single_pending_commit_omits_select_hint() -> tuple[bool, str]:
    repo = init_repo()
    try:
        f = repo / "single.txt"
        write(f, "v1\n")
        git(repo, "add", "single.txt")
        git(repo, "commit", "-m", "init")

        write(f, "v2\n")
        r = run_in_repo(repo)
        out = r.stdout
        ok = (
            r.returncode == 0
            and "1 file to commit." in out
            and "Select buckets with e.g." not in out
        )
        return ok, f"rc={r.returncode}\n{out}"
    finally:
        subprocess.run(["rm", "-rf", str(repo)], check=False)


def run_all(verbose: bool = False) -> int:
    tests = [
        ("script exists", test_script_exists),
        ("-H exits 0", test_raw_help_exits_0),
        ("-h exits 0", test_help_exits_0),
        ("-H matches color-stripped -h", test_raw_matches_color_stripped_help),
        ("dirty repo renders pending menu", test_dirty_repo_renders_pending_menu),
        ("unpushed-only mode", test_unpushed_only_mode),
        ("single pending omits select hint", test_single_pending_commit_omits_select_hint),
        ("CTA lines are flush-left", test_cta_is_flush_left),
    ]

    passed = 0
    failed = 0

    for name, fn in tests:
        ok, detail = fn()
        if ok:
            print(f"PASS: {name}")
            passed += 1
        else:
            print(f"FAIL: {name}")
            failed += 1
        if verbose or not ok:
            print(f"  {detail}")

    print(f"\nSummary: {passed} passed, {failed} failed")
    return 0 if failed == 0 else 1


def main() -> int:
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("-v", action="store_true", help="show details for passing tests too")
    ns = ap.parse_args()
    return run_all(verbose=ns.v)


if __name__ == "__main__":
    raise SystemExit(main())
