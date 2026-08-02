# Highlighted Principles and Reasoning Lenses

Use this vocabulary to make the basis of a substantive research-paper or
writing-workflow recommendation visible. A governing principle states why the
action is needed. A reasoning lens states how the issue was discovered. Neither
replaces evidence or a concrete explanation.

## Contents

- [Display contract](#display-contract)
- [Select the tag](#select-the-tag)
- [Grounding and framing](#grounding-and-framing)
- [Evidence and inference](#evidence-and-inference)
- [Content and exposition](#content-and-exposition)
- [Revision and artifact integrity](#revision-and-artifact-integrity)
- [Reasoning lenses](#reasoning-lenses)
- [Disambiguation rules](#disambiguation-rules)

## Display contract

- Render only the canonical ASCII identifier in bold Markdown, for example
  `**[IDENTIFICATION-CEILING]**`.
- Keep identifiers unchanged across interaction languages, disciplines,
  venues, paper types, and associated artifact types. Write explanations in the
  interaction language.
- Assign one governing principle to each substantive change or coherent change
  group. Add at most one secondary principle or one reasoning lens when it
  materially changes how the proposal should be judged.
- Group repeated mechanical edits. Do not tag punctuation, spelling, formatting,
  or routine propagation item by item.
- State the observed issue, responsible evidence or source, action, and preserved
  boundary separately from the tag.
- Keep tags in previews, audits, decision records, and change summaries. Never
  insert them into the target artifact, including prose, captions, equations,
  references, source comments, or publication and submission metadata.
- A tag is not evidence, a score, or hidden chain-of-thought.

```text
**[GOVERNING-PRINCIPLE]**
Optional lens: **[REASONING-LENS]**
Observed issue:
Evidence or source:
Action and preserved boundary:
```

## Select the tag

1. Identify the first violated invariant that makes the change necessary.
2. Choose the most specific governing principle below, not a broad slogan.
3. Use a reasoning lens only to expose a decision-relevant method of inquiry.
4. If no registered principle fits, give the concrete reason without inventing
   a decorative identifier.

## Grounding and framing

- `PROBLEM-CONTRACT` — define the object, objective or decision, available
  information, constraints, output, and scope independently of a proposed
  solution name.
- `CONTRACT-ALIGNMENT` — keep objective, formulation, information, design,
  inference, evaluation, and use mutually consistent; repair the earliest broken
  handoff first.
- `RESPONSIBLE-SOURCE` — resolve each fact against the current source responsible
  for that kind of fact, not memory, derived prose, or a convenient copy.
- `PROPOSITION-SUPPORT` — split compound claims into independently supportable
  propositions and attach each source only to what it establishes.
- `RELATIONAL-NOVELTY` — state novelty only as the exact difference that survives
  comparison with the closest contract-matched prior work; search absence is not
  proof of nonexistence.
- `SYMMETRIC-JUDGMENT` — apply the same evidential standard to favorable and
  adverse findings and state what evidence would reverse the judgment.
- `CONTEXT-LAYERS` — keep stable principles, project facts, author preferences,
  live external rules, and immutable templates in their proper scopes and
  lifetimes.
- `WORKFLOW-DEPENDENCY` — stabilize upstream contracts and evidence before
  dependent structuring, wording, finalization, or release work.

## Evidence and inference

- `INFORMATION-BOUNDARY` — state when and to whom each quantity or source is
  available; do not disguise target-derived, future, privileged, or
  evaluation-only information as a valid input.
- `RECONSTRUCTABLE-METHOD` — keep the formal or procedural account consistent
  with the executed, documented, proved, or otherwise responsible process,
  including consequential boundary operations.
- `CAPABILITY-STAGE` — claim a capability only to the furthest established stage:
  design permits, configuration enables, procedure executes, evaluation tests,
  or result establishes.
- `INFERENCE-LAYER` — keep observation or source, construct, inference,
  mechanism or explanation, and implication distinct; also separate novelty,
  validity, mechanism, and utility.
- `IDENTIFICATION-CEILING` — keep claim strength below what the design excludes;
  do not attribute a whole-system difference to an unisolated component.
- `COMPARISON-PARITY` — match the information, data, sampling, tuning, resources,
  protocol, and post-processing needed for the comparison, or disclose the
  difference and narrow the interpretation.
- `STATISTICAL-CONTRACT` — make the population, independent and observed units,
  pairing or clustering, denominator, aggregation, weighting, uncertainty,
  selection, and precision recoverable for each empirical quantity.
- `OPERATIONAL-SEMANTICS` — require names, metrics, and labels to match a defined
  object, operation, or validated construct rather than implying an unevaluated
  property.
- `GENERALITY-AXES` — name each varied axis of scope; breadth over one population,
  task, domain, scale, condition, method family, instrument, or budget does not
  establish breadth over another.
- `DECISION-TIMING` — distinguish prespecified, development-time, validation-time,
  and post-outcome choices; do not relabel exploratory selection as confirmatory.
- `REPRODUCTION-LEVEL` — distinguish arithmetic checking, artifact regeneration,
  model or analysis execution, and end-to-end reproduction; never describe one
  level as another.

## Content and exposition

- `SUPPORT-GATE` — assess every claim-bearing unit and each larger unit at its
  weakest load-bearing statement; investigate, narrow, disclose, or omit weak
  content according to its necessity.
- `CONTENT-NECESSITY` — retain a unit only when it performs a necessary
  definitional, inferential, evidential, boundary, reproduction, reader, or
  delivery role; correctness alone does not earn inclusion.
- `INFERENTIAL-ORDER` — order definitions, propositions, evidence, qualifiers,
  visuals, and transitions by reasoning dependency rather than drafting history
  or a universal section template.
- `CORE-COMPLETENESS` — when a primary/supporting split exists, keep the required
  central argument or decision basis in the primary artifact; supporting
  artifacts add depth rather than carrying a hidden premise.
- `TERM-STABILITY` — use one canonical term or symbol per referent within scope,
  while preserving intentional distinctions among related objects.
- `RECOVERABLE-COMPRESSION` — reduce cognitive load without losing the object,
  comparison, evidence, aggregation, qualifier, or relation needed to recover
  the meaning.
- `SEMANTIC-PRESERVATION` — do not change claims, qualifiers, logical direction,
  numbers, notation, citations, or scope during wording, translation,
  presentation, or compression work unless authorized.
- `ARTIFACT-FIT` — adapt organization, conventions, counting units, and delivery
  form to the target language, discipline, audience, paper type, and associated
  publication artifact without weakening the evidential standard.
- `ACCESSIBLE-ENCODING` — do not make essential meaning depend only on color,
  inaccessible rendering, unexplained notation, or one presentation channel.

## Revision and artifact integrity

- `AUTHORIZED-SCOPE` — let the requested mode, approved items, locked content,
  mutation scope, and external-action authority determine what may change.
- `CURRENT-INTENT` — treat the latest author-edited content and deliberate
  emphasis, voice, and deletions as current intent; do not restore an older
  choice by convenience.
- `DEPENDENCY-PROPAGATION` — propagate an authorized change through every
  dependent occurrence inside scope and report dependencies outside scope.
- `ARTIFACT-IDENTITY` — bind findings, previews, and readiness to the exact source
  snapshot, rendered instance, form state, or package; relevant changes
  invalidate dependent checks.
- `AUDIT-COVERAGE` — claim completeness only after traversing every applicable
  unit and layer within the stated boundary; search, lint, compilation, or a
  single representation is supporting evidence, not exhaustive review.
- `LIVE-REQUIREMENTS` — bind compliance to the current governing authority,
  rule-set version or cycle, paper category, publication stage, and first-party sources;
  mark inapplicable branches rather than inventing them.

## Reasoning lenses

Reasoning lenses may explain how a conclusion was reached, but they should not
be the sole rationale for an applied change.

- `CURRENT-EVIDENCE-FIRST` — inspect current literature, data, implementation,
  artifact, and research records before starting broader investigation.
- `FIRST-PRINCIPLES` — remove the proposed solution name and derive the problem
  contract and required capability from the underlying objective and constraints.
- `MOTIVATION-AS-STORY` — use the verified problem, unresolved obstacle, required
  capability, chosen principle, and decisive evidence as the argument spine.
- `DIVERGENT-THINKING` — generate bounded alternatives and diagnostic thought
  experiments, then return only decision-changing uncertainties to grounding.
- `SELF-CORRECTION` — test whether familiarity, implementation convenience, or
  author preference is biasing the decision.
- `ADVERSARIAL-REVIEW` — steelman the contribution, construct the strongest
  evidence-grounded objection and response, then adjudicate symmetrically.
- `CONFIDENCE-GATE` — use the sentence- and paragraph-level support audit that is
  operationalized by `SUPPORT-GATE`.
- `LESS-BUT-CORRECT` — prefer omission of nonessential weak detail, while using
  `CONTENT-NECESSITY`, `SUPPORT-GATE`, and `RECOVERABLE-COMPRESSION` to decide
  what may actually be removed.

## Disambiguation rules

- `RESPONSIBLE-SOURCE` asks which source owns the fact;
  `PROPOSITION-SUPPORT` asks what that source supports.
- `SUPPORT-GATE` asks whether a claim-bearing unit survives;
  `CONTENT-NECESSITY` asks whether a supported unit deserves space.
- `INFORMATION-BOUNDARY` checks availability;
  `COMPARISON-PARITY` checks fairness across alternatives.
- `COMPARISON-PARITY` does not establish attribution;
  `IDENTIFICATION-CEILING` limits attribution after the comparison.
- `RECONSTRUCTABLE-METHOD` checks fidelity of the account;
  `CAPABILITY-STAGE` checks how far demonstrated capability extends.
- `OPERATIONAL-SEMANTICS` checks whether a name is earned;
  `TERM-STABILITY` checks consistent use of the accepted name.
- `SEMANTIC-PRESERVATION` protects meaning during an edit;
  `CURRENT-INTENT` protects the author's latest deliberate choice.
- `DEPENDENCY-PROPAGATION` follows an authorized semantic change;
  it never overrides `AUTHORIZED-SCOPE`.
- `ARTIFACT-IDENTITY` proves which instance was checked;
  `AUDIT-COVERAGE` proves what applicable content or representation was checked.
