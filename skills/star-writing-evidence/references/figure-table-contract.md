# Figure and Table Contract

Use this contract before creating or materially revising a central visual.
Design the evidence comparison before selecting the layout, color, or style.

## Contents

- [Inferential role](#inferential-role)
- [Source and selection](#source-and-selection)
- [Evidence identity](#evidence-identity)
- [Visual encoding](#visual-encoding)
- [Caption contract](#caption-contract)
- [Figure-to-text boundary](#figure-to-text-boundary)
- [Final QA](#final-qa)

## Inferential Role

```text
Figure or table ID:
Reader question:
Primary inferential role or claim family:
Central claim supported:
Evidence role: primary / mechanism / boundary / diagnostic / illustration / reproducibility
Why prose alone is insufficient:
```

For a multi-panel visual, assign each panel a subordinate role and state how the
panels combine. Do not force genuinely different evidence roles into one claim,
and do not combine unrelated claims merely to save space.

## Source and Selection

| Field | Definition |
|---|---|
| Responsible data or derivation | |
| Analysis or plotting program | |
| Evidence identity of each panel | |
| Population, cases, or observations | |
| Selection rule | |
| Representative, diagnostic, or exhaustive | |
| Exclusions | |
| Transformations and preprocessing | |
| Aggregation and uncertainty | |
| Version or hash | |

Do not select a case because it looks favorable without labeling the selection
rule and evidential role. An illustrative example does not become population
evidence through visual prominence.

## Evidence Identity

Label every panel or substantive element as one of:

- raw observation;
- derived measurement;
- model output;
- reconstruction;
- schematic;
- illustration.

Record the source and transformation for evidential panels. Visually
distinguish schematics and illustrations from measured or computed results.
Presentation-only generated artwork must be disclosed and must never
masquerade as an observation, reconstruction, or scientific model output.

## Visual Encoding

| Element | Contract |
|---|---|
| Panel order | |
| Rows and columns | |
| Axes and units | |
| Scale and limits | |
| Color and accessibility | |
| Mark, line, or field encoding | |
| Baseline and proposed comparison | |
| Uncertainty or variability | |
| Annotations and thresholds | |
| Legend and labels | |

Use matched scales when visual magnitude is compared. Explain clipping,
normalization, interpolation, smoothing, log scaling, or omitted ranges.

## Caption Contract

The caption should make recoverable:

1. what is shown;
2. what each panel or encoding means;
3. the compared conditions;
4. the metric, scale, or selection rule needed for interpretation;
5. the bounded observation supported by the visual.

Avoid implementation logs, promotional interpretation, and claims that require
evidence outside the visual.

## Figure-to-Text Boundary

```text
What the visual directly shows:
What the manuscript may infer:
What the visual does not establish:
Where the quantitative result is reported:
Where the source and regeneration path are recorded:
```

## Final QA

- Verify plotted values against the responsible source.
- Verify terminology and numbers against the manuscript.
- Inspect at final publication size.
- Check grayscale and color-vision accessibility when relevant.
- Confirm that labels do not overlap, clip, or depend on hidden context.
- Confirm that the caption and Results text use the same comparison and scope.
