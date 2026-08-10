# Regras de código

## Linguagem e nomes

- Código e identificadores em inglês.
- Documentação e comentários explicativos em português PT-PT, salvo regra local diferente.
- Usar a convenção idiomática da stack e manter consistência no projeto.
- Preferir tipos explícitos nas fronteiras; evitar tipos que removam segurança sem necessidade.

## Organização

- Seguir [regras-arquitetura-modular.md](regras-arquitetura-modular.md).
- Organizar dashboards e produtos complexos por domínio/feature.
- Manter pages/layouts/entrypoints finos.
- Separar UI, estado, ações/queries, services, repositories, schemas, types, helpers e configuração quando essas responsabilidades existirem.
- Manter fetch, base de dados, SDKs externos e regras de negócio fora de componentes visuais.
- Não criar abstrações antecipadas nem ficheiros sem responsabilidade real.

## Qualidade

- Preservar comportamento fora do scope.
- Funções e componentes devem ter propósito claro e erros tratados na fronteira correta.
- Evitar logs de debug, código morto, credentials hardcoded e TODOs críticos silenciosos.
- Usar performance optimizations apenas perante custo ou evidência concreta.
- Escrever testes proporcionais ao risco: regras, autorização, regressões e estados relevantes.
- Executar lint, typecheck, testes e build aplicáveis antes do handoff.

## Git

- Commits em inglês com Conventional Commits.
- Não misturar alterações não relacionadas.
- Rever o diff e preservar trabalho existente do utilizador.
