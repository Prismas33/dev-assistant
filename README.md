# Dev Assistant

Agent skill for development assistance with auto-documentation, context management and quality gates.

## Features

- 🆕 **Project Setup** - Guided questions + doc structure creation
- 🔄 **Auto-Context** - Reads MEMORIA.md automatically without asking
- 🔍 **Discovery Mode** - Never edits code during investigation without confirmation
- ✅ **Quality Gates** - Checklists for commits, bugs, deploys
- 📝 **Auto Documentation** - Proposes diary and docs updates
- 📁 **Embedded Templates** - Full doc structure included

## Installation

```bash
npx skills add Prismas33/dev-assistant
```

## Usage

The skill activates automatically when you:
- Open a new project (setup mode)
- Work on existing project (dev mode)
- Ask investigation questions (discovery mode)

### Commands / Triggers

- New project detected → Guided setup
- "Read the memory" → Already done automatically
- "Update diary" → Proposes entry
- "Why is this happening?" → Investigation mode (no edits without confirmation)

## Structure

```
dev-assistant/
├── SKILL.md              # Main instructions
├── README.md             # This file
├── references/
│   ├── checklists.md         # Quality gates
│   ├── setup-questions.md    # New project questions
│   └── template-structure.md # Template overview
├── scripts/
│   └── init-project.ps1      # Project setup script
└── templates/                 # Embedded doc templates
    ├── MEMORIA.md
    ├── componentes/
    ├── desenvolvimento/
    ├── design/
    ├── negocio/
    ├── planeamento/
    ├── produto/
    └── tecnico/
```

## Behavior Modes

| Mode | Trigger | Behavior |
|------|---------|----------|
| **Setup** | No `doc/` folder | Ask questions, create structure |
| **Dev** | `doc/` exists | Auto-load context, propose updates |
| **Discovery** | "why?", "how?", "investigate" | Research first, ask before editing |

## Author

Prismas33

## License

MIT
