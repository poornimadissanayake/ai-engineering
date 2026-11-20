# Module 3 — Amplify

33 lectures · 5hr 41min · weeks 6–8

Multi-agent systems and MCP. Self-hosted n8n on Docker with Ollama and DeepSeek through OpenRouter,
then Firecrawl scraping and PDF extraction, then MCP end to end — host, client and server, including
writing my own server in n8n and connecting Claude to it. Closes on context engineering, the lethal
trifecta of agent security risks, and sub-workflow orchestration.

**Projects:** My own MCP server in n8n · GTM capstone — multi-agent lead generation that finds leads
via MCP (Firecrawl, Hunter.io), creates and nurtures them in Pipedrive, and books demos on Google
Calendar

## Running this

Self-hosted n8n via Docker Desktop for most of this module. [`docker-compose.yml`](docker-compose.yml)
runs n8n and Ollama side by side on one network:

```bash
docker compose up -d
docker compose exec ollama ollama pull llama3.2
```

Then open http://localhost:5678, import the workflow JSON and reconnect credentials. From inside
n8n, Ollama is at `http://ollama:11434` (not `localhost` — that would be the n8n container itself).
Set `GENERIC_TIMEZONE` in a `.env` file next to the compose file; it defaults to UTC.

If I only want n8n, the plain version still works and uses the same `n8n_data` volume:

```bash
docker volume create n8n_data
docker run -it --rm -p 5678:5678 -v n8n_data:/home/node/.n8n docker.n8n.io/n8nio/n8n
```

Accounts this module needs: OpenRouter (DeepSeek), Ollama locally, Firecrawl, Hunter.io, Tavily,
Pipedrive, Google Calendar.

No credentials are in any file here. Every JSON has placeholders in capitals (`YOUR_GOOGLE_SHEET_ID`
and so on) and expects credentials to be connected in n8n's own credential store after import.

Built against n8n 2.x node versions. On an older instance n8n flags the version on import and
I can pin it down from there.

---

## Project — Local agent (Day 1)

[`local-agent.json`](local-agent.json) · 6 nodes · import straight into n8n

A chat agent that runs entirely on my machine. The n8n chat window feeds an AI Agent backed by
Llama 3.2 on Ollama, with a 10-message window of memory. Next to it sits a disabled OpenRouter
model set to DeepSeek, so I can compare a local model with a hosted one on the same prompt.

### Setup

1. `docker compose up -d`, then pull the model: `docker compose exec ollama ollama pull llama3.2`.
2. Import the JSON.
3. Create an **Ollama** credential with Base URL `http://ollama:11434` and attach it to
   **Ollama Chat Model**. The base URL lives on the credential, not on the node, which is why it
   isn't in the JSON.
4. Open the chat (bottom of the canvas) and talk to it.
5. To swap in DeepSeek: create an **OpenRouter** credential, enable **OpenRouter Chat Model
   (DeepSeek)**, remove the Ollama link to the agent and connect OpenRouter to the agent's
   Chat Model input instead.

On Docker Desktop for Mac, Ollama runs on CPU only, so the first reply is slow while the model
loads. That's the trade: nothing leaves the machine, but it's not quick.

---

## Project — PDF invoice to sheet (Day 2)

[`pdf-to-structured.json`](pdf-to-structured.json) · 10 nodes · import straight into n8n

Drop an invoice PDF into a Google Drive folder and, within a minute, a row appears in a Google
Sheet with the supplier, invoice number, dates, currency, subtotal, tax, total and a one-line
summary of the line items. Anything that isn't a PDF is skipped.

The extraction is a Basic LLM Chain with a Structured Output Parser, so the model has to return
JSON in a fixed schema rather than prose. A Code node flattens that into one sheet row.

### Setup

1. Make a Drive folder for incoming invoices and copy its id (the last part of the folder URL)
   into **New File in Folder** — it says `YOUR_DRIVE_FOLDER_ID`.
2. Make a spreadsheet with a tab called `Invoices`. The header row is in
   [`invoice-log-template.csv`](invoice-log-template.csv) (File → Import → Upload → Insert new
   sheet, then rename the tab). Put the spreadsheet id into **Append to Sheet**.
3. Connect credentials:
   - Google Drive OAuth2, on **New File in Folder** and **Download PDF**
   - Google Sheets OAuth2, on **Append to Sheet**
   - OpenRouter, on **OpenRouter Chat Model**
4. Upload one invoice, then execute the workflow once by hand before activating it.

### How it works

Extract From File only reads PDFs with a text layer. A scanned image of an invoice comes out
empty and needs OCR first. The schema is in **Invoice Schema** — add a field there and it shows
up in the output; add the same name to **Flatten Fields** and the sheet's header row to get it
into the sheet. The prompt tells the model to copy values, not calculate them, and to treat the
invoice text as data rather than instructions.

---

## Project — My own MCP server in n8n (Day 3)

