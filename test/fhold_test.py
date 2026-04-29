#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Brian Holtz
# SPDX-License-Identifier: MIT

"""Tests for fhold.

Usage:
    fhold_test.py [-v] [-l] [-t N] [--keep-artifacts]

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
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

SCRIPT = Path(__file__).parent.parent / "fhold"
PYTHON = sys.executable


# ---------------------------------------------------------------------------
# Output helpers (same style as safewrite_test.py)
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

def sha256_of(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def strip_ansi(data: bytes) -> bytes:
    return re.sub(rb"\x1b\[[0-9;]*[A-Za-z]", b"", data)


def run_fhold(
    *args: str,
    tag_root: str | None = None,
    ttl: int | None = None,
    env_override: dict[str, str] | None = None,
) -> subprocess.CompletedProcess:
    """Run fhold with given subcommand args, injecting --tag-root and --ttl."""
    cmd = [PYTHON, str(SCRIPT)] + list(args)
    if tag_root is not None:
        cmd += ["--tag-root", tag_root]
    if ttl is not None:
        cmd += ["--ttl", str(ttl)]
    env = os.environ.copy()
    if env_override:
        env.update(env_override)
    return subprocess.run(cmd, capture_output=True, env=env)


def find_tags(tag_root: Path, suffix: str) -> list[Path]:
    """Find all tag files under tag_root containing suffix in their name."""
    if not tag_root.exists():
        return []
    return sorted(p for p in tag_root.iterdir() if suffix in p.name)


def read_tag_json(path: Path) -> dict:
    """Read a tag file as JSON."""
    return json.loads(path.read_text(encoding="utf-8"))


def make_stale_tag(tag_root: Path, target: Path, suffix: str, age_s: float = 3600) -> Path:
    """Create a tag file with old mtime, simulating a stale hold."""
    tag_root.mkdir(parents=True, exist_ok=True)
    resolved = str(target.resolve())
    key = hashlib.sha256(resolved.encode()).hexdigest()[:24]
    tag_path = tag_root / f"{key}{suffix}"
    meta = {
        "agent": "stale-agent",
        "file": str(target),
        "acquired": "2026-01-01T00:00:00",
    }
    tag_path.write_text(json.dumps(meta), encoding="utf-8")
    old_time = time.time() - age_s
    os.utime(tag_path, (old_time, old_time))
    return tag_path


# ---------------------------------------------------------------------------
# Test case harness
# ---------------------------------------------------------------------------

def test_case(desc: str, fn) -> None:
    global passed, failed, current_test_num
    current_test_num += 1
    test_descriptions.append(f"Test {current_test_num}: {desc}")

    if specific_test is not None and specific_test != current_test_num:
        return

    tmpdir = Path(tempfile.mkdtemp(prefix="fhold_test_"))
    tag_root = str(tmpdir / "tags")
    details: list[str] = []
    result = True

    try:
        result = fn(tmpdir, tag_root, details)
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


# ===========================================================================
# HELP & USAGE TESTS
# ===========================================================================

def _test_help_exits_0(tmpdir: Path, tag_root: str, details: list[str]) -> bool:
    """-h should exit 0 and print usage text."""
    r = run_fhold("-h")
    details.append(f"exit={r.returncode} stdout_len={len(r.stdout)}")
    if r.returncode != 0:
        details.append(f"expected exit 0, got {r.returncode}")
        return False
    if b"fhold" not in r.stdout:
        details.append("expected 'fhold' in usage output")
        return False
    return True


def _test_raw_help_exits_0(tmpdir: Path, tag_root: str, details: list[str]) -> bool:
    """-H should exit 0 and print raw usage text."""
    r = run_fhold("-H")
    details.append(f"exit={r.returncode} stdout_len={len(r.stdout)}")
    if r.returncode != 0:
        details.append(f"expected exit 0, got {r.returncode}")
        return False
    if b"fhold" not in r.stdout:
        details.append("expected 'fhold' in raw usage output")
        return False
    return True


def _test_help_is_colorized(tmpdir: Path, tag_root: str, details: list[str]) -> bool:
    """-h should include ANSI color sequences."""
    r = run_fhold("-h")
    details.append(f"exit={r.returncode} stdout_len={len(r.stdout)}")
    if r.returncode != 0:
        details.append(f"expected exit 0, got {r.returncode}")
        return False
    if b"\x1b[" not in r.stdout:
        details.append("expected ANSI escapes in -h output")
        return False
    return True


def _test_raw_help_is_not_colorized(tmpdir: Path, tag_root: str, details: list[str]) -> bool:
    """-H should not include ANSI color sequences."""
    r = run_fhold("-H")
    details.append(f"exit={r.returncode} stdout_len={len(r.stdout)}")
    if r.returncode != 0:
        details.append(f"expected exit 0, got {r.returncode}")
        return False
    if b"\x1b[" in r.stdout:
        details.append("did not expect ANSI escapes in -H output")
        return False
    return True


def _test_help_and_raw_help_match_when_stripped(tmpdir: Path, tag_root: str, details: list[str]) -> bool:
    """-h text should match -H text after stripping ANSI escapes."""
    rh = run_fhold("-h")
    rr = run_fhold("-H")
    details.append(f"-h exit={rh.returncode} -H exit={rr.returncode}")
    if rh.returncode != 0 or rr.returncode != 0:
        details.append("expected both -h and -H to exit 0")
        return False

    h_clean = strip_ansi(rh.stdout)
    if h_clean != rr.stdout:
        details.append("-h output (ANSI-stripped) differs from -H output")
        details.append(f"stripped_h_len={len(h_clean)} raw_len={len(rr.stdout)}")
        return False
    return True


def _test_help_follows_manpagerules_colors(tmpdir: Path, tag_root: str, details: list[str]) -> bool:
    """-h should include the ManPageRules color classes used in fhold usage."""
    r = run_fhold("-h")
    if r.returncode != 0:
        details.append(f"expected exit 0, got {r.returncode}")
        return False

    out = r.stdout

    checks = [
        (rb"\x1b\[1;34mfhold\x1b\[0m", "command style for fhold (bold DodgerBlue)"),
        (rb"\x1b\[1;36m--agent\x1b\[0m", "flag style for --agent (DeepSkyBlue)"),
        (rb"\x1b\[32m\x1b\[4m\x1b\[3mFILE\x1b\[0m", "filesystem variable style for FILE"),
        (rb"\x1b\[1;32m\x1b\[4m/tmp/fhold\.tags/\x1b\[0m", "filesystem literal style for /tmp/fhold.tags/"),
        (rb"\x1b\[35m\x1b\[3mID\x1b\[0m", "freeform variable style for ID"),
    ]

    for pattern, label in checks:
        if not re.search(pattern, out):
            details.append(f"missing style: {label}")
            return False

    return True


def _test_no_args_exits_1(tmpdir: Path, tag_root: str, details: list[str]) -> bool:
    """No arguments should exit 1 (usage error)."""
    r = run_fhold(tag_root=tag_root)
    details.append(f"exit={r.returncode} stderr={r.stderr!r}")
    if r.returncode != 1:
        details.append(f"expected exit 1, got {r.returncode}")
        return False
    return True


def _test_invalid_subcommand_exits_1(tmpdir: Path, tag_root: str, details: list[str]) -> bool:
    """Invalid subcommand should exit 1."""
    r = run_fhold("bogus", "register", str(tmpdir / "f.md"), tag_root=tag_root)
    details.append(f"exit={r.returncode} stderr={r.stderr!r}")
    if r.returncode != 1:
        details.append(f"expected exit 1, got {r.returncode}")
        return False
    return True


# ===========================================================================
# REVIEW REGISTER TESTS
# ===========================================================================

def _test_review_register_creates_tag(tmpdir: Path, tag_root: str, details: list[str]) -> bool:
    """review register should create a review_hold tag and print its path."""
    target = tmpdir / "doc.md"
    target.write_bytes(b"# Doc\n")
    r = run_fhold("review", "register", str(target), "--agent", "a1",
                  "--task", "update docs", tag_root=tag_root)
    details.append(f"exit={r.returncode} stdout={r.stdout!r} stderr={r.stderr!r}")
    if r.returncode != 0:
        details.append(f"expected exit 0, got {r.returncode}")
        return False
    # stdout should contain the tag path
    tag_path_str = r.stdout.decode().strip()
    if not tag_path_str:
        details.append("expected tag path in stdout")
        return False
    tag_path = Path(tag_path_str)
    if not tag_path.exists():
        details.append(f"tag file does not exist: {tag_path}")
        return False
    # Verify tag contains expected metadata
    meta = read_tag_json(tag_path)
    details.append(f"meta={meta}")
    if meta.get("agent") != "a1":
        details.append("expected agent=a1")
        return False
    if meta.get("task") != "update docs":
        details.append("expected task='update docs'")
        return False
    return True


def _test_review_register_records_sha256(tmpdir: Path, tag_root: str, details: list[str]) -> bool:
    """review register should record pre-write sha256 of the file."""
    target = tmpdir / "doc.md"
    content = b"# Hello\n"
    target.write_bytes(content)
    expected_hash = sha256_of(content)
    r = run_fhold("review", "register", str(target), "--agent", "a1", tag_root=tag_root)
    details.append(f"exit={r.returncode}")
    if r.returncode != 0:
        return False
    tag_path = Path(r.stdout.decode().strip())
    meta = read_tag_json(tag_path)
    actual = meta.get("pre_write_sha256") or meta.get("pre-write-sha256")
    details.append(f"expected_hash={expected_hash} actual={actual}")
    if actual != expected_hash:
        details.append("pre-write sha256 mismatch")
        return False
    return True


def _test_review_register_contention_exits_2(tmpdir: Path, tag_root: str, details: list[str]) -> bool:
    """Second review register by different agent should exit 2 (contention)."""
    target = tmpdir / "doc.md"
    target.write_bytes(b"# Doc\n")
    r1 = run_fhold("review", "register", str(target), "--agent", "a1",
                   "--task", "first task", tag_root=tag_root)
    details.append(f"r1 exit={r1.returncode}")
    if r1.returncode != 0:
        details.append("setup: first register failed")
        return False
    r2 = run_fhold("review", "register", str(target), "--agent", "a2",
                   "--task", "second task", tag_root=tag_root)
    details.append(f"r2 exit={r2.returncode} stderr={r2.stderr!r}")
    if r2.returncode != 2:
        details.append(f"expected exit 2 (contention), got {r2.returncode}")
        return False
    # stderr should mention the owning agent
    if b"a1" not in r2.stderr:
        details.append("expected owning agent 'a1' in stderr")
        return False
    return True


def _test_review_register_same_agent_succeeds(tmpdir: Path, tag_root: str, details: list[str]) -> bool:
    """Same agent re-registering review hold should succeed (idempotent or update)."""
    target = tmpdir / "doc.md"
    target.write_bytes(b"# Doc\n")
    r1 = run_fhold("review", "register", str(target), "--agent", "a1",
                   "--task", "first", tag_root=tag_root)
    details.append(f"r1 exit={r1.returncode}")
    if r1.returncode != 0:
        return False
    r2 = run_fhold("review", "register", str(target), "--agent", "a1",
                   "--task", "updated", tag_root=tag_root)
    details.append(f"r2 exit={r2.returncode}")
    if r2.returncode != 0:
        details.append(f"expected exit 0 for same agent re-register, got {r2.returncode}")
        return False
    return True


def _test_review_register_contention_shows_task(tmpdir: Path, tag_root: str, details: list[str]) -> bool:
    """Contention stderr should include the existing holder's task description."""
    target = tmpdir / "doc.md"
    target.write_bytes(b"# Doc\n")
    run_fhold("review", "register", str(target), "--agent", "a1",
              "--task", "update install steps", tag_root=tag_root)
    r2 = run_fhold("review", "register", str(target), "--agent", "a2", tag_root=tag_root)
    details.append(f"stderr={r2.stderr!r}")
    if r2.returncode != 2:
        details.append(f"expected exit 2, got {r2.returncode}")
        return False
    if b"update install steps" not in r2.stderr:
        details.append("expected task text in contention message")
        return False
    return True


