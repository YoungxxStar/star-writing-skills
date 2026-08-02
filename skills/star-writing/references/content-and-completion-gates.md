# Content and Completion Gates

Use these gates for high-stakes drafting, revision, review, or finalization of
papers and their appendices, supplements, figures, tables, rebuttals, review
reports, or release packages.

## Contents

- [Content inclusion gate](#content-inclusion-gate)
- [Confidence gate](#confidence-gate)
- [Manuscript promotion gate](#manuscript-promotion-gate)
- [Sequential completion ledger](#sequential-completion-ledger)
- [Reader-facing boundary](#reader-facing-boundary)
- [Numbers and notation](#numbers-and-notation)
- [Final-artifact validity](#final-artifact-validity)
- [Learn from corrections](#learn-from-corrections-without-overgeneralizing)

## Content inclusion gate

Make every retained unit earn its place. A unit may be a section, paragraph,
sentence, equation, symbol, table, figure, caption, footnote, or attachment.
For each unit, identify at least one necessary role:

- define an object needed later;
- advance a logical step;
- provide evidence for a material claim;
- explain a mechanism or procedure needed for interpretation;
- establish a boundary or assumption whose omission would mislead;
- enable reproduction at the promised level;
- satisfy an explicit artifact or venue obligation.

If no role survives, remove the unit. Otherwise minimize cognitive load without
losing the contract. Correctness, availability, or effort alone earns no place.

## Confidence gate

For every factual or technical detail:

1. identify the responsible source;
2. verify the detail at the precision used;
3. narrow it to the verified boundary when partial support is sufficient;
4. omit it when it is both unverified and nonessential;
5. expose the unresolved dependency when the central argument requires it.

Do not compensate for low confidence with extra explanation. Prefer a short, verified operational description to a detailed but fragile reconstruction.

Apply the gate at sentence and paragraph level. Split clauses with different
support. Classify each claim-bearing sentence with the constitution's claim
status: `established`, `bounded`, `exploratory`, `unsupported`, `contradicted`,
or `unresolved`. Assess a paragraph by its weakest load-bearing sentence. Omit
nonessential exploratory or unsupported detail and stop on a central unresolved
or contradicted dependency. Keep labels in the audit unless readers need the
epistemic boundary; do not invent numerical confidence scores.

## Manuscript promotion gate

Keep exploratory reasoning in the working record until it passes both necessity
and confidence checks:

| Reader necessity | Confidence | Action |
|---|---|---|
| Necessary | Established or bounded | Retain with the required qualifier |
| Necessary | Exploratory, unsupported, contradicted, or unresolved | Investigate, narrow, expose as unresolved, or stop |
| Nonessential | Established or bounded | Compress or omit |
| Nonessential | Exploratory, unsupported, contradicted, or unresolved | Omit |

Do not promote raw brainstorming, thought experiments, adversarial objections,
confidence labels, or discarded alternatives merely because they were useful
during reasoning. Include them only when they become supported content with a
necessary reader-facing role.

## Sequential completion ledger

A full audit must be demonstrably exhaustive rather than described as a
general reread. Traverse the applicable units in document order:

`section -> paragraph -> sentence -> equation -> table -> figure -> caption -> reference`

Record each unit as `checked`, `revised`, `retained with reason`, `unverified`,
or `not applicable`. Search, linting, and global consistency scans complement
this traversal; they do not replace it. After edits, revisit every changed unit
and its dependent uses.

For a long artifact, keep a compact section-level completion summary while
recording exceptions and changed units individually. Do not flood the author
with a sentence-by-sentence ledger unless they request it; retain enough detail
to substantiate the claimed traversal.

## Reader-facing boundary

Keep internal audit records separate from manuscript prose. Record rival
interpretations, non-conclusions, uncertainty, and evidence limits internally.
Move them into reader-facing text only when they are needed to define the
construct, prevent a likely material misreading, or state a limitation relevant
to the claim. Prefer a positive operational definition over defensive lists of
what an object is not.

## Numbers and notation

Before defining an object, decide whether it is needed. For every retained
number or symbol:

- derive or decompose it when its factors aid understanding;
- cite or name its responsible source when it is externally fixed;
- state its role when it is a design or reporting choice;
- replace it with a justified scale or range when exact precision adds no value;
- remove it when it is unexplained and immaterial.

Definition completeness is required only after the content has passed the
inclusion gate. Do not create auxiliary notation solely to make a dispensable
formula look complete.

## Final-artifact validity

Bind every readiness judgment to the exact rendered, exported, packaged, or
released artifact. Any recompilation, regeneration, export, compression,
archive rebuild, or content change invalidates checks that depend on the old
binary. Re-run the affected checks and record the final path, size, hash, and
remaining warnings before declaring completion.

## Learn from corrections without overgeneralizing

Classify recurring author corrections as one of:

- scientific fact;
- project contract;
- venue rule;
- author preference;
- general writing principle;
- execution failure;
- missing skill behavior.

Update universal skill guidance only for the final two categories or for a
demonstrably general principle. Keep project terminology, local punctuation
choices, venue limits, and artifact-specific targets in their proper overlays.
