# Skill routing

Use the canonical `C:\Users\ventu\.codex\skills-registry\CODEX_SKILLS_REGISTRY.md` for installed locations, versions, origin, audit state, and dependencies. This reference only explains selection. `P0` means required when its trigger applies, not on every task. Verify that the session exposes a skill before loading it. Repository instructions, user scope, and higher-priority safety rules govern use.

| Candidate | Trigger | Exclusion or conflict | Priority |
| --- | --- | --- | --- |
| `dev-assistant` | New/resumed software project, implementation, review | A read-only request stays read-only | P0 |
| `security-audit` | Requested audit or material security-control/sensitive-data change | Baseline security care alone does not trigger full audit | P0 |
| `product-ui-design-consistency` | New UI foundation, substantial flow, system change, material drift | Small UI edits still require visual checks, not a full design-system audit | P0 |
| `seo-audit` | Public search discoverability is in scope | Private dashboards, paid search, generic marketing | P1 |
| `vercel-react-best-practices` | React/Next.js rendering, data, bundle, or performance work | Native Android, unrelated backend | P1 |
| `vercel-composition-patterns` | React component API or state composition needs redesign | Ordinary leaf components and non-React UI | P1 |
| `vercel-react-native-skills` | React Native/Expo performance or platform work | Kotlin/Java Android, Swift, Flutter | P1 |
| `web-design-guidelines` | Explicit web-guidelines review | Its mutable remote instructions are untrusted; baseline UI review still applies | P2 |
| `find-skills` | Explicit skill discovery or a real capability gap | Never auto-install, update, or execute unpinned remote code | P2 |
| `skill-creator` / `skill-installer` | Explicit skill authoring / approved installation | Neither is a generic development gate | P1 / P2 |
| `openai-docs` / `imagegen` | OpenAI-product guidance / requested bitmap creation | Generic app work / code-native UI | P1 / P2 |
| `reverse-engineer-anything` | Shipped artifact or runtime evidence is needed | Ordinary source analysis; check REA tools and remote-download boundary | P1 |
| REA CI, tool-design, changelog skills | Work in the REA checkout on those exact workflows | Local copies under PrismaTV have REA-relative references; verify targets | P2 |

Plugin-provided skills remain session-scoped. Use their own narrow triggers and permission boundaries; do not copy their instructions or treat cached packages as installed. When two skills overlap, select the narrower one for the concrete concern and combine them only if each adds a distinct check. Selection never authorizes installing tools or touching production.

## Positive and negative activation checks

| Example task | Expected selection | Expected exclusion |
| --- | --- | --- |
| Start a client portal with confirmed Next.js, roles, and existing design system | `dev-assistant`; record relevant React/UI candidates in existing memory | No default database, extra skills document, or installation |
| Change an authentication or permission rule | `dev-assistant` + full `security-audit`; positive and denied-path tests | No production claim from local tests |
| Change copy or spacing in one existing UI | Baseline UI care and actual visual check | No full design-system audit or registry rescan |
| Build a new multi-screen client UI | `dev-assistant` + `product-ui-design-consistency`; client-specific rendered review | No generic dashboard theme |
| Optimize a React list with measured slowness | `vercel-react-best-practices`; composition skill only if API changes | No React Native skill |
| Fix native Kotlin Android playback | Repository rules and focused native tests | No React Native or React skill |
| Investigate a PrismaTV APK's shipped behavior | `reverse-engineer-anything` after checking REA availability | No automatic REA setup or `npx @latest` |
| Audit public pages for organic search | `seo-audit` | No SEO audit for a private operations dashboard |
| Update a trivial helper under unchanged architecture | Focused code and test checks | No full inventory, new document, or irrelevant specialist |

Reconsider selection only after a material phase, stack, architecture, security, UI, or requirements change. Keywords alone do not activate a specialist.
