# AI Engineering

My work through the [complete AI Engineering curriculum](https://edwarddonner.com/curriculum/) by Ed Donner, at a committed pace of **2 hours per week**.

The required path is curriculum courses **4 → 5 → 6, in that order**: Core, then Agents, then Production. Every project here is runnable. Every week is logged. The progress table below is the status report.

**Started:** 7 September 2026 · **Pace:** 2 hrs/week · **Required path target:** May 2027

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
| 1 | Sep 7–13 | 1 · First LLM product | Env, Chat Completions API, first notebook | Repo scaffold, website summarizer | ⚪ |
| 2 | Sep 14–20 | 1 · First LLM product | Prompting; compare frontier models | Multi-model comparison note | ⚪ |
| 3 | Sep 21–27 | 1 · First LLM product | Finish the week 1 commercial project | Runnable summarizer app | ⚪ |
| 4 | Sep 28–Oct 4 | 2 · Multimodal chatbot | Frontier APIs, Gradio UI | Gradio chatbot shell | ⚪ |
| 5 | Oct 5–11 | 2 · Multimodal chatbot | Customer-service + multimodal agent | Chatbot project | ⚪ |
| 6 | Oct 12–18 | 3 · Open source | Hugging Face, Ollama, local models | Local model run + notes | ⚪ |
| 7 | Oct 19–25 | 3 · Open source | Automated solution with open-source | Meeting-minutes project | ⚪ |
| 8 | Oct 26–Nov 1 | 4 · Model selection | Evaluate models for code and business tasks | Evaluation notebook | ⚪ |
| 9 | Nov 2–8 | 4 · Model selection | Code-generation showdown | Code-gen comparison + pick | ⚪ |
| 10 | Nov 9–15 | 5 · RAG | Embeddings, vector stores, LangChain | First RAG pipeline | ⚪ |
| 11 | Nov 16–22 | 5 · RAG | Knowledge-worker project | End-to-end RAG app | ⚪ |
| 12 | Nov 23–29 | 6 · Training | Data curation for fine-tuning | Curated dataset in repo | ⚪ |
| 13 | Nov 30–Dec 6 | 6 · Training | Fine-tune a frontier model | Fine-tune run + eval notes | ⚪ |
| 14 | Dec 7–13 | 7 · Fine-tuning OSS | QLoRA setup and training loop | QLoRA notebook | ⚪ |
| 15 | Dec 14–20 | 7 · Fine-tuning OSS | Open-source vs frontier bake-off | Eval against base + frontier | ⚪ |
| 16 | Dec 21–27 | 8 · Agentic system | Multi-agent architecture | Agent scaffolding | ⚪ |
| 17 | Dec 28–Jan 3 | 8 · Agentic system | Capstone + certificate | Autonomous agent + certificate | ⚪ |

Legend: ⚪ not started · 🔵 in progress · ✅ done · ⏭️ skipped (reason in the log)

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
LEARNING-LOG.md      one entry per week: covered, built, skipped, takeaways
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

Projects call frontier model APIs and need your own keys. Where a course offers a local
alternative (Ollama, DeepSeek), the project README notes it.

**No secrets are committed to this repo.** `.env` is gitignored; `.env.example` lists the
variable names only.

---

## Why the phases are in this order

The required path is Ed Donner's AI Engineer tracks **in curriculum order: 4, then 5, then 6** — Core, Agents, Production. Validation is the projects in this repo, not course-watching alone.

Builder, Coder, and Leader sit after that. Azure, other clouds, and certs are fine once 4–6 are done.

Sections covering ground I already work in daily are skipped deliberately rather than
sat through — every skip is recorded in [LEARNING-LOG.md](LEARNING-LOG.md) with the reason,
so the decision is auditable.

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
