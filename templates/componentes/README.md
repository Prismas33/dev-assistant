# Catálogo de Componentes

> Referência de todos os componentes reutilizáveis do projeto.

---

## Como Usar Este Catálogo

Cada componente documentado deve incluir:
1. Descrição e propósito
2. Props disponíveis
3. Exemplo de uso
4. Variantes (se existirem)
5. Notas de acessibilidade

---

## Componentes UI Base

### Button
📁 `src/components/ui/button.tsx`

Botão reutilizável com várias variantes e tamanhos.

| Prop | Tipo | Default | Descrição |
|------|------|---------|-----------|
| `variant` | `'default' \| 'secondary' \| 'outline' \| 'ghost' \| 'destructive'` | `'default'` | Estilo visual |
| `size` | `'sm' \| 'default' \| 'lg'` | `'default'` | Tamanho |
| `disabled` | `boolean` | `false` | Desativado |
| `asChild` | `boolean` | `false` | Usar elemento filho |

```tsx
import { Button } from '@/components/ui/button'

<Button variant="outline" size="lg">
  Click me
</Button>
```

---

### Input
📁 `src/components/ui/input.tsx`

Campo de input de texto.

| Prop | Tipo | Default | Descrição |
|------|------|---------|-----------|
| `type` | `string` | `'text'` | Tipo de input |
| `placeholder` | `string` | - | Placeholder |
| `disabled` | `boolean` | `false` | Desativado |

```tsx
import { Input } from '@/components/ui/input'

<Input 
  type="email" 
  placeholder="email@exemplo.com" 
/>
```

---

### Card
📁 `src/components/ui/card.tsx`

Container com bordas e padding.

```tsx
import { 
  Card, 
  CardHeader, 
  CardTitle, 
  CardDescription, 
  CardContent, 
  CardFooter 
} from '@/components/ui/card'

<Card>
  <CardHeader>
    <CardTitle>Título</CardTitle>
    <CardDescription>Descrição opcional</CardDescription>
  </CardHeader>
  <CardContent>
    Conteúdo principal
  </CardContent>
  <CardFooter>
    <Button>Ação</Button>
  </CardFooter>
</Card>
```

---

### Badge
📁 `src/components/ui/badge.tsx`

Label pequeno para estados ou categorias.

| Prop | Tipo | Default | Descrição |
|------|------|---------|-----------|
| `variant` | `'default' \| 'secondary' \| 'outline' \| 'destructive'` | `'default'` | Estilo |

```tsx
import { Badge } from '@/components/ui/badge'

<Badge variant="secondary">Novo</Badge>
```

---

## Componentes de Layout

### Header
📁 `src/components/layout/header.tsx`

Descrição e uso...

---

## Componentes de Features

### [NomeFeature]
📁 `src/components/features/[nome]/`

Descrição e uso...

---

## Template para Novos Componentes

```markdown
### NomeDoComponente
📁 `src/components/[categoria]/[nome].tsx`

Descrição breve do componente e quando usar.

| Prop | Tipo | Default | Descrição |
|------|------|---------|-----------|
| `prop1` | `string` | - | Descrição |
| `prop2` | `boolean` | `false` | Descrição |

\```tsx
import { NomeDoComponente } from '@/components/[caminho]'

<NomeDoComponente prop1="valor">
  Children
</NomeDoComponente>
\```

**Notas:**
- Consideração especial 1
- Consideração especial 2
```
