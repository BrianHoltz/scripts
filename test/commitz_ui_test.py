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
import re
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "commitz_ui"
PYTHON = "/usr/bin/python3"


def strip_ansi(text: str) -> str:
    return re.sub(r"\x1b\[[0-9;]*[A-Za-z]", "", text)


def run(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run([PYTHON, str(SCRIPT), *args], capture_output=True, text=True)


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


def run_all(verbose: bool = False) -> int:
    tests = [
        ("script exists", test_script_exists),
        ("-H exits 0", test_raw_help_exits_0),
        ("-h exits 0", test_help_exits_0),
        ("-H matches color-stripped -h", test_raw_matches_color_stripped_help),
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
