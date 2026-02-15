# Regras de Documentação

> Como documentar o projeto de forma consistente e útil.

---

## 1. Estrutura de Documentação

```
doc/
├── MEMORIA.md              # Contexto para IA (OBRIGATÓRIO)
├── componentes/
│   └── README.md           # Catálogo de componentes
├── desenvolvimento/
│   ├── diario.md           # Registo diário de trabalho
│   ├── regras-codigo.md    # Convenções de código
│   ├── regras-documentacao.md  # Este ficheiro
│   ├── regras-layout.md    # Convenções de UI
│   └── regras-seguranca.md # Práticas de segurança
├── design/
│   └── design-system.md    # Cores, tipografia, componentes
├── negocio/
│   ├── mercado.md          # Análise de mercado
│   ├── modelo-negocio.md   # Como o projeto gera valor
│   └── visao-geral.md      # O que é o projeto
├── planeamento/
│   ├── riscos.md           # Riscos identificados
│   └── roadmap.md          # Plano de desenvolvimento
├── produto/
│   ├── features-mvp.md     # Funcionalidades do MVP
│   ├── fluxo-produto.md    # User flows
│   └── kpis.md             # Métricas de sucesso
└── tecnico/
    ├── arquitetura.md      # Stack e decisões técnicas
    ├── integracoes.md      # APIs e serviços externos
    └── variaveis-ambiente.md # Configuração
```

---

## 2. Formato dos Ficheiros

### Headers
```markdown
# Título Principal

> Descrição breve do documento (1-2 linhas)

---

## Secção 1
...
```

### Hierarquia
- `#` - Título do documento (1 por ficheiro)
- `##` - Secções principais
- `###` - Subsecções
- `####` - Detalhes (usar com moderação)

### Listas
```markdown
<!-- Para tarefas/checklists -->
- [ ] Item por fazer
- [x] Item completo

<!-- Para informação -->
- Item simples
- Outro item
  - Sub-item

<!-- Para passos sequenciais -->
1. Primeiro passo
2. Segundo passo
3. Terceiro passo
```

---

## 3. Diário de Desenvolvimento

### Formato do Diário
O ficheiro `diario.md` documenta o progresso diário:

```markdown
# Diário de Desenvolvimento

---

## [DATA] - Título Descritivo

### Objetivos
- O que se pretendia fazer

### Realizado
- [ ] Tarefa 1
- [x] Tarefa 2 completa
- [x] Tarefa 3 completa

### Detalhes Técnicos
Notas sobre implementação, decisões tomadas, problemas resolvidos.

### Próximos Passos
- O que fazer a seguir

---

## [DATA ANTERIOR] - Outro Dia
...
```

### O Que Documentar
- ✅ Funcionalidades implementadas
- ✅ Bugs corrigidos
- ✅ Decisões técnicas importantes
- ✅ Problemas encontrados e soluções
- ✅ Dependências adicionadas
- ✅ Migrações de base de dados
- ❌ Não documentar detalhes triviais

### Quando Atualizar
- No final de cada sessão de trabalho
- Antes de fazer commit significativo
- Quando houver decisões importantes

---

## 4. MEMORIA.md

### Propósito
O ficheiro `MEMORIA.md` serve como contexto para assistentes de IA. Deve conter tudo o que um assistente precisa saber para ajudar no projeto.

### Secções Obrigatórias
1. **Identidade** - Nome, descrição, propósito
2. **Stack Tecnológico** - Linguagens, frameworks, versões
3. **Estrutura** - Pastas e organização do código
4. **Convenções** - Padrões de código e nomenclatura
5. **Base de Dados** - Tabelas e relações principais
6. **APIs** - Endpoints disponíveis
7. **Comandos** - Como correr, testar, deploy

### Manter Atualizado
- Atualizar quando adicionar novas tecnologias
- Atualizar quando criar novas tabelas/APIs
- Atualizar quando mudar estrutura de pastas
- Rever semanalmente para garantir precisão

---

## 5. Documentação de Componentes

