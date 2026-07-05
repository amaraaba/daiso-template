# Contributing to DAISO

## Who
Any Intel engineer. No git knowledge required.

## What

| I want to... | Where |
|--------------|-------|
| Share a workflow | `packs/<domain>/skills/<name>/SKILL.md` |
| Document knowledge | `packs/<domain>/products/<product>/knowledge/guides/` or `reference/` |
| Add structured data | `packs/<domain>/products/<product>/knowledge/data/` (TOML + README) |
| Build a tool | `packs/<domain>/tools/` |

## How

**Recommended:** Work with Copilot, then say "push my changes." DAISO handles git.

**Manual:** Branch → edit → PR → champion review.

## Standards

- Skills: YAML front-matter (`name`, `description`, `tools`), "When to use", "Steps", "Key rules"
- Knowledge: YAML front-matter (`title`, `domain`, `product`, `author`, `date`)
- Data: TOML + companion README

## Review

- Pack content → champion
- Shared content → DAISO maintainers
