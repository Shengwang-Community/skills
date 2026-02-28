# Contributing

## Scope

This repository stores AI agent skills for Shengwang (Agora) workflows.
Changes should improve routing accuracy, execution quality, and maintainability.

## Required Rules

1. Keep one canonical skill tree under `skills/`.
2. Every skill directory must have one `SKILL.md` entrypoint.
3. Every `SKILL.md` must include YAML frontmatter with:
   - `name`
   - `description`
   - `metadata.author`
   - `metadata.version`
4. Use relative links for local references.
5. Put detailed docs under `references/`; keep `SKILL.md` focused on workflow.
6. Never commit secrets, tokens, or private credentials.

## Naming

- Skill directory names: lowercase kebab-case.
- Skill names (`frontmatter.name`): unique across repository.
- Prefer `shengwang-` prefix for shared platform skills.

## Pull Request Checklist

- [ ] Skill routing logic is still correct from `skills/SKILL.md`.
- [ ] New or changed links are valid.
- [ ] No duplicate skill names.
- [ ] No orphaned files left behind.
- [ ] `scripts/validate-skills.sh` passes locally.

## Local Validation

```bash
bash scripts/validate-skills.sh
```
