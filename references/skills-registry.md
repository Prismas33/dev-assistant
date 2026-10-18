# Central skills registry

The canonical file on this Windows installation is `C:\Users\ventu\.codex\skills-registry\CODEX_SKILLS_REGISTRY.md`. Its machine-readable manifest and review metadata are alongside it. `E:\utilitarios\CODEX_SKILLS_REGISTRY.md` is a one-way mirror; versioned snapshots, source archives, checksums, and recovery instructions live in `E:\utilitarios\codex-skills-backup`.

## When to consult or reconcile

- At a new project's discovery, or when resuming without a reliable selection, read the canonical catalog and verify the actual stack and project rules. If it is missing or was reconciled more than seven days ago, run `python scripts/skills_registry.py reconcile --if-stale-days 7` from the installed `dev-assistant` folder. If filesystem access prevents the write, use the available skill list and report the registry gap; do not claim reconciliation.
- Reconsider the selected skills after a material phase, stack, architecture, security, interface, or requirements change. Do not load this catalog for every small task.
- For an approved install, update, or removal, run the reviewed command through `scripts/invoke-managed-skill-change.ps1 -Reviewed -Event install|update|remove -Executable <program> -ChangeArguments <arguments>` (choose one event). The wrapper stops on command failure and immediately reconciles the catalog, manifest, backup, and history on success. For a change already performed outside the wrapper, run `python scripts/skills_registry.py reconcile --event install` (or `update` / `remove`). Validate discovery in a fresh Codex session where relevant.
- Periodic reconciliation detects skills installed outside this process. The seven-day freshness check occurs at project onboarding or material reselection; operators may additionally schedule the same command weekly under the owner's Windows account. Do not register a task under a different account or without checking its permissions.

## Evidence and review

The registry records skill files found under the global `.codex/skills` and `.agents/skills` roots, including `.system`, plus repository `.agents/skills` under configured project roots. It separately records installed plugins from `codex plugin list --json`; plugin caches and the current session's exposed skills are different states. Unknown new skills remain `por auditar`. Review their source revision, license, scripts, dependencies, credential access, destructive operations, and compatibility before adding them to the routing shortlist.

The `skills-metadata.json` alongside the catalog holds curated category, trigger, exclusions, dependencies, and audit state. Keep facts there; do not edit the generated inventory table directly. If the Markdown and manifest differ, reconciliation stops rather than overwriting an unexplained edit.

## Installation and recovery boundary

Reconciliation never installs, updates, or removes packages. Download and audit a pinned revision through the appropriate installer only after the user authorizes that change. After the installer succeeds, reconcile immediately. Verify with `python scripts/skills_registry.py verify`.

For recovery, follow `E:\utilitarios\codex-skills-backup\RESTORE.md`. A snapshot needs its Markdown, manifest, and SHA-256 sidecar. Recovery explicitly archives the current C: version first and requires `restore --snapshot-id ... --expected-sha256 ... --apply`; then reconcile the restored catalog against the actual disk. Never copy the E: mirror over C: merely because it exists.

Only Git-tracked files of the four own skill packages are archived; possible credential files or high-confidence secrets block an archive. The `owned-sources/versions.json` manifest records exact commits and ZIP hashes. External skills have version/source metadata for a reviewed reinstallation, not an unverified offline code backup.