def _test_review_register_default_agent(tmpdir: Path, tag_root: str, details: list[str]) -> bool:
    """Without --agent, should default to $WIBEY_SESSION_ID or $USER."""
    target = tmpdir / "doc.md"
    target.write_bytes(b"# Doc\n")
    r = run_fhold("review", "register", str(target), tag_root=tag_root,
                  env_override={"WIBEY_SESSION_ID": "session-42"})
    details.append(f"exit={r.returncode}")
    if r.returncode != 0:
        return False
    tag_path = Path(r.stdout.decode().strip())
    meta = read_tag_json(tag_path)
    details.append(f"agent={meta.get('agent')}")
    if meta.get("agent") != "session-42":
        details.append("expected agent from WIBEY_SESSION_ID")
        return False
    return True


# ===========================================================================
# REVIEW RELEASE TESTS
# ===========================================================================

def _test_review_release_removes_tag(tmpdir: Path, tag_root: str, details: list[str]) -> bool:
    """review release should remove the review_hold tag."""
    target = tmpdir / "doc.md"
    target.write_bytes(b"# Doc\n")
    r1 = run_fhold("review", "register", str(target), "--agent", "a1", tag_root=tag_root)
    if r1.returncode != 0:
        details.append(f"setup failed: {r1.stderr!r}")
        return False
    tag_path = Path(r1.stdout.decode().strip())
    if not tag_path.exists():
        details.append("tag should exist before release")
        return False
    r2 = run_fhold("review", "release", str(target), tag_root=tag_root)
    details.append(f"release exit={r2.returncode}")
    if r2.returncode != 0:
        details.append(f"expected exit 0, got {r2.returncode}")
        return False
    if tag_path.exists():
        details.append("tag file should be removed after release")
        return False
    return True


