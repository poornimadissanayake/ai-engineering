# Module 3 — Amplify

Multi-agent systems and MCP. Self-hosted n8n on Docker with Ollama and DeepSeek through OpenRouter,
then Firecrawl scraping and PDF extraction, then MCP end to end — host, client and server, including
writing my own server in n8n and connecting Claude to it. Closes on context engineering, the lethal
trifecta of agent security risks, and sub-workflow orchestration.

**Projects:** My own MCP server in n8n · GTM capstone — multi-agent lead generation that finds leads
via MCP (Firecrawl, Hunter.io), creates and nurtures them in Pipedrive, and books demos on Google
Calendar

## Running this

Self-hosted n8n via Docker Desktop for most of this module:

```bash
docker volume create n8n_data
docker run -it --rm -p 5678:5678 -v n8n_data:/home/node/.n8n docker.n8n.io/n8nio/n8n
```

Then open http://localhost:5678, import the workflow JSON and reconnect credentials.

Accounts this module needs: OpenRouter (DeepSeek), Ollama locally, Firecrawl, Hunter.io, Tavily,
Pipedrive, Google Calendar.

Setup notes per project go here as they are built.
