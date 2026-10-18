---
name: dev-assistant
description: Development workflow and skill coordinator for project discovery, safe setup, modular architecture, documentation, and proportional quality gates. Use when starting or resuming a software project, implementing or fixing code, reviewing a repository, or deciding which available specialist skills and validations apply. In discovery and bug diagnosis, investigate and propose before editing unless implementation is requested.
metadata:
  version: "1.2.1"
---

# Dev Assistant

## Start every task from evidence

1. Inspect the repository structure, status, project instructions, package manifests, entrypoints, and relevant configuration before writing code.
2. Search for and read the current project memory automatically: `doc/MEMORIA.md`, `docs/memory/PROJECT_MEMORY.md`, or `docs/memory/MEMORY_QUICK.md`.
3. Read relevant project rules, ADRs, roadmap, recent diary entries, and the real runtime path for the requested behavior.
4. Do not ask the user to repeat facts already present in the repository.
5. Briefly state the structure and responsibility split to use before implementation.

If sources conflict, identify the conflict. Prefer accepted decisions and current code/runtime evidence over old summaries. Never silently invent missing product, security, legal, pricing, provider, or hosting decisions; record them as `TBD` or request direction when they materially change the result.

## Coordinate available skills

At the start of a new project, or when resuming one without a reliable selection, confirm the actual stack from manifests and code, then identify the product goals, users and interfaces, data boundaries, risk, and development phase. Read the canonical registry at `C:\Users\ventu\.codex\skills-registry\CODEX_SKILLS_REGISTRY.md` for installed versions and audit status. If missing or older than seven days, reconcile once using [references/skills-registry.md](references/skills-registry.md); do not recheck on every small task. Inspect skills actually exposed in the session and the repository; use [references/skill-catalog.md](references/skill-catalog.md) for routing. Do not infer a stack from a project name or install or update skills as part of selection.

Select only skills whose trigger and dependencies match the task. Prefer a repository-specific instruction or accepted design decision over generic skill advice, subject to higher-priority safety and user instructions. A specialist skill adds a workflow for its own domain; it does not grant permission for deployments, remote installs, credentials, or destructive actions. If two skills overlap, use the narrower one for the concrete concern and combine them only when both add distinct checks.

For a new project, record a short selection and reason in its existing canonical memory, architecture, or setup document. Include material exclusions or missing dependencies. Do not create a separate skills document just for this. Reassess when the phase, stack, architecture, security boundary, interface, or requirements change materially. For a small task under unchanged conditions, reuse the current selection and inspect only directly relevant skills; do not rescan the whole library or rewrite project documentation.

Apply these baseline standards on every relevant change, even when no specialist skill is loaded:

- **Security:** assess the affected trust boundary, permissions, secrets, sensitive data, and deployment impact in proportion to risk. Load the full `security-audit` workflow for a security request or a material change to a security control or sensitive data path.
- **UI/UX:** when an interface changes, use the client's identity and existing design system, interaction patterns, accessibility, and real content. Avoid generic AI styling. Render and inspect the changed interface in applicable states and viewports when technically possible; report what could not be viewed. Load `product-ui-design-consistency` for a new interface foundation, substantial flow, design-system change, or material visual drift.
- **Tests:** choose focused tests and runtime checks that cover the behavior and meaningful failure cases. State which gates ran and which did not.
- **Documentation:** update the canonical project documentation when decisions, contracts, architecture, operational behavior, or scope materially change; avoid new documents and diary entries for trivial edits.

Following a baseline rule is not the same as running a complete specialist skill. Read only the skill and references needed for the current work. Run approved skill installations, updates, and removals through `scripts/invoke-managed-skill-change.ps1` so the registry and E: backup reconcile after success. Reconcile changes made outside this process periodically before reporting the inventory as current.

## Classify the request

### Discovery or diagnosis

Examples: investigate, review, explain, why did this happen, audit current behavior.

- Inspect and report first.
- Do not edit code, deploy, commit, or mutate external state without an explicit implementation request.
- For a bug report, identify the root cause and propose the smallest fix before asking for confirmation.

### Implementation

Examples: create, implement, add, fix, refactor, prepare, configure, update.

- Treat a clear imperative as authorization for scoped local changes.
- Preserve current behavior outside the requested scope.
- Implement, validate proportionally, and hand off the actual result.
- Do not stop at a plan while safe in-scope implementation remains.

### Documentation or setup

- If the user explicitly asks to prepare/setup the project or create documentation, create the applicable structure without asking again.
- If the user only asks whether setup is advisable, analyze and wait for confirmation.
- Never overwrite existing project documentation automatically.

## Set up a new project safely

When no recognized memory exists, read [references/setup-questions.md](references/setup-questions.md) and [references/documentation-manifest.md](references/documentation-manifest.md).