def _test_review_release_nonexistent_exits_3(tmpdir: Path, tag_root: str, details: list[str]) -> bool:
    """Releasing a review hold that doesn't exist should exit 3."""
    target = tmpdir / "doc.md"
    target.write_bytes(b"# Doc\n")
    r = run_fhold("review", "release", str(target), tag_root=tag_root)
    details.append(f"exit={r.returncode} stderr={r.stderr!r}")
    if r.returncode != 3:
        details.append(f"expected exit 3, got {r.returncode}")
        return False
    return True


# ===========================================================================
# REVIEW CHECK TESTS
# ===========================================================================

def _test_review_check_shows_hold_info(tmpdir: Path, tag_root: str, details: list[str]) -> bool:
    """review check should print hold info when a hold exists."""
    target = tmpdir / "doc.md"
    target.write_bytes(b"# Doc\n")
    run_fhold("review", "register", str(target), "--agent", "a1",
              "--task", "my task", tag_root=tag_root)
    r = run_fhold("review", "check", str(target), tag_root=tag_root)
    details.append(f"exit={r.returncode} stdout={r.stdout!r}")
    if r.returncode != 0:
        details.append(f"expected exit 0, got {r.returncode}")
        return False
    out = r.stdout.decode()
    if "a1" not in out:
        details.append("expected agent 'a1' in output")
        return False
    if "my task" not in out:
        details.append("expected task in output")
        return False
    return True


