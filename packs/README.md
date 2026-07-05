# DAISO Packs

Each domain owns a **pack** — a self-contained folder with instructions, skills, knowledge, and MCP tools.

## Pack Structure

```
packs/<domain>/
├── instructions.md          # Domain-level rules (product-agnostic)
├── skills/                  # Domain skills
│   └── <skill-name>/
│       └── SKILL.md
├── products/                # Product-specific content
│   └── <product>/
│       ├── instructions.md  # Product-specific rules
│       ├── config.toml      # Paths, vault project, etc.
│       └── knowledge/       # Product knowledge
│           ├── guides/
│           ├── reference/
│           └── data/
└── mcp/                     # MCP tools
    ├── pack.toml            # Pack manifest
    └── tools.py             # Tool implementations
```

## Active Packs

| Pack | Org | Domain | Status | Champion |
|------|-----|--------|--------|----------|
| `<your-domain>` | `<your-org>` | `<description>` | Scaffold | `@champion` |

Any Intel team can add a pack. See `templates/pack-checklist.md` for the full checklist.

## Creating a New Pack

See `templates/pack-checklist.md`.
