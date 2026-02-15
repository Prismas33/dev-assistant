# Integrações

> APIs e serviços externos integrados no projeto.

---

## Serviços Integrados

| Serviço | Propósito | Status |
|---------|-----------|--------|
| [Serviço 1] | [Descrição] | ✅ Ativo |
| [Serviço 2] | [Descrição] | 🚧 Em desenvolvimento |

---

## Template de Integração

### [Nome do Serviço]

**Website:** [URL]  
**Documentação:** [URL da docs]  
**Dashboard:** [URL do dashboard]

#### Credenciais Necessárias
```bash
# .env.local
SERVICE_API_KEY="..."
SERVICE_API_SECRET="..."
SERVICE_WEBHOOK_SECRET="..."
```

#### Configuração
1. Criar conta em [URL]
2. Obter API keys no dashboard
3. Adicionar ao `.env.local`
4. [Outros passos específicos]

#### Uso no Código
```typescript
// src/lib/services/nome-servico.ts
import { ServiceClient } from 'service-sdk'

const client = new ServiceClient({
  apiKey: process.env.SERVICE_API_KEY,
})

export async function exemploFuncao() {
  return client.method()
}
```

#### Endpoints Usados
| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/api/resource` | GET | Lista recursos |
| `/api/resource` | POST | Cria recurso |

#### Webhooks
| Evento | URL Local | Descrição |
|--------|-----------|-----------|
| `event.created` | `/api/webhooks/service` | Quando evento é criado |

#### Limites e Quotas
| Limite | Valor | Plano |
|--------|-------|-------|
| Requests/mês | 10,000 | Free |
| Requests/segundo | 10 | Free |

#### Troubleshooting
- **Erro X:** Solução Y
- **Erro Z:** Solução W

---

## Webhooks

### Configuração Local (Desenvolvimento)
```bash
# Usar ngrok ou similar para expor localhost
ngrok http 3000

# Configurar URL no dashboard do serviço:
# https://xxx.ngrok.io/api/webhooks/service
```

### Verificação de Assinatura
```typescript
// src/app/api/webhooks/service/route.ts
import { headers } from 'next/headers'
import crypto from 'crypto'

export async function POST(request: Request) {
  const body = await request.text()
  const signature = headers().get('x-signature')
  
  const expectedSignature = crypto
    .createHmac('sha256', process.env.WEBHOOK_SECRET!)
    .update(body)
    .digest('hex')
  
  if (signature !== expectedSignature) {
    return new Response('Invalid signature', { status: 401 })
  }
  
  // Processar webhook...
}
```

---

## APIs Internas

### [Nome da API]
```
Base URL: /api/[recurso]
Autenticação: Bearer token / Session
```

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/recurso` | Lista todos |
| GET | `/api/recurso/:id` | Obtém um |
| POST | `/api/recurso` | Cria novo |
| PUT | `/api/recurso/:id` | Atualiza |
| DELETE | `/api/recurso/:id` | Remove |

---

## Checklist de Nova Integração

- [ ] Documentar neste ficheiro
- [ ] Adicionar variáveis de ambiente a `.env.example`
- [ ] Criar client/service em `src/lib/services/`
- [ ] Implementar error handling
- [ ] Configurar webhooks (se aplicável)
- [ ] Testar em ambiente local
- [ ] Configurar variáveis em staging/production
