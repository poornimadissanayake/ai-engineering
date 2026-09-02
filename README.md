# AI Engineering

My work through the [complete AI Engineering curriculum](https://edwarddonner.com/curriculum/) by Ed Donner, at a committed pace of **2 hours per week**.

The required path is curriculum courses **4 → 5 → 6, in that order**: Core, then Agents, then Production. Validation is the projects — every one runnable, linked from the table below.

**Started:** 31 August 2026 · **Pace:** 2 hrs/week · **Required path target:** late May 2027

---

## Projects

What Ryan (or anyone) should scan first. Each row is a deliverable, not a lecture.

| Project | Module | What it does | Link | Status |
|---|---|---|---|---|
| Website summarizer | Core 1 | Fetches a page, summarizes it via Chat Completions | [`01-llm-engineering/01-first-llm-product/`](01-llm-engineering/01-first-llm-product/) | ⚪ |
| Multimodal chatbot | Core 2 | Gradio customer-service / multimodal agent | [`01-llm-engineering/02-multimodal-chatbot/`](01-llm-engineering/02-multimodal-chatbot/) | ⚪ |
| Meeting minutes | Core 3 | Automated write-up on a local / open-source model | [`01-llm-engineering/03-open-source/`](01-llm-engineering/03-open-source/) | ⚪ |
| Code-gen showdown | Core 4 | Same task across models; written pick and why | [`01-llm-engineering/04-model-selection/`](01-llm-engineering/04-model-selection/) | ⚪ |
| RAG knowledge worker | Core 5 | Embeddings + vector store + LangChain Q&A | [`01-llm-engineering/05-rag/`](01-llm-engineering/05-rag/) | ⚪ |
| Frontier fine-tune | Core 6 | Curated dataset and a fine-tuned frontier model | [`01-llm-engineering/06-training/`](01-llm-engineering/06-training/) | ⚪ |
| QLoRA bake-off | Core 7 | Open-source QLoRA vs base vs frontier | [`01-llm-engineering/07-fine-tuning/`](01-llm-engineering/07-fine-tuning/) | ⚪ |
| Autonomous agent | Core 8 | Multi-agent capstone + course certificate | [`01-llm-engineering/08-agents/`](01-llm-engineering/08-agents/) | ⚪ |

Agents and Production projects get added here when those phases start.

Legend: ⚪ not started · 🔵 in progress · ✅ done · ⏭️ watched at speed (project still built; note in the log)

---

## Progress

| Phase | Course | Hours | Weeks | Status |
|---|---|---:|---|---|
| 1 | [Core Track](https://www.udemy.com/course/llm-engineering-master-ai-and-large-language-models/) — LLMs, RAG, LangChain, fine-tuning | 33.5 | 1–17 | 🔵 In progress |
| 2 | [Agentic Track](https://www.udemy.com/course/the-complete-agentic-ai-engineering-course/) — agent loops, CrewAI, LangGraph, MCP | 21.0 | 18–28 | ⚪ Not started |
| 3 | [Production Track](https://www.udemy.com/course/generative-and-agentic-ai-in-production/) — Vercel, AWS, GCP, Azure, LangFuse | 18.7 | 29–37 | ⚪ Not started |

### After the required path

| Phase | Course | Hours | Status |
|---|---|---:|---|
| — | [AI Coder](https://www.udemy.com/course/ai-coder-from-vibe-coder-to-agentic-engineer/) — Claude Code, sub-agents, swarms | 16.3 | ⚪ Optional |
| — | [AI Builder](https://www.udemy.com/course/ai-builder-with-n8n-create-agents-voice-agents/) — n8n, voice agents | 14.3 | ⚪ Optional |
| — | [AI Leader](https://www.udemy.com/course/executive-briefing-generative-ai-and-large-language-models-llm/) — strategy, roadmaps | 3.8 | ⚪ Optional |

### Phase 1 — Core Track, week by week

| Wk | Dates | Module | Target | Built | Status |
|---:|---|---|---|---|---|
| 1 | Aug 31–Sep 4 | 1 · First LLM product | Env, Chat Completions API, first notebook | Repo scaffold, website summarizer | ⚪ |
| 2 | Sep 7–11 | 1 · First LLM product | Prompting; compare frontier models | Multi-model comparison note | ⚪ |
| 3 | Sep 14–18 | 1 · First LLM product | Finish the week 1 commercial project | Runnable summarizer app | ⚪ |
| 4 | Sep 21–25 | 2 · Multimodal chatbot | Frontier APIs, Gradio UI | Gradio chatbot shell | ⚪ |
| 5 | Sep 28–Oct 2 | 2 · Multimodal chatbot | Customer-service + multimodal agent | Chatbot project | ⚪ |
| 6 | Oct 5–9 | 3 · Open source | Hugging Face, Ollama, local models | Local model run + notes | ⚪ |
| 7 | Oct 12–16 | 3 · Open source | Automated solution with open-source | Meeting-minutes project | ⚪ |
| 8 | Oct 19–23 | 4 · Model selection | Evaluate models for code and business tasks | Evaluation notebook | ⚪ |
| 9 | Oct 26–30 | 4 · Model selection | Code-generation showdown | Code-gen comparison + pick | ⚪ |
| 10 | Nov 2–6 | 5 · RAG | Embeddings, vector stores, LangChain | First RAG pipeline | ⚪ |
| 11 | Nov 9–13 | 5 · RAG | Knowledge-worker project | End-to-end RAG app | ⚪ |
| 12 | Nov 16–20 | 6 · Training | Data curation for fine-tuning | Curated dataset in repo | ⚪ |
| 13 | Nov 23–27 | 6 · Training | Fine-tune a frontier model | Fine-tune run + eval notes | ⚪ |
| 14 | Nov 30–Dec 4 | 7 · Fine-tuning OSS | QLoRA setup and training loop | QLoRA notebook | ⚪ |
| 15 | Dec 7–11 | 7 · Fine-tuning OSS | Open-source vs frontier bake-off | Eval against base + frontier | ⚪ |
| 16 | Dec 14–18 | 8 · Agentic system | Multi-agent architecture | Agent scaffolding | ⚪ |
| 17 | Jan 4–8 | 8 · Agentic system | Capstone + certificate | Autonomous agent + certificate | ⚪ |

Dec 21–Jan 1 is a holiday buffer. The capstone is the first full week of January, not Christmas week.

---

## Repository layout

```
01-llm-engineering/  Phase 1 — Core Track (curriculum 4)
  01-first-llm-product/   frontier APIs, first commercial project
  02-multimodal-chatbot/  Gradio UI, multimodal / customer-service agent
  03-open-source/         Hugging Face, Ollama, local models
  04-model-selection/     evaluating models for code and business tasks
  05-rag/                 embeddings, vector stores, LangChain
  06-training/            data curation, fine-tuning a frontier model
  07-fine-tuning/         QLoRA on open-source
  08-agents/              autonomous multi-agent capstone
02-agentic/          Phase 2 — Agentic Track (curriculum 5)
  01-foundations/      agents from scratch, no framework
  02-openai-sdk/       OpenAI Agents SDK
  03-crewai/           CrewAI crews
  04-langgraph/        LangChain / LangGraph
  05-frameworks/       AutoGen, Google ADK, Pydantic AI
  06-mcp/              Model Context Protocol servers & clients
03-production/       Phase 3 — Production Track (curriculum 6)
04-ai-coder/         optional — after 4, 5, 6
05-ai-builder/       optional — after 4, 5, 6
06-ai-leader/        optional — after 4, 5, 6
LEARNING-LOG.md      one entry per week: covered, built, watched at speed, takeaways
```

Each project folder has its own README with what it does and how to run it.

---

## Running anything here

```bash
git clone https://github.com/poornimadissanayake/ai-engineering.git
cd ai-engineering
cp .env.example .env        # add your own API keys
uv sync                     # or: pip install -r requirements.txt
```

`pyproject.toml` / `requirements.txt` cover the Core Track baseline (OpenAI, Jupyter, Gradio). Later modules that need heavier stacks (Hugging Face, QLoRA) add extras in that folder's README.

Projects call frontier model APIs and need your own keys. Where a course offers a local
alternative (Ollama, DeepSeek), the project README notes it.

**No secrets are committed to this repo.** `.env` is gitignored; `.env.example` lists the
variable names only.

---

## Why the phases are in this order

The required path is Ed Donner's AI Engineer tracks **in curriculum order: 4, then 5, then 6** — Core, Agents, Production. Validation is the projects in this repo.

Builder, Coder, and Leader sit after that. Azure, other clouds, and certs are fine once 4–6 are done.

Video I already work in daily I watch at speed. Every project still gets built. Anything treated that way is noted in [LEARNING-LOG.md](LEARNING-LOG.md).

---

## Certificates

| Course | Certificate | Date |
|---|---|---|
| Core Track | — | — |
| Agentic Track | — | — |
| Production Track | — | — |
| AI Coder | — | — |
| AI Builder | — | — |
| AI Leader | — | — |
