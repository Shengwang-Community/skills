# Contributing

## Scope

This repository stores AI agent skills for Shengwang workflows,
following the [Agent Skills](https://agentskills.io) open standard.
Changes should improve routing accuracy, execution quality, and maintainability.

## Required Rules

1. All skill content lives under `skills/voice-ai-integration/`.
2. The root skill directory has one `SKILL.md` entrypoint with YAML frontmatter.
3. Sub-module directories use `README.md` (no YAML frontmatter needed).
4. The root `SKILL.md` must include YAML frontmatter with:
   - `name` (max 64 chars, lowercase kebab-case)
   - `description` (max 1024 chars, includes trigger phrases)
   - `license`
   - `metadata.author`
   - `metadata.version`
5. Do NOT use `triggers` as a top-level frontmatter field — fold trigger phrases into `description`.
6. Use relative links for local references.
7. Put detailed docs under `references/`; keep `SKILL.md` and `README.md` focused on workflow.
8. Never commit secrets, tokens, or private credentials.

## Naming

- Directory names: lowercase kebab-case.
- Skill names (`frontmatter.name`): unique across repository.
- Prefer `shengwang-` prefix for skill names.

## Pull Request Checklist

- [ ] Routing logic is still correct from `skills/voice-ai-integration/SKILL.md`.
- [ ] New or changed links are valid.
- [ ] No duplicate skill names.
- [ ] No orphaned files left behind.
- [ ] No hardcoded credentials.
- [ ] `scripts/validate-skills.sh` passes locally.

## Local Validation

```bash
bash scripts/validate-skills.sh
```