def _test_review_check_no_hold_exits_3(tmpdir: Path, tag_root: str, details: list[str]) -> bool:
    """review check when no hold exists should exit 3."""
    target = tmpdir / "doc.md"
    target.write_bytes(b"# Doc\n")
    r = run_fhold("review", "check", str(target), tag_root=tag_root)
    details.append(f"exit={r.returncode}")
    if r.returncode != 3:
        details.append(f"expected exit 3, got {r.returncode}")
        return False
    return True


# ===========================================================================
# PERMIT REGISTER TESTS
# ===========================================================================

def _test_permit_register_creates_tag(tmpdir: Path, tag_root: str, details: list[str]) -> bool:
    """permit register should create a permit tag and print its path."""
    target = tmpdir / "doc.md"
    target.write_bytes(b"# Doc\n")
    r = run_fhold("permit", "register", str(target), "--agent", "a1", tag_root=tag_root)
    details.append(f"exit={r.returncode} stdout={r.stdout!r}")
    if r.returncode != 0:
        details.append(f"expected exit 0, got {r.returncode}")
        return False
    tag_path_str = r.stdout.decode().strip()
    tag_path = Path(tag_path_str)
    if not tag_path.exists():
        details.append(f"tag file does not exist: {tag_path}")
        return False
    # Tag name should contain agent ID
    if "a1" not in tag_path.name:
        details.append(f"expected agent ID in tag filename: {tag_path.name}")
        return False
    return True


def _test_permit_multiple_agents(tmpdir: Path, tag_root: str, details: list[str]) -> bool:
    """Multiple agents can register permits for the same file."""
    target = tmpdir / "doc.md"
    target.write_bytes(b"# Doc\n")
    r1 = run_fhold("permit", "register", str(target), "--agent", "a1", tag_root=tag_root)
    r2 = run_fhold("permit", "register", str(target), "--agent", "a2", tag_root=tag_root)
    details.append(f"r1 exit={r1.returncode} r2 exit={r2.returncode}")
    if r1.returncode != 0 or r2.returncode != 0:
        details.append("both permits should succeed")
        return False
    # Both tags should exist
    tags = find_tags(Path(tag_root), ".concurrent_write_permit.")
    details.append(f"permit tags found: {len(tags)}")
    if len(tags) < 2:
        details.append("expected 2 permit tags")
        return False
    return True


def _test_permit_register_idempotent(tmpdir: Path, tag_root: str, details: list[str]) -> bool:
    """Same agent re-registering permit should succeed without creating duplicates."""
    target = tmpdir / "doc.md"
    target.write_bytes(b"# Doc\n")
    r1 = run_fhold("permit", "register", str(target), "--agent", "a1", tag_root=tag_root)
    r2 = run_fhold("permit", "register", str(target), "--agent", "a1", tag_root=tag_root)
    details.append(f"r1 exit={r1.returncode} r2 exit={r2.returncode}")
    if r1.returncode != 0 or r2.returncode != 0:
        return False
    tags = find_tags(Path(tag_root), ".concurrent_write_permit.a1")
    details.append(f"tags for a1: {len(tags)}")
    if len(tags) != 1:
        details.append("expected exactly 1 tag for a1 (idempotent)")
        return False
    return True


# ===========================================================================
# PERMIT RELEASE TESTS
# ===========================================================================

def _test_permit_release_removes_tag(tmpdir: Path, tag_root: str, details: list[str]) -> bool:
    """permit release should remove this agent's permit tag."""
    target = tmpdir / "doc.md"
    target.write_bytes(b"# Doc\n")
    run_fhold("permit", "register", str(target), "--agent", "a1", tag_root=tag_root)
    r = run_fhold("permit", "release", str(target), "--agent", "a1", tag_root=tag_root)
    details.append(f"exit={r.returncode}")
    if r.returncode != 0:
        details.append(f"expected exit 0, got {r.returncode}")
        return False
    tags = find_tags(Path(tag_root), ".concurrent_write_permit.a1")
    if tags:
        details.append("tag should be removed after release")
        return False
    return True


def _test_permit_release_nonexistent_exits_3(tmpdir: Path, tag_root: str, details: list[str]) -> bool:
    """Releasing a permit that doesn't exist should exit 3."""
    target = tmpdir / "doc.md"
    target.write_bytes(b"# Doc\n")
    r = run_fhold("permit", "release", str(target), "--agent", "a1", tag_root=tag_root)
    details.append(f"exit={r.returncode}")
    if r.returncode != 3:
        details.append(f"expected exit 3, got {r.returncode}")
        return False
    return True


def _test_permit_release_only_own_tag(tmpdir: Path, tag_root: str, details: list[str]) -> bool:
    """permit release should only remove the specified agent's tag, not others."""
    target = tmpdir / "doc.md"
    target.write_bytes(b"# Doc\n")
    run_fhold("permit", "register", str(target), "--agent", "a1", tag_root=tag_root)
    run_fhold("permit", "register", str(target), "--agent", "a2", tag_root=tag_root)
    run_fhold("permit", "release", str(target), "--agent", "a1", tag_root=tag_root)
    tags = find_tags(Path(tag_root), ".concurrent_write_permit.")
    details.append(f"remaining tags: {[t.name for t in tags]}")
    if len(tags) != 1:
        details.append("expected 1 remaining permit tag")
        return False
    if "a2" not in tags[0].name:
        details.append("expected a2's tag to remain")
        return False
    return True


