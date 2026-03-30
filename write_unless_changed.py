#!/usr/bin/env python3
"""Safely write file content with advisory lock + CAS revalidation.

Usage:
  write_unless_changed.py TARGET --from NEW_CONTENT_FILE --expect-sha256 HASH [--note TEXT] [--lock-root .agent-locks] [--ttl 120]
  cat new.txt | write_unless_changed.py TARGET --stdin --expect-sha256 HASH [--note TEXT] [--lock-root .agent-locks] [--ttl 120]

--expect-sha256 is the sha256 of the file as the caller read it before deciding to write.
  If the file has changed since then (CAS mismatch), the write is aborted with exit 3.
  Omit to skip the CAS check (advisory lock only).

Exit codes:
  0 success
  2 lock acquisition timeout
  3 stale read / CAS mismatch
  4 verification failure
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import socket
import sys
import threading
import time
from pathlib import Path
from typing import Optional


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_bytes(path: Path) -> bytes:
    if not path.exists():
        return b""
    return path.read_bytes()


def fingerprint(path: Path) -> dict:
    if not path.exists():
        return {
            "exists": False,
            "size": 0,
            "mtime_ns": 0,
            "sha256": sha256_bytes(b""),
        }
    data = path.read_bytes()
    st = path.stat()
    return {
        "exists": True,
        "size": st.st_size,
        "mtime_ns": st.st_mtime_ns,
        "sha256": sha256_bytes(data),
    }


def canonical_key(path: Path) -> str:
    canon = str(path.resolve())
    return hashlib.sha256(canon.encode("utf-8")).hexdigest()[:24]


def load_meta(meta_file: Path) -> Optional[dict]:
    try:
        return json.loads(meta_file.read_text(encoding="utf-8"))
    except Exception:
        return None


def is_stale(meta: Optional[dict], now: float, ttl: int) -> bool:
    if not meta:
        return True
    hb = meta.get("heartbeat_at", 0)
    try:
        hb = float(hb)
    except Exception:
        return True
    return (now - hb) > ttl


def write_meta(meta_file: Path, meta: dict) -> None:
    meta_file.write_text(json.dumps(meta, indent=2, sort_keys=True), encoding="utf-8")


# TODO: support multiple TARGET --from FILE [--expect-sha256 HASH] tuples in a single invocation,
# acquiring all locks in canonical (sorted resolved-path) order to prevent deadlock, then writing
# all-or-nothing and releasing in reverse order.


def acquire_lock(lock_dir: Path, target: Path, ttl: int, wait_s: int, owner: str, note: str = "") -> Optional[Path]:
    lock_dir.mkdir(parents=True, exist_ok=True)
    lock_path = lock_dir / f"{canonical_key(target)}.lock"
    meta_file = lock_path / "lock.json"

    deadline = time.time() + wait_s
    while True:
        now = time.time()
        try:
            os.mkdir(lock_path)
            meta = {
                "owner": owner,
                "pid": os.getpid(),
                "hostname": socket.gethostname(),
                "started_at": now,
                "heartbeat_at": now,
                "target": str(target.resolve()),
                "note": note,
            }
            write_meta(meta_file, meta)
            return lock_path
        except FileExistsError:
            meta = load_meta(meta_file)
            if is_stale(meta, now, ttl):
                stale_owner = (meta or {}).get("owner", "unknown")
                stale_hb = (meta or {}).get("heartbeat_at", "unknown")
                stale_note = (meta or {}).get("note", "")
                note_part = f", note={stale_note!r}" if stale_note else ""
                print(
                    f"Stale lock detected at {lock_path} (owner={stale_owner}, heartbeat_at={stale_hb}{note_part}). Breaking lock.",
                    file=sys.stderr,
                )
                try:
                    if meta_file.exists():
                        meta_file.unlink()
                    os.rmdir(lock_path)
                except Exception:
                    pass
            else:
                if now >= deadline:
                    return None
                time.sleep(0.25)


def start_heartbeat(lock_path: Path, stop_evt: threading.Event, interval_s: float = 10.0) -> threading.Thread:
    meta_file = lock_path / "lock.json"

    def _run() -> None:
        while not stop_evt.wait(interval_s):
            meta = load_meta(meta_file)
            if not meta:
                continue
            meta["heartbeat_at"] = time.time()
            try:
                write_meta(meta_file, meta)
            except Exception:
                pass

    t = threading.Thread(target=_run, name="agent-lock-heartbeat", daemon=True)
    t.start()
    return t


def write_in_place(path: Path, data: bytes) -> None:
    if path.exists():
        with path.open("r+b") as f:
            f.seek(0)
            f.truncate(0)
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
    else:
        with path.open("wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())


def release_lock(lock_path: Path) -> None:
    meta_file = lock_path / "lock.json"
    try:
        if meta_file.exists():
            meta_file.unlink()
    finally:
        try:
            os.rmdir(lock_path)
        except Exception:
            pass


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Safe write with advisory lock and CAS revalidation")
    p.add_argument("target", help="Target file path")
    src = p.add_mutually_exclusive_group(required=True)
    src.add_argument("--from", dest="from_file", help="Path to file containing new content")
    src.add_argument("--stdin", action="store_true", help="Read new content from stdin")
    p.add_argument("--lock-root", default=".agent-locks", help="Directory for lock entries")
    p.add_argument("--ttl", type=int, default=120, help="Stale lock TTL in seconds")
    p.add_argument("--wait", type=int, default=30, help="Max seconds to wait for lock")
    p.add_argument("--owner", default=os.environ.get("USER", "unknown"), help="Owner label in lock metadata")
    p.add_argument("--expect-sha256", dest="expect_sha256", default=None,
                   help="SHA-256 of the file as the caller read it; write aborts if file has changed (CAS)")
    p.add_argument("--note", default="",
                   help="Free-form advisory text stored in the lock (agent name, task ID, prompt summary, etc.)")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    target = Path(args.target).expanduser()
    lock_root = Path(args.lock_root).expanduser()

    if args.stdin:
        new_data = sys.stdin.buffer.read()
    else:
        new_data = Path(args.from_file).expanduser().read_bytes()

    lock_path = acquire_lock(lock_root, target, ttl=args.ttl, wait_s=args.wait, owner=args.owner, note=args.note)
    if lock_path is None:
        print(f"Failed to acquire lock for {target} within {args.wait}s", file=sys.stderr)
        return 2

    stop_evt = threading.Event()
    hb = start_heartbeat(lock_path, stop_evt)

    try:
        if args.expect_sha256 is not None:
            current_sha256 = fingerprint(target)["sha256"]
            if current_sha256 != args.expect_sha256:
                print(
                    f"CAS mismatch for {target}: expected {args.expect_sha256}, found {current_sha256}",
                    file=sys.stderr,
                )
                return 3

        write_in_place(target, new_data)

        final_data = read_bytes(target)
        if sha256_bytes(final_data) != sha256_bytes(new_data):
            print(f"Verification failed after write for {target}", file=sys.stderr)
            return 4

        print(f"Wrote {len(new_data)} bytes safely to {target}")
        return 0
    finally:
        stop_evt.set()
        hb.join(timeout=1.0)
        release_lock(lock_path)


if __name__ == "__main__":
    raise SystemExit(main())
