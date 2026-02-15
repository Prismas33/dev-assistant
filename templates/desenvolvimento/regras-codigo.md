# Regras de Código

> Convenções e boas práticas para manter o código consistente e de qualidade.

---

## 1. Linguagem & Nomenclatura

### Código
- **Variáveis/Funções:** camelCase em inglês
- **Componentes React:** PascalCase
- **Ficheiros componentes:** kebab-case ou PascalCase (consistente no projeto)
- **Constantes:** SCREAMING_SNAKE_CASE
- **Types/Interfaces:** PascalCase com prefixo descritivo

```typescript
// ✅ Bom
const userName = 'João'
const MAX_RETRIES = 3
function calculateTotal() {}
interface UserProfile {}
type PaymentStatus = 'pending' | 'completed'

// ❌ Evitar
const nome_utilizador = 'João'
const maxRetries = 3
function calcular_total() {}
```

### Comentários e Documentação
- Comentários em **português** (PT-PT)
- JSDoc para funções públicas
- README e docs em português

```typescript
/**
 * Calcula o preço total com IVA
 * @param preco - Preço base sem IVA
 * @param taxa - Taxa de IVA (default: 0.23)
 * @returns Preço com IVA incluído
 */
function calcularPrecoComIva(preco: number, taxa = 0.23): number {
  // Arredondar para 2 casas decimais
  return Math.round(preco * (1 + taxa) * 100) / 100
}
```

---

## 2. TypeScript

### Strict Mode
- Sempre usar `strict: true` no tsconfig
- Evitar `any` - usar `unknown` se necessário
- Definir tipos explícitos para funções públicas

```typescript
// ✅ Bom
function processUser(user: User): ProcessedUser {
  return { ...user, processed: true }
}

// ❌ Evitar
function processUser(user: any) {
  return { ...user, processed: true }
}
```

### Interfaces vs Types
- **Interface:** Para objetos que podem ser extendidos
- **Type:** Para unions, intersections, tipos utilitários

```typescript
// Interface para entidades
interface User {
  id: string
  name: string
  email: string
}

// Type para unions
type Status = 'pending' | 'active' | 'inactive'

// Type para derivados
type UserWithRole = User & { role: Role }
```

---

## 3. React & Componentes

### Estrutura de Componente
```tsx
'use client' // Apenas se necessário

import { useState, useEffect } from 'react'
import { ExternalLib } from 'external-lib'
import { LocalComponent } from '@/components/ui'
import { useCustomHook } from '@/hooks'
import { someUtil } from '@/lib/utils'

// Types no topo
interface ComponentProps {
  title: string
  onAction: () => void
  children?: React.ReactNode
}

// Componente
export function ComponentName({ title, onAction, children }: ComponentProps) {
  // 1. Hooks primeiro
  const [state, setState] = useState(false)
  const { data } = useCustomHook()
  
  // 2. Efeitos
  useEffect(() => {
    // ...
  }, [])
  
  // 3. Handlers
  const handleClick = () => {
    onAction()
  }
  
  // 4. Render
  return (
    <div>
      <h1>{title}</h1>
      {children}
    </div>
  )
}
```

### Regras de Componentes
- [ ] Um componente por ficheiro
- [ ] Props tipadas com interface
- [ ] Componentes pequenos e focados (< 200 linhas)
- [ ] Extrair lógica complexa para hooks
- [ ] Usar composição em vez de herança

### Client vs Server Components (Next.js App Router)
```tsx
// Server Component (default) - para dados estáticos, SEO
export default async function Page() {
  const data = await fetchData()
  return <div>{data}</div>
}

// Client Component - para interatividade
'use client'
export function InteractiveComponent() {
  const [state, setState] = useState()
  return <button onClick={() => setState(...)}>Click</button>
}
```

---

## 4. Imports & Exports

### Ordem de Imports
1. React/Framework
2. Bibliotecas externas
3. Componentes locais (@/)
4. Hooks locais
5. Utils/Lib
6. Types
7. Styles