# ===========================================================================
# PERMIT CHECK TESTS
# ===========================================================================

def _test_permit_check_lists_holders(tmpdir: Path, tag_root: str, details: list[str]) -> bool:
    """permit check should list all active permit holders."""
    target = tmpdir / "doc.md"
    target.write_bytes(b"# Doc\n")
    run_fhold("permit", "register", str(target), "--agent", "a1", tag_root=tag_root)
    run_fhold("permit", "register", str(target), "--agent", "a2", tag_root=tag_root)
    r = run_fhold("permit", "check", str(target), tag_root=tag_root)
    details.append(f"exit={r.returncode} stdout={r.stdout!r}")
    if r.returncode != 0:
        details.append(f"expected exit 0, got {r.returncode}")
        return False
    out = r.stdout.decode()
    if "a1" not in out or "a2" not in out:
        details.append("expected both agents in output")
        return False
    return True


def _test_permit_check_no_permits_exits_3(tmpdir: Path, tag_root: str, details: list[str]) -> bool:
    """permit check with no permits should exit 3."""
    target = tmpdir / "doc.md"
    target.write_bytes(b"# Doc\n")
    r = run_fhold("permit", "check", str(target), tag_root=tag_root)
    details.append(f"exit={r.returncode}")
    if r.returncode != 3:
        details.append(f"expected exit 3, got {r.returncode}")
        return False
    return True


# ===========================================================================
# STATUS TESTS
# ===========================================================================

def _test_status_no_holds(tmpdir: Path, tag_root: str, details: list[str]) -> bool:
    """status with no holds should report 'reviewed' mode."""
    target = tmpdir / "doc.md"
    target.write_bytes(b"# Doc\n")
    r = run_fhold("status", str(target), tag_root=tag_root)
    details.append(f"exit={r.returncode} stdout={r.stdout!r}")
    if r.returncode != 0:
        details.append(f"expected exit 0, got {r.returncode}")
        return False
    out = r.stdout.decode()
    if "reviewed" not in out.lower():
        details.append("expected 'reviewed' in status output")
        return False
    return True


def _test_status_with_review_hold(tmpdir: Path, tag_root: str, details: list[str]) -> bool:
    """status with a review hold should mention the hold and agent."""
    target = tmpdir / "doc.md"
    target.write_bytes(b"# Doc\n")
    run_fhold("review", "register", str(target), "--agent", "a1", tag_root=tag_root)
    r = run_fhold("status", str(target), tag_root=tag_root)
    details.append(f"exit={r.returncode} stdout={r.stdout!r}")
    if r.returncode != 0:
        return False
    out = r.stdout.decode()
    if "review" not in out.lower():
        details.append("expected 'review' in status")
        return False
    if "a1" not in out:
        details.append("expected agent 'a1' in status")
        return False
    return True


def _test_status_with_permits(tmpdir: Path, tag_root: str, details: list[str]) -> bool:
    """status with permit holds should report 'unreviewed' mode."""
    target = tmpdir / "doc.md"
    target.write_bytes(b"# Doc\n")
    run_fhold("permit", "register", str(target), "--agent", "a1", tag_root=tag_root)
    r = run_fhold("status", str(target), tag_root=tag_root)
    details.append(f"exit={r.returncode} stdout={r.stdout!r}")
    if r.returncode != 0:
        return False
    out = r.stdout.decode()
    if "unreviewed" not in out.lower():
        details.append("expected 'unreviewed' in status")
        return False
    if "a1" not in out:
        details.append("expected agent 'a1' in status")
        return False
    return True


def _test_status_shows_file_sha256(tmpdir: Path, tag_root: str, details: list[str]) -> bool:
    """status should include the file's current sha256."""
    target = tmpdir / "doc.md"
    content = b"# Status test\n"
    target.write_bytes(content)
    expected = sha256_of(content)
    r = run_fhold("status", str(target), tag_root=tag_root)
    details.append(f"exit={r.returncode} stdout={r.stdout!r}")
    if r.returncode != 0:
        return False
    # At least the first 12 hex chars should appear
    if expected[:12] not in r.stdout.decode():
        details.append(f"expected sha256 prefix {expected[:12]} in output")
        return False
    return True


def _test_status_permit_count(tmpdir: Path, tag_root: str, details: list[str]) -> bool:
    """status should report the number of active permits."""
    target = tmpdir / "doc.md"
    target.write_bytes(b"# Doc\n")
    run_fhold("permit", "register", str(target), "--agent", "a1", tag_root=tag_root)
    run_fhold("permit", "register", str(target), "--agent", "a2", tag_root=tag_root)
    r = run_fhold("status", str(target), tag_root=tag_root)
    details.append(f"stdout={r.stdout!r}")
    out = r.stdout.decode()
    # Should mention 2 permit holds
    if "2" not in out:
        details.append("expected count '2' in status output")
        return False
    return True


# ===========================================================================
# GC TESTS
# ===========================================================================