[`mcp-server.json`](mcp-server.json) · 4 nodes · import straight into n8n

An MCP server, built as an n8n workflow, for a small fictional furniture shop. Any MCP client can
connect to it and get three tools:

| Tool | What it does |
|---|---|
| **Get Product Catalogue** | Reads every row of the `Products` sheet (sku, name, category, price, stock, lead time) |
| **Calculator** | Arithmetic, so totals and discounts aren't left to the model |
| **Convert Currency** | Calls the free Frankfurter API for today's ECB rate |

The catalogue is in [`product-catalogue.csv`](product-catalogue.csv) — eight made-up products.

### Setup

1. Make a spreadsheet, import `product-catalogue.csv` as a tab called `Products`, and put the
   spreadsheet id into **Get Product Catalogue** (`YOUR_GOOGLE_SHEET_ID`).
2. Connect a Google Sheets OAuth2 credential on that node.
3. On **MCP Server Trigger**, create a **Bearer Auth** credential with a long random token
   (`openssl rand -hex 32` makes one). Any client without that token gets refused.
4. Save and activate the workflow, then copy the **Production URL** from the trigger. It ends in
   `/mcp/product-catalogue`.

### Connecting Claude Desktop

Claude Desktop starts local MCP servers as commands, so the n8n server goes through the
`mcp-remote` bridge. In Claude Desktop: Settings → Developer → Edit Config, and add:

```json
{
  "mcpServers": {
    "n8n-product-catalogue": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "http://localhost:5678/mcp/product-catalogue",
        "--header",
        "Authorization: Bearer ${AUTH_TOKEN}"
      ],
      "env": {
        "AUTH_TOKEN": "YOUR_BEARER_TOKEN"
      }
    }
  }
}
```

Use the Production URL from step 4 (older n8n versions put the SSE endpoint at `.../sse`).
Restart Claude Desktop, and the three tools show up under the tools menu. Something like
"What's the cheapest chair, and what is it in euros?" should call the catalogue and then the
currency tool. Every call also shows as an execution in n8n.

The token sits in that config file in plain text, so it's a local-only setup. Making the server
reachable from outside my machine would need HTTPS in front of n8n first.

---

## Project — GTM capstone: multi-agent lead generation (Days 4–5)

Four workflows: one orchestrator agent and three sub-workflows it calls as tools.

| File | Nodes | Role |
|---|---:|---|
| [`gtm-orchestrator.json`](gtm-orchestrator.json) | 7 | Form for the ideal customer profile → orchestrator agent → run summary |
| [`gtm-lead-researcher.json`](gtm-lead-researcher.json) | 7 | Agent that finds companies via Firecrawl MCP and contacts via Hunter.io |
| [`gtm-crm-writer.json`](gtm-crm-writer.json) | 16 | Finds or creates the organization, person and deal in Pipedrive |
| [`gtm-demo-booker.json`](gtm-demo-booker.json) | 9 | Holds a free calendar slot and drafts the invitation in Gmail |

```
                 ICP Form (industry, location, size, max leads, book demos?)
                                      │
                                      ▼
                        ┌───────────────────────────┐
                        │   GTM Orchestrator agent  │
                        └───────────────────────────┘
                 tool │               tool │               tool │
                      ▼                    ▼                    ▼
        ┌──────────────────────┐ ┌──────────────────┐ ┌──────────────────────┐
        │ Lead Researcher      │ │ CRM Writer       │ │ Demo Booker          │
        │ agent                │ │ (no LLM)         │ │ (no LLM)             │
        │  ├ Firecrawl MCP     │ │  Pipedrive:      │ │  Calendar: busy      │
        │  ├ Hunter.io HTTP    │ │  org → person    │ │  slots → hold slot   │
        │  └ structured output │ │  → deal          │ │  Gmail: DRAFT only   │
        └──────────────────────┘ └──────────────────┘ └──────────────────────┘
                      │                    │                    │
                      └──── leads ─────────┴──── ids ───────────┘
                                      │
                                      ▼
                                 Run Summary
```

The orchestrator calls the researcher, hands the leads it got back to the CRM writer, and — only
if I picked "yes" for "Book demos" — calls the demo booker for up to three contacts that are new
to the CRM. Each sub-workflow is a normal workflow with an Execute Workflow Trigger, so I can run
and debug it on its own before the orchestrator ever touches it.

### Import order

The orchestrator points at the sub-workflows by id, so they have to exist first.

1. Import `gtm-lead-researcher.json`, `gtm-crm-writer.json` and `gtm-demo-booker.json`. Save each
   one (and publish it, on n8n versions that have a Publish button).
2. Copy each one's workflow id — it's the part of the URL after `/workflow/`.
3. Import `gtm-orchestrator.json` and paste the ids into its three tool nodes:
   - **Research Leads** → `YOUR_LEAD_RESEARCHER_WORKFLOW_ID`
   - **Write Leads to Pipedrive** → `YOUR_CRM_WRITER_WORKFLOW_ID`
   - **Book Demo** → `YOUR_DEMO_BOOKER_WORKFLOW_ID`

   Or pick each one from the list in the node instead of pasting the id.

