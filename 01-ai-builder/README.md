# Phase 1 — AI Builder

[Course](https://www.udemy.com/course/ai-builder-with-n8n-create-agents-voice-agents/) · 14.3 hrs · weeks 1–8 · Aug 31 – Oct 23, 2026

Curriculum course 1, and where I started. Low-code agents in n8n: workflow automation against the
tools I already use, then ElevenLabs voice agents over a Supabase RAG store, then self-hosted n8n,
MCP and a multi-agent go-to-market capstone.

88 lectures in three sections — the course calls them weeks; at 2 hrs/week they take me eight.

## Modules

- [`01-automate/`](01-automate/) — Automate: workflows in n8n Cloud · 30 lectures · 4hr 58min
- [`02-accelerate/`](02-accelerate/) — Accelerate: voice agents and RAG · 25 lectures · 3hr 42min
- [`03-amplify/`](03-amplify/) — Amplify: multi-agent systems and MCP · 33 lectures · 5hr 41min

Every lecture and build, grouped by my study week with tick boxes: [`TASKS.md`](TASKS.md).

## Projects

Three, one per section. See the [projects index](../README.md#projects) on the repo home page.

## How work lands here

n8n is low-code, so the artefact is the workflow, not a source tree. Each project folder gets the
workflow exported as JSON plus a README on what it does and what it connects to.

**Export without credentials.** n8n's plain export embeds credential *references*, not secrets, but
check any JSON before committing it — no keys, no tokens, no account ids.

## Check on first import

The workflow JSON was written against n8n 2.x node versions but has not been imported yet. These
are the parameters most likely to need a touch in the editor the first time each one is opened:

- **Gmail draft** (`gmail-draft-replies`, `gtm-demo-booker`) — thread id and recipient on draft create.
- **Google Drive** (`rag-ingest`, `pdf-to-structured`) — download options for Google Docs conversion.
- **Supabase vector store** (`rag-ingest`, `voice-agent-backend`) — table and query name, tool mode.
- **MCP** (`mcp-server`, `gtm-lead-researcher`) — the server's production URL path and the client
  transport (streamable HTTP vs SSE).
- **Pipedrive** (`gtm-crm-writer`) — search result shape and person/deal association fields.
- **Google Calendar** (`gtm-demo-booker`) — availability output format and attendee fields.
- **Model names** — OpenRouter and Ollama model slugs change; pick a current one if one is refused.

When a workflow has run end to end, tick its line in [`TASKS.md`](TASKS.md) and set the project to ✅
on the [repo home page](../README.md#projects).
