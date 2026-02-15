# Regras de Layout & UI/UX

> Convenções de design e layout para interfaces consistentes.

---

## 1. Sistema de Grid

### Container Padrão
```tsx
// Container com largura máxima e padding
<div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
  {children}
</div>
```

### Breakpoints (Tailwind)
| Prefixo | Min-Width | Descrição |
|---------|-----------|-----------|
| `sm`    | 640px     | Mobile landscape / tablet pequeno |
| `md`    | 768px     | Tablet |
| `lg`    | 1024px    | Desktop pequeno |
| `xl`    | 1280px    | Desktop |
| `2xl`   | 1536px    | Desktop grande |

### Mobile First
```tsx
// ✅ Mobile first - adicionar estilos para ecrãs maiores
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
```

---

## 2. Espaçamento

### Escala de Spacing
Usar sempre a escala do Tailwind para consistência:

| Classe | Valor | Uso típico |
|--------|-------|------------|
| `gap-1` / `p-1` | 4px | Espaço mínimo |
| `gap-2` / `p-2` | 8px | Entre elementos inline |
| `gap-3` / `p-3` | 12px | Padding interno compacto |
| `gap-4` / `p-4` | 16px | Padding padrão |
| `gap-6` / `p-6` | 24px | Entre secções pequenas |
| `gap-8` / `p-8` | 32px | Entre secções médias |
| `gap-12` / `p-12` | 48px | Entre secções grandes |
| `gap-16` / `p-16` | 64px | Entre blocos principais |

### Regras de Espaçamento
```tsx
// ✅ Cards
<div className="p-4 sm:p-6"> // 16px mobile, 24px desktop

// ✅ Espaço entre elementos de formulário
<div className="space-y-4">
  <Input />
  <Input />
  <Button />
</div>

// ✅ Margens de secção
<section className="py-12 sm:py-16 lg:py-24">
```

---

## 3. Tipografia

### Escala de Tamanhos
```tsx
// Headings
<h1 className="text-3xl sm:text-4xl lg:text-5xl font-bold">
<h2 className="text-2xl sm:text-3xl font-bold">
<h3 className="text-xl sm:text-2xl font-semibold">
<h4 className="text-lg font-semibold">

// Body
<p className="text-base">    // 16px - texto principal
<p className="text-sm">      // 14px - texto secundário
<p className="text-xs">      // 12px - labels, captions
```

### Cores de Texto
```tsx
// Hierarquia de importância
<p className="text-foreground">      // Texto principal
<p className="text-muted-foreground"> // Texto secundário
<p className="text-primary">         // Links, ações
<p className="text-destructive">     // Erros
```

### Line Height
```tsx
// Texto longo - mais espaçamento
<p className="leading-relaxed">

// Títulos - mais apertado
<h1 className="leading-tight">
```

---

## 4. Cores

### Semantic Colors (CSS Variables)
```css
/* Usar sempre cores semânticas, não cores diretas */
:root {
  --background: 0 0% 100%;
  --foreground: 0 0% 3.9%;
  --primary: 220 90% 56%;
  --primary-foreground: 0 0% 100%;
  --secondary: 0 0% 96.1%;
  --muted: 0 0% 96.1%;
  --muted-foreground: 0 0% 45.1%;
  --accent: 0 0% 96.1%;
  --destructive: 0 84.2% 60.2%;
  --border: 0 0% 89.8%;
  --ring: 220 90% 56%;
}
```

### Uso Correto
```tsx
// ✅ Usar cores semânticas
<div className="bg-background text-foreground">
<div className="bg-primary text-primary-foreground">
<div className="border-border">
<div className="text-muted-foreground">

// ❌ Evitar cores hardcoded
<div className="bg-blue-500">
<div className="text-gray-600">
```

---

## 5. Componentes UI

### Buttons
```tsx
// Hierarquia de botões
<Button>Primary Action</Button>           // Ação principal
<Button variant="secondary">Secondary</Button>  // Ação secundária
<Button variant="outline">Tertiary</Button>    // Menos destaque
<Button variant="ghost">Ghost</Button>         // Mínimo destaque
<Button variant="destructive">Delete</Button>  // Ação perigosa

// Tamanhos
<Button size="sm">Small</Button>   // 32px altura
<Button size="default">Medium</Button>  // 40px altura
<Button size="lg">Large</Button>   // 48px altura
```

### Cards
```tsx
<Card>
  <CardHeader>
    <CardTitle>Título</CardTitle>
    <CardDescription>Descrição opcional</CardDescription>
  </CardHeader>
  <CardContent>
    {/* Conteúdo principal */}
  </CardContent>
  <CardFooter>
    {/* Ações */}
  </CardFooter>
</Card>
```

### Forms
```tsx
<form className="space-y-4">
  <div className="space-y-2">
    <Label htmlFor="email">Email</Label>
    <Input id="email" type="email" placeholder="email@exemplo.com" />
    <p className="text-sm text-muted-foreground">
      Texto de ajuda opcional
    </p>
  </div>
  
  <div className="space-y-2">
    <Label htmlFor="password">Password</Label>
    <Input id="password" type="password" />
  </div>
  
  <Button type="submit" className="w-full">
    Submeter
  </Button>
</form>
```

