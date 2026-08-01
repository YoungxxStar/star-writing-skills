# High-signal prose diagnostics

Use these patterns as prompts for judgment. Diagnose their function in context before changing them.

## Contents

- [Credibility leaks](#credibility-leaks)
- [Generic scaffolding](#generic-scaffolding)
- [Significance and novelty inflation](#significance-and-novelty-inflation)
- [Treadmill prose](#treadmill-prose)
- [Sentence-to-sentence logic](#sentence-to-sentence-logic)
- [Paragraph-reshuffle immunity](#paragraph-reshuffle-immunity)
- [Synthetic symmetry](#synthetic-symmetry)
- [Formulaic contrast and concession](#formulaic-contrast-and-concession)
- [Hedge and emphasis stacking](#hedge-and-emphasis-stacking)
- [Vague analytic gloss](#vague-analytic-gloss)
- [Synonym cycling](#synonym-cycling)
- [Overpacked sentences](#overpacked-sentences)
- [Rhythm without authorial control](#rhythm-without-authorial-control)
- [Boundary test](#boundary-test)

## Credibility leaks

Flag:

- visible placeholders, assistant markup, or model-limit disclaimers;
- vague authorities such as unnamed experts, studies, or independent tests;
- citations that appear decorative or disconnected from the proposition;
- speculative gap-filling presented as background fact;
- internal run labels or drafting notes left in reader-facing prose.

Remove artifacts. Replace vague authority only with supplied, traceable evidence. Otherwise flag the sentence rather than inventing support.

## Generic scaffolding

Flag openings, transitions, and conclusions that could surround almost any topic:

- broad scene-setting that delays the research question;
- meta-narration about what the section will explore;
- repeated recap of what the reader just read;
- empty summary frames;
- generic future promises.

Cut the frame or replace it with the section's actual proposition.

## Significance and novelty inflation

Flag language that tells the reader a result is important, surprising, transformative, first, general, or robust without showing the comparison that earns the label.

Check especially:

- promotional adjectives attached to abstract nouns;
- self-labeling statements that call an idea clever or counterintuitive;
- invented labels used instead of explaining a mechanism;
- historical or prestigious name-dropping used as borrowed weight;
- claims that nobody has studied or named a problem without literature support.

Preserve the evidence and remove the instruction about how the reader should feel.

Do not assume all promotional language is semantically empty. A statement about
novelty, importance, generality, mechanism, or future utility is a claim even
when expressed as hype. If removing it changes the paper's position, flag the
change or obtain authorization rather than silently deleting it.

## Treadmill prose

Ask what new information each sentence and paragraph contributes. Flag passages that:

- restate the premise in new words;
- repeat the same conclusion after each result;
- use several abstractions where one concrete statement would suffice;
- narrate the writing process instead of advancing the argument;
- could lose a large fraction of their words without losing content.

Lead with the proposition and retain only the reasoning, evidence, and qualification needed to support it.

## Sentence-to-sentence logic

For each adjacent sentence pair, identify the actual relation: definition,
elaboration, evidence, inference, cause, contrast, condition, narrowing, or
consequence. The second sentence should retain a clear anchor from the first
and add a proposition that advances the argument.

Treat connectives as logical claims. `Therefore` requires an inference,
`however` a genuine contrast, `also` a parallel addition, `even though` a
concession, and `rather than` a real alternative. When the prerequisite is
absent, repair the reasoning, order, or missing proposition. Do not disguise
the break by substituting another connective.

## Paragraph-reshuffle immunity

Test whether adjacent paragraphs can be swapped without affecting comprehension. If so:

- identify the missing dependency;
- add the necessary bridge;
- reorder by logic;
- or present genuinely independent items as an explicit set.

Do not add connective words when the missing element is reasoning.

## Synthetic symmetry

Flag repeated structural templates rather than isolated punctuation or vocabulary:

- consecutive sentences with the same length and syntax;
- every paragraph using the same number of sentences;
- repeated rule-of-three groupings;
- parallel contrast formulas used as hooks;
- lists padded to a predetermined number;
- identically shaped topic and synthesis sentences.

Vary structure only enough to reflect differences in thought. Do not manufacture irregularity.

## Formulaic contrast and concession

Inspect patterns such as:

- repeated "not X but Y" pivots;
- vague "although progress has been made" concessions;
- multi-step negation followed by a reveal;
- rhetorical questions that delay a known answer.

State the positive claim directly unless the contrast carries scientific information. Make both sides specific when the concession is necessary.

## Hedge and emphasis stacking

Flag stacked modals, intensifiers, and reader-steering cues that obscure commitment:

- multiple hedges on one prediction;
- repeated signals such as notably, importantly, or surprisingly;
- throat-clearing before a direct statement;
- empty assurances of clarity, significance, or honesty.

Retain uncertainty required by the evidence. Remove only redundant calibration.

## Vague analytic gloss

Flag clauses that announce meaning without providing a mechanism or consequence, including strings of participles that merely call a result symbolic, reflective, enabling, or illustrative.

Replace the gloss with a specific implication supported by the evidence, or cut it.

## Synonym cycling

Flag stylistic substitutions that make one scientific object appear to be several objects. Repeat the canonical term when precision requires it.

Do not replace a technical term merely because it recurs.

## Overpacked sentences

Flag sentences that carry several of the following at once:

- problem;
- mechanism;
- comparison;
- result;
- interpretation;
- limitation.

Split at a real logical boundary. Preserve the relation between the resulting sentences.

## Rhythm without authorial control

Read the passage aloud. Flag cadence that is mechanically uniform, excessively smooth, or dominated by stock transitions.

Adjust rhythm through sentence boundaries and emphasis only after preserving argument structure. Do not introduce fragments, informality, first person, or punctuation quirks that are absent from the author's voice.

## Boundary test

Reject a proposed polish edit when it changes:

- what happened;
- why it happened;
- how certain the statement is;
- the population, regime, or conditions covered;
- the variable isolated by a comparison;
- the relationship between a citation and a claim.

Route such changes to scientific review, evidence verification, or author decision.
