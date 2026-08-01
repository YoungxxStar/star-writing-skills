# Closest-Work and Citation Audit

Use this reference when literature determines novelty, positioning, or the accuracy of a technical statement.

## Contents

- [Build the comparison set](#build-the-comparison-set)
- [Expand the search](#expand-the-search)
- [Compare contracts](#compare-contracts)
- [Try to falsify novelty](#try-to-falsify-novelty)
- [Audit citation granularity](#audit-citation-granularity)
- [Determine the surviving contribution](#determine-the-surviving-contribution)
- [Revise only after the audit](#revise-only-after-the-audit)

## Build the Comparison Set

Include, when relevant:

1. the closest problem formulation;
2. the closest information and output contract;
3. the closest mechanism;
4. the strongest established practical alternative;
5. the simplest plausible alternative;
6. work from neighboring fields using different terminology.

Do not define closeness by shared method names alone.

## Expand the Search

When direct method-name search is insufficient, search by the question that
could invalidate or deepen the frame:

1. field taxonomies and accepted problem names;
2. documented failures, limitations, and hidden assumptions;
3. mechanism terms such as observability, identifiability, objective mismatch,
   construct validity, or feedback;
4. neighboring disciplines that name the same structure differently;
5. evaluation, deployment, workflow, and system-level evidence;
6. direct tests, controls, counterexamples, and negative results that could
   falsify the motivation.

Use these as search directions, not a mandatory number of rounds. Record
unresolved directions and retrieval limits. A narrow search that finds no match
does not establish priority.

## Compare Contracts

| Work | Objective | Available information and timing | Output | Assumptions | Mechanism | Evidence contract | Scope and boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |

Record what the paper actually establishes, not what later literature commonly attributes to it.

Distinguish:

- a learned mapping from the downstream system that uses it;
- a forward model from search, control, decision, or optimization performed afterward;
- a representation from the task-level capability;
- a design intention from an isolated empirical effect;
- evaluation on a setting from a guarantee over that setting.

## Try to Falsify Novelty

Test these hypotheses:

- The same problem already exists under another name.
- The same inputs and outputs are already connected by another method.
- The contribution is a recombination of known elements rather than a new mechanism.
- The claimed capability comes from added information, data, scale, or computation.
- The novelty is primarily evaluation, interface, synthesis, or application rather than architecture or theory.
- A simpler information-matched alternative could explain the result.

Search to challenge the claim, not merely to collect supporting citations. If the novelty survives, state the exact axis on which it survives.

Avoid categorical priority claims unless the search scope and evidence justify them. “No retrieved source” means unresolved search status, not proof of absence.

## Audit Citation Granularity

Split prose at logical clauses. For each clause, record:

| Proposition | Source | Source location | Verdict | Repair |
| --- | --- | --- | --- | --- |

Use the verdicts:

- **Supported:** the source directly establishes the proposition.
- **Partially supported:** the source supports a narrower or conditional form.
- **Unsupported:** the source is relevant but does not establish the proposition.
- **Contradicted:** the source states or demonstrates something incompatible.
- **Unresolved:** the source or required passage has not been verified.

Common failures:

- one citation is placed after several claims but supports only one;
- a paper's application is cited as its learned output;
- multiple papers with different contracts are summarized as one method class;
- a survey substitutes for an original technical source;
- an abstract is used to infer details available only in methods, appendices, or code;
- a citation supports existence but not priority, superiority, limitation, or causality;
- bibliographic metadata comes from an inconsistent preprint and publication mix.

## Determine the Surviving Contribution

Classify the exact difference as one or more of:

- problem formulation;
- information contract;
- mechanism;
- interface or composition;
- theoretical result;
- evaluation design;
- metric or diagnostic;
- dataset or resource;
- empirical finding;
- application or synthesis.

Then state:

1. what prior work already establishes;
2. what remains different;
3. why that difference matters;
4. what evidence supports the present difference;
5. what stronger novelty claim is not justified.

This result should drive both Related Work and the contribution statement. Do not make prior work artificially weak to make the present work appear strong.

## Revise Only After the Audit

When revision is authorized:

- group sources by the positioning question they answer;
- place citations at the supported clauses;
- narrow inaccurate comparisons;
- distinguish heterogeneous contracts explicitly;
- preserve useful prior capability before stating the remaining boundary;
- use established terminology unless a new term resolves a real distinction.

Do not copy distinctive phrasing or reconstruct the current paper around another source's rhetoric.
