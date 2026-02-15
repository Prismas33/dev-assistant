# KPIs e Métricas

> Métricas chave para medir sucesso do produto.

---

## North Star Metric

**[Nome da Métrica Principal]**

A métrica mais importante que indica se estamos a entregar valor:

> Exemplo: "Número de [ações de valor] por semana"

---

## Métricas por Categoria

### Aquisição
Como chegamos a novos utilizadores?

| Métrica | Definição | Target | Atual |
|---------|-----------|--------|-------|
| Visitantes únicos | Visitantes/mês no site | 10k | - |
| Sign-ups | Novos registos/mês | 500 | - |
| Conversion rate | Visitantes → Sign-ups | 5% | - |
| CAC | Custo por aquisição | €10 | - |

### Ativação
Utilizadores entendem o valor?

| Métrica | Definição | Target | Atual |
|---------|-----------|--------|-------|
| Activation rate | % que completa onboarding | 70% | - |
| Time to value | Tempo até 1ª ação de valor | <5min | - |
| Setup completion | % que configura perfil | 80% | - |

### Retenção
Utilizadores voltam?

| Métrica | Definição | Target | Atual |
|---------|-----------|--------|-------|
| DAU/MAU | Utilizadores diários/mensais | 40% | - |
| D1/D7/D30 | Retenção dia 1/7/30 | 60/40/25% | - |
| Churn rate | % que cancela/mês | <5% | - |

### Revenue
Estamos a gerar receita?

| Métrica | Definição | Target | Atual |
|---------|-----------|--------|-------|
| MRR | Monthly Recurring Revenue | €5k | - |
| ARPU | Average Revenue Per User | €20 | - |
| LTV | Lifetime Value | €200 | - |
| LTV/CAC | Ratio valor/custo | >3 | - |

### Referral
Utilizadores recomendam?

| Métrica | Definição | Target | Atual |
|---------|-----------|--------|-------|
| NPS | Net Promoter Score | >50 | - |
| Referral rate | % que convida outros | 10% | - |
| Viral coefficient | Novos users por user | >1 | - |

---

## Dashboard de Métricas

### Métricas Diárias
- [ ] DAU (Daily Active Users)
- [ ] Sign-ups
- [ ] [Ação de valor principal]

### Métricas Semanais
- [ ] WAU (Weekly Active Users)
- [ ] Activation rate
- [ ] Churn

### Métricas Mensais
- [ ] MRR
- [ ] MAU
- [ ] NPS
- [ ] Cohort analysis

---

## Ferramentas de Analytics

| Ferramenta | Propósito | Status |
|------------|-----------|--------|
| [Analytics tool] | Tráfego web | [ ] Configurado |
| [Product analytics] | Eventos in-app | [ ] Configurado |
| [Error tracking] | Erros e crashes | [ ] Configurado |

### Eventos a Rastrear

| Evento | Categoria | Propriedades |
|--------|-----------|--------------|
| `sign_up` | Aquisição | source, plan |
| `login` | Engagement | method |
| `[ação_valor]` | Activation | type, count |
| `upgrade` | Revenue | from_plan, to_plan |
| `churn` | Retention | reason, tenure |

---

## OKRs (Exemplo)

### Q[X] 202[X]

**Objective 1: [Nome do objetivo]**
- KR1: [Resultado chave mensurável] - Target: X
- KR2: [Resultado chave mensurável] - Target: Y
- KR3: [Resultado chave mensurável] - Target: Z

**Objective 2: [Nome do objetivo]**
- KR1: ...
- KR2: ...

---

## Revisão de Métricas

### Cadência
- **Diária:** Check rápido das métricas core
- **Semanal:** Revisão de tendências
- **Mensal:** Análise profunda, cohorts
- **Trimestral:** Revisão de OKRs

### Alertas
Configurar alertas para:
- [ ] Spike de erros (>X% erro rate)
- [ ] Drop de sign-ups (>Y% vs média)
- [ ] Churn acima do target
- [ ] Revenue abaixo do esperado
