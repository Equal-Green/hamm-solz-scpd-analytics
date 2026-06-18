"""Inventory the raw INFORMACIÓN archive: top-level folders, file types, counts.

Used by the Data Quality "The archive" tab to orient the reader on what the
source delivery contains and how each folder feeds the data model.
"""
import mmap
import os
import struct
from collections import Counter, defaultdict

from config import ZIP_PATH


def scan_archive(zip_path=ZIP_PATH):
    """Yield (top_folder, filename, ext) for every file under INFORMACIÓN/."""
    with open(zip_path, "rb") as f:
        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        try:
            off = 0
            seen = set()
            while True:
                p = mm.find(b"PK\x03\x04", off)
                if p == -1:
                    break
                fnl = struct.unpack_from("<H", mm, p + 26)[0]
                name = mm[p + 30:p + 30 + fnl].decode("utf-8", "replace")
                if name.startswith("INFORMACIÓN/") and not name.endswith("/") \
                        and name not in seen:
                    seen.add(name)
                    parts = name.split("/")
                    top = parts[1] if len(parts) > 2 else "(root)"
                    ext = os.path.splitext(name)[1].lower().lstrip(".") or "—"
                    yield top, name, ext
                off = p + 4
        finally:
            mm.close()


def folder_inventory(zip_path=ZIP_PATH):
    """Per top-level folder: file count + extension histogram."""
    counts = Counter()
    exts = defaultdict(Counter)
    total = 0
    all_exts = Counter()
    for top, name, ext in scan_archive(zip_path):
        counts[top] += 1
        exts[top][ext] += 1
        all_exts[ext] += 1
        total += 1
    def _order(k):
        head = k.split(".")[0].strip()
        return (k == "(root)", int(head) if head.isdigit() else 9999, k)

    folders = []
    for top in sorted(counts, key=_order):
        folders.append({
            "folder": top,
            "files": counts[top],
            "exts": dict(exts[top].most_common()),
        })
    return {"total_files": total, "folders": folders,
            "ext_totals": dict(all_exts.most_common())}
