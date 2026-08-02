---
name: star-writing-ledger
description: Create, audit, and maintain a project Writing Ledger through one-decision-at-a-time collaboration. Use when a research paper needs stable core propositions, concept boundaries, canonical terms, names, acronyms, labels, or symbols across sections, artifacts, languages, or collaborators, or when those records conflict. Do not use it as scientific evidence or for a routine local wording choice.
---

# STAR Writing: Writing Ledger

Build one project-level semantic and expression contract through focused author
decisions. Present one load-bearing decision at a time, let only accepted state
bind downstream writing, and keep every other status visibly nonbinding.

## Set the mode and authority

- Use **audit** to inspect current state, manuscript usage, and source conflicts
  without changing project files.
- Use **converge** to resolve one candidate decision at a time. Keep accepted,
  provisional, and unresolved outcomes in the current task unless persistence is
  authorized.
- Use **revise** only when the user authorizes creation or update of the named
  project-state files. Approval of one displayed entry applies only to that
  entry under the previously stated write boundary.

Calling this skill, asking to discuss, or accepting a recommendation does not
by itself authorize manuscript propagation, Git actions, submission actions,
or plugin maintenance. State at the start whether accepted entries will be
stored immediately, held task-local until a final review, or only previewed.
Keep provisional and unresolved entries task-local unless the user separately
authorizes their nonbinding persistence.

Read the complete
[Writing Ledger contract](../star-writing/references/writing-ledger-contract.md)
and resolve project paths through
[the state and path policy](../star-writing/references/state-and-paths.md).
Use [the decision-card contract](references/decision-card.md) for every
interactive entry. Use
[the highlighted principles](../star-writing/references/principle-tags.md) to
explain substantive decisions without putting tags into the ledger.
Use the claim statuses defined in
[the writing constitution](../star-writing/references/constitution.md) when a
proposition carries an epistemic judgment.

Do not load the
[shared evolution policy](../star-writing/references/evolution-policy.md) for
ordinary ledger work. If the user explicitly asks the plugin to learn from the
workflow, keep this skill responsible for the project ledger and route only the
reusable skill-maintenance question to `star-writing-evolve`.

## Bind the logical ledger

Treat the Writing Ledger as one logical view with three noncompeting owners:

- `.star-writing/paper-contract.md` owns current core propositions, their role,
  scope, epistemic status, and responsible sources;
- `.star-writing/terminology-and-symbols.md` owns concept identities,
  distinctions, canonical terms, names, acronyms, labels, aliases, and symbols;
- `.star-writing/decision-log.md` owns why an accepted state materially changed
  and what the change superseded.

Use the bundled [paper-contract template](../star-writing/references/paper-contract.md),
[concept, terminology, and symbol template](../star-writing/references/terminology-and-symbols.md),
and [decision-log template](../star-writing/references/decision-log.md).
Never create a fourth project file that repeats these facts merely to provide a
unified view. The skill is the unified controller; the files retain single
responsibility.

Use legacy state in place. An unversioned row without an ID or decision status
is accepted only when it is explicitly canonical or locked, unambiguous, and
consistent with responsible sources and current author intent. Otherwise queue
it as an unresolved classification. Add structure only to entries touched by
an authorized decision; do not force a bulk migration.

The ledger is project state, not scientific evidence. Current code, data,
mathematics, primary literature, protocol records, or live requirements remain
responsible for factual verification. When a responsible source contradicts a
ledger entry, treat it as stale and nonbinding in the current task, then
reconcile it. `stale` is a verification condition, not a fifth decision status.
Change the persistent status to `unresolved` only when that entry update is
authorized; do not obey the ledger blindly or silently overwrite it.

## Build the decision queue

Inspect the current manuscript, responsible sources, existing ledger entries,
and concurrent edits. Build a task-local queue containing only items that are
load-bearing, reused across locations, likely to drift, already inconsistent,
or necessary to distinguish related objects. Do not register every ordinary
noun, grammatical variant, local dummy index, or temporary brainstorming label.

Order decisions by dependency:

1. core research object, question, bounded thesis, contribution, and nonclaim;
2. concept or referent identity, operational boundary, and relation to nearby
   concepts;
3. canonical term, formal name, acronym, label, language-specific rendering,
   and deprecated alias;
4. symbol, source macro, type or shape, domain, unit, availability, and scope;
5. first definition and dependent prose, equation, visual, supporting, response,
   or release locations.

Do not ask the user to fill every field. Prefill what responsible sources
establish, expose the uncertainty, and discuss only the decision that changes
meaning or future consistency.

## Resolve one entry at a time

Present exactly one decision card unless the user explicitly requests a batch
or fast mode. Keep formulas legible and ask one focused question. Offer
`accept`, `revise`, `defer`, or `inspect source` as actions without forcing those
literal words. `defer` leaves the entry task-local as `unresolved`; it does not
create a fifth status or authorize persistence.

Interpret approval narrowly:

- `OK` or equivalent accepts only the currently displayed entry when the card
  and user-authorized persistence mode were already explicit;
