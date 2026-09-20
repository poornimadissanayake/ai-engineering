# Phase 1 — AI Builder

[Course](https://www.udemy.com/course/ai-builder-with-n8n-create-agents-voice-agents/) · 14.3 hrs · weeks 1–8 · Aug 31 – Oct 23, 2026

Curriculum course 1, and where I started. Low-code agents in n8n: workflow automation against the
tools I already use, then ElevenLabs voice agents over a Supabase RAG store, then self-hosted n8n,
MCP and a multi-agent go-to-market capstone.

88 lectures in three sections — the course calls them weeks; at 2 hrs/week they take me eight.

## Modules

- [`01-automate/`](01-automate/) — Automate: workflows in n8n Cloud
- [`02-accelerate/`](02-accelerate/) — Accelerate: voice agents and RAG
- [`03-amplify/`](03-amplify/) — Amplify: multi-agent systems and MCP

## Projects

Three, one per section. See the [projects index](../README.md#projects) on the repo home page.

## How work lands here

n8n is low-code, so the artefact is the workflow, not a source tree. Each project folder gets the
workflow exported as JSON plus a README on what it does and what it connects to.

**Export without credentials.** n8n's plain export embeds credential *references*, not secrets, but
check any JSON before committing it — no keys, no tokens, no account ids.
