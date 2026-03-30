#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Brian Holtz
# SPDX-License-Identifier: MIT

"""Tests for write_if_unchanged.

Usage:
    write_if_unchanged_test.py [-v] [-l] [-t N] [--keep-artifacts]

Options:
  -h, --help          Show this message and exit
  -v                  Always show test details, even if all tests pass
  -l, --list-tests    List available tests and exit
  -t N, --test N      Run only test number N
  --keep-artifacts    Do not clean up temp dirs after running

Exit codes:
  0  all tests passed
  1  one or more tests failed
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

SCRIPT = Path(__file__).parent / "write_if_unchanged"
PYTHON = sys.executable


# ---------------------------------------------------------------------------
# Output helpers
# ---------------------------------------------------------------------------

def _tty() -> bool:
    return sys.stdout.isatty()


def color_pass(desc: str) -> None:
    if _tty():
        print(f"\033[1;92mPASS: {desc}\033[0m")
    else:
        print(f"PASS: {desc}")


def color_fail(desc: str) -> None:
    if _tty():
        print(f"\033[1;91mFAIL: {desc}\033[0m")
    else:
        print(f"FAIL: {desc}")


def header(text: str) -> None:
    if _tty():
        print(f"\033[1m{text}\033[0m")
    else:
        print(text)


# ---------------------------------------------------------------------------
# Test runner state
# ---------------------------------------------------------------------------

passed = 0
failed = 0
current_test_num = 0
test_descriptions: list[str] = []

specific_test: int | None = None
verbose: bool = False
keep_artifacts: bool = False


# ---------------------------------------------------------------------------
# Low-level helpers
# ---------------------------------------------------------------------------

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def strip_ansi(data: bytes) -> bytes:
    return re.sub(rb"\x1b\[[0-9;]*[A-Za-z]", b"", data)


def run(
    target: str,
    *,
    from_file: str | None = None,
    stdin_data: bytes | None = None,
    expect_sha256: str | None = None,
    note: str | None = None,
    lock_root: str,
    ttl: int = 120,
    wait: int = 5,
    owner: str = "test",
) -> subprocess.CompletedProcess:
    cmd = [PYTHON, str(SCRIPT), target]
    if stdin_data is not None:
        cmd += ["--stdin"]
    else:
        cmd += ["--from", from_file]
    if expect_sha256 is not None:
        cmd += ["--expect-sha256", expect_sha256]
    if note is not None:
        cmd += ["--note", note]
    cmd += ["--lock-root", lock_root, "--ttl", str(ttl), "--wait", str(wait), "--owner", owner]
    return subprocess.run(
        cmd,
        input=stdin_data,
        capture_output=True,
    )


def plant_stale_lock(lock_root: Path, target: Path, age_s: float = 300, note: str = "") -> Path:
    """Create a lock dir with an expired heartbeat, simulating a crashed writer."""
    key = hashlib.sha256(str(target.resolve()).encode()).hexdigest()[:24]
    lock_path = lock_root / f"{key}.lock"
    lock_path.mkdir(parents=True, exist_ok=True)
    meta = {
        "owner": "crashed-agent",
        "pid": 99999,
        "hostname": "ghost",
        "started_at": time.time() - age_s,
        "heartbeat_at": time.time() - age_s,
        "target": str(target.resolve()),
        "note": note,
    }
    (lock_path / "lock.json").write_text(json.dumps(meta), encoding="utf-8")
    return lock_path


def plant_live_lock(lock_root: Path, target: Path, owner: str = "blocker") -> Path:
    """Create a lock dir with a fresh heartbeat, simulating an active writer."""
    key = hashlib.sha256(str(target.resolve()).encode()).hexdigest()[:24]
    lock_path = lock_root / f"{key}.lock"
    lock_path.mkdir(parents=True, exist_ok=True)
    meta = {
        "owner": owner,
        "pid": 99999,
        "hostname": "other",
        "started_at": time.time(),
        "heartbeat_at": time.time(),
        "target": str(target.resolve()),
        "note": "",
    }
    (lock_path / "lock.json").write_text(json.dumps(meta), encoding="utf-8")
    return lock_path


# ---------------------------------------------------------------------------
# Test case harness
# ---------------------------------------------------------------------------

def test_case(desc: str, fn) -> None:
    global passed, failed, current_test_num
    current_test_num += 1
    test_descriptions.append(f"Test {current_test_num}: {desc}")

    if specific_test is not None and specific_test != current_test_num:
        return

    tmpdir = Path(tempfile.mkdtemp(prefix="wiu_test_"))
    lock_root = str(tmpdir / "locks")
    details: list[str] = []
    result = True

    try:
        result = fn(tmpdir, lock_root, details)
    except Exception as exc:
        details.append(f"Exception: {exc}")
        result = False
    finally:
        if not keep_artifacts:
            shutil.rmtree(tmpdir, ignore_errors=True)
        else:
            details.append(f"Artifacts: {tmpdir}")

    if verbose or not result:
        header(f"### Test {current_test_num}: {desc}")
        for line in details:
            print(f"  {line}")

    if result:
        color_pass(desc)
        passed += 1
    else:
        color_fail(desc)
        failed += 1


# ---------------------------------------------------------------------------
# Individual tests
# ---------------------------------------------------------------------------

def _test_write_new_file(tmpdir: Path, lock_root: str, details: list[str]) -> bool:
    target = tmpdir / "new.txt"
    src = tmpdir / "src.txt"
    src.write_bytes(b"hello world")

    r = run(str(target), from_file=str(src), lock_root=lock_root)
    details.append(f"exit={r.returncode} stdout={r.stdout!r} stderr={r.stderr!r}")
    if r.returncode != 0:
        return False
    if target.read_bytes() != b"hello world":
        details.append("content mismatch")
        return False
    return True


def _test_overwrite_existing_file(tmpdir: Path, lock_root: str, details: list[str]) -> bool:
    target = tmpdir / "file.txt"
    target.write_bytes(b"old content")
    src = tmpdir / "src.txt"
    src.write_bytes(b"new content")

    r = run(str(target), from_file=str(src), lock_root=lock_root)
    details.append(f"exit={r.returncode}")
    if r.returncode != 0:
        return False
    if target.read_bytes() != b"new content":
        details.append(f"expected 'new content', got {target.read_bytes()!r}")
        return False
    return True


def _test_stdin_mode(tmpdir: Path, lock_root: str, details: list[str]) -> bool:
    target = tmpdir / "out.txt"
    r = run(str(target), stdin_data=b"via stdin", lock_root=lock_root)
    details.append(f"exit={r.returncode}")
    if r.returncode != 0:
        return False
    if target.read_bytes() != b"via stdin":
        details.append("content mismatch")
        return False
    return True


def _test_cas_match_succeeds(tmpdir: Path, lock_root: str, details: list[str]) -> bool:
    target = tmpdir / "cas.txt"
    target.write_bytes(b"original")
    h = sha256(b"original")
    src = tmpdir / "src.txt"
    src.write_bytes(b"updated")

    r = run(str(target), from_file=str(src), expect_sha256=h, lock_root=lock_root)
    details.append(f"exit={r.returncode}")
    if r.returncode != 0:
        return False
    if target.read_bytes() != b"updated":
        details.append("content not updated")
        return False
    return True


def _test_cas_mismatch_aborts(tmpdir: Path, lock_root: str, details: list[str]) -> bool:
    target = tmpdir / "cas.txt"
    target.write_bytes(b"original")
    stale_hash = sha256(b"something else i read earlier")
    src = tmpdir / "src.txt"
    src.write_bytes(b"updated")

    r = run(str(target), from_file=str(src), expect_sha256=stale_hash, lock_root=lock_root)
    details.append(f"exit={r.returncode} stderr={r.stderr!r}")
    if r.returncode != 3:
        details.append(f"expected exit 3, got {r.returncode}")
        return False
    if target.read_bytes() != b"original":
        details.append("file was modified despite mismatch")
        return False
    if b"CAS mismatch" not in r.stderr:
        details.append("expected 'CAS mismatch' in stderr")
        return False
    return True


def _test_cas_nonexistent_file(tmpdir: Path, lock_root: str, details: list[str]) -> bool:
    """CAS hash of empty (nonexistent) file matches sha256(b''), so write should succeed."""
    target = tmpdir / "new.txt"
    h = sha256(b"")  # fingerprint() returns sha256("") for missing files
    src = tmpdir / "src.txt"
    src.write_bytes(b"brand new")

    r = run(str(target), from_file=str(src), expect_sha256=h, lock_root=lock_root)
    details.append(f"exit={r.returncode}")
    if r.returncode != 0:
        return False
    if target.read_bytes() != b"brand new":
        details.append("content mismatch")
        return False
    return True


def _test_lock_timeout(tmpdir: Path, lock_root: str, details: list[str]) -> bool:
    target = tmpdir / "locked.txt"
    target.write_bytes(b"content")
    lock_root_path = Path(lock_root)
    plant_live_lock(lock_root_path, target)

    src = tmpdir / "src.txt"
    src.write_bytes(b"new")
    # wait=1 so the test completes quickly
    r = run(str(target), from_file=str(src), lock_root=lock_root, wait=1)
    details.append(f"exit={r.returncode} stderr={r.stderr!r}")
    if r.returncode != 2:
        details.append(f"expected exit 2, got {r.returncode}")
        return False
    if b"Failed to acquire lock" not in r.stderr:
        details.append("expected 'Failed to acquire lock' in stderr")
        return False
    return True


def _test_stale_lock_broken(tmpdir: Path, lock_root: str, details: list[str]) -> bool:
    target = tmpdir / "stale.txt"
    target.write_bytes(b"old")
    lock_root_path = Path(lock_root)
    lock_root_path.mkdir(parents=True, exist_ok=True)
    plant_stale_lock(lock_root_path, target, age_s=300)

    src = tmpdir / "src.txt"
    src.write_bytes(b"new")
    r = run(str(target), from_file=str(src), lock_root=lock_root, ttl=120)
    details.append(f"exit={r.returncode} stderr={r.stderr!r}")
    if r.returncode != 0:
        details.append("expected stale lock to be broken and write to succeed")
        return False
    if target.read_bytes() != b"new":
        details.append("content not updated after stale lock break")
        return False
    if b"Stale lock detected" not in r.stderr:
        details.append("expected 'Stale lock detected' in stderr")
        return False
    return True


def _test_stale_lock_note_in_message(tmpdir: Path, lock_root: str, details: list[str]) -> bool:
    target = tmpdir / "noted.txt"
    target.write_bytes(b"old")
    lock_root_path = Path(lock_root)
    lock_root_path.mkdir(parents=True, exist_ok=True)
    plant_stale_lock(lock_root_path, target, age_s=300, note="agent=claude, task=abc123")

    src = tmpdir / "src.txt"
    src.write_bytes(b"new")
    r = run(str(target), from_file=str(src), lock_root=lock_root, ttl=120)
    details.append(f"stderr={r.stderr!r}")
    if b"abc123" not in r.stderr:
        details.append("expected note text in stale lock message")
        return False
    return True


def _test_note_stored_in_lock_json(tmpdir: Path, lock_root: str, details: list[str]) -> bool:
    """After a successful write, lock dir is removed — verify note was written by checking
    the success path indirectly: plant a stale lock with no note, write with --note, and
    confirm the write succeeds (lock dir gets created, used, and cleaned up correctly).
    Also verify via a failing CAS that lock.json is created with the note before the abort."""
    target = tmpdir / "noted.txt"
    target.write_bytes(b"original")

    src = tmpdir / "src.txt"
    src.write_bytes(b"new")

    # We can't easily inspect lock.json mid-flight without threading, so just confirm note
    # is surfaced when the lock is stale (tested in _test_stale_lock_note_in_message).
    # Here: just verify --note doesn't break a successful write.
    h = sha256(b"original")
    r = run(str(target), from_file=str(src), expect_sha256=h, note="task=test-note-123", lock_root=lock_root)
    details.append(f"exit={r.returncode}")
    if r.returncode != 0:
        return False
    if target.read_bytes() != b"new":
        details.append("content not updated")
        return False
    return True


def _test_inode_preserved(tmpdir: Path, lock_root: str, details: list[str]) -> bool:
    target = tmpdir / "inode.txt"
    target.write_bytes(b"original")
    inode_before = target.stat().st_ino

    src = tmpdir / "src.txt"
    src.write_bytes(b"replaced")
    r = run(str(target), from_file=str(src), lock_root=lock_root)
    details.append(f"exit={r.returncode}")
    if r.returncode != 0:
        return False

    inode_after = target.stat().st_ino
    details.append(f"inode before={inode_before} after={inode_after}")
    if inode_before != inode_after:
        details.append("inode changed — in-place write failed")
        return False
    return True


def _test_stdout_reports_bytes(tmpdir: Path, lock_root: str, details: list[str]) -> bool:
    target = tmpdir / "out.txt"
    src = tmpdir / "src.txt"
    src.write_bytes(b"12345")
    r = run(str(target), from_file=str(src), lock_root=lock_root)
    details.append(f"stdout={r.stdout!r}")
    if b"5 bytes" not in r.stdout:
        details.append("expected byte count in stdout")
        return False
    return True


def _test_usage_error_exits_1(tmpdir: Path, lock_root: str, details: list[str]) -> bool:
    """Missing --from/--stdin should exit 1 (usage error), not 2."""
    cmd = [PYTHON, str(SCRIPT), str(tmpdir / "x.txt"), "--lock-root", lock_root]
    r = subprocess.run(cmd, capture_output=True)
    details.append(f"exit={r.returncode} stderr={r.stderr!r}")
    if r.returncode != 1:
        details.append(f"expected exit 1, got {r.returncode}")
        return False
    return True


def _test_help_flag_exits_0(tmpdir: Path, lock_root: str, details: list[str]) -> bool:
    """-h should exit 0 and print usage text."""
    cmd = [PYTHON, str(SCRIPT), "-h"]
    r = subprocess.run(cmd, capture_output=True)
    details.append(f"exit={r.returncode} stdout_len={len(r.stdout)}")
    if r.returncode != 0:
        details.append(f"expected exit 0, got {r.returncode}")
        return False
    if b"write_if_unchanged" not in r.stdout:
        details.append("expected usage text in stdout")
        return False
    return True


def _test_usage_matches_help_output(tmpdir: Path, lock_root: str, details: list[str]) -> bool:
    """Raw usage (-H) must exactly match color-stripped help output (-h)."""
    raw = subprocess.run([PYTHON, str(SCRIPT), "-H"], capture_output=True)
    help_out = subprocess.run([PYTHON, str(SCRIPT), "-h"], capture_output=True)

    details.append(
        f"raw_exit={raw.returncode} help_exit={help_out.returncode} "
        f"raw_len={len(raw.stdout)} help_len={len(help_out.stdout)}"
    )

    if raw.returncode != 0:
        details.append(f"-H exited {raw.returncode}: stderr={raw.stderr!r}")
        return False
    if help_out.returncode != 0:
        details.append(f"-h exited {help_out.returncode}: stderr={help_out.stderr!r}")
        return False

    stripped_help = strip_ansi(help_out.stdout)
    if raw.stdout != stripped_help:
        details.append(f"raw stdout={raw.stdout!r}")
        details.append(f"stripped help stdout={stripped_help!r}")
        return False
    return True


def _test_binary_content(tmpdir: Path, lock_root: str, details: list[str]) -> bool:
    """Binary data (null bytes, high bytes) should roundtrip correctly."""
    target = tmpdir / "bin.dat"
    payload = bytes(range(256)) * 4  # 1024 bytes, all byte values
    r = run(str(target), stdin_data=payload, lock_root=lock_root)
    details.append(f"exit={r.returncode}")
    if r.returncode != 0:
        return False
    actual = target.read_bytes()
    if actual != payload:
        details.append(f"content mismatch: expected {len(payload)} bytes, got {len(actual)}")
        return False
    return True


def _test_lock_cleaned_up(tmpdir: Path, lock_root: str, details: list[str]) -> bool:
    """After a successful write the lock directory should be removed."""
    target = tmpdir / "clean.txt"
    src = tmpdir / "src.txt"
    src.write_bytes(b"data")
    r = run(str(target), from_file=str(src), lock_root=lock_root)
    details.append(f"exit={r.returncode}")
    if r.returncode != 0:
        return False
    lock_root_path = Path(lock_root)
    remaining = list(lock_root_path.glob("*.lock")) if lock_root_path.exists() else []
    details.append(f"remaining locks: {remaining}")
    if remaining:
        details.append("lock directory not cleaned up")
        return False
    return True


# ---------------------------------------------------------------------------
# Test registry
# ---------------------------------------------------------------------------

TESTS = [
    ("write new file (--from)",                     _test_write_new_file),
    ("overwrite existing file (--from)",            _test_overwrite_existing_file),
    ("write via --stdin",                           _test_stdin_mode),
    ("CAS match — write succeeds",                  _test_cas_match_succeeds),
    ("CAS mismatch — aborts with exit 3",           _test_cas_mismatch_aborts),
    ("CAS on nonexistent file (empty hash)",        _test_cas_nonexistent_file),
    ("lock timeout — exit 2",                       _test_lock_timeout),
    ("stale lock broken — write succeeds",          _test_stale_lock_broken),
    ("stale lock message includes --note text",     _test_stale_lock_note_in_message),
    ("--note accepted without breaking write",      _test_note_stored_in_lock_json),
    ("inode preserved on overwrite",                _test_inode_preserved),
    ("stdout reports byte count",                   _test_stdout_reports_bytes),
    ("usage error exits 1",                         _test_usage_error_exits_1),
    ("-h flag exits 0 with usage",                  _test_help_flag_exits_0),
    ("raw usage matches --help output",             _test_usage_matches_help_output),
    ("binary content roundtrips",                   _test_binary_content),
    ("lock cleaned up after write",                 _test_lock_cleaned_up),
]


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def list_tests() -> None:
    print("Available tests:")
    for i, (desc, _) in enumerate(TESTS, 1):
        print(f"  {i:2d}: {desc}")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Tests for write_if_unchanged",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("-v", dest="verbose", action="store_true",
                   help="Always show test details")
    p.add_argument("-l", "--list-tests", action="store_true",
                   help="List tests and exit")
    p.add_argument("-t", "--test", type=int, metavar="N",
                   help="Run only test number N")
    p.add_argument("--keep-artifacts", action="store_true",
                   help="Do not clean up temp dirs after running")
    return p.parse_args()


def main() -> int:
    global verbose, specific_test, keep_artifacts

    args = parse_args()
    verbose = args.verbose
    specific_test = args.test
    keep_artifacts = args.keep_artifacts

    if args.list_tests:
        list_tests()
        return 0

    for desc, fn in TESTS:
        test_case(desc, fn)

    print()
    total = passed + failed
    ran = total if specific_test is None else min(total, 1)
    print(f"{passed}/{ran} tests passed" + (f", {failed} failed" if failed else ""))
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
