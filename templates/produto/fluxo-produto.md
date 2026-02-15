# Fluxos do Produto

> User flows e jornadas do utilizador.

---

## Fluxos Principais

### 1. Onboarding / Registo

```
┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐
│ Landing │ ──▶ │ Registo │ ──▶ │ Verify  │ ──▶ │ Setup   │
│  Page   │     │  Form   │     │  Email  │     │ Profile │
└─────────┘     └─────────┘     └─────────┘     └─────────┘
                                                     │
                                                     ▼
                                               ┌─────────┐
                                               │Dashboard│
                                               └─────────┘
```

**Passos detalhados:**
1. Utilizador chega à landing page
2. Clica em "Criar conta"
3. Preenche email e password
4. Recebe email de verificação
5. Clica no link de verificação
6. Configura perfil inicial
7. Acede ao dashboard

---

### 2. Login

```
┌─────────┐     ┌─────────┐     ┌─────────┐
│  Login  │ ──▶ │ Verify  │ ──▶ │Dashboard│
│  Form   │     │ (2FA?)  │     │         │
└─────────┘     └─────────┘     └─────────┘
      │
      ▼ (erro)
┌─────────────┐
│ Forgot Pass │
└─────────────┘
```

---

### 3. [Nome do Fluxo Principal]

```
[Desenhar o fluxo aqui]
```

**Passos detalhados:**
1. ...
2. ...
3. ...

---

## Estados e Condições

### Estados do Utilizador

| Estado | Descrição | Acesso |
|--------|-----------|--------|
| Anónimo | Sem conta | Landing, Pricing |
| Registado | Conta não verificada | Verificação pendente |
| Verificado | Email confirmado | Dashboard (limitado) |
| Subscrito | Plano ativo | Dashboard completo |
| Admin | Administrador | Tudo + Admin panel |

### Condições de Transição

```
Anónimo ──[regista]──▶ Registado
Registado ──[verifica email]──▶ Verificado  
Verificado ──[subscreve]──▶ Subscrito
Subscrito ──[cancela]──▶ Verificado
```

---

## Wireframes / Mockups

### Ecrã: [Nome]
```
┌────────────────────────────────────┐
│  Header                            │
├────────────────────────────────────┤
│                                    │
│  ┌──────────┐    ┌──────────┐     │
│  │  Card 1  │    │  Card 2  │     │
│  └──────────┘    └──────────┘     │
│                                    │
│  ┌─────────────────────────────┐  │
│  │    Main Content Area        │  │
│  │                             │  │
│  └─────────────────────────────┘  │
│                                    │
├────────────────────────────────────┤
│  Footer                            │
└────────────────────────────────────┘
```

---

## Edge Cases

### Erros Comuns
| Situação | Comportamento esperado |
|----------|------------------------|
| Email já existe | Mostrar erro, sugerir login |
| Password fraca | Mostrar requisitos |
| Session expirada | Redirect para login |
| Sem permissão | Mostrar erro 403 |

### Estados Vazios
| Ecrã | Estado vazio |
|------|--------------|
| Lista de X | "Ainda não tem X. Criar primeiro?" |
| Pesquisa sem resultados | "Sem resultados. Tente outros termos." |

---

## Notificações e Feedback

### Mensagens de Sucesso
- "Conta criada com sucesso!"
- "Alterações guardadas."
- "[Item] criado com sucesso."

### Mensagens de Erro
- "Email ou password incorretos."
- "Não foi possível completar a ação. Tente novamente."
- "Sessão expirada. Faça login novamente."

### Loading States
- Skeleton loaders para listas
- Spinner para ações
- Progress bar para uploads

---

## Mobile Considerations

### Navegação Mobile
- [ ] Menu hamburger
- [ ] Bottom navigation (se aplicável)
- [ ] Gestos (swipe, pull-to-refresh)

### Adaptações
| Desktop | Mobile |
|---------|--------|
| Sidebar | Drawer/Sheet |
| Tabela | Cards empilhados |
| Modal grande | Fullscreen |
