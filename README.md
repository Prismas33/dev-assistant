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
