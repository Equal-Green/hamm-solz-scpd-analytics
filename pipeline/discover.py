"""Scan the source ZIP and report which target files are present."""
import os

from config import FILES, ZIP_PATH
from pipeline.extract import scan_zip_for


def inventory(zip_path=ZIP_PATH):
    """Return a list of inventory rows, one per configured file, each with:
    key, match, found (bool), filename, header_offset, data_offset.
    """
    if not os.path.exists(zip_path):
        raise FileNotFoundError(f"Source ZIP not found: {zip_path}")

    matches = [f["match"] for f in FILES]
    hits = scan_zip_for(zip_path, matches)
    by_match = {}
    for h in hits:
        for spec in FILES:
            if spec["match"] in h["filename"]:
                by_match.setdefault(spec["match"], h)

    rows = []
    for spec in FILES:
        hit = by_match.get(spec["match"])
        rows.append(
            {
                "key": spec["key"],
                "match": spec["match"],
                "expected_rows": spec["expected_rows"],
                "found": hit is not None,
                "filename": hit["filename"] if hit else None,
                "header_offset": hit["header_offset"] if hit else None,
                "data_offset": hit["data_offset"] if hit else None,
            }
        )
    return rows
