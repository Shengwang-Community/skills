# Skills Runbook

Use this checklist before merging non-trivial changes.

## Preflight

1. Confirm the change belongs under `skills/`.
2. Confirm all edited skills keep a valid `SKILL.md` frontmatter.
3. Confirm links in edited markdown files still resolve.

## Routing Safety

1. Start at `skills/SKILL.md`.
2. Verify each route target exists.
3. Verify renamed skills are reflected in route tables.

## Content Safety

1. No hardcoded credentials.
2. Environment variables referenced from docs.
3. No machine-local absolute paths in skill content.

## Validation

```bash
bash scripts/validate-skills.sh
```

## Release Notes (Optional)

For larger changes, include:

1. Files changed
2. Routing behavior changes
3. Any migration note for existing users
