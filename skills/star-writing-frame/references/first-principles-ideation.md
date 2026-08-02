# First-Principles Framing and Ideation

Use this workflow for an early idea, several competing stories, an unclear
motivation, or a design whose necessity has not been established. Exploration
creates candidates; it does not turn them into manuscript facts.

## Contents

- [Ground before diverging](#ground-before-diverging)
- [Ask the motivation triad](#ask-the-motivation-triad)
- [Reason from first principles](#reason-from-first-principles)
- [Use disciplined divergence](#use-disciplined-divergence)
- [Run a self-correction check](#run-a-self-correction-check)
- [Converge](#converge)

## Ground before diverging

Start from the strongest material already available:

- current literature syntheses, closest-work notes, and verified sources;
- data, analyses, figures, and negative or anomalous results;
- experiment, implementation, derivation, and decision records.

Separate `verified`, `inferred`, and `open` items. Conduct incremental research
only for a named unresolved decision, such as terminology, closest work, a
mechanistic premise, or a contradictory result. Do not restart a broad search
when the existing record already answers the question.
Check the date, scope, and source coverage of the existing synthesis; treat a
stale or materially incomplete record as an unresolved input.

Scan the applicable handoffs:

`real objective -> formulation -> available information -> representation -> procedure or optimization -> evaluation -> use`

Look for a lost variable, hidden assumption, false equivalence, structural
mismatch, or proxy that changes meaning between adjacent stages.

## Ask the motivation triad

### What?

State the phenomenon, decision, object, or capability independently of the
proposed method. Specify the available information, desired output, operating
conditions, and scope.

### Why?

State the consequence of leaving the question unresolved and the obstacle that
prevents the current practice from resolving it. Replace broad importance with
a concrete scientific, explanatory, decision, or use consequence.

### Why this?

Derive the required design properties from the obstacle, then test whether the
proposed principle supplies them. Compare against a simpler change, a known
alternative, and a change in information or resources. If several approaches
satisfy the requirement, describe the proposal as one justified route; do not
claim that it is the only route without identifying evidence.

The motivation is the story spine:

`what matters -> why it remains unresolved -> what capability is required -> why the design follows -> what evidence closes the argument`

## Reason from first principles

1. Remove the proposed names and implementation labels.
2. State the invariant facts, constraints, information, and desired outcome.
3. Derive necessary capabilities without assuming the current solution.
4. Generate alternative formulations, explanations, and design principles.
5. Reintroduce the proposed design and identify which requirements it meets.
6. Separate necessary principles from convenient implementation choices.

## Use disciplined divergence

Brainstorm beyond the preferred account, but label every candidate as supported,
inferred, or speculative. Useful thought experiments include:

- remove the proposed component or information;
- hold the observed state fixed while changing a prescribed choice;
- swap the proposed mechanism for a simpler alternative;
- test a null, limiting, extreme, or counterexample case;
- imagine an oracle and ask which remaining difficulty it removes;
- ask what observation would reverse the preferred explanation.

Use thought experiments to expose assumptions, failure modes, discriminating
tests, and new hypotheses. Do not present them as empirical or theoretical
evidence unless they are subsequently established.

Keep candidate reasoning compact:

| Candidate account | Fracture or assumption | Required capability | Simplest rival | Discriminating evidence | Status |
|---|---|---|---|---|---|

## Run a self-correction check

Ask:

- Which premise is being accepted because the current method already uses it?
- Which conclusion would change if the same evidence favored an alternative?
- What result, source, or counterexample would change the current judgment?
- Is a candidate surviving because it is familiar, easy to write, or already
  implemented rather than because it is best supported?
- Has adverse or inconvenient evidence been preserved?

Record material changes of interpretation in the current task. Update a
persistent decision log only when the state policy and user authorization
permit it.

## Converge

Compare candidates by problem value, consistency with current sources,
distinction from closest work, evidential support, field-appropriate testability
or adjudicability, simplicity, and scope. Use falsifiability where it applies.
Select the strongest bounded account, state why alternatives lost, and list the
evidence that would still change the decision. If a consequential unknown
remains discoverable, return to targeted grounding rather than filling the gap
with prose.