---

## 6. Layout Patterns

### Dashboard Layout
```tsx
<div className="flex min-h-screen">
  {/* Sidebar */}
  <aside className="hidden md:flex w-64 flex-col border-r">
    <nav className="flex-1 p-4">
      {/* Menu items */}
    </nav>
  </aside>
  
  {/* Main content */}
  <main className="flex-1">
    <header className="border-b px-4 py-3">
      {/* Top bar */}
    </header>
    <div className="p-4 sm:p-6 lg:p-8">
      {/* Page content */}
    </div>
  </main>
</div>
```

### Page Header
```tsx
<div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
  <div>
    <h1 className="text-2xl font-bold">Título da Página</h1>
    <p className="text-muted-foreground">Descrição opcional</p>
  </div>
  <div className="flex gap-2">
    <Button variant="outline">Ação Secundária</Button>
    <Button>Ação Principal</Button>
  </div>
</div>
```

### Lista com Ações
```tsx
<div className="divide-y rounded-lg border">
  {items.map((item) => (
    <div 
      key={item.id}
      className="flex items-center justify-between p-4 hover:bg-muted/50"
    >
      <div>
        <p className="font-medium">{item.title}</p>
        <p className="text-sm text-muted-foreground">{item.subtitle}</p>
      </div>
      <div className="flex gap-2">
        <Button variant="ghost" size="sm">Edit</Button>
        <Button variant="ghost" size="sm">Delete</Button>
      </div>
    </div>
  ))}
</div>
```

---

## 7. Responsividade

### Hide/Show por Breakpoint
```tsx
// Mostrar só em mobile
<div className="block md:hidden">Mobile only</div>

// Mostrar só em desktop
<div className="hidden md:block">Desktop only</div>

// Componentes diferentes por tamanho
<MobileNav className="md:hidden" />
<DesktopNav className="hidden md:flex" />
```

### Flex/Grid Responsivo
```tsx
// Stack em mobile, row em desktop
<div className="flex flex-col md:flex-row gap-4">

// 1 coluna mobile, 2 tablet, 3 desktop
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">

// Sidebar fixa em desktop, drawer em mobile
<aside className="hidden lg:block w-64">
<Sheet className="lg:hidden">
```

### Padding Responsivo
```tsx
// Menos padding em mobile
<div className="p-4 sm:p-6 lg:p-8">

// Container com margens responsivas
<div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
```

---

## 8. Estados Interativos

### Hover & Focus
```tsx
// Button hover
<button className="hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-ring">

// Card hover
<div className="transition-colors hover:bg-muted/50">

// Link hover
<a className="hover:underline hover:text-primary">
```

### Loading States
```tsx
// Button loading
<Button disabled>
  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
  A processar...
</Button>

// Skeleton loading
<div className="space-y-2">
  <Skeleton className="h-4 w-[250px]" />
  <Skeleton className="h-4 w-[200px]" />
</div>
```

### Empty States
```tsx
<div className="flex flex-col items-center justify-center py-12 text-center">
  <Icon className="h-12 w-12 text-muted-foreground mb-4" />
  <h3 className="font-semibold">Sem resultados</h3>
  <p className="text-sm text-muted-foreground mt-1">
    Tente ajustar os filtros de pesquisa
  </p>
  <Button variant="outline" className="mt-4">
    Limpar filtros
  </Button>
</div>
```

---

## 9. Acessibilidade

### Contrast & Legibilidade
- [ ] Ratio mínimo 4.5:1 para texto normal
- [ ] Ratio mínimo 3:1 para texto grande
- [ ] Não usar só cor para transmitir informação

### Keyboard Navigation
```tsx
// Todos os elementos interativos focáveis
<button>OK</button> // ✅ Focável por defeito
<div onClick={...}>Click</div> // ❌ Não focável
<div role="button" tabIndex={0} onClick={...}>Click</div> // ✅ Focável

// Focus visible
<button className="focus-visible:ring-2 focus-visible:ring-ring">
```

### Screen Readers
```tsx
// Labels em inputs
<Label htmlFor="email">Email</Label>
<Input id="email" aria-describedby="email-hint" />
<p id="email-hint" className="text-sm text-muted-foreground">
  O teu email de contacto
</p>

// Ícones decorativos
<Icon aria-hidden="true" />

// Ícones com significado
<button aria-label="Fechar menu">
  <X aria-hidden="true" />
</button>
```

---

## 10. Checklist de Layout

### Antes de Commit
- [ ] Funciona em mobile (320px)
- [ ] Funciona em tablet (768px)
- [ ] Funciona em desktop (1280px+)
- [ ] Espaçamento consistente
- [ ] Texto legível (tamanho e contraste)
- [ ] Estados hover/focus visíveis
- [ ] Loading states implementados
- [ ] Empty states implementados
- [ ] Navegação por teclado funciona
