# Interactive Revision and TUI Output

Use this workflow when the user wants to inspect proposed manuscript changes
before they are applied, or when technical reasoning must remain legible in a
terminal-style interface.

## Preview before editing

Treat the first phase as read-only. Present a stable legend:

- **KEEP / green:** current text remains unchanged;
- **CHANGE / red:** this exact span is proposed for revision or removal;
- **DECIDE / amber:** evidence or author intent is unresolved.

Use actual color only when the interface supports it. Otherwise use accessible
labels such as `🟩 KEEP`, `🟥 CHANGE`, and `🟨 DECIDE`; never make meaning depend
on color alone. This preview legend is intentional and need not imitate a Git
diff.

State the source path and snapshot or hash once before the item list. For each
proposed item, show:

1. a stable item number and source location;
2. the current span and proposed replacement;
3. one highlighted governing principle from
   [principle-tags.md](principle-tags.md), followed by the concrete scientific
   or reader-facing reason and its responsible evidence or source;
4. the claims, symbols, citations, and qualifiers held fixed;
5. any unresolved evidence or confidence boundary.

Show only enough unchanged context to judge the edit. Do not flood the preview
with whole green sections. Do not modify the source until the user approves the
corresponding items.

In a direct response to the current preview, treat an explicit `OK`, `apply
all`, or equivalent confirmation as approval of all displayed `CHANGE` items.
Apply only named items when approval is partial. Questions, tentative reactions,
or new constraints do not authorize an edit; update the preview instead.

## Apply approved items

1. Reread the latest source and detect concurrent changes.
2. Apply only approved item numbers within the authorized scope.
3. Re-preview any item whose source or meaning changed before application.
4. Inspect the resulting semantic diff and local context.
5. Compile, render, or run targeted checks when the change affects layout,
   equations, citations, references, or generated artifacts.
6. Report applied, skipped, and unresolved items separately.

In the application report, retain the governing tag for each substantive item
or grouped edit. The tag remains author-facing metadata and must not be copied
into the source artifact.

## Display formulas legibly

- Put a consequential equation on its own line instead of embedding it in a
  dense sentence or table cell.
- Use rendered Markdown math when the interface supports it. Otherwise provide
  a compact Unicode or plain-text form with readable subscripts and operators.
- Break long expressions at logical operators and align continuations.
- Define the role of every symbol immediately below or beside the equation.
- Avoid manuscript-only macros, raw spacing commands, and unexplained notation
  in interactive output.
- Do not duplicate every equation in two formats. Add a plain-text companion
  only when rendering is uncertain or the formula is central to the decision.
