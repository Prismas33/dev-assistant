# Setup Questions - New Project

When a new project is detected (no `doc/MEMORIA.md`), ask these questions:

---

## Required Questions

### 1. Identification
```
What's the project name?
```

### 2. Project Type
```
What type of project?
- Web App (SPA/SSR)
- Mobile App (React Native/Flutter)
- API Backend
- Bot/Automation
- CLI Tool
- Other: ___
```

### 3. Tech Stack
```
What's the tech stack?

Frontend: [Next.js / React / Vue / Svelte / Other]
Backend: [Node.js / Python / Go / Other]
Database: [PostgreSQL / MySQL / MongoDB / Supabase / Firebase / Other]
Auth: [Firebase / NextAuth / Clerk / Custom / Other]
Hosting: [Vercel / Railway / DigitalOcean / AWS / Other]
```

### 4. Description
```
Describe the project in 1-2 sentences:
```

### 5. Problem
```
What problem does it solve? What's the user's pain point?
```

### 6. Audience
```
Who's the target audience?
```

---

## Optional Questions (if relevant)

### 7. Business Model
```
How will it generate revenue?
- SaaS (subscription)
- Freemium
- One-time purchase
- Ads
- Other
- Not defined yet
```

### 8. MVP Scope
```
What are the essential MVP features?
```

### 9. Timeline
```
Is there a specific deadline or timeline?
```

### 10. Integrations
```
Will it integrate with external services?
(APIs, payments, email, etc.)
```

---

## Defaults (if no answer)

| Field | Default |
|-------|---------|
| Name | Project folder name |
| Type | Web App |
| Frontend | Next.js 14 |
| Backend | Node.js |
| Database | PostgreSQL |
| Auth | To be defined |
| Hosting | To be defined |

---

## Setup Flow

```
1. DETECT new project (no doc/)
   ↓
2. ASK: "I detected this is a new project. Want me to set up documentation?"
   ↓
3. IF yes → Guided questions
   ↓
4. CREATE doc/ structure from templates
   ↓
5. FILL MEMORIA.md with answers
   ↓
6. CREATE first diary entry
   ↓
7. CONFIRM: "Documentation created! Summary: [...]"
```