1. Extract answers already available from source documents and repository context.
2. Ask only for blocking information that cannot be inferred safely.
3. Do not apply technology defaults as accepted decisions; mark unknown stack choices as `TBD`.
4. Create every applicable required template, not a partial subset.
5. Use `scripts/init-project.ps1` to create missing files without overwriting existing ones.
6. Fill `doc/MEMORIA.md`, create the first diary entry, and validate with `scripts/validate-project-docs.ps1`.
7. Report files created, files preserved, gaps, decisions, risks, validation, and the next approval boundary.

The documentation manifest is a completeness contract. A folder listed in the full template must contain its expected files unless the project uses a documented legacy structure or a file is explicitly marked not applicable.

## Enforce modular architecture

Read [references/modular-architecture.md](references/modular-architecture.md) before scaffolding, implementing a feature, or reviewing maintainability.

- Keep `page`, `layout`, `App`, `main`, `index`, and other entry files thin: route concerns, metadata, dependency wiring, and composition only.
- Give each independent responsibility its own component or module.
- Extract a visual section when it has its own identity, behavior, state, tests, or evolution, even if currently used by one page.
- Separate state/hooks, actions/queries, services/use-cases, repositories/data access, schemas/validation, types, helpers, constants, and configuration when those responsibilities exist.
- Keep database access, fetch calls, external SDKs, privileged operations, and business rules out of visual components.
- Organize dashboards and complex products by feature/domain.
- Do not use arbitrary line limits. File size is a review signal; responsibility, coupling, testability, and independent evolution determine extraction.
- Do not create empty layers or split trivial markup merely to increase file count.

Reject an implementation as incomplete when an entrypoint accumulates multiple independent UI sections, complex state, data access, validation, and business rules.

## Apply security gates

Use the security baseline above for all changes. For a security audit, incident, or a material change to authentication, sessions, authorization, credentials, secrets, sensitive-data handling, uploads, payments, webhooks, or security deployment:

1. Load and follow the full `security-audit` skill before editing.
2. Map affected browser/frontend, API/BFF, database, proxy/CDN, native or legacy clients, and deployment/rollback contracts as applicable.
3. Define focused positive and negative tests for the changed control and compatible clients.
4. Sequence backend compatibility before dependent frontend behavior when needed.
5. Distinguish local checks from device, staging, and production proof; do not claim deployment validation from a static check or local build.

Ordinary changes that merely mention a cookie, log line, or API do not automatically require a full audit. Escalate when the trust boundary or security behavior actually changes, or when the user asks for the audit.

## Validate proportionally

Read [references/checklists.md](references/checklists.md) for the applicable gate.

- Run the narrowest useful lint, typecheck, tests, build, migration validation, or runtime check for the change.
- Separate code-review evidence from build, device, staging, and production evidence.
- Never claim a check passed if it was not run or did not complete.
- Inspect existing long-running build/test processes before starting another.
- Preserve unrelated user changes and report blockers honestly.

## Maintain project documentation

- Update documentation directly when the user asked for documentation/setup or when documentation is an explicit deliverable.
- After code implementation, propose or perform diary, memory, component, ADR, and changelog updates according to the user's authorization and project rules.
- Update `MEMORIA.md` for architectural or scope changes, not trivial edits.
- Add diary entries for meaningful work and ADRs for durable technical decisions.
- Keep code and identifiers in English; use Portuguese PT-PT for project documentation and explanatory comments unless project rules say otherwise.
- Use Conventional Commits in English when committing.
- Never place secrets, real PII, or credential-looking examples in documentation.

## Detect maintenance signals

- Mention relevant `TODO` comments.
- Prioritize `FIXME`.
- Flag `HACK` and `TEMP` with their risk and removal condition.
- Treat duplicated data access, repeated business logic, direct SDK calls in UI, and oversized entrypoints as architectural findings.

## Bundled resources

- [references/documentation-manifest.md](references/documentation-manifest.md): required setup structure and source-of-truth rules.
- [references/modular-architecture.md](references/modular-architecture.md): responsibility boundaries and review gate.
- [references/setup-questions.md](references/setup-questions.md): questions for genuinely missing context.
- [references/checklists.md](references/checklists.md): proportional quality gates.
- [references/skill-catalog.md](references/skill-catalog.md): routing rules and activation checks; read at onboarding or material re-selection.
- [references/skills-registry.md](references/skills-registry.md): canonical registry, reconciliation, backup, and recovery procedure.
- `scripts/skills_registry.py`: read-only inventory with atomic catalog/backup updates and guarded restore; use only on onboarding, material changes, or skill management.
- `scripts/invoke-managed-skill-change.ps1`: run one already reviewed skill change, then reconcile automatically; no remote package is selected by the wrapper.
- `templates/`: merge-safe project documentation templates.
- `scripts/init-project.ps1`: create missing template files without overwriting project files.
- `scripts/validate-project-docs.ps1`: verify documentation completeness and placeholders.
