# Arquitetura técnica

**Estado:** TBD

## Stack confirmada

| Camada | Tecnologia/versão | Decisão/evidência |
| --- | --- | --- |
| Frontend/runtime | TBD | TBD |
| Backend/API | TBD | TBD |
| Base de dados | TBD | TBD |
| Auth | TBD | TBD |
| Infraestrutura | TBD | TBD |

Não apresentar defaults ou preferências como decisões.

## Estrutura por responsabilidade

```text
src/
├── app-or-entrypoints/          # Rotas e composição fina
├── components/                  # UI realmente partilhada
├── features/
│   └── <feature>/
│       ├── components/
│       ├── hooks-or-store/
│       ├── actions-or-mutations/
│       ├── queries/
│       ├── services/
│       ├── repositories/
│       ├── schemas/
│       ├── helpers/
│       └── types/
└── infrastructure-or-lib/       # Responsabilidades transversais
```

Adaptar os nomes à stack. Criar apenas camadas que correspondam a responsabilidades reais.

## Regra arquitetural

- Entry files compõem módulos importados e fazem apenas orquestração leve.
- Cada secção visual independente tem componente próprio.
- Estado, dados, validação, negócio e providers ficam separados da apresentação.
- Dependências privilegiadas permanecem no servidor.
- Não existem limites rígidos de linhas; separar por responsabilidade e testabilidade.

## Fronteiras e fluxos

Documentar clientes, servidor, dados, providers, trust boundaries, dados públicos/privados e fluxos principais.

## Ambientes e operação

Documentar development, staging, production, migrations, observabilidade, backups, rollback e comandos verificados. Manter desconhecidos como `TBD`.

## Decisões

Registar decisões duradouras em ADRs quando o projeto usar esse padrão.
