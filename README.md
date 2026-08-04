# STAR Writing Skills

### Toward a research-writing agent that learns with you—under your control.

**Understand first. Decide together. Write from evidence.**

STAR Writing Skills is a Codex plugin for researchers who need more than prose
generation. Give it a manuscript or project path. STAR begins by mapping the
actual paper, its evidence, and its unresolved decisions. It then helps you
converge on the story, preserve accepted propositions and terminology, preview
consequential changes before editing, and carry the same contract through
review and submission preparation.

The vision is a writing agent that becomes a better collaborator over time—not
through hidden memory or silent self-modification, but through preferences you
confirm and project decisions you accept. Reusable skill evolution is handled
by the optional, separately governed STAR HotSkills companion.

**Typical outputs:** Paper Map · motivation and argument audit · Writing Ledger ·
claim–evidence review · method–implementation check · approval-gated revision
preview · submission-readiness audit

STAR is designed for different research fields, languages, paper types, and
publication stages. Scientific claims remain grounded in responsible code,
data, mathematics, literature, and records. Submission requirements remain
bound to current authoritative sources.

## One paper, five controlled moves

1. **Start with a path.** `star-writing-start` reads the complete current
   manuscript and the associated sources needed to understand its load-bearing
   claims. It returns a compact Paper Map and does not edit anything.
2. **Find the defensible story.** Framing, literature, method, and evidence
   workflows help distinguish the real problem, defensible contribution,
   executed method, and supported conclusion before drafting begins.
3. **Settle one consequential decision at a time.** The Writing Ledger lets author
   and agent converge on core propositions, concepts, terms, names, and symbols
   without treating author approval as scientific evidence.
4. **Preview before touching the manuscript.** A conversation-native TUI-style
   preview makes proposed changes and unresolved decisions visible.
5. **Carry accepted decisions forward.** Drafting, polishing, review, and
   submission checks reuse the accepted contract, apply only authorized edits,
   and report what remains unresolved.

```text
Source: main.tex @ <current-snapshot>

🟩 KEEP 01 · Introduction, problem statement
   Current text remains unchanged.

🟥 CHANGE 02 · Results, paragraph 2 · [SUPPORT-GATE]
   Current:  “The method generalizes to unseen conditions.”
   Proposed: “The method improves accuracy in the evaluated held-out regimes.”
   Reason:   The experiment varies regimes, not every condition class.
   Held fixed: reported values, evaluation set, and citation.

🟨 DECIDE 03 · Discussion, mechanism claim
   Evidence does not yet distinguish the proposed mechanism from alternatives.

Author: Apply 02 only.
```

This is a structured conversational preview, not a separate terminal
application. The source is reread before approved items are applied.

## Try it on a paper

Use the router for a guided end-to-end session:

```text
Use $star-writing-skills:star-writing on <project-or-paper-path>.

Begin with read-only onboarding. Bind the canonical manuscript snapshot and
build a compact Paper Map.

Then help me compare defensible story frames and converge on the research
contract, motivation, and argument spine before drafting. When a load-bearing
proposition, concept, term, or symbol is ready, route it through the Writing
Ledger one decision at a time. Keep decisions task-local unless I separately
authorize project-state writes.

Once the frame and evidence are stable, show a numbered
KEEP / CHANGE / DECIDE preview of the proposed manuscript revision, routed
through star-writing-draft where new composition is needed and bound to the
current source snapshot. Do not edit until I approve specific item numbers.
Apply only approved items, run the relevant checks, and report applied,
skipped, and unresolved items separately.

Do not perform Git, plugin evolution, installation, external submission, or
publication actions. Run a read-only submission-readiness audit only if I
request it.
```

For the smallest first step:

```text
Use $star-writing-skills:star-writing-start on <paper-or-project-path>.
Build a compact Paper Map and recommend the next defensible step.
Read-only; do not create project state or edit files.
```

## Install with Codex

Paste the following request into a Codex agent with terminal and plugin
management access:

```text
Install or update STAR Writing Skills from
https://github.com/YoungxxStar/star-writing-skills

Read INSTALL.md in the repository completely before acting. Begin with a
read-only preflight. Resolve the exact source commit, manifest identity and
version, existing marketplace entry, staging destination, and current plugin
state. Show me the planned writes and deletions before requesting approval.

After approval, validate and stage that exact revision through Codex's bundled
plugin-creator workflow, then install it with the official Codex plugin command
through the correct local marketplace. Do not modify the development checkout,
hand-edit marketplace files, directly modify or delete generated caches, use
force, or change unrelated plugins. Do not commit, push, tag, publish, or
release anything.

Report the installed source commit and version, all validation results, and
remind me to start a new Codex thread so the installed snapshot is loaded.
```

The agent-guided, manual, update, rollback, and troubleshooting procedures are
in [INSTALL.md](INSTALL.md).

## Learn and remember

STAR Writing separates three forms of task and project learning from generic
skill evolution:

