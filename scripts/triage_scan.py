"""Decompress and scan iTrace triage_data logs for errors.

Handles double-compressed (.gz.bz2) and single-compressed logs on Samba/UNC.
Usage:
  py scripts/triage_scan.py <triage_data_dir> [--file NAME] [--full] [--tail N]
Paths may be given as NFS (/nfs/...) and are translated to Samba UNC.
"""
import bz2
import gzip
import os
import re
import sys
import argparse

SAMBA = r"\\?\UNC\sc8-samba.sc.intel.com\nfs"


def to_unc(p: str) -> str:
    if p.startswith("/nfs/"):
        rest = p[len("/nfs/"):].replace("/", "\\")
        return SAMBA + "\\" + rest
    return p


def decomp(path: str) -> str:
    data = open(path, "rb").read()
    # peel bz2 then gzip if present, based on suffix / magic
    if path.endswith(".bz2"):
        data = bz2.decompress(data)
        path = path[:-4]
    if path.endswith(".gz") or data[:2] == b"\x1f\x8b":
        data = gzip.decompress(data)
    return data.decode("utf-8", errors="replace")


ERR_RE = re.compile(
    r"error|fatal|abort|exception|cannot|no such|not found|traceback|"
    r"\bfail(ed|ure)?\b|\bERROR\b|assert|undefined|missing|invalid|denied",
    re.I,
)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dir")
    ap.add_argument("--file", default=None, help="scan only this filename")
    ap.add_argument("--full", action="store_true", help="print full decompressed content")
    ap.add_argument("--tail", type=int, default=0, help="print last N lines")
    ap.add_argument("--context", type=int, default=0, help="lines of context around matches")
    args = ap.parse_args()

    d = to_unc(args.dir)
    names = [args.file] if args.file else sorted(os.listdir(d))
    for name in names:
        fp = os.path.join(d, name)
        if not os.path.isfile(fp):
            continue
        if not (name.endswith((".bz2", ".gz", ".log")) or ".log" in name):
            continue
        try:
            text = decomp(fp)
        except Exception as e:  # noqa: BLE001
            print(f"== {name}: SKIP ({e})")
            continue
        lines = text.splitlines()
        print(f"\n===== {name}  ({len(lines)} lines) =====")
        if args.full:
            print(text)
            continue
        if args.tail:
            print("\n".join(lines[-args.tail:]))
            continue
        hits = [i for i, l in enumerate(lines) if ERR_RE.search(l)]
        if not hits:
            print("  (no error-like lines)")
            continue
        shown = set()
        for i in hits:
            lo = max(0, i - args.context)
            hi = min(len(lines), i + args.context + 1)
            for j in range(lo, hi):
                if j in shown:
                    continue
                shown.add(j)
                print(f"  {j:5}: {lines[j][:400]}")


if __name__ == "__main__":
    main()
