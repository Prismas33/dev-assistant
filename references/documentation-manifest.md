# Documentation manifest

## Source-of-truth rule

Use one documented canonical structure:

- New structure: `doc/`, with `doc/MEMORIA.md` as the continuity entrypoint.
- Legacy structure: an existing `docs/memory/` convention already used by the repository.

Do not create parallel `doc/` and `docs/` trees containing duplicate specifications unless the repository explicitly defines their different responsibilities. If both exist, document which is canonical and make the other link to it.

## Full new-project structure

```text
doc/
├── MEMORIA.md
├── CHANGELOG.md
├── componentes/
│   └── README.md
├── desenvolvimento/
│   ├── README.md
│   ├── diario.md
│   ├── regras-codigo.md
│   ├── regras-documentacao.md
│   ├── regras-layout.md
│   └── regras-seguranca.md
├── design/
│   └── design-system.md
├── negocio/
│   ├── mercado.md
│   ├── modelo-negocio.md
│   └── visao-geral.md
├── planeamento/
│   ├── riscos.md
│   └── roadmap.md
├── produto/
│   ├── features-mvp.md
│   ├── fluxo-produto.md
│   └── kpis.md
└── tecnico/
    ├── arquitetura.md
    ├── integracoes.md
    └── variaveis-ambiente.md
```

Create every applicable file. Preserve existing files byte-for-byte unless the user asked to update them. Mark unknown decisions as `TBD`; do not fill templates with fabricated prices, metrics, providers, versions, deadlines, or URLs.

## Setup support files

When the user asks for full project setup, also evaluate root `README.md`, `.gitignore`, `.env.example`, package/runtime manifest, formatter/linter/typecheck/tests, CI, and Git initialization.

These are technical setup, not documentation-only work. Do not create them when the user explicitly limits scope to documentation.

## Completion report

Report created and preserved files, decisions, open questions, risks, source conflicts, checks run, unavailable checks, and the next action requiring approval.