def _test_gc_removes_stale_review_hold(tmpdir: Path, tag_root: str, details: list[str]) -> bool:
    """gc should remove stale review holds (mtime > TTL)."""
    target = tmpdir / "doc.md"
    target.write_bytes(b"# Doc\n")
    tag_root_path = Path(tag_root)
    stale_tag = make_stale_tag(tag_root_path, target, ".review_hold", age_s=3600)
    details.append(f"stale tag: {stale_tag}")
    if not stale_tag.exists():
        details.append("setup: stale tag not created")
        return False
    r = run_fhold("gc", tag_root=tag_root, ttl=1800)
    details.append(f"exit={r.returncode} stdout={r.stdout!r}")
    if r.returncode != 0:
        details.append(f"expected exit 0, got {r.returncode}")
        return False
    if stale_tag.exists():
        details.append("stale review hold should be removed by gc")
        return False
    return True


def _test_gc_removes_stale_permit(tmpdir: Path, tag_root: str, details: list[str]) -> bool:
    """gc should remove stale permit holds (mtime > TTL)."""
    target = tmpdir / "doc.md"
    target.write_bytes(b"# Doc\n")
    tag_root_path = Path(tag_root)
    stale_tag = make_stale_tag(tag_root_path, target, ".concurrent_write_permit.old_agent", age_s=3600)
    details.append(f"stale tag: {stale_tag}")
    r = run_fhold("gc", tag_root=tag_root, ttl=1800)
    details.append(f"exit={r.returncode}")
    if r.returncode != 0:
        return False
    if stale_tag.exists():
        details.append("stale permit should be removed by gc")
        return False
    return True


def _test_gc_preserves_fresh_holds(tmpdir: Path, tag_root: str, details: list[str]) -> bool:
    """gc should not remove holds that are within TTL."""
    target = tmpdir / "doc.md"
    target.write_bytes(b"# Doc\n")
    # Create a fresh hold via register
    r1 = run_fhold("review", "register", str(target), "--agent", "a1", tag_root=tag_root)
    if r1.returncode != 0:
        details.append("setup: register failed")
        return False
    tag_path = Path(r1.stdout.decode().strip())
    r = run_fhold("gc", tag_root=tag_root, ttl=1800)
    details.append(f"gc exit={r.returncode}")
    if r.returncode != 0:
        return False
    if not tag_path.exists():
        details.append("fresh hold should not be removed by gc")
        return False
    return True


def _test_gc_empty_tag_root(tmpdir: Path, tag_root: str, details: list[str]) -> bool:
    """gc on non-existent tag root should succeed quietly."""
    r = run_fhold("gc", tag_root=tag_root, ttl=1800)
    details.append(f"exit={r.returncode}")
    if r.returncode != 0:
        details.append(f"expected exit 0, got {r.returncode}")
        return False
    return True


# ===========================================================================
# TAG KEY / PATH TESTS
# ===========================================================================

def _test_tag_key_deterministic(tmpdir: Path, tag_root: str, details: list[str]) -> bool:
    """Same file should produce the same tag key on successive calls."""
    target = tmpdir / "doc.md"
    target.write_bytes(b"# Doc\n")
    r1 = run_fhold("review", "register", str(target), "--agent", "a1", tag_root=tag_root)
    tag1 = r1.stdout.decode().strip()
    run_fhold("review", "release", str(target), tag_root=tag_root)
    r2 = run_fhold("review", "register", str(target), "--agent", "a1", tag_root=tag_root)
    tag2 = r2.stdout.decode().strip()
    details.append(f"tag1={tag1} tag2={tag2}")
    if tag1 != tag2:
        details.append("tag paths should be deterministic for same file")
        return False
    return True


def _test_different_files_different_keys(tmpdir: Path, tag_root: str, details: list[str]) -> bool:
    """Different files should produce different tag keys."""
    f1 = tmpdir / "doc1.md"
    f2 = tmpdir / "doc2.md"
    f1.write_bytes(b"# A\n")
    f2.write_bytes(b"# B\n")
    r1 = run_fhold("review", "register", str(f1), "--agent", "a1", tag_root=tag_root)
    r2 = run_fhold("review", "register", str(f2), "--agent", "a1", tag_root=tag_root)
    tag1 = r1.stdout.decode().strip()
    tag2 = r2.stdout.decode().strip()
    details.append(f"tag1={tag1} tag2={tag2}")
    if tag1 == tag2:
        details.append("different files should have different tag paths")
        return False
    return True


def _test_review_hold_tag_suffix(tmpdir: Path, tag_root: str, details: list[str]) -> bool:
    """Review hold tag should end with .review_hold."""
    target = tmpdir / "doc.md"
    target.write_bytes(b"# Doc\n")
    r = run_fhold("review", "register", str(target), "--agent", "a1", tag_root=tag_root)
    tag_path = r.stdout.decode().strip()
    details.append(f"tag_path={tag_path}")
    if not tag_path.endswith(".review_hold"):
        details.append("expected .review_hold suffix")
        return False
    return True


def _test_permit_tag_suffix(tmpdir: Path, tag_root: str, details: list[str]) -> bool:
    """Permit tag should end with .concurrent_write_permit.AGENT."""
    target = tmpdir / "doc.md"
    target.write_bytes(b"# Doc\n")
    r = run_fhold("permit", "register", str(target), "--agent", "myagent", tag_root=tag_root)
    tag_path = r.stdout.decode().strip()
    details.append(f"tag_path={tag_path}")
    if not tag_path.endswith(".concurrent_write_permit.myagent"):
        details.append("expected .concurrent_write_permit.myagent suffix")
        return False
    return True


