---
name: star-writing-frame
description: Audit or revise a research paper's first-principles motivation, problem formulation, contribution logic, and argument spine. Use for early ideation or brainstorming; the what, why, and why-this test; diagnosing vague, incremental, method-first, or disconnected stories; separating objective, information, design, evidence, and use; or connecting failures to mechanisms and direct tests across fields and projects. Default to analysis unless revision is explicitly requested.
---

# STAR Writing: Research Framing

Do not load the
[shared evolution policy](../star-writing/references/evolution-policy.md) for
ordinary paper work. If the user explicitly asks the plugin to learn, or this
task exposes a material, plausibly reusable success, correction, or gap, keep
this skill responsible for the paper, retain only a task-local candidate, and route plugin
maintenance to `star-writing-evolve`. Feedback alone cannot authorize a source
change.

## Set the Mode

Classify the request before acting.

- Use **explore** when the problem, motivation, or candidate explanation is
  unsettled. Generate bounded alternatives and diagnostic thought experiments
  without presenting them as facts or editing the manuscript.
- Use **converge** when several candidate frames exist. Compare them against the
  current literature, data, implementation, and evidence, then select the
  strongest defensible frame or name the decision-changing uncertainty.
- Use **audit** by default. Diagnose the framing and report proposed corrections without changing source text or files.
- Use **revise** only when the user explicitly asks to rewrite, edit, or implement changes.
- Preserve locked claims, terminology, and author emphasis. Flag conflicts with evidence instead of silently resolving them.
- Scale the audit to the risk. Inspect the whole argument for a paper-level claim; inspect only the necessary context for a local wording question.

Treat the structures below as diagnostic lenses, not mandatory prose templates.

Load the existing
[project terminology and symbol ledger](../star-writing/references/terminology-and-symbols.md)
before renaming a research object, problem, capability, or contribution. Treat
a proposed naming change as a scientific decision, not a synonym swap.

For an early idea, several possible stories, or an unclear motivation, read
[references/first-principles-ideation.md](references/first-principles-ideation.md).
Start from the current literature synthesis, data, analyses, and research
records; conduct only the incremental investigation needed to resolve a named
uncertainty.

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

Use the motivation triad as a diagnostic:

- **What?** What exact object, question, or capability is at issue?
- **Why?** Why does resolving it matter, and what obstacle keeps it unresolved?
- **Why this?** Which required property does the proposed principle supply, and
  could a simpler or established alternative supply it?

Treat motivation as the argument's story spine, not as decorative background.
Do not claim that the proposal is the only solution unless the evidence rules
out other viable routes.

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

First state the strongest version of the current frame that the evidence can
support. Then ask the strongest adverse questions:

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

For **exploration**, return:

1. the current evidence basis and unresolved question;
2. the `what / why / why this` motivation triad without the method name;
3. distinct candidate frames or mechanisms with epistemic status;
4. diagnostic thought experiments and the uncertainty each tests;
5. the targeted grounding needed before convergence.

For **convergence**, return:

1. the selected bounded frame, or the unresolved discriminator;
2. why it survives the closest alternatives and current evidence;
3. rejected or deferred alternatives and the concrete reason for each;
4. the evidence that would change the judgment;
5. no manuscript prose unless revision is also authorized.

For an **audit**, return:

1. a one-sentence current frame;
2. the `what / why / why this` motivation triad;
3. a fracture map identifying the earliest broken handoff;
4. the contribution chain with epistemic status for weak links;
5. the strongest defensible claim and its boundary;
6. prioritized corrections, separating writing fixes from research or evidence gaps.

For a **revision**, first perform the compact audit, then provide:

1. the revised passage or structure;
2. one highlighted governing principle per substantive change, using
   [the controlled tags](../star-writing/references/principle-tags.md), followed
   by its concrete evidence and reason;
3. the scientific meaning preserved;
4. the claims narrowed, strengthened, or removed;
5. unresolved evidence needs.

Write decisively at the evidence-supported ceiling. Do not inflate the claim, but do not weaken a directly established result through habitual hedging.
