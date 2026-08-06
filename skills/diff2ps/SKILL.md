---
name: diff2ps
description: Compare two exact document versions or Git revisions and produce a source-verified semantic handoff in TeX and PDF. Use after large, repeated, or multi-version manuscript changes when the author needs an exhaustive endpoint comparison with gray [before] excerpts, red [after] excerpts, and blue sequential [psN] comments explaining substantive changes. Also use for a read-only semantic diff audit. Do not use for an ordinary raw line diff or to revise the source manuscript itself.
---

# Diff2PS

Turn two exact document snapshots into an auditable author handoff. Use textual
diff to establish coverage, semantic reading to decide what changed, and source
reverse checks to keep quoted text distinct from commentary.

## Select the mode

- Use **audit** when the user asks only to compare, inspect, or explain. Return
  the semantic change ledger without writing artifacts.
- Use **draft** when the user asks for a comparison TeX, PDF, redline, or
  handoff package. Write only new derived artifacts at explicit output paths.
- Route requests to change either input document to the responsible STAR
  Writing skill. Diff2PS explains completed change; it does not perform it.

Do not load the
[evolution handoff overlay](../star-writing/references/evolution-policy.md) for
ordinary comparison work. If reusable learning is explicitly requested, finish
the handoff and return only a public-safe task-local signal to STAR HotSkills.

## Bind the two endpoints

Resolve `before` and `after` before interpretation.

- For Git input, resolve both user-supplied branches, tags, or commits to exact
  commit IDs and read the same repository-relative path without checking out or
  changing either revision. Use `scripts/diff2ps.py snapshot` when useful.
- For direct UTF-8 files, record each resolved path and SHA-256 digest.
- For PDF, DOCX, or another binary document, record the binary artifact digest,
  extractor and options, and extracted-text digest. State that source-verbatim
  checks apply to that identified text projection, not to the binary container.
- Stop if either endpoint, document path, text projection, or order is
  ambiguous. Never infer the original version from modification time.

Treat the inputs as read-only. Refuse an output path that aliases an input.
Discover an existing Project Writing Ledger and load only accepted entries
needed to interpret intentional terms, claims, and boundaries under the
[Writing Ledger contract](../star-writing/references/writing-ledger-contract.md).
Do not update project state.

## Establish complete diff coverage

Run a full textual diff before writing comments. For normalized UTF-8 inputs,
use:

```bash
python3 scripts/diff2ps.py prepare \
  --before <before.txt> --after <after.txt> \
  --before-label <before-id> --after-label <after-id> \
  --output-dir <working-directory>
```

This creates `diff.patch` and `coverage.json` with stable `H001`, `H002`, ...
hunk IDs. Traverse every hunk in document order and classify it. Search, word
diff, and section-level summaries may help, but none replaces the complete hunk
ledger. If source includes other files, first resolve whether the comparison
unit is one entry file, its expanded include graph, or a delivered package.
Never claim whole-document coverage for an entry-file-only diff.

## Convert diff into semantic changes

For each hunk, compare objects and propositions rather than surface strings:

- research object, operational definition, terminology, scope, and nonclaims;
- problem, motivation, contribution, novelty, and relation to prior work;
- information availability, method operations, equations, parameters, and
  implementation contract;
- data, study design, comparison, units, metrics, results, uncertainty, and
  interpretation;
- figures, tables, captions, citations, ethics, reproducibility, availability,
  limitations, and conclusion.

Assign every hunk and every non-empty changed line to a substantive change or
an exact before/after non-substantive exclusion. Allowed exclusions are `reflow`, `reorder`,
`style-only`, `formatting`, `metadata`, and `generated`. Paragraph splitting,
line wrapping, relocation, and meaning-preserving polish remain in the coverage
ledger but do not earn a `[psN]` item.

One semantic change may cover several hunks, and a mixed hunk may belong to both
a substantive item and an exact exclusion when their source spans differ. Do not concatenate non-contiguous
sentences and call the result verbatim; use separate items or one exact
contiguous excerpt plus cross-referenced items. Compare endpoint meaning, not
the chronology or presumed intent of intermediate commits unless the user asks
for a history analysis.

## Build the comparison specification

Create one UTF-8 JSON object:

```json
{
  "title": "Semantic version handoff",
  "changes": [
    {
      "ps": 1,
      "section": "Introduction",
      "status": "modified",
      "hunks": ["H001"],
      "before": "exact contiguous before text",
      "after": "exact contiguous after text",
      "comment": "What changed semantically, why it matters, and its boundary."
    }
  ],
  "excluded_hunks": [
    {"hunks": ["H002"], "reason": "reflow", "before": "exact old span", "after": "exact new span", "note": "Meaning preserved."}
  ]
}
```

Use `null` for `before` with `status: added`, and `null` for `after` with
`status: deleted`. Number comments continuously from `ps1` in document order.
Gray `[before]` and red `[after]` contain only exact source text. Blue `[psN]`
contains the author-facing comment. State an observed semantic effect and its
evidence; call it the author's reason only when a responsible record supplies
that intention. Never put a summary into `[before]` or `[after]`.

## Validate and render

Use the helper to enforce endpoint digests, exact-substring fidelity,
added/deleted absence rules, sequential numbering, complete hunk classification,
and non-empty changed-line coverage:

```bash
python3 scripts/diff2ps.py render \
  --spec <comparison.json> --coverage <coverage.json> \
  --before <before.txt> --after <after.txt> \
  --output-tex <comparison.tex> --compile
```

The renderer escapes source excerpts instead of executing document commands.
Compile in a temporary directory, preserve the TeX, and run three passes with
the selected available engine (pdfLaTeX by default). Inspect the final PDF at
the title, early, middle, late, and dense-change pages. Report compilation or
font limitations rather than weakening source fidelity to make the file build.

Apply these gates before handoff:

1. **Identity:** exact endpoint IDs, paths or projections, and hashes recorded.
2. **Coverage:** every diff hunk and non-empty changed line classified; no
   summary-only sampling.
3. **Fidelity:** every non-null `[before]` and `[after]` found verbatim in its
   bound source.
4. **Semantics:** exclusions are genuinely meaning-preserving; each `[psN]`
   explains a substantive difference without inventing intention.
5. **Presentation:** markers remain readable without color, numbering is
   continuous, and TeX/PDF correspond to the same specification.
6. **Preservation:** inputs and unrelated project files remain unchanged.

Use the shared
[principle registry](../star-writing/references/principle-tags.md) in the final
change report, usually **[AUDIT-COVERAGE]**, **[RESPONSIBLE-SOURCE]**, or
**[ARTIFACT-IDENTITY]**. Keep those controlled tags outside the comparison
artifact; `[psN]` is a locator, not a principle tag.

## Deliver the handoff

Lead with artifact paths. Report endpoint identities, hunk count, substantive
`ps` count, excluded-hunk count by reason, unresolved classifications, build
command, PDF pages and hash, and confirmation that inputs were unchanged. Do
not say "all substantive changes" when any hunk, include, projection, or
rendered page remains unchecked.