### Setup

1. **Lead Researcher**
   - **Firecrawl MCP**: replace `YOUR_FIRECRAWL_API_KEY` in the endpoint URL with my Firecrawl
     key. Firecrawl's hosted MCP server takes the key in the URL, so the URL itself is a secret —
     never export or commit this workflow with the real key in it.
   - **Hunter Domain Search**: a **Query Auth** credential with name `api_key` and my Hunter.io
     key as the value.
   - **Researcher Model**: an OpenRouter credential.
2. **CRM Writer**: a Pipedrive API credential on all five Pipedrive nodes.
3. **Demo Booker**:
   - Google Calendar OAuth2 on **Get Busy Slots** and **Hold Demo Slot**, and my calendar id in
     both (`YOUR_CALENDAR_ID` — for my main calendar that's my Google account address).
   - Gmail OAuth2 on **Draft Invitation**.
   - Working hours and slot length are the constants at the top of **Pick Slot** (10:00–16:00,
     30 minutes, weekdays) in the instance timezone.
4. **Orchestrator**: an OpenRouter credential on **Orchestrator Model**.
5. Test each sub-workflow on its own first: open it, pin some sample input on the trigger and
   execute. Then open the orchestrator's form URL, start with "Max leads" at 2 and "Book demos"
   at no, and check Pipedrive before turning demos on.

### How it works

- **Researcher.** The agent searches with Firecrawl (only `firecrawl_search` and
  `firecrawl_scrape` are exposed, not crawl or extract), asks Hunter for named people at each
  domain, and has to answer in the Leads Schema: `[{company, domain, contact_name,
  contact_email, title, reason}]`. **Clean Leads** then drops anything without a well-formed
  email on the company's own domain, dedupes, and cuts every field to one short line.
- **CRM writer.** One lead at a time: search the organization by exact name, create it if
  missing; search the person by exact email; if they're already there, leave them alone and
  report the existing ids; if not, create the person and a deal. It returns how many were
  created and how many already existed, with the ids.
- **Demo booker.** Reads the busy slots for the next seven days, picks the first free 30-minute
  weekday slot in working hours, puts a "Demo (HOLD)" event on my calendar with the lead as an
  attendee but with notifications set to none, and writes a Gmail **draft** invitation. I read
  and send it myself.
- **Orchestrator.** Its prompt fixes the order of the three calls, tells it to pass the leads
  through unchanged, and caps demos at three per run. The form value for leads is capped at ten.

The Day 4 "structured output vs tools" lecture is the reason the researcher returns a schema and
the CRM writer and demo booker have no model at all: once the leads are in a fixed shape,
writing them to a CRM or a calendar is plain plumbing, and plumbing doesn't need judgement.

### Security — the lethal trifecta

The trifecta is an agent that has all three of: access to private data, exposure to untrusted
content, and a way to communicate externally. With all three, text planted on a web page can
steer the agent into sending my data somewhere.

| Part | Private data | Untrusted content | External communication |
|---|---|---|---|
| Lead Researcher agent | no | **yes** — web pages, search results | no — read-only tools |
| CRM Writer | **yes** — my CRM | values only, never instructions | no |
| Demo Booker | **yes** — my calendar | values only, never instructions | drafts only, nothing sent |
| Orchestrator agent | ids and slot times only | **yes**, second-hand, via the researcher | can trigger the CRM writer and demo booker |

How the design keeps any one model from holding all three:

- **The agent that reads the web can't act.** The researcher has search, scrape and Hunter lookup,
  nothing that writes or sends.
- **Web text reaches the rest only as fields.** The structured output parser and Clean Leads
  reduce everything to six short, single-line fields with a validated email. A paragraph of
  injected instructions doesn't survive that intact.
- **No web content flows into the CRM writer's instructions, because it has none.** It and the
  demo booker are deterministic workflows with no LLM. A company name that says "ignore previous
  instructions" just becomes an oddly named organization in Pipedrive. The CRM writer also
  re-validates every lead it's handed rather than trusting the orchestrator.
- **Nothing goes out without me.** The demo booker writes a Gmail draft, never sends, and the
  calendar hold is created with notifications off, so the lead isn't emailed by Google either.
  The invitation text is a fixed template, not model output.
- **Private data stays put.** The orchestrator sees ids, statuses and one chosen slot time, never
  my calendar or the rest of the CRM.

What's left: the orchestrator does read web-derived text (mainly the `reason` field) and can
choose which tool to call with which lead. The worst it could be steered into is adding a bogus
lead to Pipedrive or holding a slot for one, and both still stop at a draft I review. If I ever
switch the Gmail node from draft to send, the trifecta closes — so I won't.
