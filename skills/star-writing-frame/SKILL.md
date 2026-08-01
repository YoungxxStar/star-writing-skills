---
name: star-writing-frame
description: Audit or revise a paper's research framing, problem formulation, contribution logic, and argument spine. Use when Codex needs to turn an early idea into a defensible research question; diagnose why an abstract, introduction, method rationale, or whole-paper story feels vague, incremental, or disconnected; separate objective, formulation, information, design, inference, evaluation, and use; or connect assumptions and failures to mechanisms and direct evidence. Default to analysis without editing unless the user explicitly requests revision.
---

# STAR Writing: Research Framing

## Set the Mode

Classify the request before acting.

- Use **audit** by default. Diagnose the framing and report proposed corrections without changing source text or files.
- Use **revise** only when the user explicitly asks to rewrite, edit, or implement changes.
- Preserve locked claims, terminology, and author emphasis. Flag conflicts with evidence instead of silently resolving them.
- Scale the audit to the risk. Inspect the whole argument for a paper-level claim; inspect only the necessary context for a local wording question.

Treat the structures below as diagnostic lenses, not mandatory prose templates.

## Build the Framing Map

Recover the intended research meaning before polishing sentences.

1. State the **objective** independently of the proposed method, including the
   scenario, stakeholder or scientific audience, decision, inquiry, or use, and
   the value of resolving it.
2. Define the **formulation**: object of study, known quantities, unknown quantities, and desired output, decision, explanation, estimate, or proof.
3. Define the **information contract**: what is available, to whom, and at what time.
4. State the **design response**: principle, mechanism, and interface.
5. Define the **inference or use-time contract**: operating conditions, inputs, constraints, and outputs.
6. Define the **evaluation contract**: comparison, estimand, unit of analysis, metric, and scope.
7. State the **use claim**: what the established result enables and what remains hypothetical.

When timing is part of the motivation, state the enabling change: new data,
measurement, theory, computation, evaluation capability, or operating need
that makes the question newly tractable or consequential. Do not invent a
“why now” argument when none is supported.

Test every handoff:

`objective -> formulation -> information -> design -> inference -> evaluation -> use`

Locate the first broken or unsupported handoff. Do not repair a framing fracture with stronger adjectives or smoother transitions.

Read [references/fracture-audit.md](references/fracture-audit.md) for a whole-paper audit, a new-idea diagnosis, or a difficult framing dispute. Skip it for a straightforward local edit.

## Trace the Design Logic

For each central contribution, test this reasoning chain:

`Assumption -> Violation -> Failure -> Missing capability -> Design principle -> Mechanism -> Direct evidence`

- Verify that the stated assumption is actually made in the relevant setting.
- Distinguish an observed failure from a hypothesized explanation.
- Test whether another cause could explain the failure.
- Describe the missing capability without naming the proposed method.
- Show how the mechanism realizes the design principle.
- Attribute an effect only to what the direct comparison isolates.
- Mark an untested link as intended, inferred, or unresolved.

Do not require every link to appear as a separate sentence. Require the scientific logic to survive when reconstructed.

## Challenge the Frame

Ask the strongest adverse questions:

- Does the problem remain meaningful if the proposed method is removed?
- Is the stakeholder, decision, inquiry, or scientific value concrete enough to
  explain why the problem matters?
- If the paper claims a timely opportunity, what verified change makes it
  possible or urgent now?
- Is the formulation recognized under another name?
- Does the design receive information unavailable to alternatives or at use time?
- Does the evaluation measure the stated objective?
- Does the evidence isolate the claimed mechanism?
- Does the use claim exceed the evaluated setting?
- Is a simpler explanation or design still viable?

Invoke `star-writing-literature` when the closest prior formulation is uncertain. Invoke `star-writing-evidence` when attribution, statistical support, or evaluation validity is the primary uncertainty.

## Deliver the Result

For an **audit**, return:

1. a one-sentence current frame;
2. a fracture map identifying the earliest broken handoff;
3. the contribution chain with epistemic status for weak links;
4. the strongest defensible claim and its boundary;
5. prioritized corrections, separating writing fixes from research or evidence gaps.

For a **revision**, first perform the compact audit, then provide:

1. the revised passage or structure;
2. the scientific meaning preserved;
3. the claims narrowed, strengthened, or removed;
4. unresolved evidence needs.

Write decisively at the evidence-supported ceiling. Do not inflate the claim, but do not weaken a directly established result through habitual hedging.
