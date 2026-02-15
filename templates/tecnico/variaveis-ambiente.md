# Variáveis de Ambiente

> Configuração de variáveis de ambiente do projeto.

---

## Setup Rápido

1. Copiar `.env.example` para `.env.local`
2. Preencher os valores
3. Reiniciar o servidor de desenvolvimento

```bash
cp .env.example .env.local
```

---

## Variáveis Necessárias

### Base de Dados
```bash
# URL de conexão à base de dados
DATABASE_URL="postgresql://user:password@host:port/database"
```

### Autenticação
```bash
# Secret para JWT/sessões (gerar com: openssl rand -base64 32)
AUTH_SECRET="secret-key-here"

# Provider OAuth (se usado)
GOOGLE_CLIENT_ID=""
GOOGLE_CLIENT_SECRET=""
```

### APIs Externas
```bash
# [Nome do serviço]
SERVICE_API_KEY=""
SERVICE_API_URL=""
```

### Aplicação
```bash
# URL base da aplicação
NEXT_PUBLIC_APP_URL="http://localhost:3000"

# Ambiente
NODE_ENV="development"
```

---

## Variáveis por Ambiente

### Development (.env.local)
```bash
DATABASE_URL="postgresql://localhost:5432/dev_db"
NEXT_PUBLIC_APP_URL="http://localhost:3000"
```

### Staging
```bash
DATABASE_URL="postgresql://staging-host/staging_db"
NEXT_PUBLIC_APP_URL="https://staging.exemplo.com"
```

### Production
```bash
DATABASE_URL="postgresql://prod-host/prod_db"
NEXT_PUBLIC_APP_URL="https://exemplo.com"
```

---

## Convenções

### Prefixo NEXT_PUBLIC_
Variáveis com prefixo `NEXT_PUBLIC_` são expostas ao browser.

```bash
# ✅ Seguro expor ao cliente
NEXT_PUBLIC_API_URL="https://api.exemplo.com"
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY="pk_live_..."

# ❌ NUNCA expor ao cliente (sem prefixo)
DATABASE_URL="..."
STRIPE_SECRET_KEY="sk_live_..."
API_SECRET="..."
```

### Tipos de Variáveis

| Tipo | Exemplo | Exposição |
|------|---------|-----------|
| Secrets | `API_SECRET_KEY` | Server only |
| Credentials | `DATABASE_URL` | Server only |
| Public config | `NEXT_PUBLIC_*` | Client + Server |

---

## Ficheiros de Configuração

### .env.example
Incluir no git com valores de exemplo:
```bash
# Base de dados
DATABASE_URL=

# Autenticação
AUTH_SECRET=

# APIs
SERVICE_API_KEY=
```

### .env.local
**NUNCA incluir no git** - contém valores reais:
```bash
DATABASE_URL="postgresql://..."
AUTH_SECRET="real-secret-here"
```

### .gitignore
```gitignore
# Environment files
.env
.env.local
.env.*.local
```

---

## Validação

### Schema de Validação (Zod)
```typescript
// src/lib/env.ts
import { z } from 'zod'

const envSchema = z.object({
  DATABASE_URL: z.string().url(),
  AUTH_SECRET: z.string().min(32),
  NEXT_PUBLIC_APP_URL: z.string().url(),
})

export const env = envSchema.parse({
  DATABASE_URL: process.env.DATABASE_URL,
  AUTH_SECRET: process.env.AUTH_SECRET,
  NEXT_PUBLIC_APP_URL: process.env.NEXT_PUBLIC_APP_URL,
})
```

### Uso Tipado
```typescript
import { env } from '@/lib/env'

// Tipado e validado
const dbUrl = env.DATABASE_URL
```

---

## Troubleshooting

### Variável não definida
```
Error: Missing environment variable: DATABASE_URL
```
→ Verificar se `.env.local` existe e contém a variável

### Variável não acessível no cliente
```
NEXT_PUBLIC_API_URL is undefined
```
→ Verificar prefixo `NEXT_PUBLIC_`
→ Reiniciar servidor de desenvolvimento

### Variável exposta acidentalmente
Se uma secret foi exposta:
1. Revogar/rodar a key imediatamente
2. Verificar `.gitignore`
3. Remover do histórico git se necessário

---

## Checklist

### Novo Projeto
- [ ] `.env.example` criado
- [ ] `.env.local` no `.gitignore`
- [ ] Schema de validação configurado

### Nova Variável
- [ ] Adicionar a `.env.example`
- [ ] Documentar neste ficheiro
- [ ] Adicionar ao schema de validação
- [ ] Configurar em todos os ambientes