| Layer | What changes | Persistence |
|---|---|---|
| Task adaptation | The current response follows new evidence and feedback | Current task only |
| Author style profile | Confirmed recurring presentation preferences guide later interactions | Only after an authorized project-local or cross-project profile write |
| Project Writing Ledger | Accepted propositions, concepts, terms, and symbols constrain later project writing | Only after an authorized project-state write |
| Skill evolution | A reusable lesson may change a maintained skill | External to this plugin; use STAR HotSkills with separate evidence and authorization |

The Project Writing Ledger is one logical contract over
`.star-writing/paper-contract.md`,
`.star-writing/terminology-and-symbols.md`, and
`.star-writing/decision-log.md`. It records accepted project meaning and
expression; it does not replace responsible scientific sources.

One local edit never becomes a permanent author preference. A preference must
be confirmed or supported by repeated evidence, and its profile governs
presentation rather than scientific truth.

STAR Writing does not create an evolution pool or modify its own skills. When a
reusable workflow gap is worth investigating, it can produce a minimized,
public-safe handoff. Invoke `hotskills-selfevol star-writing-skills` in STAR
HotSkills to evaluate and, when separately authorized, implement that change.
The Writing Ledger remains project meaning and expression state, never
skill-evolution evidence.

## Skill map

The bundle contains one router and ten focused paper skills.

| Stage | Skill | Responsibility |
|---|---|---|
| Coordinate | `star-writing` | Route paper-wide and multi-stage work |
| Orient | `star-writing-start` | Bind the canonical snapshot, build a Paper Map, and recommend the next route |
| Decide | `star-writing-ledger` | Converge on core propositions, concepts, terms, names, and symbols |
| Frame | `star-writing-frame` | Test the problem, motivation, novelty, and argument spine |
| Ground | `star-writing-literature` | Verify closest work, citations, and positioning |
| Specify | `star-writing-method` | Align information, notation, equations, procedures, and implementation |
| Evidence | `star-writing-evidence` | Audit study design, metrics, results, figures, tables, and claim support |
| Compose | `star-writing-draft` | Draft and restructure from an accepted frame and evidence base |
| Refine | `star-writing-polish` | Improve language without silently changing scientific content |
| Challenge | `star-writing-review` | Run skeptical novelty, validity, mechanism, utility, and consistency reviews |
| Deliver | `star-writing-submit` | Check live venue rules, rendered artifacts, identity, and packages |

Use a focused skill when one responsibility clearly owns the task. Use the
router when the work spans several stages.

## Control model

- `start`, `review`, `inspect`, and `audit` are read-only by default.
- `preview` shows numbered proposals; it does not edit source files.
- A named-file edit authorizes only that writing scope. Project state, Git,
  installation, publication, submission, and external skill evolution remain
  separate.
- Only accepted, source-consistent Ledger entries constrain later writing.
- A substantive recommendation exposes its governing principle, such as
  **[SUPPORT-GATE]**, **[TERM-STABILITY]**, or **[CONTRACT-ALIGNMENT]**; these
  tags are interaction metadata, not manuscript content or evidence.
- Full audits traverse the artifact in document order. Search, compilation,
  and linting are supporting checks rather than substitutes for complete review.
- Submission checks are bound to the named venue, cycle, track, stage, and
  accessible live requirements.
- Final readiness is bound to the exact rendered or packaged artifact. A
  relevant regeneration invalidates dependent checks.

See the [router](skills/star-writing/SKILL.md) for the complete workflow and
mode contract.

## Development and validation

From the canonical development checkout:

```bash
python3 scripts/validate_plugin_suite.py
python3 <plugin-creator-root>/scripts/validate_plugin.py .
```

The suite validator checks plugin structure, local links, portability, routing,
Writing Ledger contracts, and the behavioral specifications in
`evals/cases.json`. These checks do not execute an agent or prove writing
quality. Consequential behavioral changes require matched clean-context tests
before release.

## Contributors and history

- Maintainer: [YoungxxStar](https://github.com/YoungxxStar)
- Contributor: `kingstar`
- Contributions: [CONTRIBUTING.md](CONTRIBUTING.md)
- License: [MIT](LICENSE)
- Development milestones: [CHANGELOG.md](CHANGELOG.md)

## Acknowledgments and inspiration

STAR Writing Skills grew from our manuscript-development practice and was also
informed by several public projects and standards:

- [`nature-writing`](https://github.com/Yuan1z0825/nature-skills/tree/main/skills/nature-writing)
  in [`Yuan1z0825/nature-skills`](https://github.com/Yuan1z0825/nature-skills)
  provided a useful reference for modular, section-aware scientific-writing
  workflows.
- [Hermes Agent](https://github.com/NousResearch/hermes-agent) motivated our
  earlier exploration of reviewable workflow improvement. Generic skill
  evolution now lives in the separate STAR HotSkills project.
- The [Agent Skills specification](https://agentskills.io) informed the
  portable `SKILL.md` package structure.

We thank the maintainers and contributors of these projects. Each project
retains its own authorship and license.

If STAR Writing Skills is useful to you, please consider starring or forking
the repository. Ideas, issue reports, and contributions are welcome—read the
[contribution guide](CONTRIBUTING.md) and help us build it together.
