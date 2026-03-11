# OpenHands development workflow

This repo uses [OpenHands](https://github.com/All-Hands-AI/OpenHands) so that **coding issues can be handled by an AI agent**: someone opens an issue, the workflow runs the agent, and a draft PR (or branch) is created.

The workflow is **generic** and can be copied to any repository.

---

## How to use it

1. **Create an issue** describing the coding task (bug fix, feature, refactor, etc.).
2. **Trigger the agent** in one of these ways:
   - **Label** (recommended): Add one of these labels to the issue (or PR):
     - **`fix-me`** – Existing project; agent implements or fixes what the issue describes.
     - **`create-project`** – Empty or bootstrap repo; agent creates the project from the issue.
     - **`fix-me-experimental`** – Same as `fix-me` but uses the latest OpenHands dev build.
   - **Comment**: In the issue or on a PR review, write a comment that contains **`@openhands-agent`**. Only OWNER/COLLABORATOR/MEMBER can trigger this way.
3. The workflow runs, then:
   - On **success**: A **draft PR** is created and linked in a comment.
   - On **failure**: A **branch** is created and linked so you can inspect partial work.

You can also run the workflow **manually** from the **Actions** tab: choose “OpenHands – Resolve issue / PR”, use “Run workflow”, and set the issue (or PR) number.

---

## One-time setup (repo and secrets)

1. **Workflow file**  
   Ensure `.github/workflows/openhands-resolver.yml` is present (this repo already has it).

2. **Permissions**  
   In the repo: **Settings → Actions → General → Workflow permissions**  
   - Choose **Read and write permissions**.  
   - Enable **Allow GitHub Actions to create and approve pull requests** (if available).

3. **Secrets** (Settings → Secrets and variables → Actions):
   - **`LLM_API_KEY`** (required): API key for the LLM (e.g. Anthropic Claude, OpenAI).  
   - **`PAT_TOKEN`** (optional): Personal access token with `contents`, `issues`, `pull requests`, `workflows` (read/write). If unset, the default `GITHUB_TOKEN` is used.  
   - **`PAT_USERNAME`** (optional): GitHub username for the PAT; used for commit/PR attribution.  
   - **`LLM_MODEL`** (optional): Model identifier (e.g. `anthropic/claude-sonnet-4-20250514`).  
   - **`LLM_BASE_URL`** (optional): Base URL when using an API proxy.  
   - **`CODEX_API_KEY`** (optional): If set, used instead of `LLM_API_KEY` (e.g. for OpenAI Codex).

4. **Labels**  
   Create these labels in the repo if you use them: `fix-me`, `create-project`, `fix-me-experimental`.

---

## Optional: project-specific agent instructions

To steer how the agent works in **this** repo (tech stack, tests, conventions), add or edit:

**`.openhands/microagents/repo.md`**

Put there:

- Tech stack and package manager.
- How to install deps, run the app, run tests, run lint/format.
- Code style and where to add new code.

The resolver loads this file into the agent’s context. See the template in this repo and [OpenHands – Providing custom instructions](https://github.com/OpenHands/OpenHands/blob/main/openhands/resolver/README.md#providing-custom-instructions).

---

## Optional: customizing the workflow

When you **call** this workflow from another workflow (`workflow_call`) or run it **manually** (`workflow_dispatch`), you can pass inputs, for example:

- **`target_branch`**: Branch to open the PR against (default `main`).
- **`pr_type`**: `draft` or `ready`.
- **`max_iterations`**: Cap on agent steps (default `50`).
- **`LLM_MODEL`**, **`base_container_image`**, **`runner`**: Model, sandbox image, and runner.

For more options, see the workflow file and [OpenHands GitHub Action – Custom configurations](https://docs.openhands.dev/usage/how-to/github-action#custom-configurations).

---

## Summary

| You want to…                    | Do this…                                                                 |
|---------------------------------|---------------------------------------------------------------------------|
| Have the agent fix an issue     | Add label **`fix-me`** (or comment **`@openhands-agent`**) on the issue. |
| Have the agent bootstrap a repo | Add label **`create-project`** on the issue.                             |
| Run the agent manually          | Actions → “OpenHands – Resolve issue / PR” → Run workflow + issue number. |
| Tell the agent how this repo works | Edit **`.openhands/microagents/repo.md`**.                            |

No extra config files are required beyond the workflow and, optionally, `.openhands/microagents/repo.md`.
