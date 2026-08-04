# Contributing to STAR Writing Skills

Thank you for helping make research-writing agents more rigorous, useful, and
responsive to their users. Documentation, examples, evaluation cases, bug
reports, and focused skill improvements are welcome.

## Start with the scope

- Open an issue before a broad workflow, architecture, or behavioral change.
- A small documentation correction or narrowly scoped regression fix may go
  directly to a pull request.
- Keep contributions language-, field-, project-, paper-type-, and
  venue-neutral unless the change is explicitly a scoped overlay.
- Do not include private manuscripts, unpublished results, credentials,
  personal identifiers, machine-specific paths, or proprietary examples.

The canonical Git checkout is the development source. Do not develop against
an installed plugin cache or generated marketplace copy.

## Make one evidence-grounded change

Explain:

1. the observable problem or missing capability;
2. the current rule or component that owns it;
3. the proposed behavior and its intended scope;
4. evidence that distinguishes the change from the current behavior;
5. the nearest valid behavior that must not regress.

Prefer correcting or simplifying an existing owner over adding duplicate
instructions. A new skill needs a distinct trigger, responsibility, and output
contract. Project conventions and individual preferences do not automatically
belong in the reusable plugin.

Generic skill evolution is managed outside this repository by STAR HotSkills.
Within STAR Writing, the
[handoff overlay](skills/star-writing/references/evolution-policy.md) keeps
paper work, Writing Ledger state, and reusable maintenance requests separate.

## Preserve user control

Keep these actions separate in both implementation and documentation:

- read-only audit;
- manuscript or project-state write;
- canonical plugin-source change;
- commit and tag;
- installation and marketplace update;
- push, publication, and release.

Do not make a stored file, prior approval, silence, or praise authorize a later
state-changing action.

## Validate the contribution

Run from the canonical development checkout:

```bash
python3 scripts/validate_plugin_suite.py
python3 <plugin-creator-root>/scripts/validate_plugin.py .
```

Also run the focused validator and clean-context behavioral cases affected by
the change. A positive case must demonstrate the intended behavior, and the
nearest negative case must protect a valid alternative. Structural validation
alone does not establish writing quality.

Do not change the plugin version or create a release tag unless a maintainer
requests it.

## Pull-request checklist

- [ ] The change has one clear owner and bounded purpose.
- [ ] Responsible evidence or a reproducible failure is identified.
- [ ] Unrelated files and generated caches are excluded.
- [ ] Privacy and machine-path checks pass.
- [ ] Local Markdown links resolve.
- [ ] Relevant positive and negative cases pass.
- [ ] Documentation and metadata match the implemented behavior.
- [ ] Remaining limitations and untested generality axes are disclosed.

## License

By submitting a contribution, you represent that you have the right to submit
it and agree that it will be licensed under the repository's
[MIT License](LICENSE).
