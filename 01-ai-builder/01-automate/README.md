# Module 1 — Automate

30 lectures · 4hr 58min · weeks 1–3

Workflows in n8n Cloud. First agent on OpenRouter and OpenAI, then what an agent actually is: tool
calling, the illusion of memory, and how to evaluate one without anthropomorphising it. Then the
canvas — nodes, triggers, JSON, expressions, API-key and OAuth2 auth — wired into Google Sheets,
Drive, Gmail, Telegram, Slack and Pushover.

**Projects:** Portfolio rebalancer — monitors MarketStack prices and rebalances a Google Sheets
portfolio, with Gmail and Pushover notifications

## Running this

n8n Cloud, no local setup. Import the workflow JSON, reconnect credentials in n8n's own credential
store, then activate.

Accounts this module needs: n8n Cloud, OpenRouter or OpenAI, Google (Sheets, Drive, Gmail),
MarketStack, Telegram, Slack, Pushover.

---

## Project — Portfolio rebalancer

[`portfolio-rebalancer.json`](portfolio-rebalancer.json) · 12 nodes · import straight into n8n

Weekdays at 17:00 it reads my holdings from a Google Sheet, pulls closing prices from MarketStack,
and works out how far each holding has drifted from its target weight. If anything is more than
5 percentage points off, an OpenAI agent writes a short note on it, Pushover sends that to my
phone, and one row per holding is appended to a log sheet. If nothing has drifted it stops at a
no-op and stays quiet.

It suggests trades. It does not place them.

### The spreadsheet

One spreadsheet, two tabs.

**`Portfolio`** — what I hold. `target_weight` is a fraction, and the column should sum to 1.

| ticker | name | shares | target_weight |
|---|---|---:|---:|
| AAPL | Apple | 50 | 0.30 |
| MSFT | Microsoft | 30 | 0.30 |
| GOOGL | Alphabet | 20 | 0.40 |

**`Rebalance Log`** — written by the workflow. Header row only to start with.

Both tabs are here as CSVs, so the sheet is an import rather than typing columns by hand:
[`portfolio-template.csv`](portfolio-template.csv) and
[`rebalance-log-template.csv`](rebalance-log-template.csv). In Google Sheets, File → Import →
Upload, and choose "Insert new sheet", then rename the tabs to `Portfolio` and `Rebalance Log`.
The holdings above are placeholders — swap in your own.

### Setup

1. Import the JSON into n8n (Workflows → Import from File).
2. Put your spreadsheet id into **Get Portfolio** and **Log to Sheet** — both say `YOUR_GOOGLE_SHEET_ID`.
3. Put your Pushover user key into **Notify (Pushover)**.
4. Connect four credentials, none of which are in this file:
   - Google Sheets OAuth2, on both Sheets nodes
   - **Query Auth** on *Fetch Prices*, with name `access_key` and your MarketStack key as the value
   - OpenAI, on the chat model
   - Pushover
5. Execute once by hand before activating the schedule.

### Where the numbers come from

The arithmetic is all in the **Compute Drift** code node — drift, target values and share deltas
are computed in JavaScript, not by the model. The agent only writes the covering note, so a bad
generation cannot change a number. The threshold is `DRIFT_THRESHOLD` on the first line of that
node.

Worked example, 50 AAPL @ 200, 30 MSFT @ 400, 20 GOOGL @ 150 against targets of 30/30/40:

| ticker | weight | target | drift | action | delta |
|---|---:|---:|---:|---|---:|
| AAPL | 40% | 30% | +10 pts | SELL | −12 |
| MSFT | 48% | 30% | +18 pts | SELL | −11 |
| GOOGL | 12% | 40% | −28 pts | BUY | +47 |

Built against n8n 2.x node versions. On an older instance n8n flags the version on import and
you can pin it down from there.
