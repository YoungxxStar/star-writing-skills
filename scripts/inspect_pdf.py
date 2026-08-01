#!/usr/bin/env python3
"""Inspect a rendered research PDF without modifying it.

Reports the exact path, SHA-256, size, page geometry, fonts, raster resolution,
and largest embedded raster objects. Optional thresholds make the command fail
closed for a venue-specific finalization gate.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


FONT_TRAILER = re.compile(
    r"\s+(yes|no)\s+(yes|no)\s+(yes|no)\s+\d+\s+\d+\s*$"
)


def run(*args: str) -> str:
    return subprocess.run(
        args,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ).stdout


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def parse_pdfinfo(path: Path) -> dict[str, str]:
    info: dict[str, str] = {}
    for line in run("pdfinfo", str(path)).splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        info[key.strip()] = value.strip()
    return info


def parse_fonts(path: Path) -> dict[str, Any]:
    lines = run("pdffonts", str(path)).splitlines()[2:]
    count = 0
    type3: list[str] = []
    unembedded: list[str] = []
    unparsable: list[str] = []
    for line in lines:
        if not line.strip():
            continue
        count += 1
        if "Type 3" in line:
            type3.append(line.strip())
        match = FONT_TRAILER.search(line)
        if match is None:
            unparsable.append(line.strip())
        elif match.group(1) != "yes":
            unembedded.append(line.strip())
    return {
        "count": count,
        "type3": type3,
        "unembedded": unembedded,
        "unparsable": unparsable,
    }


def size_bytes(value: str) -> int:
    match = re.fullmatch(r"([0-9.]+)([KMG]?)B?", value)
    if match is None:
        raise ValueError(f"unrecognized embedded size: {value!r}")
    number = float(match.group(1))
    factor = {"": 1, "K": 1024, "M": 1024**2, "G": 1024**3}[match.group(2)]
    return round(number * factor)


def parse_images(path: Path) -> list[dict[str, Any]]:
    images: list[dict[str, Any]] = []
    for line in run("pdfimages", "-list", str(path)).splitlines():
        cells = line.split()
        if len(cells) < 16 or not cells[0].isdigit():
            continue
        try:
            images.append(
                {
                    "page": int(cells[0]),
                    "number": int(cells[1]),
                    "type": cells[2],
                    "width": int(cells[3]),
                    "height": int(cells[4]),
                    "x_ppi": int(cells[12]),
                    "y_ppi": int(cells[13]),
                    "embedded_bytes": size_bytes(cells[14]),
                }
            )
        except ValueError as exc:
            raise RuntimeError(f"could not parse pdfimages row: {line}") from exc
    return images


def inspect(path: Path, top: int) -> dict[str, Any]:
    info = parse_pdfinfo(path)
    fonts = parse_fonts(path)
    images = parse_images(path)
    raster = [item for item in images if item["type"] == "image"]
    largest = sorted(raster, key=lambda item: item["embedded_bytes"], reverse=True)
    return {
        "path": str(path),
        "sha256": sha256(path),
        "bytes": path.stat().st_size,
        "pages": int(info["Pages"]) if info.get("Pages", "").isdigit() else info.get("Pages"),
        "page_size": info.get("Page size"),
        "pdf_version": info.get("PDF version"),
        "encrypted": info.get("Encrypted"),
        "fonts": fonts,
        "raster_images": len(raster),
        "minimum_ppi": min(
            (min(item["x_ppi"], item["y_ppi"]) for item in raster),
            default=None,
        ),
        "largest_raster_objects": largest[:top],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--max-bytes", type=int)
    parser.add_argument("--min-ppi", type=int)
    parser.add_argument("--require-embedded-fonts", action="store_true")
    parser.add_argument("--forbid-type3", action="store_true")
    parser.add_argument("--top", type=int, default=10)
    args = parser.parse_args()

    for program in ("pdfinfo", "pdffonts", "pdfimages"):
        if shutil.which(program) is None:
            print(f"missing required program: {program}", file=sys.stderr)
            return 2

    path = args.pdf.expanduser().resolve()
    if not path.is_file():
        print(f"PDF not found: {path}", file=sys.stderr)
        return 2

    report = inspect(path, max(args.top, 0))
    failures: list[str] = []
    if args.max_bytes is not None and report["bytes"] > args.max_bytes:
        failures.append(
            f"size {report['bytes']} exceeds maximum {args.max_bytes} bytes"
        )
    minimum_ppi = report["minimum_ppi"]
    if (
        args.min_ppi is not None
        and minimum_ppi is not None
        and minimum_ppi < args.min_ppi
    ):
        failures.append(f"minimum raster resolution {minimum_ppi} < {args.min_ppi} ppi")
    if args.require_embedded_fonts and report["fonts"]["unembedded"]:
        failures.append("unembedded fonts detected")
    if args.forbid_type3 and report["fonts"]["type3"]:
        failures.append("Type 3 fonts detected")
    if report["fonts"]["unparsable"]:
        failures.append("one or more pdffonts rows could not be parsed")

    report["failures"] = failures
    print(json.dumps(report, indent=2, sort_keys=True))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
