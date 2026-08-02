# Writing Ledger Consumer Contract

The project Writing Ledger is the canonical current semantic and expression
contract for downstream writing. It is a logical view, not a fourth state file:

- `paper-contract.md` owns current core-proposition entries and their statuses;
- `terminology-and-symbols.md` owns concepts, terms, names, acronyms, labels,
  aliases, and symbols;
- `decision-log.md` preserves why accepted state changed.

Resolve these paths under `.star-writing/` using
[state-and-paths.md](state-and-paths.md). Bundled files are immutable templates.
`star-writing-ledger` is the controller for interactive decisions and persistent
ledger-entry updates.

## Discover and project

Before substantive work, resolve the project root through the state policy and
check the exact hidden paths `.star-writing/paper-contract.md`,
`.star-writing/terminology-and-symbols.md`, and
`.star-writing/decision-log.md`. Do not rely on a broad file listing that may
omit hidden paths. Only after this exact check may a skill conclude that no
project ledger exists. If it exists, freeze a task-local projection containing
only the active entries relevant to the current task before producing prose:

- local wording or translation: matching term, concept, symbol, and core
  proposition IDs;
- method or equation work: relevant concepts, symbols, availability, and first
  definitions;
- framing or literature work: core propositions, concept distinctions, field
  terms, and deprecated aliases;
- full drafting, review, or submission: the active ledger and applicable
  propagation state.

Do not load historical decision entries or unrelated tables merely to satisfy a
ritual. If no ledger exists, continue a simple or well-specified task from the
supplied context. Do not create state or launch an interview automatically.
Route to `star-writing-ledger` when a missing or conflicting semantic decision
would materially affect the work.

For a legacy project-state row without an ID or decision status, preserve it as
accepted only when it is explicitly marked canonical or locked, remains
unambiguous, and does not conflict with a responsible source or the author's
current intent. Otherwise keep it task-local as unclassified and route the
material choice for reconciliation. Add IDs and statuses only during an
authorized entry update; do not require or perform a bulk migration.
An explicitly filled legacy bounded-thesis or central-claim field may serve as
the accepted proposition for its recorded snapshot when its current intent and
scope are unambiguous. Otherwise treat it as an unclassified framing input.
Assign a stable ID only when that individual entry is first updated under
authorization; ID assignment does not authorize a whole-file schema rewrite.

## Obey current accepted state

- Treat current `accepted` entries as binding expression constraints within
  their stated scope.
- Preserve distinct concept IDs even when surface names are similar.
- Use one canonical term or symbol for one referent within scope; repeat it when
  precision is better than stylistic variation.
- Keep `provisional` content visibly bounded. Do not promote `unresolved` or
  `superseded` entries into authoritative prose.
- Respect locks, first-definition locations, deprecated aliases, language or
  formula renderings, and explicit nonclaims.

Current owner tables use `accepted`, `provisional`, or `unresolved`.
`superseded` belongs to decision history, except for untouched legacy rows.
`stale` is a task-level verification condition that makes an entry nonbinding
until reconciliation; it is not another decision status.

Decision and epistemic status constrain different things. `accepted` fixes the
author's selected project meaning or expression; it does not establish a
scientific proposition. For a claim-bearing accepted entry:

- state `established` content only within its verified scope;
- preserve every qualifier on `bounded` content;
- present `exploratory` content only as a hypothesis, candidate explanation, or
  planned direction;
- do not state `unsupported`, `contradicted`, or `unresolved` content as a
  finding or premise.

When such an entry must be mentioned for an explicit artifact role, expose its
epistemic status rather than laundering it through canonical wording.

The ledger does not prove a scientific fact. Verify consequential content
against the responsible code, data, mathematics, protocol, literature, or live
requirement. If that source or the user's latest deliberate edit conflicts with
the ledger, do not silently restore either version. Preserve the current task
scope, report the conflict, and route reconciliation to `star-writing-ledger`.

## Keep ownership and authority separate

Paper skills may build a task-local projection and propose a ledger candidate.
They must not silently write or reinterpret a canonical ledger entry. An
authorized manuscript edit does not authorize a ledger update, and an
authorized ledger update does not authorize manuscript or artifact propagation.

After an accepted semantic change, update its single current-state owner first.
Propagate only through separately authorized locations and record partial or
pending dependencies. Never use string-wide replacement until each occurrence
has been classified by referent and scope.
