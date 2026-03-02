# Contributing

## Scope

This repository stores AI agent skills for Shengwang (Agora) workflows,
following the [Agent Skills](https://agentskills.io) open standard.
Changes should improve routing accuracy, execution quality, and maintainability.

## Required Rules

1. All skill content lives under `skills/shengwang-integration/`.
2. Every sub-module directory must have one `SKILL.md` entrypoint.
3. Every `SKILL.md` must include YAML frontmatter with:
   - `name` (max 64 chars, lowercase kebab-case)
   - `description` (max 1024 chars, includes trigger phrases)
   - `license`
   - `metadata.author`
   - `metadata.version`
4. Do NOT use `triggers` as a top-level frontmatter field — fold trigger phrases into `description`.
5. Use relative links for local references.
6. Put detailed docs under `references/`; keep `SKILL.md` focused on workflow.
7. Never commit secrets, tokens, or private credentials.

## Naming

- Directory names: lowercase kebab-case.
- Skill names (`frontmatter.name`): unique across repository.
- Prefer `shengwang-` or `integrate-shengwang-` prefix.

## Pull Request Checklist

- [ ] Routing logic is still correct from `skills/shengwang-integration/SKILL.md`.
- [ ] New or changed links are valid.
- [ ] No duplicate skill names.
- [ ] No orphaned files left behind.
- [ ] No hardcoded credentials.
- [ ] `scripts/validate-skills.sh` passes locally.

## Local Validation

```bash
bash scripts/validate-skills.sh
```
