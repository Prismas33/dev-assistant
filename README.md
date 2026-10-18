# Dev Assistant

Codex skill for repository discovery, project continuity, safe documentation setup, modular architecture, and proportional quality gates.

## Highlights

- Reads project memory and current source of truth before acting.
- Separates discovery/diagnosis from authorized implementation.
- Creates the full documentation manifest without overwriting existing files.
- Enforces thin entrypoints and one module per independent responsibility, without arbitrary line limits.
- Selects available specialist skills by verified stack, project phase, risk, and task; reassesses only after material changes.
- Applies baseline security, UI/UX, testing, and documentation standards while reserving full specialist workflows for their actual triggers.
- Routes material security changes through the `security-audit` skill.
- Validates documentation completeness with a bundled script.
- Reconciles the central C: skills registry with installed packages and mirrors verified history to E: when projects begin or the skill inventory changes.

## Installation

```bash
npx skills add Prismas33/dev-assistant
```

## Bundled tools

```powershell
# Create only missing documentation files
.\scripts\init-project.ps1 -ProjectPath "C:\path\to\project"

# Validate required structure
.\scripts\validate-project-docs.ps1 -ProjectPath "C:\path\to\project" -StructureOnly
```

The initializer preserves existing documentation by default. Use `-Overwrite` only with explicit authorization.

## Central skills registry

The canonical catalog is `C:\Users\ventu\.codex\skills-registry\CODEX_SKILLS_REGISTRY.md`; `E:\utilitarios\CODEX_SKILLS_REGISTRY.md` is the verified mirror. Run `python scripts/skills_registry.py reconcile` after approved skill changes or at a new project when the registry is stale. Run `python scripts/skills_registry.py verify` to check the catalog, mirror, and source archives. See `references/skills-registry.md` for scope and recovery.

For a previously audited skill change, `scripts/invoke-managed-skill-change.ps1` runs the exact reviewed command and reconciles on success. The wrapper does not choose or download packages.
