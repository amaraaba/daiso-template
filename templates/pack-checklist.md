# New Pack Checklist

Any Intel team can add a pack. A pack is a self-contained folder under `packs/<domain>/` with your team’s instructions, skills, knowledge, and tools.

- [ ] Create `packs/<domain>/` (use your team name, e.g. `firmware`, `platform`, `ip-design`)
- [ ] Write `instructions.md` — domain rules that apply across all products
- [ ] Create `mcp/pack.toml` — pack manifest
- [ ] Create `products/<product>/` with `config.toml` + `knowledge/`
- [ ] Add at least one skill (see `templates/skill-template.md`)
- [ ] Add at least one knowledge file
- [ ] Assign a champion (the person who reviews PRs for this pack)
- [ ] Update `packs/README.md` — add your pack to the Active Packs table
- [ ] Update `packs/skills-catalog.md` — list your skills so engineers can discover them
- [ ] Open a PR
