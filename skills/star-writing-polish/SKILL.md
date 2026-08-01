---
name: star-writing-polish
description: Detect and correct artificial, generic, overproduced, or machine-like patterns in scientific and scholarly prose while preserving the author's voice and every scientific invariant. Use when asked to polish, humanize, translate, remove AI-like writing, tighten language, improve flow, or edit manuscript prose in place. Support detect-only, rewritten-output, and in-place edit modes. Do not use for scientific review unless the user explicitly requests prose polishing.
---

# STAR Writing: Polish

Improve the prose without changing the science. Treat artificial-writing signals as contextual diagnostics, not as proof of authorship or a mechanical list of forbidden words.

## Select the mode

- **Detect:** Identify issues and explain their effect. Do not rewrite.
- **Rewrite:** Return a minimally revised version of the supplied passage.
- **Edit:** Modify the named file in place with targeted changes.

Use detect mode when the user asks to review, scan, diagnose, or flag only. Use edit mode only when the user asks to change a file. Otherwise use rewrite mode.

A review request does not authorize polishing. Keep scientific review, structural revision, and prose polishing distinct.

For translation, use rewrite or edit mode and preserve the same invariants.
Translate the scientific relation, not the source language's surface syntax.

## Freeze scientific invariants

Before changing prose, identify and preserve:

- scientific meaning and logical direction;
- claims, qualifiers, modality, negation, and causal strength;
- numbers, units, equations, variables, and aggregation;
- citations and the propositions they support;
- canonical terms, acronyms, labels, and notation;
- comparisons, baselines, conditions, and scope;
- paragraph function and author-approved emphasis.

Do not silently correct a scientific inconsistency through wording. Flag it for evidence or review work. Do not add facts, examples, citations, mechanisms, or stronger implications.

Treat the latest author-edited text as the source of current intent. Do not
restore a deleted term, argument, emphasis, or sentence merely because it
appeared in an older draft or generated answer.

Treat novelty, importance, mechanism, causality, generality, and future utility
as claim-bearing content even when they appear in promotional wording. They are
not automatically disposable filler.

## Resolve instruction conflicts

Check whether the requested tone can coexist with semantic preservation. For
example, “make this restrained” can conflict with preserving an unqualified
claim that a result is transformative.

- Do not claim to satisfy both constraints by merely smoothing the promotional
  sentence.
- In detect mode, identify the conflict.
- In rewrite mode, give the closest meaning-preserving revision and flag the
  phrase that prevents the requested tone. When useful, provide a clearly
  labeled optional version that narrows or removes the claim.
- In edit mode, do not make the meaning-changing alternative without explicit
  authorization.

If the user explicitly authorizes removing fluff, delete purely metadiscursive
or redundant rhetoric. Still report any deleted sentence that asserted novelty,
importance, mechanism, generality, or utility.

## Establish the voice

1. Read enough surrounding text to identify the manuscript's register.
2. Prefer the author's strongest unchanged passages as the voice reference.
3. Preserve deliberate directness, technical repetition, cadence, and field-specific usage.
4. Remove awkwardness only when it impairs clarity, precision, flow, or credibility.
5. Avoid replacing the author's voice with uniformly polished house style.

For repeated collaboration, read the authorized project or user profile. If
none exists, follow
[state-and-paths.md](../star-writing/references/state-and-paths.md), then use
[references/author-style-profile.md](references/author-style-profile.md) as an
immutable template and create a working copy only with authorization. Treat the
working profile as a preference layer, not scientific evidence or universal
writing law.

## Diagnose before editing

Read [references/high-signal-diagnostics.md](references/high-signal-diagnostics.md) for the full diagnostic set.

Prioritize:

1. credibility leaks and unsourced authority;
2. generic scaffolding that substitutes for content;
3. significance or novelty inflation;
4. low information density and repeated restatement;
5. synthetic symmetry, metronomic rhythm, and formulaic paragraph roles;
6. vague transitions or missing argumentative bridges;
7. synonym cycling that destabilizes technical terms;
8. excessive hedging, throat-clearing, and reader-steering;
9. conclusions that promise more than the evidence establishes.

Judge patterns in context. Preserve a word, transition, sentence form, or repeated term when it is accurate and useful. Do not enforce word bans, fixed sentence lengths, punctuation quotas, mandatory first person, or artificial variation.

Separate audit language from manuscript language. Statements about rival
interpretations, numerical floors, non-conclusions, incomparable quantities,
or what a visual does not prove belong in an internal ledger by default. Retain
them in reader-facing prose only when they define the construct, prevent a
likely material misreading, or state a limitation that changes the claim.
Prefer a direct positive definition over defensive `not X`, `rather than Y`,
or reviewer-addressing prose.

## Apply the smallest effective change

1. Fix integrity and meaning-adjacent risks first.
2. Repair the span that causes the problem.
3. Rebuild a paragraph only when sentence-level patches cannot restore its progression.
4. Rebuild a larger passage only when generic scaffolding or low-density repetition controls the structure.
5. Repeat the clearest technical term instead of cycling synonyms.
6. Replace evaluative labels with the fact, mechanism, comparison, or consequence that earns them.
7. Make logical relations explicit without adding decorative transitions.
8. Vary rhythm only where the existing cadence is mechanically uniform.
9. Preserve already strong passages unchanged.

Do not make prose more persuasive by increasing claim strength. Do not trade a necessary qualifier for brevity.
Do not launder an unsupported promotional claim into more fluent prose.

## Apply exact local compression

When the user requests a fixed word reduction or a local shortening:

1. record the exact authorized span and locked neighboring text;
2. count words using one consistent rule before editing;
3. remove empty transitions, repeated subjects, redundant modifiers, and
   already-established context before scientific content;
4. preserve definitions, qualifiers, comparison variables, denominators,
   citation scope, antecedents, and logical bridges;
5. recount and report the exact reduction;
6. inspect the local diff and reject incidental changes;
7. compile or render when the edit may change pagination, equations, references,
   or layout.

Do not treat a request to remove one or several words as authorization to
rewrite the paragraph.

## Verify the revision

Compare the revision against the source sentence by sentence.

- Confirm that every number, citation, symbol, term, comparison, and qualifier is unchanged unless the user explicitly authorized a correction.
- Confirm that no inference became a fact, no association became causation, and no bounded result became a general claim.
- Confirm that paragraph order and connective logic still express the same argument.
- Confirm that the result sounds like the same author with clearer control.
- Inspect the diff after an in-place edit and revert incidental changes.

Stop and report rather than rewrite when the requested polish depends on resolving missing evidence, conflicting facts, ambiguous terminology, or a substantive argument choice.

## Return by mode

### Detect

Return:

- the affected span;
- the diagnostic pattern;
- why it weakens this passage;
- whether to keep, revise, or investigate it.

Separate clear problems from judgment calls.

### Rewrite

Return the revised passage. Add only a compact change summary and any unresolved
claim-bearing phrase that prevented the requested tone. Label any
meaning-changing alternative explicitly.

### Edit

Apply targeted changes, reread the edited context, inspect the diff, and report the touched locations and preserved boundaries. Do not paste the full file unless requested.
