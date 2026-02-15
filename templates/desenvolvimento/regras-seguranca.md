# Regras de Segurança

> Práticas de segurança obrigatórias para proteger dados e utilizadores.

---

## 1. Autenticação

### Passwords
- [ ] Mínimo 8 caracteres
- [ ] Hash com bcrypt/argon2 (nunca plain text)
- [ ] Rate limiting em login (5 tentativas/15 min)
- [ ] Bloquear conta após N tentativas falhadas

```typescript
// ✅ Validação de password
const passwordSchema = z.string()
  .min(8, 'Mínimo 8 caracteres')
  .regex(/[A-Z]/, 'Pelo menos uma maiúscula')
  .regex(/[0-9]/, 'Pelo menos um número')
```

### Sessões
- [ ] Tokens JWT com expiração curta (15min - 1h)
- [ ] Refresh tokens com expiração longa (7-30 dias)
- [ ] Invalidar sessões em logout
- [ ] Regenerar session ID após login

### Multi-Factor Authentication (MFA)
- [ ] Oferecer 2FA para contas sensíveis
- [ ] TOTP ou SMS como segundo fator
- [ ] Backup codes para recuperação

---

## 2. Autorização

### Row Level Security (RLS)
```sql
-- Utilizadores só vêem os seus próprios dados
CREATE POLICY "Users can view own data"
  ON tabela FOR SELECT
  USING (auth.uid() = user_id);

-- Utilizadores só editam os seus dados
CREATE POLICY "Users can update own data"
  ON tabela FOR UPDATE
  USING (auth.uid() = user_id);
```

### Verificações no Backend
```typescript
// ✅ SEMPRE verificar autorização no backend
export async function GET(request: Request) {
  const user = await getAuthUser()
  
  if (!user) {
    return new Response('Unauthorized', { status: 401 })
  }
  
  // Verificar se user tem acesso ao recurso
  const hasAccess = await checkUserAccess(user.id, resourceId)
  
  if (!hasAccess) {
    return new Response('Forbidden', { status: 403 })
  }
  
  // Proceder...
}
```

### Princípio do Menor Privilégio
- [ ] Dar apenas permissões necessárias
- [ ] Roles bem definidos (user, admin, etc.)
- [ ] Verificar permissões em cada operação

---

## 3. Validação de Input

### NUNCA Confiar no Frontend
```typescript
// ❌ MAU - confiar em dados do cliente
const { userId, role } = req.body
await updateUser(userId, { role }) // Vulnerável!

// ✅ BOM - validar e verificar
const schema = z.object({
  userId: z.string().uuid(),
  // role NÃO vem do cliente - vem da sessão
})

const user = await getAuthUser()
if (user.role !== 'admin') {
  throw new Error('Forbidden')
}
```

### Sanitização
```typescript
// Input de texto
import DOMPurify from 'dompurify'
const cleanHtml = DOMPurify.sanitize(userInput)

// SQL - usar prepared statements
const { data } = await supabase
  .from('users')
  .select('*')
  .eq('id', userId) // Parâmetro escapado automaticamente

// ❌ NUNCA fazer isto
const query = `SELECT * FROM users WHERE id = '${userId}'` // SQL Injection!
```

### Validação com Zod
```typescript
const userSchema = z.object({
  email: z.string().email(),
  name: z.string().min(2).max(100),
  age: z.number().int().min(0).max(150),
  phone: z.string().regex(/^[923][0-9]{8}$/), // Telefone PT
})

// Validar
const result = userSchema.safeParse(input)
if (!result.success) {
  return { error: result.error.format() }
}
```

---

## 4. Proteção de APIs

### Rate Limiting
```typescript
// Middleware de rate limiting
import { Ratelimit } from '@upstash/ratelimit'
import { Redis } from '@upstash/redis'

const ratelimit = new Ratelimit({
  redis: Redis.fromEnv(),
  limiter: Ratelimit.slidingWindow(10, '10 s'), // 10 requests por 10s
})

export async function middleware(request: Request) {
  const ip = request.headers.get('x-forwarded-for') ?? '127.0.0.1'
  const { success } = await ratelimit.limit(ip)
  
  if (!success) {
    return new Response('Too Many Requests', { status: 429 })
  }
}
```

### CORS
```typescript
// next.config.js
const nextConfig = {
  async headers() {
    return [
      {
        source: '/api/:path*',
        headers: [
          { key: 'Access-Control-Allow-Origin', value: process.env.ALLOWED_ORIGIN },
          { key: 'Access-Control-Allow-Methods', value: 'GET, POST, PUT, DELETE' },
          { key: 'Access-Control-Allow-Headers', value: 'Content-Type, Authorization' },
        ],
      },
    ]
  },
}
```

