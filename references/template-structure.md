# Template Structure - Reference

Complete documentation template structure.

---

## Folder Structure

```
doc/
├── MEMORIA.md                    # ⭐ MAIN FILE - Project context
│
├── componentes/
│   └── README.md                 # UI components catalog
│
├── desenvolvimento/
│   ├── README.md                 # Folder index
│   ├── diario.md                 # 📅 Development diary (update frequently)
│   ├── regras-codigo.md          # Code conventions
│   ├── regras-documentacao.md    # Documentation rules
│   ├── regras-layout.md          # UI patterns
│   └── regras-seguranca.md       # Security practices
│
├── design/
│   └── design-system.md          # Colors, typography, components
│
├── negocio/
│   ├── mercado.md                # Market analysis
│   ├── modelo-negocio.md         # Monetization, pricing
│   └── visao-geral.md            # Product description
│
├── planeamento/
│   ├── riscos.md                 # Identified risks
│   └── roadmap.md                # Development plan
│
├── produto/
│   ├── features-mvp.md           # MVP scope
│   ├── fluxo-produto.md          # User flows
│   └── kpis.md                   # Success metrics
│
└── tecnico/
    ├── arquitetura.md            # Stack and technical decisions
    ├── integracoes.md            # External APIs
    └── variaveis-ambiente.md     # .env configuration
```

---

## Priority Order

### Day 1 (Required)
1. ✅ MEMORIA.md - Complete context
2. ✅ desenvolvimento/diario.md - First entry
3. ✅ tecnico/arquitetura.md - Chosen stack

### Week 1
4. negocio/visao-geral.md
5. produto/features-mvp.md
6. planeamento/roadmap.md

### Ongoing
- diario.md - Each session
- MEMORIA.md - Architectural changes
- componentes/ - When creating components