- `OK, but use Y` treats Y as the revised candidate. Accept it only when it
  remains within the verified meaning and source boundary; otherwise show Y as
  a new unresolved card;
- `continue` continues the current discussion and neither accepts nor advances
  an unresolved entry;
- `apply all` covers only entries already displayed in the named batch;
- silence, praise, or approval of manuscript prose does not update the ledger.

First establish identity, then attach labels and notation. Do not merge two
entries because their strings look similar. Compare operational definition,
input and output contract, domain, type, unit, availability, scope, and role.
Preserve real distinctions and scoped multilingual or prose-versus-formula
renderings.

Do not combine concept identity and canonical naming in one unresolved card.
Use a neutral temporary referent key for the concept card. Select or coin a
term only after the concept boundary is accepted and established field usage
has been checked. Never invent a compromise label merely to reconcile several
unverified aliases. If a term conflict exposes an uncertain concept boundary,
return to the concept card first.

## Separate decision and evidence status

Use current-owner decision status `accepted`, `provisional`, or `unresolved`.
Record `superseded` only in decision history, except for untouched legacy rows.
For claim-bearing propositions, separately use the constitution's epistemic
status `established`, `bounded`, `exploratory`, `unsupported`, `contradicted`,
or `unresolved`. A user can choose a name or approve wording, but approval does
not turn an exploratory scientific claim into an established one.

Responsible sources constrain factual meaning and epistemic status. The author
decision selects the project expression and intended bounded position among
source-consistent alternatives. Do not let either authority impersonate the
other.

Persistence of `provisional` or `unresolved` entries requires explicit
authorization and remains nonbinding. Only `accepted` entries bind later
writing. A legacy superseded row may remain until an authorized entry-level
cleanup; do not force a migration.

Do not invent an operational definition, relationship, symbol role, or source
to complete a table. Keep a low-confidence item provisional or unresolved and
state the decision-changing check. Only accepted current entries constrain
downstream expression. A locked entry requires an explicit author decision to
supersede, but it still yields to verified responsible evidence through a new
reconciliation decision.

## Persist and propagate safely

For each authorized persistent current-owner entry:

1. name its single owner file and reread that file against the inspected
   snapshot;
2. reuse the entry's existing stable ID, or allocate one greater than the
   highest `P-###`, `C-###`, `T-###`, or `S-###` ever assigned in that
   namespace after checking the owner and relevant decision history; never fill
   an ID gap, reserve an ID in task-local work, or reuse a retired ID;
3. update only that authorized entry; update a required cross-reference only
   when its owner is inside the same named write boundary, otherwise report it
   as pending;
4. add a decision-log entry only for a material change to prior accepted state
   and only when that file is inside the stated write boundary; otherwise report
   the history update as pending;
5. report manuscript and artifact dependencies as pending unless propagation is
   separately authorized;
6. after authorized propagation, record the exact checked locations and source
   snapshot only when the propagation ledger's owner file is also authorized;
   otherwise report that record update as pending. Never claim completeness
   beyond the audited scope.

Never use an unbounded global replacement to propagate terminology or symbols.
Resolve each occurrence by referent and scope. If another writer changed the
same owner or entry, stop and reconcile semantically rather than overwrite.

## Route verification without losing control

Keep this skill as the interaction controller while requesting the narrow
expert judgment needed for an entry:

- route problem, thesis, contribution, or story logic to `star-writing-frame`;
- route established field terminology and aliases to `star-writing-literature`;
- route symbol meaning, type, shape, domain, unit, and availability to
  `star-writing-method`;
- route claim status and evidence strength to `star-writing-evidence`;
- route authorized manuscript propagation to `star-writing-draft` or
  meaning-preserving surface propagation to `star-writing-polish`;
- route whole-artifact consistency to `star-writing-review` and delivered
  artifact consistency to `star-writing-submit`.

The expert skill supplies evidence or analysis. This skill returns to the same
decision card and owns the accepted project-state update.

## Deliver the result

For each turn, report:

1. the single decision card and responsible source boundary;
2. the decision status and whether discussion was deferred;
3. the owner file and write state, if persistence was authorized;
4. dependencies changed, pending, or outside scope;
5. the next highest-dependency decision, without presenting its full card until
   the current decision is resolved or deferred.

Label substantive recommendations and applied-change summaries with the most
specific governing principle, usually **[PROBLEM-CONTRACT]**, **[RESPONSIBLE-SOURCE]**,
**[OPERATIONAL-SEMANTICS]**, **[TERM-STABILITY]**, or
**[DEPENDENCY-PROPAGATION]**. The tag explains the rule; it is not evidence.
For an applied ledger update, name the exact owner, entry, snapshot comparison,
and checks performed; do not report only that validation passed.

Stop and request reconciliation when project root or source identity is
ambiguous, responsible sources conflict, the current author edit may represent
new intent, a locked entry would change, the write boundary is absent, or a
concurrent update prevents safe entry-level merging.