### Headers de Segurança
```typescript
// next.config.js
const securityHeaders = [
  { key: 'X-DNS-Prefetch-Control', value: 'on' },
  { key: 'Strict-Transport-Security', value: 'max-age=63072000; includeSubDomains' },
  { key: 'X-Frame-Options', value: 'SAMEORIGIN' },
  { key: 'X-Content-Type-Options', value: 'nosniff' },
  { key: 'Referrer-Policy', value: 'origin-when-cross-origin' },
  { key: 'Permissions-Policy', value: 'camera=(), microphone=(), geolocation=()' },
]
```

---

## 5. Dados Sensíveis

### Variáveis de Ambiente
```bash
# .env.local (NUNCA commitar)
DATABASE_URL=postgres://...
API_SECRET_KEY=sk_live_...
STRIPE_SECRET_KEY=sk_live_...

# .env.example (commitar - sem valores)
DATABASE_URL=
API_SECRET_KEY=
STRIPE_SECRET_KEY=
```

### Exposição ao Cliente
```typescript
// ✅ Variáveis públicas (prefixo NEXT_PUBLIC_)
NEXT_PUBLIC_API_URL=https://api.exemplo.com
NEXT_PUBLIC_STRIPE_PUBLIC_KEY=pk_live_...

// ❌ Variáveis secretas (sem prefixo - só server)
STRIPE_SECRET_KEY=sk_live_...
DATABASE_URL=postgres://...
```

### Logs
```typescript
// ❌ NUNCA logar dados sensíveis
console.log('User:', user) // Pode conter password hash!
console.log('Card:', cardNumber) // Dados de cartão!

// ✅ Logar apenas o necessário
console.log('User login:', { id: user.id, email: user.email })
console.log('Payment processed:', { orderId, amount })
```

---

## 6. RGPD & Privacidade

### Consentimento
- [ ] Obter consentimento explícito antes de processar dados
- [ ] Permitir retirar consentimento facilmente
- [ ] Registar data/hora do consentimento

```typescript
interface ConsentRecord {
  userId: string
  consentType: 'marketing' | 'analytics' | 'necessary'
  granted: boolean
  timestamp: Date
  ipAddress: string
}
```

### Direito ao Esquecimento
```typescript
// Endpoint para apagar dados do utilizador
export async function DELETE(request: Request) {
  const user = await getAuthUser()
  
  // Apagar todos os dados do utilizador
  await supabase.from('user_data').delete().eq('user_id', user.id)
  await supabase.from('user_logs').delete().eq('user_id', user.id)
  await supabase.auth.admin.deleteUser(user.id)
  
  return new Response('Dados apagados', { status: 200 })
}
```

### Exportação de Dados
```typescript
// Endpoint para exportar dados
export async function GET(request: Request) {
  const user = await getAuthUser()
  
  const userData = await supabase
    .from('users')
    .select('*')
    .eq('id', user.id)
    .single()
  
  const userOrders = await supabase
    .from('orders')
    .select('*')
    .eq('user_id', user.id)
  
  return Response.json({
    profile: userData,
    orders: userOrders,
    exportedAt: new Date().toISOString(),
  })
}
```

---

## 7. Uploads de Ficheiros

### Validação
```typescript
const ALLOWED_TYPES = ['image/jpeg', 'image/png', 'image/webp']
const MAX_SIZE = 5 * 1024 * 1024 // 5MB

function validateFile(file: File): boolean {
  // Verificar tipo MIME
  if (!ALLOWED_TYPES.includes(file.type)) {
    throw new Error('Tipo de ficheiro não permitido')
  }
  
  // Verificar tamanho
  if (file.size > MAX_SIZE) {
    throw new Error('Ficheiro demasiado grande (max 5MB)')
  }
  
  // Verificar extensão (double check)
  const ext = file.name.split('.').pop()?.toLowerCase()
  if (!['jpg', 'jpeg', 'png', 'webp'].includes(ext || '')) {
    throw new Error('Extensão não permitida')
  }
  
  return true
}
```

### Storage Seguro
- [ ] Guardar fora da pasta pública
- [ ] Gerar nomes únicos (UUID)
- [ ] Validar no servidor (não só no cliente)
- [ ] Scan de malware se possível

---

## 8. Checklist de Segurança

### Antes de Deploy
- [ ] Sem secrets em código
- [ ] .env.local no .gitignore
- [ ] HTTPS obrigatório
- [ ] Headers de segurança configurados
- [ ] Rate limiting ativo
- [ ] RLS configurado em todas as tabelas
- [ ] Validação de input em todos os endpoints
- [ ] Logs sem dados sensíveis

### Periódico
- [ ] Atualizar dependências (npm audit)
- [ ] Rever logs de acesso
- [ ] Testar recuperação de password
- [ ] Verificar permissões de roles
- [ ] Backup de dados testado

---

## 9. Recursos

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Supabase Security](https://supabase.com/docs/guides/auth/row-level-security)
- [Next.js Security](https://nextjs.org/docs/advanced-features/security-headers)
- [RGPD Guidelines](https://gdpr.eu/)
