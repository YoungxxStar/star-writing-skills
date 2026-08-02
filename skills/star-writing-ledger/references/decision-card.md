# Writing Ledger Decision Card

Use one card for one semantic decision. Prefill source-grounded fields and ask
only the question that changes the entry. Do not turn the card into a form the
user must complete.

```text
Entry: <stable ID when already assigned, otherwise temporary referent key> | <proposition / concept / term / symbol>
Current uses: <only the conflicting or representative forms>
Responsible source: <source and snapshot, or unresolved>
Recommended current form: <one bounded proposition, definition, name, or symbol>
Meaning boundary: <scope, qualifier, type, unit, availability, or nonclaim>
Distinguish from: <nearest object that must not be collapsed>
Decision status: <accepted / provisional / unresolved>
Epistemic status: <claim status or not applicable>
Dependencies: <locations that would require a separate propagation action>
Question: <one decision-changing question>
```

Show one bold governing-principle tag before the concrete rationale. Keep the
tag out of project-state and manuscript files.

## Owner selection

| Entry | Stable ID | Current-state owner |
|---|---|---|
| Core question, bounded thesis, contribution, or nonclaim | `P-###` | `paper-contract.md` |
| Concept, referent, operational definition, or relation | `C-###` | `terminology-and-symbols.md` |
| Canonical term, name, acronym, label, rendering, or alias | `T-###` | `terminology-and-symbols.md` |
| Symbol or source macro and its semantic contract | `S-###` | `terminology-and-symbols.md` |
| Reason an accepted entry materially changed | affected entry ID | `decision-log.md` |

One decision has one current-state owner. Cross-references may point to an ID;
they must not repeat the definition in another file.

## Inclusion tests

Include an entry only when at least one answer is yes:

- Does it carry a central claim, distinction, definition, or method contract?
- Is it reused across sections, equations, visuals, languages, or artifacts?
- Could changing it alter scientific meaning, claim strength, or information
  availability?
- Has it drifted across authors, sources, versions, or representations?
- Must a deprecated form be recorded to prevent its return?

Otherwise keep the wording local. A ledger that records every word becomes a
new source of ambiguity and context cost.

## Identity tests

Before merging or renaming, compare:

- referent and operational definition;
- input, output, and information contract;
- type, shape, domain, index set, and unit;
- observation, prescription, derivation, latent status, or availability;
- scope, language, prose or formula role, and first definition.

Surface similarity does not establish identity. Local dummy indices may reuse a
glyph when their scope is unambiguous; two global objects may not share one
symbol merely because the manuscript currently does so.

## Acceptance tests

Before setting a task-local decision to `accepted`, confirm:

- the exact candidate was shown and accepted under the stated persistence mode,
  or an existing accepted ledger entry or explicit current author lock already
  records the same decision unchanged;
- its factual content is supported or carries the correct epistemic boundary;
- neighboring concepts remain distinguishable;

Before persistent recording, additionally confirm:

- the project root, single owner file, and persistence scope are explicit;
- the owner was reread against the inspected snapshot;
- an existing stable ID is reused, or a new ID one greater than the namespace's
  historical maximum is allocated only after checking the current owner and
  relevant decision history;
- concurrent-file state is clear.

If any condition fails, keep the item provisional or unresolved. Prefer an
empty cell with an explicit unresolved status over a plausible invention.
