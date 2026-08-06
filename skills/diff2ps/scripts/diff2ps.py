#!/usr/bin/env python3
"""Prepare, validate, and render source-faithful semantic version handoffs."""

from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

EXCLUSION_REASONS = {
    "formatting", "generated", "metadata", "reflow", "reorder", "style-only"
}


def fail(message: str) -> None:
    raise SystemExit(f"diff2ps: {message}")


def read_utf8(path: Path) -> str:
    try:
        return path.read_bytes().decode("utf-8")
    except UnicodeDecodeError:
        fail(f"{path} is not UTF-8 text; create and identify a text projection first")


def digest(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def write(path: Path, text: str, force: bool) -> None:
    if path.exists() and not force:
        fail(f"refusing to overwrite {path}; pass --force for a derived artifact")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def git_output(repo: Path, *args: str) -> bytes:
    result = subprocess.run(
        ["git", "-C", str(repo), *args], capture_output=True, check=False
    )
    if result.returncode:
        fail(result.stderr.decode("utf-8", "replace").strip())
    return result.stdout


def snapshot(args: argparse.Namespace) -> None:
    rel = Path(args.path)
    if rel.is_absolute() or ".." in rel.parts:
        fail("--path must be a repository-relative path without '..'")
    repo, out = Path(args.repo).resolve(), Path(args.output_dir).resolve()
    if (repo / rel).resolve() in {out / "before.txt", out / "after.txt", out / "source-identities.json"}: fail("snapshot outputs must not alias the working-tree source path")
    identities: dict[str, dict[str, str]] = {}
    for role, ref in (("before", args.before_ref), ("after", args.after_ref)):
        commit = git_output(repo, "rev-parse", "--verify", "--end-of-options", f"{ref}^{{commit}}").decode().strip()
        data = git_output(repo, "show", f"{commit}:{rel.as_posix()}")
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            fail(f"{role} snapshot is not UTF-8 text")
        write(out / f"{role}.txt", text, args.force)
        identities[role] = {"ref": ref, "commit": commit, "path": rel.as_posix(), "digest": digest(data)}
    write(out / "source-identities.json", json.dumps(identities, indent=2) + "\n", args.force)
    print(json.dumps(identities, indent=2))


def prepare(args: argparse.Namespace) -> None:
    before_path, after_path = Path(args.before).resolve(), Path(args.after).resolve()
    before, after = read_utf8(before_path), read_utf8(after_path)
    lines = list(difflib.unified_diff(
        before.splitlines(keepends=True), after.splitlines(keepends=True),
        fromfile=args.before_label, tofile=args.after_label, n=args.context,
    ))
    headers, hunks, current = lines[:2], [], []
    for line in lines[2:]:
        if line.startswith("@@"):
            if current:
                hunks.append(current)
            current = [line]
        elif current:
            current.append(line)
    if current:
        hunks.append(current)
    out = Path(args.output_dir).resolve()
    if {out / "diff.patch", out / "coverage.json"} & {before_path, after_path}:
        fail("derived coverage paths must not alias either endpoint")
    patch = "".join(headers + [line for hunk in hunks for line in hunk])
    coverage = {
        "before": {"label": args.before_label, "digest": digest(before.encode())},
        "after": {"label": args.after_label, "digest": digest(after.encode())},
        "hunks": [
            {"id": f"H{i:03d}", "header": h[0].strip(),
             "before_start": int(re.match(r"@@ -(\d+)", h[0]).group(1)),
             "before_count": int((re.match(r"@@ -\d+(?:,(\d+))?", h[0]).group(1) or "1")),
             "after_start": int(re.search(r"\+(\d+)", h[0]).group(1)),
             "after_count": int((re.search(r"\+\d+(?:,(\d+))?", h[0]).group(1) or "1")),
             "removed_lines": [x[1:].rstrip("\n") for x in h[1:] if x.startswith("-")],
             "added_lines": [x[1:].rstrip("\n") for x in h[1:] if x.startswith("+")]}
            for i, h in enumerate(hunks, 1)
        ],
    }
    write(out / "diff.patch", patch, args.force)
    write(out / "coverage.json", json.dumps(coverage, indent=2) + "\n", args.force)
    print(json.dumps({"hunks": len(hunks), "output_dir": str(out)}, indent=2))


def load_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot read JSON from {path}: {exc}")
    if not isinstance(value, dict):
        fail(f"{path} must contain a JSON object")
    return value


def validate(spec: dict, coverage: dict, before: str, after: str) -> dict:
    if coverage.get("before", {}).get("digest") != digest(before.encode()) or coverage.get("after", {}).get("digest") != digest(after.encode()):
        fail("coverage identities do not match the supplied endpoint files")
    changes, excluded = spec.get("changes"), spec.get("excluded_hunks", [])
    if not isinstance(changes, list) or not isinstance(excluded, list):
        fail("spec changes and excluded_hunks must be lists")
    ranges = {h["id"]: h for h in coverage.get("hunks", [])}
    known = set(ranges)
    substantive, exclusions = set(), set()
    for index, item in enumerate(changes, 1):
        if item.get("ps") != index:
            fail("ps values must be sequential integers starting at 1")
        if item.get("status") not in {"added", "deleted", "modified"}:
            fail(f"ps{index} has an invalid status")
        for field in ("section", "comment"):
            if not isinstance(item.get(field), str) or not item[field].strip():
                fail(f"ps{index} requires non-empty {field}")
        ids = item.get("hunks")
        if not isinstance(ids, list) or not ids:
            fail(f"ps{index} must cite at least one diff hunk")
        substantive.update(ids)
        old, new, status = item.get("before"), item.get("after"), item["status"]
        if status != "added" and (not isinstance(old, str) or old not in before):
            fail(f"ps{index} [before] is not an exact source substring")
        if status != "deleted" and (not isinstance(new, str) or new not in after):
            fail(f"ps{index} [after] is not an exact source substring")
        for role, source, excerpt in (("before", before, old), ("after", after, new)):
            if excerpt is None:
                continue
            positions, offset = [], 0
            while (found := source.find(excerpt, offset)) >= 0:
                positions.append(source.count("\n", 0, found) + 1); offset = found + 1
            if not any(
                ranges[h][f"{role}_start"] <= line < ranges[h][f"{role}_start"] + ranges[h][f"{role}_count"]
                for h in ids if h in ranges for line in positions
            ):
                fail(f"ps{index} [{role}] does not intersect its cited hunk range")
        if status == "added" and old is not None:
            fail(f"ps{index} added status requires null before")
        if status == "deleted" and new is not None:
            fail(f"ps{index} deleted status requires null after")
        if status == "modified" and old == new:
            fail(f"ps{index} modified excerpts are identical")
    for item in excluded:
        ids = item.get("hunks")
        if not isinstance(ids, list) or not ids:
            fail("each excluded_hunks item must cite hunks")
        if item.get("reason") not in EXCLUSION_REASONS or not str(item.get("note", "")).strip():
            fail("each excluded_hunks item needs an allowed reason and a non-empty note")
        for role, source in (("before", before), ("after", after)):
            excerpt = item.get(role)
            if excerpt is not None and (not isinstance(excerpt, str) or excerpt not in source):
                fail(f"excluded hunk [{role}] is not an exact source substring")
        exclusions.update(ids)
    unknown = (substantive | exclusions) - known
    missing = known - substantive - exclusions
    if unknown or missing:
        fail(f"coverage failed: unknown={sorted(unknown)}, missing={sorted(missing)}")
    for hunk_id, hunk in ranges.items():
        owners = [x for x in changes + excluded if hunk_id in x.get("hunks", [])]
        for role in ("before", "after"):
            spans = [x[role] for x in owners if isinstance(x.get(role), str)]
            uncovered = [line for line in hunk[f"{'removed' if role == 'before' else 'added'}_lines"] if line.strip() and not any(line in span for span in spans)]
            if uncovered:
                fail(f"{hunk_id} has unaccounted {role} lines: {uncovered}")
    return {"hunks": len(known), "changes": len(changes), "excluded": len(exclusions)}


def tex_escape(value: str) -> str:
    table = {"\\": r"\textbackslash{}", "{": r"\{", "}": r"\}", "$": r"\$", "&": r"\&",
             "#": r"\#", "%": r"\%", "_": r"\_", "^": r"\textasciicircum{}", "~": r"\textasciitilde{}"}
    return "".join(table.get(char, char) for char in value).replace("\n", "\\par\n")


def render(args: argparse.Namespace) -> None:
    spec, coverage = load_json(Path(args.spec)), load_json(Path(args.coverage))
    before, after = read_utf8(Path(args.before)), read_utf8(Path(args.after))
    summary = validate(spec, coverage, before, after)
    body, section = [], None
    for item in spec["changes"]:
        if item["section"] != section:
            section = item["section"]
            body.append(r"\section*{" + tex_escape(section) + "}")
        old = item.get("before") or "[No corresponding passage in the before snapshot.]"
        new = item.get("after") or "[No corresponding passage in the after snapshot.]"
        body.extend([
            r"\subsection*{[ps" + str(item["ps"]) + "]}",
            r"{\color{BeforeGray}\textbf{[before]} " + tex_escape(old) + r"}\par",
            r"{\color{AfterRed}\textbf{[after]} " + tex_escape(new) + r"}\par",
            r"{\color{CommentBlue}\textbf{[ps" + str(item["ps"]) + "] comment} " + tex_escape(item["comment"]) + r"}\par",
        ])
    excluded = [
        r"\item \texttt{" + tex_escape(", ".join(item["hunks"])) + "}: "
        + tex_escape(item["reason"] + " -- " + item["note"])
        for item in spec.get("excluded_hunks", [])
    ] or [r"\item None."]
    tex = r"""\documentclass[11pt]{article}
\usepackage[margin=25mm]{geometry}
\usepackage[T1]{fontenc}\usepackage[utf8]{inputenc}
\usepackage{xcolor,hyperref}
\newif\ifCJKavailable
\IfFileExists{CJKutf8.sty}{\CJKavailabletrue\usepackage{CJKutf8}}{\CJKavailablefalse}
\definecolor{BeforeGray}{RGB}{112,112,112}
\definecolor{AfterRed}{RGB}{190,0,0}
\definecolor{CommentBlue}{RGB}{0,92,170}
\setlength{\parindent}{0pt}\setlength{\parskip}{0.6em}\emergencystretch=2em
\begin{document}\ifCJKavailable\begin{CJK*}{UTF8}{gbsn}\fi
\begin{center}\LARGE """ + tex_escape(spec.get("title", "Semantic version handoff")) + r"""\end{center}
\textbf{[before]} """ + tex_escape(coverage["before"]["label"] + " — " + coverage["before"]["digest"]) + r"""\par
\textbf{[after]} """ + tex_escape(coverage["after"]["label"] + " — " + coverage["after"]["digest"]) + r"""\par
Every non-empty changed line is classified. Gray and red are source-verbatim projections; blue is the semantic handoff comment.
""" + "\n".join(body) + r"""
\section*{Non-substantive hunk classifications}
\begin{itemize}
""" + "\n".join(excluded) + r"""
\end{itemize}
\ifCJKavailable\end{CJK*}\fi\end{document}
"""
    output = Path(args.output_tex).resolve()
    if output in {Path(args.before).resolve(), Path(args.after).resolve(), Path(args.spec).resolve(), Path(args.coverage).resolve()} or (args.compile and output.with_suffix(".pdf") in {Path(args.before).resolve(), Path(args.after).resolve(), Path(args.spec).resolve(), Path(args.coverage).resolve()}):
        fail("derived TeX path must not alias an input or control file")
    write(output, tex, args.force)
    if args.compile:
        if output.with_suffix(".pdf").exists() and not args.force:
            fail(f"refusing to overwrite {output.with_suffix('.pdf')}; pass --force for a derived artifact")
        engine = shutil.which(args.engine)
        if not engine:
            fail(f"{args.engine} is unavailable; TeX was created but PDF was not compiled")
        with tempfile.TemporaryDirectory(prefix="diff2ps-build-") as build:
            for _ in range(3):
                result = subprocess.run([engine, "-interaction=nonstopmode", "-halt-on-error",
                                         f"-output-directory={build}", str(output)], capture_output=True)
                if result.returncode:
                    fail(result.stdout.decode("utf-8", "replace")[-4000:])
            shutil.copy2(Path(build) / f"{output.stem}.pdf", output.with_suffix(".pdf"))
    print(json.dumps(summary | {"tex": str(output), "pdf": str(output.with_suffix('.pdf')) if args.compile else None}, indent=2))


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    commands = root.add_subparsers(required=True)
    snap = commands.add_parser("snapshot")
    snap.add_argument("--repo", required=True); snap.add_argument("--before-ref", required=True)
    snap.add_argument("--after-ref", required=True); snap.add_argument("--path", required=True)
    snap.add_argument("--output-dir", required=True); snap.add_argument("--force", action="store_true")
    snap.set_defaults(run=snapshot)
    prep = commands.add_parser("prepare")
    prep.add_argument("--before", required=True); prep.add_argument("--after", required=True)
    prep.add_argument("--before-label", default="before"); prep.add_argument("--after-label", default="after")
    prep.add_argument("--output-dir", required=True); prep.add_argument("--context", type=int, default=3)
    prep.add_argument("--force", action="store_true"); prep.set_defaults(run=prepare)
    out = commands.add_parser("render")
    for name in ("spec", "coverage", "before", "after", "output-tex"):
        out.add_argument(f"--{name}", required=True)
    out.add_argument("--compile", action="store_true"); out.add_argument("--engine", default="pdflatex")
    out.add_argument("--force", action="store_true")
    out.set_defaults(run=render)
    return root


if __name__ == "__main__":
    options = parser().parse_args()
    options.run(options)