```typescript
// 1. React
import { useState, useEffect } from 'react'

// 2. Externas
import { format } from 'date-fns'
import { z } from 'zod'

// 3. Componentes
import { Button, Card } from '@/components/ui'
import { Header } from '@/components/layout'

// 4. Hooks
import { useAuth, useMediaQuery } from '@/hooks'

// 5. Utils
import { cn, formatCurrency } from '@/lib/utils'

// 6. Types
import type { User, Post } from '@/types'
```

### Path Aliases
Configurar no `tsconfig.json`:
```json
{
  "compilerOptions": {
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

---

## 5. Error Handling

### Try-Catch Pattern
```typescript
async function fetchUser(id: string): Promise<User | null> {
  try {
    const response = await fetch(`/api/users/${id}`)
    
    if (!response.ok) {
      throw new Error(`HTTP error: ${response.status}`)
    }
    
    return await response.json()
  } catch (error) {
    console.error('Erro ao buscar utilizador:', error)
    return null
  }
}
```

### Error Boundaries (React)
```tsx
'use client'

import { ErrorBoundary } from 'react-error-boundary'

function ErrorFallback({ error, resetErrorBoundary }) {
  return (
    <div role="alert">
      <p>Algo correu mal:</p>
      <pre>{error.message}</pre>
      <button onClick={resetErrorBoundary}>Tentar novamente</button>
    </div>
  )
}

// Uso
<ErrorBoundary FallbackComponent={ErrorFallback}>
  <ComponentQuePodeFalhar />
</ErrorBoundary>
```

---

## 6. Performance

### React
- [ ] Usar `useMemo` para cálculos pesados
- [ ] Usar `useCallback` para funções passadas como props
- [ ] Lazy loading para componentes grandes
- [ ] Virtualização para listas longas

```typescript
// Memoização
const expensiveValue = useMemo(() => {
  return heavyCalculation(data)
}, [data])

// Callback estável
const handleSubmit = useCallback((values) => {
  submitForm(values)
}, [submitForm])

// Lazy loading
const HeavyComponent = lazy(() => import('./HeavyComponent'))
```

### Next.js
- [ ] Usar Server Components sempre que possível
- [ ] Image optimization com `next/image`
- [ ] Font optimization com `next/font`
- [ ] Prefetching inteligente

---

## 7. Testes

### Nomenclatura
```typescript
// Ficheiro: component-name.test.tsx ou component-name.spec.tsx

describe('ComponentName', () => {
  it('should render correctly', () => {})
  it('should handle click event', () => {})
  it('should display error when invalid', () => {})
})
```

### Cobertura Mínima
- Funções utilitárias: 90%+
- Componentes críticos: 80%+
- APIs: 85%+

---

## 8. Git & Commits

### Conventional Commits
```
type(scope): description

[optional body]

[optional footer]
```

**Types:**
- `feat`: Nova funcionalidade
- `fix`: Correção de bug
- `docs`: Documentação
- `style`: Formatação (não afeta código)
- `refactor`: Refatoração
- `test`: Testes
- `chore`: Manutenção

**Exemplos:**
```
feat(auth): add social login with Google
fix(dashboard): resolve chart rendering issue
docs(readme): update installation instructions
refactor(api): simplify error handling
```

### Branches
- `main`: Produção
- `develop`: Desenvolvimento
- `feature/nome`: Nova feature
- `fix/nome`: Correção
- `hotfix/nome`: Correção urgente em produção

---

## 9. Checklist de Code Review

- [ ] Código segue convenções do projeto
- [ ] TypeScript sem erros/warnings
- [ ] Sem `any` desnecessários
- [ ] Componentes < 200 linhas
- [ ] Funções < 50 linhas
- [ ] Nomes descritivos
- [ ] Sem código comentado
- [ ] Sem console.logs de debug
- [ ] Error handling adequado
- [ ] Testes para código crítico
- [ ] Performance considerada
- [ ] Acessibilidade considerada