### Estrutura
```markdown
# Nome do Componente

> Descrição breve

## Props

| Prop | Tipo | Default | Descrição |
|------|------|---------|-----------|
| `variant` | `'default' \| 'outline'` | `'default'` | Estilo visual |
| `size` | `'sm' \| 'md' \| 'lg'` | `'md'` | Tamanho |

## Uso

\`\`\`tsx
import { Componente } from '@/components/ui/componente'

<Componente variant="outline" size="lg">
  Conteúdo
</Componente>
\`\`\`

## Variantes

### Default
Descrição e quando usar...

### Outline
Descrição e quando usar...

## Acessibilidade
- Notas sobre a11y
- ARIA attributes usados

## Notas
- Considerações especiais
- Limitações conhecidas
```

---

## 6. Documentação de APIs

### Formato
```markdown
# API: Nome do Recurso

## Endpoints

### GET /api/recurso
Lista todos os recursos.

**Query Parameters:**
| Param | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `page` | number | Não | Página (default: 1) |
| `limit` | number | Não | Items por página (default: 10) |

**Response:**
\`\`\`json
{
  "data": [...],
  "total": 100,
  "page": 1
}
\`\`\`

---

### POST /api/recurso
Cria novo recurso.

**Body:**
\`\`\`json
{
  "nome": "string",
  "email": "string"
}
\`\`\`

**Response:** `201 Created`
\`\`\`json
{
  "id": "uuid",
  "nome": "string",
  "email": "string",
  "createdAt": "ISO date"
}
\`\`\`

**Erros:**
| Código | Descrição |
|--------|-----------|
| 400 | Validação falhou |
| 401 | Não autenticado |
| 409 | Email já existe |
```

---

## 7. Comentários no Código

### Quando Comentar
```typescript
// ✅ Explicar PORQUÊ, não O QUÊ
// Usamos debounce de 300ms porque a API tem rate limit de 10 req/s
const debouncedSearch = useMemo(
  () => debounce(search, 300),
  []
)

// ✅ Documentar decisões não óbvias
// O Supabase não suporta ILIKE com acentos, por isso normalizamos primeiro
const normalizedQuery = removeAccents(query)

// ❌ Não comentar código óbvio
// Incrementa o contador (ÓBVIO!)
counter++
```

### JSDoc para Funções Públicas
```typescript
/**
 * Calcula o preço final com desconto e IVA.
 * 
 * @param basePrice - Preço base em cêntimos
 * @param discountPercent - Percentagem de desconto (0-100)
 * @param includeVat - Se deve incluir IVA (23%)
 * @returns Preço final em cêntimos
 * 
 * @example
 * calculateFinalPrice(1000, 10, true) // 1107 (10€ - 10% + 23% IVA)
 */
function calculateFinalPrice(
  basePrice: number,
  discountPercent: number,
  includeVat: boolean
): number {
  // ...
}
```

### TODO Comments
```typescript
// TODO: Implementar paginação quando tivermos mais de 100 items
// FIXME: Este workaround pode ser removido após upgrade do React
// HACK: Contorna bug do Safari com flexbox
// NOTE: Este endpoint é chamado frequentemente, considerar cache
```

---

## 8. Commits e Changelog

### Formato de Commits
```
tipo(escopo): descrição curta

Corpo opcional com mais detalhes.

Refs: #123
```

### Tipos de Commit
| Tipo | Descrição |
|------|-----------|
| `feat` | Nova funcionalidade |
| `fix` | Correção de bug |
| `docs` | Documentação |
| `style` | Formatação (não afeta código) |
| `refactor` | Refatorização |
| `test` | Testes |
| `chore` | Manutenção |

### Exemplos
```
feat(auth): adiciona login com Google

fix(dashboard): corrige gráfico que não carregava em Safari

docs: atualiza README com instruções de setup

refactor(api): extrai lógica de validação para utils
```

---

## 9. Checklist de Documentação

### Novo Projeto
- [ ] MEMORIA.md criado e completo
- [ ] README.md com instruções de setup
- [ ] Estrutura de pastas documentada
- [ ] Variáveis de ambiente documentadas

### Nova Funcionalidade
- [ ] Diário atualizado
- [ ] MEMORIA.md atualizado (se relevante)
- [ ] Componentes documentados
- [ ] APIs documentadas
- [ ] Commit message descritivo

### Revisão Semanal
- [ ] MEMORIA.md ainda preciso?
- [ ] Diário em dia?
- [ ] TODOs resolvidos ou ainda válidos?
- [ ] Documentação de componentes atual?
