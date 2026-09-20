# AI Engineering

My work through the [complete AI Engineering curriculum](https://edwarddonner.com/curriculum/) by Ed Donner, at a committed pace of **2 hours per week**.

All six courses, in the curriculum's own order **1 → 6**: Builder, Coder, Leader, then Core, Agents, Production. Validation is the projects — every one runnable, linked from the table below.

**Started:** 31 August 2026 · **Pace:** 2 hrs/week · **Total:** 107.6 hrs over 55 weeks · **Target:** early October 2027

---

## Projects

Each row is a project I build, not a lecture.

| Project | Module | What it does | Link | Status |
|---|---|---|---|---|
| Portfolio rebalancer | Builder 1 | Monitors MarketStack prices and rebalances a Google Sheets portfolio | [`01-ai-builder/01-automate/`](01-ai-builder/01-automate/) | ⚪ |
| Voice agent | Builder 2 | ElevenLabs + Twilio phone agent answering from a Supabase RAG store | [`01-ai-builder/02-accelerate/`](01-ai-builder/02-accelerate/) | ⚪ |
| GTM multi-agent system | Builder 3 | Finds leads via MCP, enriches them into Pipedrive, books demos | [`01-ai-builder/03-amplify/`](01-ai-builder/03-amplify/) | ⚪ |
| Website summarizer | Core 1 | Fetches a page, summarizes it via Chat Completions | [`04-llm-engineering/01-first-llm-product/`](04-llm-engineering/01-first-llm-product/) | ⚪ |
| Multimodal chatbot | Core 2 | Gradio customer-service / multimodal agent | [`04-llm-engineering/02-multimodal-chatbot/`](04-llm-engineering/02-multimodal-chatbot/) | ⚪ |
| Meeting minutes | Core 3 | Automated write-up on a local / open-source model | [`04-llm-engineering/03-open-source/`](04-llm-engineering/03-open-source/) | ⚪ |
| Code-gen showdown | Core 4 | Same task across models; written pick and why | [`04-llm-engineering/04-model-selection/`](04-llm-engineering/04-model-selection/) | ⚪ |
| RAG knowledge worker | Core 5 | Embeddings + vector store + LangChain Q&A | [`04-llm-engineering/05-rag/`](04-llm-engineering/05-rag/) | ⚪ |
| Frontier fine-tune | Core 6 | Curated dataset and a fine-tuned frontier model | [`04-llm-engineering/06-training/`](04-llm-engineering/06-training/) | ⚪ |
| QLoRA bake-off | Core 7 | Open-source QLoRA vs base vs frontier | [`04-llm-engineering/07-fine-tuning/`](04-llm-engineering/07-fine-tuning/) | ⚪ |
| Autonomous agent | Core 8 | Multi-agent capstone + course certificate | [`04-llm-engineering/08-agents/`](04-llm-engineering/08-agents/) | ⚪ |

Coder, Leader, Agents and Production projects get added here when those phases start.

Legend: ⚪ not started · 🔵 in progress · ✅ done · ⏭️ watched at speed (project still built; note in the log)

---

## Progress

| Phase | Course | Hours | Weeks | Status |
|---|---|---:|---|---|
| 1 | [AI Builder](https://www.udemy.com/course/ai-builder-with-n8n-create-agents-voice-agents/) — n8n, voice agents, MCP | 14.3 | 1–8 | 🔵 In progress |
| 2 | [AI Coder](https://www.udemy.com/course/ai-coder-from-vibe-coder-to-agentic-engineer/) — Claude Code, sub-agents, swarms | 16.3 | 9–16 | ⚪ Not started |
| 3 | [AI Leader](https://www.udemy.com/course/executive-briefing-generative-ai-and-large-language-models-llm/) — strategy, roadmaps | 3.8 | 17–18 | ⚪ Not started |
| 4 | [Core Track](https://www.udemy.com/course/llm-engineering-master-ai-and-large-language-models/) — LLMs, RAG, LangChain, fine-tuning | 33.5 | 19–35 | ⚪ Not started |
| 5 | [Agentic Track](https://www.udemy.com/course/the-complete-agentic-ai-engineering-course/) — agent loops, CrewAI, LangGraph, MCP | 21.0 | 36–46 | ⚪ Not started |
| 6 | [Production Track](https://www.udemy.com/course/generative-and-agentic-ai-in-production/) — Vercel, AWS, GCP, Azure, LangFuse | 18.7 | 47–55 | ⚪ Not started |

Dec 21, 2026 – Jan 1, 2027 is a holiday buffer, and it falls on a phase boundary: AI Coder finishes
the week before, AI Leader starts the first full week of January.

### Phase 1 — AI Builder, week by week

The course runs as three "weeks" of five days, 88 lectures. At 2 hrs/week that is eight of mine.

| Wk | Dates | Module | Target | Built | Status |
|---:|---|---|---|---|---|
| 1 | Aug 31–Sep 4 | 1 · Automate | n8n Cloud setup; first agent on OpenRouter / OpenAI; what an agent actually is | First n8n agent workflow | ⚪ |
| 2 | Sep 7–11 | 1 · Automate | Tool calling, evaluating agents; canvas, nodes, triggers; Sheets + Drive | Gmail draft-reply agent | ⚪ |
| 3 | Sep 14–18 | 1 · Automate | JSON, expressions, OAuth2, webhooks; Telegram, Slack, Pushover; If nodes | Portfolio rebalancer — Project 1 | ⚪ |
| 4 | Sep 21–25 | 2 · Accelerate | ElevenLabs Agent Platform; agent tools, widgets, n8n webhooks | First voice agent | ⚪ |
| 5 | Sep 28–Oct 2 | 2 · Accelerate | RAG and embeddings; Supabase vector store; Twilio phone number | Voice agent — Project 2 | ⚪ |
| 6 | Oct 5–9 | 3 · Amplify | Cloud vs self-hosted; n8n on Docker; Ollama and DeepSeek | Self-hosted n8n instance | ⚪ |
| 7 | Oct 12–16 | 3 · Amplify | Firecrawl, PDF extraction; MCP host / client / server; Hunter.io | My own MCP server in n8n | ⚪ |
| 8 | Oct 19–23 | 3 · Amplify | Context engineering, the lethal trifecta; Pipedrive SDR; sub-workflows | GTM capstone — Project 3 + certificate | ⚪ |

---

## Repository layout

```
01-ai-builder/       Phase 1 — AI Builder (curriculum 1)
  01-automate/         n8n Cloud workflows; Sheets, Gmail, Slack, Telegram
  02-accelerate/       ElevenLabs voice agents, Supabase RAG, Twilio
  03-amplify/          self-hosted n8n, MCP, multi-agent GTM capstone
02-ai-coder/         Phase 2 — AI Coder (curriculum 2)
03-ai-leader/        Phase 3 — AI Leader (curriculum 3)
04-llm-engineering/  Phase 4 — Core Track (curriculum 4)
  01-first-llm-product/   frontier APIs, first commercial project
  02-multimodal-chatbot/  Gradio UI, multimodal / customer-service agent
  03-open-source/         Hugging Face, Ollama, local models
  04-model-selection/     evaluating models for code and business tasks
  05-rag/                 embeddings, vector stores, LangChain
  06-training/            data curation, fine-tuning a frontier model
  07-fine-tuning/         QLoRA on open-source
  08-agents/              autonomous multi-agent capstone
05-agentic/          Phase 5 — Agentic Track (curriculum 5)
  01-foundations/      agents from scratch, no framework
  02-openai-sdk/       OpenAI Agents SDK
  03-crewai/           CrewAI crews
  04-langgraph/        LangChain / LangGraph
  05-frameworks/       AutoGen, Google ADK, Pydantic AI
  06-mcp/              Model Context Protocol servers & clients
06-production/       Phase 6 — Production Track (curriculum 6)
LEARNING-LOG.md      one entry per week: covered, built, watched at speed, takeaways
```

Each project folder has its own README with what it does and how to run it.

---

## Running anything here

```bash
git clone https://github.com/poornimadissanayake/ai-engineering.git
cd ai-engineering
cp .env.example .env        # add your own API keys
```

**Phase 1 needs no Python.** AI Builder runs in n8n — workflows are committed as exported JSON and
imported into n8n Cloud, with credentials reconnected in n8n's own credential store. Module 3
self-hosts n8n on Docker; that command is in [`01-ai-builder/03-amplify/`](01-ai-builder/03-amplify/).
Phase 2 is driven from the Claude Code CLI, and phase 3 produces writing rather than code.

**Phases 4–6 are Python.** From phase 4 on:

```bash
uv sync                     # or: pip install -r requirements.txt
```

`pyproject.toml` / `requirements.txt` cover the Core Track baseline (OpenAI, Jupyter, Gradio).
Later modules that need heavier stacks (Hugging Face, QLoRA) add extras in that folder's README.

Projects call frontier model APIs and need your own keys. Where a course offers a local
alternative (Ollama, DeepSeek), the project README notes it.

**No secrets are committed to this repo.** `.env` is gitignored; `.env.example` lists the
variable names only. n8n workflow exports get checked for embedded keys before they land here.

---

## Why the phases are in this order

Straight down Ed Donner's curriculum, 1 to 6. He says the six courses complement each other and
can be taken in any order, but that the listed order is the most natural progression — and he names
AI Builder as one of two recommended starting points: use products to build agents, then use agents
to build products.

So I started in n8n. Low-code first means working agents in week one, and the concepts that carry
into the Core Track — tool calling, RAG, MCP, context engineering — arrive attached to something
that already runs. The engineering half then rebuilds them properly in Python.

Video I already work in daily I watch at speed. Every project still gets built. Anything treated
that way is noted in [LEARNING-LOG.md](LEARNING-LOG.md).

---

## Certificates

| Course | Certificate | Date |
|---|---|---|
| AI Builder | — | — |
| AI Coder | — | — |
| AI Leader | — | — |
| Core Track | — | — |
| Agentic Track | — | — |
| Production Track | — | — |
