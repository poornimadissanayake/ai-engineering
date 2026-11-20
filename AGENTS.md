# AGENTS.md

Context for any coding agent working in this repo. Kept short on purpose: everything here is loaded
into the context window on every turn, so it carries only what an agent cannot work out by reading
the code.

## What this repo is

My work through Ed Donner's six-course AI Engineering curriculum. One folder per course, one
sub-folder per project. Each project stands alone — its own README, its own dependencies, its own
run command. Nothing is shared between projects except the root `.env.example`.

## Layout

- `01-ai-builder/` — n8n workflows, committed as exported JSON. No code to run here.
- `02-ai-coder/` — full-stack projects (Next.js, FastAPI). Each has its own `AGENTS.md`; read that
  one first when working inside it.
- `04-llm-engineering/`, `05-agentic/`, `06-production/` — Python, managed with `uv` from the root
  `pyproject.toml` unless a project folder has its own.
- `TASKS.md` in each course folder is the lecture and build checklist. `LEARNING-LOG.md` is mine —
  do not write to it.

## Rules

- **Secrets never land in the repo.** Keys go in `.env` / `.env.local` (git-ignored). n8n
  exports carry credential references only; replace ids, emails, phone numbers and sheet ids with
  `YOUR_…` placeholders before committing.
- **Stay in the project folder you were asked to work in.** Do not touch sibling projects or the
  root README unless asked.
- **Every project must run from a fresh clone** with the commands in its README. If you change how
  something runs, change the README in the same commit.
- **Tests before claims.** A project with tests is not done until they pass locally; say which
  command you ran.
- **Cheap models by default.** Course projects call OpenRouter or OpenAI; default to a small model
  and read the model name from an environment variable.
- **Ask before adding a dependency** that a project does not already use.

## Commands

```bash
uv sync                              # Python baseline (phases 4–6)
cd 02-ai-coder/01-digital-twin && npm install && npm run dev
cd 02-ai-coder/02-kanban && uv sync && uv run pytest -q
```
