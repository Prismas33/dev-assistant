# Design System

> Os valores de cor, tipografia e CSS abaixo ilustram a estrutura do documento; não constituem uma identidade visual aprovada. Para cada cliente, confirmar marca, público, dispositivos, conteúdo e design system existente antes de adotar ou substituir estes exemplos.

> Sistema de design do projeto.

---

## 1. Cores

### Cores Primárias
```css
:root {
  /* Cor principal da marca */
  --primary: 220 90% 56%;           /* HSL: Azul */
  --primary-foreground: 0 0% 100%;  /* Texto sobre primary */
}
```

### Cores de Interface
```css
:root {
  /* Fundos */
  --background: 0 0% 100%;          /* Fundo principal */
  --card: 0 0% 100%;                /* Fundo de cards */
  --muted: 0 0% 96.1%;              /* Fundo secundário */
  
  /* Texto */
  --foreground: 0 0% 3.9%;          /* Texto principal */
  --muted-foreground: 0 0% 45.1%;   /* Texto secundário */
  
  /* Bordas */
  --border: 0 0% 89.8%;             /* Bordas padrão */
  --ring: 220 90% 56%;              /* Focus ring */
  
  /* Estados */
  --destructive: 0 84.2% 60.2%;     /* Erro/Perigo */
  --success: 142 76% 36%;           /* Sucesso */
  --warning: 38 92% 50%;            /* Aviso */
}
```

### Dark Mode
```css
.dark {
  --background: 0 0% 3.9%;
  --foreground: 0 0% 98%;
  --card: 0 0% 3.9%;
  --muted: 0 0% 14.9%;
  --muted-foreground: 0 0% 63.9%;
  --border: 0 0% 14.9%;
}
```

---

## 2. Tipografia

### Font Family
```css
:root {
  --font-sans: 'Inter', system-ui, sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
}
```

### Escala de Tamanhos
| Classe | Tamanho | Line Height | Uso |
|--------|---------|-------------|-----|
| `text-xs` | 12px | 16px | Labels, captions |
| `text-sm` | 14px | 20px | Texto secundário |
| `text-base` | 16px | 24px | Texto principal |
| `text-lg` | 18px | 28px | Subtítulos |
| `text-xl` | 20px | 28px | Títulos pequenos |
| `text-2xl` | 24px | 32px | Títulos médios |
| `text-3xl` | 30px | 36px | Títulos grandes |
| `text-4xl` | 36px | 40px | Hero titles |

### Font Weights
| Classe | Peso | Uso |
|--------|------|-----|
| `font-normal` | 400 | Texto corrido |
| `font-medium` | 500 | Ênfase leve |
| `font-semibold` | 600 | Subtítulos |
| `font-bold` | 700 | Títulos |

---

## 3. Espaçamento

### Escala Base (4px)
| Valor | Pixels | Uso típico |
|-------|--------|------------|
| 1 | 4px | Mínimo |
| 2 | 8px | Entre elementos inline |
| 3 | 12px | Padding compacto |
| 4 | 16px | Padding padrão |
| 6 | 24px | Gap em cards |
| 8 | 32px | Entre secções |
| 12 | 48px | Margens de página |
| 16 | 64px | Entre blocos |

---

## 4. Sombras

```css
:root {
  --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
}
```

---

## 5. Border Radius

| Classe | Valor | Uso |
|--------|-------|-----|
| `rounded-sm` | 2px | Subtil |
| `rounded` | 4px | Padrão |
| `rounded-md` | 6px | Cards, inputs |
| `rounded-lg` | 8px | Modais, grandes cards |
| `rounded-xl` | 12px | Hero sections |
| `rounded-full` | 9999px | Pills, avatares |

---

## 6. Componentes

### Button
```tsx
// Variantes disponíveis
<Button variant="default">Primary</Button>
<Button variant="secondary">Secondary</Button>
<Button variant="outline">Outline</Button>
<Button variant="ghost">Ghost</Button>
<Button variant="destructive">Destructive</Button>

// Tamanhos
<Button size="sm">Small</Button>
<Button size="default">Default</Button>
<Button size="lg">Large</Button>
```

### Input
```tsx
<Input placeholder="Placeholder text" />
<Input type="email" />
<Input disabled />
```

### Card
```tsx
<Card>
  <CardHeader>
    <CardTitle>Título</CardTitle>
    <CardDescription>Descrição</CardDescription>
  </CardHeader>
  <CardContent>Conteúdo</CardContent>
  <CardFooter>Footer</CardFooter>
</Card>
```

### Badge
```tsx
<Badge>Default</Badge>
<Badge variant="secondary">Secondary</Badge>
<Badge variant="outline">Outline</Badge>
<Badge variant="destructive">Destructive</Badge>
```

---

## 7. Ícones

### Biblioteca
Usar [Lucide React](https://lucide.dev/) para ícones.

```tsx
import { Home, Settings, User, Search } from 'lucide-react'

<Home className="h-5 w-5" />
```

### Tamanhos Padrão
| Contexto | Tamanho |
|----------|---------|
| Em texto | `h-4 w-4` |
| Em botões | `h-5 w-5` |
| Standalone | `h-6 w-6` |
| Hero | `h-8 w-8` ou maior |

---

## 8. Animações

### Transições Padrão
```css
/* Hover states */
transition: all 150ms ease;

/* Modais, drawers */
transition: all 200ms ease-out;

/* Page transitions */
transition: all 300ms ease-in-out;
```

### Classes Tailwind
```tsx
<button className="transition-colors hover:bg-primary/90">
<div className="transition-opacity duration-200">
<div className="animate-spin">
<div className="animate-pulse">
```

---

## 9. Breakpoints

| Nome | Min-Width | Descrição |
|------|-----------|-----------|
| `sm` | 640px | Mobile landscape |
| `md` | 768px | Tablet |
| `lg` | 1024px | Desktop pequeno |
| `xl` | 1280px | Desktop |
| `2xl` | 1536px | Desktop grande |

---

## 10. Acessibilidade

### Cores
- Contraste mínimo 4.5:1 para texto normal
- Contraste mínimo 3:1 para texto grande (18px+)

### Focus States
```tsx
<button className="focus:outline-none focus-visible:ring-2 focus-visible:ring-ring">
```

### Screen Readers
```tsx
// Esconder visualmente mas manter para SR
<span className="sr-only">Descrição para screen reader</span>

// Ícones decorativos
<Icon aria-hidden="true" />
```
