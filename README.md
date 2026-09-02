# AI Engineering

My work through the [complete AI Engineering curriculum](https://edwarddonner.com/curriculum/) by Ed Donner — six courses, 107.5 hours of content, at a committed pace of **2 hours per week**.

Every project here is runnable. Every week is logged. The progress table below is the status report.

**Started:** 7 September 2026 · **Pace:** 2 hrs/week · **Target completion:** September 2027

---

## Progress

| Phase | Course | Hours | Weeks | Status |
|---|---|---:|---|---|
| 1 | [Agentic Track](https://www.udemy.com/course/the-complete-agentic-ai-engineering-course/) — agents, frameworks, MCP | 21.0 | 1–11 | 🔵 In progress |
| 2 | [AI Coder](https://www.udemy.com/course/ai-coder-from-vibe-coder-to-agentic-engineer/) — Claude Code, sub-agents, swarms | 16.3 | 12–19 | ⚪ Not started |
| 3 | [Production Track](https://www.udemy.com/course/generative-and-agentic-ai-in-production/) — deploy, IaC, observability | 18.7 | 20–28 | ⚪ Not started |
| 4 | [Core Track](https://www.udemy.com/course/llm-engineering-master-ai-and-large-language-models/) — RAG, fine-tuning | 33.5 | 29–45 | ⚪ Not started |
| 5 | [AI Builder](https://www.udemy.com/course/ai-builder-with-n8n-create-agents-voice-agents/) — n8n, voice agents | 14.3 | 46–52 | ⚪ Not started |
| 6 | [AI Leader](https://www.udemy.com/course/executive-briefing-generative-ai-and-large-language-models-llm/) — strategy, roadmaps | 3.8 | 53–54 | ⚪ Not started |

### Phase 1 — Agentic Track, week by week

| Wk | Dates | Module | Target | Built | Status |
|---:|---|---|---|---|---|
| 1 | Sep 7–13 | 1 · Foundations | Agentic landscape, LLM API mechanics, environment setup | Repo scaffold, first notebook run | ⚪ |
| 2 | Sep 14–20 | 1 · Foundations | Raw tool calling, the agent loop, state by hand | Hand-rolled tool-calling loop, no framework | ⚪ |
| 3 | Sep 21–27 | 1 · Foundations | Project: Career Digital Twin + web deploy | Deployed agent (live URL) | ⚪ |
| 4 | Sep 28–Oct 4 | 2 · OpenAI Agents SDK | Agents, runners, sessions, structured outputs, guardrails | Hand-rolled vs. SDK comparison note | ⚪ |
| 5 | Oct 5–11 | 2 · OpenAI Agents SDK | Handoffs, agents-as-tools; sales team + Deep Research projects | 2 multi-agent projects | ⚪ |
| 6 | Oct 12–18 | 3 · CrewAI | Roles, goals, tasks; YAML crews; sequential vs. hierarchical | A working crew + its config | ⚪ |
| 7 | Oct 19–25 | 3 · CrewAI | Projects: Stock Picker, Engineering Team | 2 projects + review-quality notes | ⚪ |
| 8 | Oct 26–Nov 1 | 4 · LangGraph | State graphs, conditional routing, checkpointing; Sidekick | Checkpointed graph agent | ⚪ |
| 9 | Nov 2–8 | 5 · Frameworks | AutoGen, Google ADK, AWS Strands, Pydantic AI; Agent Creator | Framework decision matrix | ⚪ |
| 10 | Nov 9–15 | 6 · MCP | MCP architecture; building a server and client | My own MCP server | ⚪ |
| 11 | Nov 16–22 | 6 · MCP | Capstone: multi-agent Trading Floor over MCP | Capstone + certificate | ⚪ |

Legend: ⚪ not started · 🔵 in progress · ✅ done · ⏭️ skipped (reason in the log)

---

## Repository layout

```
01-agentic/          Phase 1 — agents, frameworks, MCP
  01-foundations/      agents from scratch, no framework
  02-openai-sdk/       OpenAI Agents SDK
  03-crewai/           CrewAI crews
  04-langgraph/        LangChain / LangGraph
  05-frameworks/       AutoGen, Google ADK, Pydantic AI
  06-mcp/              Model Context Protocol servers & clients
02-ai-coder/         Phase 2 — agentic coding, Claude Code, sub-agents
03-production/       Phase 3 — deployment, IaC, observability, guardrails
04-llm-engineering/  Phase 4 — RAG, data curation, fine-tuning
05-ai-builder/       Phase 5 — n8n automations, voice agents
06-ai-leader/        Phase 6 — strategy notes and capability roadmap
LEARNING-LOG.md      one entry per week: covered, built, skipped, takeaways
```

Each project folder has its own README with what it does and how to run it.

---

## Running anything here

```bash
git clone https://github.com/<my-handle>/ai-engineering.git
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

The curriculum's default order starts with the low-code and leadership material. I resequenced
it by relevance to my work as an AI engineer on Arcadea's central AI team: agents and MCP first
(Phase 1), then the agentic coding toolchain I use daily (Phase 2), then production deployment
(Phase 3). The depth and breadth tracks follow. If the plan is ever cut short, the most
valuable material is already done and in this repo.

Sections covering ground I already work in daily are skipped deliberately rather than
sat through — every skip is recorded in [LEARNING-LOG.md](LEARNING-LOG.md) with the reason,
so the decision is auditable.

---

## Certificates

| Course | Certificate | Date |
|---|---|---|
| Agentic Track | — | — |
| AI Coder | — | — |
| Production Track | — | — |
| Core Track | — | — |
| AI Builder | — | — |
| AI Leader | — | — |
