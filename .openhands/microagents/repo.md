# Repository instructions for OpenHands

This file is loaded by the OpenHands resolver when working on this repo. Customize it so the agent follows your stack and conventions.

## What to add here

- **Tech stack**: Languages, frameworks, package manager (npm/pip/cargo/etc.).
- **Setup**: How to install dependencies and run the project locally.
- **Testing**: How to run tests (e.g. `npm test`, `pytest`, `cargo test`).
- **Linting/formatting**: Linter and formatter commands, and that changes should pass them.
- **Conventions**: Code style, naming, where to put new files, any project-specific rules.
- **Relevant docs**: Links to internal docs or key external docs the agent should follow.

## Example (replace with your project)

```markdown
- This is a Node/TypeScript project. Use npm; do not use yarn or pnpm.
- Setup: `npm ci`. Run app: `npm start`. Tests: `npm test`. Lint: `npm run lint`.
- New features go under `src/`. Follow existing patterns in the codebase.
- Prefer existing utilities in `src/utils/` before adding new dependencies.
```

Keep this file under version control and update it when your setup or conventions change.
