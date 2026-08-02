---
name: star-writing-literature
description: Audit or revise literature positioning, Related Work, novelty claims, and citation support in research papers across fields. Use to identify or compare closest work, verify whether citations support exact propositions, distinguish sources by problem, information, assumptions, outputs, mechanisms, and evidence, organize a synthesis, or test a contribution against prior art. Default to analysis unless revision is explicitly requested.
---

# STAR Writing: Literature Positioning and Citation Audit

Do not load the
[shared evolution policy](../star-writing/references/evolution-policy.md) for
ordinary paper work. If the user explicitly asks the plugin to learn, or this
task exposes a material, plausibly reusable success, correction, or gap, keep
this skill responsible for the paper, retain only a task-local candidate, and route plugin
maintenance to `star-writing-evolve`. Feedback alone cannot authorize a source
change.

## Set the Mode

- Use **audit** by default. Inspect sources and report findings without modifying the manuscript or bibliography.
- Use **revise** only when the user explicitly requests rewritten prose or file changes.
- Separate a missing source, an inaccurate citation, a weak comparison, and an unsupported novelty claim. They require different remedies.
- Read primary sources deeply enough to verify the proposition at issue. Do not rely on another paper's summary when the distinction affects novelty or technical accuracy.

## Decompose the Manuscript Claims

Split the target passage into atomic propositions. A sentence may contain several independently citable claims about:

- the problem or setting;
- available information and timing;
- output or objective;
- assumptions;
- mechanism;
- empirical or theoretical evidence;
- limitation or scope.

Audit each proposition separately. Do not let one relevant citation appear to support an entire compound sentence.

## Identify the Closest Work

Search beyond shared keywords. Compare work by:

1. scientific objective and problem formulation;
2. information available at training, inference, observation, intervention, or evaluation;
3. output, decision, estimate, explanation, or guarantee;
4. assumptions and operating regime;
5. core mechanism;
6. evidence and evaluation contract;
7. established scope and stated limitations.

Use [references/closest-work-audit.md](references/closest-work-audit.md) when novelty is central, several works are easily conflated, a broad literature paragraph needs synthesis, or citation support is disputed.

## Run an Adversarial Novelty Audit

Attempt to disprove the novelty claim before defending it.

- Search alternate terminology and neighboring fields.
- Expand beyond method-name search to field taxonomies, documented failures and
  assumptions, deeper mechanism terms, evaluation or deployment critiques, and
  the evidence that would falsify the proposed motivation.
- Look for the same information contract under a different method name.
- Identify the strongest conceptual predecessor, the strongest practical alternative, and the simplest plausible baseline.
- Ask whether the apparent difference is only notation, scale, data, implementation, or evaluation.
- Check whether prior work already establishes the claimed capability, even if by another mechanism.
- Treat failure to find a source as search status, not proof that no source exists.

State the exact surviving difference. Distinguish novelty of problem, mechanism, interface, evidence, resource, or synthesis; do not convert one type into another.

## Enforce Clause-Level Citation Support

- Place a citation next to the proposition it supports.
- Verify the cited work's actual inputs, outputs, assumptions, and evidence.
- Do not cite a downstream application as proof of the learned mechanism.
- Do not cite a complete pipeline as proof that one component performs every operation.
- Do not combine distinct works into one shared capability unless each supports that characterization.
- Prefer a canonical published version when available; use an original preprint when it is the authoritative or only version.
- Verify authorship, title, year, venue, and persistent identifier when bibliography accuracy is in scope.
- Narrow the prose when the source supports only a narrower statement.

Learn conceptual and rhetorical moves from sources, not distinctive wording.

## Verify terminology

When a term determines the problem, novelty, method, or claimed scope, verify
its established meaning rather than choosing it for rhetorical force. Prefer
field standards, authoritative definitions, canonical literature, and primary
sources. For a new, ambiguous, or cross-field term, also check an applicable
and sufficiently mature Wikipedia page, when useful, for common usage, aliases,
neighboring terms, and source trails; follow the responsible references for
consequential technical claims. Record
the accepted term, definition, source, distinctions, and deprecated aliases in
the current task. Update the
[project terminology ledger](../star-writing/references/terminology-and-symbols.md)
only when the state policy and user authorization permit it.
Do not coin a new label when an established term already matches the same
object and contract.

## Synthesize Rather Than List

Organize Related Work around questions needed to locate the contribution:

`established capability -> differing contracts or assumptions -> remaining boundary -> relevance`

Use this as a reasoning pattern, not a fixed paragraph template. Represent prior work at its strongest defensible scope. A fair comparison makes the surviving novelty more credible.

## Deliver the Result

For an **audit**, return:

1. an atomic claim-to-source table with verdicts: supported, partially supported, unsupported, contradicted, or unresolved;
2. a closest-work comparison across the relevant contracts;
3. the adversarial novelty verdict and strongest counterexample;
4. the exact defensible novelty boundary;
5. citation repairs, missing-source needs, and claims requiring evidence rather than prose.

For a **revision**, perform the audit first, then provide:

1. revised literature or positioning text;
2. clause-level citation placement;
3. a short account of corrected comparisons and narrowed or strengthened
   claims, each substantive change labeled with
   [a highlighted governing principle](../star-writing/references/principle-tags.md)
   and supported by a separately stated source or reason;
4. unresolved source or bibliography issues.

Never invent citation keys, bibliographic facts, paper contents, or claims of priority.
