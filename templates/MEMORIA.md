# [NOME_PROJETO] - Memória do Projeto

> Este documento serve como contexto principal para desenvolvimento e assistentes de IA.
> Atualizar sempre que houver mudanças significativas na arquitetura ou scope.

---

## 🎯 Visão Geral

**O que é:** [Descrição em 1-2 frases]

**Problema que resolve:** [Qual dor do utilizador resolve]

**Público-alvo:** [Quem são os utilizadores]

**Proposta de valor:** [Porque é melhor que alternativas]

---

## 🛠️ Stack Técnico

### Frontend
- **Framework:** [Next.js X.X / React X.X / Vue X.X]
- **Styling:** [Tailwind CSS vX / CSS Modules / Styled Components]
- **State:** [Zustand / Redux / Context API]
- **Forms:** [React Hook Form / Formik]

### Backend
- **Runtime:** [Node.js / Deno / Bun]
- **API:** [REST / GraphQL / tRPC]
- **Auth:** [Supabase Auth / NextAuth / Clerk]

### Base de Dados
- **DB:** [PostgreSQL / MySQL / MongoDB]
- **ORM:** [Prisma / Drizzle / TypeORM]
- **Hosting:** [Supabase / PlanetScale / Railway]

### Infraestrutura
- **Hosting:** [Vercel / Railway / AWS]
- **CDN:** [Cloudflare / Vercel Edge]
- **Storage:** [S3 / Cloudflare R2 / Supabase Storage]

---

## 📁 Estrutura do Projeto

```
/
├── src/
│   ├── app/              # Páginas (App Router)
│   ├── components/       # Componentes React
│   │   ├── ui/          # Componentes base (Button, Input, etc.)
│   │   ├── features/    # Componentes de feature
│   │   ├── layout/      # Header, Footer, Sidebar
│   │   └── sections/    # Secções de página
│   ├── lib/             # Utilitários e serviços
│   │   ├── supabase/    # Clients Supabase
│   │   ├── services/    # Lógica de negócio
│   │   └── validations/ # Schemas Zod
│   ├── hooks/           # Custom hooks
│   ├── types/           # TypeScript types
│   └── constants/       # Constantes
├── public/              # Assets estáticos
├── doc/                 # Documentação
└── [db-folder]/         # Migrations (supabase/, prisma/, etc.)
```

---

## 👥 Tipos de Utilizador

| Tipo | Descrição | Permissões |
|------|-----------|------------|
| [Tipo 1] | [Descrição] | [Lista de permissões] |
| [Tipo 2] | [Descrição] | [Lista de permissões] |
| [Admin] | [Descrição] | [Acesso total] |

---

## 🗄️ Modelo de Dados (Principais)

### [Tabela Principal]
```sql
- id: UUID (PK)
- user_id: UUID (FK -> auth.users)
- [campo]: [tipo]
- created_at: timestamp
- updated_at: timestamp
```

### [Outra Tabela]
```sql
- id: UUID (PK)
- [referencia]_id: UUID (FK)
- [campo]: [tipo]
- status: enum
```

---

## 🔐 Autenticação & Autorização

### Fluxo de Auth
1. [Passo 1]
2. [Passo 2]
3. [Passo 3]

### Proteção de Rotas
- **Públicas:** `/`, `/login`, `/registo`
- **Autenticadas:** `/dashboard/*`, `/perfil`
- **Admin:** `/admin/*`

### Row Level Security (RLS)
- [Tabela X]: Users só vêem próprios registos
- [Tabela Y]: [Regra específica]

---

## 📊 APIs Principais

| Endpoint | Método | Descrição | Auth |
|----------|--------|-----------|------|
| `/api/[recurso]` | GET | Listar | ✅ |
| `/api/[recurso]` | POST | Criar | ✅ |
| `/api/[recurso]` | PUT | Atualizar | ✅ |
| `/api/[recurso]` | DELETE | Apagar | ✅ |

---

## 💰 Modelo de Negócio

### Planos
| Plano | Preço | Features |
|-------|-------|----------|
| Free | €0 | [Features básicas] |
| Pro | €X/mês | [Features avançadas] |
| Enterprise | Custom | [Tudo + suporte] |

### Métricas Chave
- [KPI 1]
- [KPI 2]
- [KPI 3]

---

## 🚀 Estado Atual

### Fase
- [ ] Ideação
- [ ] MVP
- [ ] Beta
- [ ] Produção
- [ ] Escala

### Últimas Alterações
- [Data]: [Descrição]
- [Data]: [Descrição]

### Próximos Passos
- [ ] [Tarefa prioritária 1]
- [ ] [Tarefa prioritária 2]
- [ ] [Tarefa prioritária 3]

---

## 🔗 Links Úteis

- **Repo:** [URL]
- **Staging:** [URL]
- **Produção:** [URL]
- **Design:** [Figma URL]
- **DB Dashboard:** [Supabase/outro URL]

---

## 📝 Notas para IA

Ao trabalhar neste projeto:

1. **Linguagem:** Código em inglês, comentários/docs em português PT-PT
2. **Estilo:** [Preferências de código - ver regras-codigo.md]
3. **Commits:** Conventional commits em inglês
4. **Testes:** [Estratégia de testes]

### Contexto Importante
- [Nota específica 1]
- [Nota específica 2]
- [Decisão técnica importante]