# ===========================================================================
# MODE TRANSITION TESTS (full workflow)
# ===========================================================================

def _test_workflow_review_to_permit_to_review(tmpdir: Path, tag_root: str, details: list[str]) -> bool:
    """Full workflow: review hold -> release -> permit -> release -> back to reviewed."""
    target = tmpdir / "doc.md"
    target.write_bytes(b"# Doc\n")

    # Step 1: review hold
    r = run_fhold("review", "register", str(target), "--agent", "a1", tag_root=tag_root)
    if r.returncode != 0:
        details.append(f"step 1 failed: {r.stderr!r}")
        return False

    # Step 2: status should show review hold
    r = run_fhold("status", str(target), tag_root=tag_root)
    if "a1" not in r.stdout.decode():
        details.append("step 2: expected a1 in status")
        return False

    # Step 3: release review hold
    r = run_fhold("review", "release", str(target), tag_root=tag_root)
    if r.returncode != 0:
        details.append(f"step 3 failed: {r.stderr!r}")
        return False

    # Step 4: register permits
    r = run_fhold("permit", "register", str(target), "--agent", "a2", tag_root=tag_root)
    if r.returncode != 0:
        details.append(f"step 4 failed: {r.stderr!r}")
        return False

    # Step 5: status should show unreviewed
    r = run_fhold("status", str(target), tag_root=tag_root)
    if "unreviewed" not in r.stdout.decode().lower():
        details.append(f"step 5: expected 'unreviewed', got: {r.stdout!r}")
        return False

    # Step 6: release permit
    r = run_fhold("permit", "release", str(target), "--agent", "a2", tag_root=tag_root)
    if r.returncode != 0:
        details.append(f"step 6 failed: {r.stderr!r}")
        return False

    # Step 7: status should be back to reviewed (no holds)
    r = run_fhold("status", str(target), tag_root=tag_root)
    out = r.stdout.decode().lower()
    details.append(f"final status: {r.stdout!r}")
    if "reviewed" not in out:
        details.append("expected 'reviewed' mode after all holds released")
        return False
    # Should NOT say "unreviewed"
    if "unreviewed" in out:
        details.append("should not say 'unreviewed' when no holds exist")
        return False
    return True


def _test_contention_then_permit_workflow(tmpdir: Path, tag_root: str, details: list[str]) -> bool:
    """Agent 2 hits contention, user resolves, agent 2 switches to permit mode."""
    target = tmpdir / "doc.md"
    target.write_bytes(b"# Doc\n")

    # Agent 1 registers review hold
    run_fhold("review", "register", str(target), "--agent", "a1",
              "--task", "editing", tag_root=tag_root)

    # Agent 2 tries review register -> contention
    r = run_fhold("review", "register", str(target), "--agent", "a2", tag_root=tag_root)
    if r.returncode != 2:
        details.append(f"expected contention (exit 2), got {r.returncode}")
        return False

    # User resolves: release agent 1's hold, agent 2 goes permit mode
    run_fhold("review", "release", str(target), tag_root=tag_root)
    r = run_fhold("permit", "register", str(target), "--agent", "a2", tag_root=tag_root)
    if r.returncode != 0:
        details.append(f"permit register failed: {r.stderr!r}")
        return False

    # Agent 1 checks status, sees permit mode, joins
    r = run_fhold("status", str(target), tag_root=tag_root)
    if "unreviewed" not in r.stdout.decode().lower():
        details.append(f"expected unreviewed mode, got: {r.stdout!r}")
        return False

    r = run_fhold("permit", "register", str(target), "--agent", "a1", tag_root=tag_root)
    if r.returncode != 0:
        details.append(f"agent 1 permit failed: {r.stderr!r}")
        return False

    # Both permits active
    r = run_fhold("status", str(target), tag_root=tag_root)
    details.append(f"final status: {r.stdout!r}")
    if "2" not in r.stdout.decode():
        details.append("expected 2 permit holders in status")
        return False
    return True


# ===========================================================================
# EDGE CASE TESTS
# ===========================================================================

def _test_nonexistent_file_review_register(tmpdir: Path, tag_root: str, details: list[str]) -> bool:
    """review register on a file that doesn't exist should still work
    (file may be about to be created)."""
    target = tmpdir / "not_yet.md"
    r = run_fhold("review", "register", str(target), "--agent", "a1", tag_root=tag_root)
    details.append(f"exit={r.returncode} stdout={r.stdout!r}")
    # Should succeed — the file might be about to be created
    if r.returncode != 0:
        details.append(f"expected exit 0, got {r.returncode}")
        return False
    return True


def _test_tag_root_created_automatically(tmpdir: Path, tag_root: str, details: list[str]) -> bool:
    """--tag-root directory should be created if it doesn't exist."""
    deep_root = str(tmpdir / "deep" / "nested" / "tags")
    target = tmpdir / "doc.md"
    target.write_bytes(b"# Doc\n")
    r = run_fhold("review", "register", str(target), "--agent", "a1", tag_root=deep_root)
    details.append(f"exit={r.returncode}")
    if r.returncode != 0:
        details.append(f"expected exit 0, got {r.returncode}")
        return False
    if not Path(deep_root).exists():
        details.append("tag-root should be created automatically")
        return False
    return True


