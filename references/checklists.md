# Proportional quality gates

Apply only gates relevant to the requested work. Never claim evidence from a check that was not run.

## New documentation setup

- [ ] Source documents and repository instructions read.
- [ ] Canonical `doc/` or legacy structure chosen and documented.
- [ ] Every applicable manifest file exists.
- [ ] `MEMORIA.md` contains real context, not fabricated defaults.
- [ ] First diary entry exists.
- [ ] Existing documentation was preserved unless explicitly updated.
- [ ] Local Markdown links resolve.
- [ ] No secrets, PII, or credential-looking examples.
- [ ] Documentation validator passes, or unresolved placeholders are reported.

## Architecture and implementation

- [ ] Entrypoints remain thin.
- [ ] Each independent responsibility has its own component/module.
- [ ] UI is separated from state, data access, validation, and business rules.
- [ ] No artificial layers or trivial fragmentation.
- [ ] Existing behavior outside scope is preserved.
- [ ] Focused lint/typecheck/tests/build completed as applicable.

## Interface change

- [ ] Client identity, existing tokens/components, and real user task checked.
- [ ] Relevant normal, loading, empty, error, and long-content states considered.
- [ ] Changed interface rendered and inspected at applicable viewports and interaction states when technically possible; gaps reported explicitly.
- [ ] Keyboard, focus, semantics, contrast, and touch behavior checked as applicable.
- [ ] `product-ui-design-consistency` loaded when the change establishes or substantially changes the visual system or flow.

## Bug diagnosis and fix

- [ ] Original behavior reproduced or evidenced.
- [ ] Root cause identified before editing.
- [ ] Smallest causal fix applied after authorization.
- [ ] Original scenario and relevant edge cases tested.
- [ ] Regression test added when practical.
- [ ] Documentation updated if the bug changes known behavior or architecture.

## Security-sensitive change

- [ ] Affected trust boundary and impact classified.
- [ ] Full `security-audit` skill loaded when the task changes a security control or requests an audit.
- [ ] Cross-layer contract mapped.
- [ ] Authorization and negative cases tested.
- [ ] Secrets and sensitive data absent from URL, storage, bundle, console, and logs.
- [ ] Backend compatibility precedes dependent frontend.
- [ ] Staging/production validation and rollback are known when deploying.

## Commit or handoff

- [ ] Working tree reviewed; unrelated changes preserved.
- [ ] No debug logs, hardcoded credentials, critical silent TODOs, or temporary files.
- [ ] Actual checks and limitations reported.
- [ ] Memory, diary, ADR, component docs, and changelog considered proportionally.
- [ ] Commit uses Conventional Commits in English when requested.