def _test_review_register_records_timestamp(tmpdir: Path, tag_root: str, details: list[str]) -> bool:
    """Review hold tag should contain a timestamp."""
    target = tmpdir / "doc.md"
    target.write_bytes(b"# Doc\n")
    r = run_fhold("review", "register", str(target), "--agent", "a1", tag_root=tag_root)
    if r.returncode != 0:
        details.append(f"register failed: {r.stderr!r}")
        return False
    tag_path = Path(r.stdout.decode().strip())
    meta = read_tag_json(tag_path)
    details.append(f"meta keys: {list(meta.keys())}")
    acquired = meta.get("acquired") or meta.get("timestamp")
    if not acquired:
        details.append("expected 'acquired' or 'timestamp' in tag metadata")
        return False
    return True


def _test_status_missing_file(tmpdir: Path, tag_root: str, details: list[str]) -> bool:
    """status on a file that doesn't exist should still work (report no holds)."""
    target = tmpdir / "ghost.md"
    r = run_fhold("status", str(target), tag_root=tag_root)
    details.append(f"exit={r.returncode} stdout={r.stdout!r}")
    if r.returncode != 0:
        details.append(f"expected exit 0, got {r.returncode}")
        return False
    return True


# ---------------------------------------------------------------------------
# Test registry
# ---------------------------------------------------------------------------

TESTS = [
    # Help & usage
    ("-h exits 0 with usage",                          _test_help_exits_0),
    ("-H exits 0 with raw usage",                      _test_raw_help_exits_0),
    ("-h output is colorized",                         _test_help_is_colorized),
    ("-H output is plain text",                        _test_raw_help_is_not_colorized),
    ("-h stripped matches -H",                         _test_help_and_raw_help_match_when_stripped),
    ("-h follows ManPageRules color classes",          _test_help_follows_manpagerules_colors),
    ("no args exits 1",                                _test_no_args_exits_1),
    ("invalid subcommand exits 1",                     _test_invalid_subcommand_exits_1),

    # review register
    ("review register creates tag",                    _test_review_register_creates_tag),
    ("review register records sha256",                 _test_review_register_records_sha256),
    ("review register records timestamp",              _test_review_register_records_timestamp),
    ("review register contention exits 2",             _test_review_register_contention_exits_2),
    ("review register same agent succeeds",            _test_review_register_same_agent_succeeds),
    ("review register contention shows task",          _test_review_register_contention_shows_task),
    ("review register default agent from env",         _test_review_register_default_agent),

    # review release
    ("review release removes tag",                     _test_review_release_removes_tag),
    ("review release nonexistent exits 3",             _test_review_release_nonexistent_exits_3),

    # review check
    ("review check shows hold info",                   _test_review_check_shows_hold_info),
    ("review check no hold exits 3",                   _test_review_check_no_hold_exits_3),

    # permit register
    ("permit register creates tag",                    _test_permit_register_creates_tag),
    ("permit multiple agents coexist",                 _test_permit_multiple_agents),
    ("permit register idempotent",                     _test_permit_register_idempotent),

    # permit release
    ("permit release removes tag",                     _test_permit_release_removes_tag),
    ("permit release nonexistent exits 3",             _test_permit_release_nonexistent_exits_3),
    ("permit release only own tag",                    _test_permit_release_only_own_tag),

    # permit check
    ("permit check lists holders",                     _test_permit_check_lists_holders),
    ("permit check no permits exits 3",                _test_permit_check_no_permits_exits_3),

    # status
    ("status no holds = reviewed",                     _test_status_no_holds),
    ("status with review hold",                        _test_status_with_review_hold),
    ("status with permits = unreviewed",               _test_status_with_permits),
    ("status shows file sha256",                       _test_status_shows_file_sha256),
    ("status shows permit count",                      _test_status_permit_count),

    # gc
    ("gc removes stale review hold",                   _test_gc_removes_stale_review_hold),
    ("gc removes stale permit",                        _test_gc_removes_stale_permit),
    ("gc preserves fresh holds",                       _test_gc_preserves_fresh_holds),
    ("gc on empty tag root succeeds",                  _test_gc_empty_tag_root),

    # tag key / path
    ("tag key is deterministic",                       _test_tag_key_deterministic),
    ("different files get different keys",             _test_different_files_different_keys),
    ("review hold tag ends with .review_hold",         _test_review_hold_tag_suffix),
    ("permit tag ends with .concurrent_write_permit",  _test_permit_tag_suffix),

    # workflows
    ("full workflow: review -> permit -> review",      _test_workflow_review_to_permit_to_review),
    ("contention -> permit mode workflow",             _test_contention_then_permit_workflow),

    # edge cases
    ("review register on nonexistent file",            _test_nonexistent_file_review_register),
    ("tag root created automatically",                 _test_tag_root_created_automatically),
    ("status on missing file",                         _test_status_missing_file),
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
        description="Tests for fhold",
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
