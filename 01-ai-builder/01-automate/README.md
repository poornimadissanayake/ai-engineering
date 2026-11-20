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

---

## Exercise — First agent

[`first-agent.json`](first-agent.json) · 5 nodes · import straight into n8n

The Day 1 agent. I type into n8n's chat panel and an AI Agent answers through OpenRouter, with a
window of the last ten messages as memory and a calculator as its one tool. It is small on
purpose: it is the smallest thing that shows all three agent inputs — model, memory, tools —
plugged into one node.

### Setup

1. Import the JSON into n8n (Workflows → Import from File).
2. Connect an **OpenRouter** credential on *OpenRouter Chat Model*. The model is
   `openai/gpt-4o-mini`; any OpenRouter model id works, including the free ones.
3. Open the chat (the **Chat** button under the canvas) and ask it something with arithmetic in
   it — "what is 17.5% of 2,340?" — then something that refers back to an earlier message.
4. Execute once by hand before activating anything.

### What to look at

The execution log shows the agent's turns. A maths question should show a call to the
**Calculator** tool; a follow-up like "and double that?" only works because **Simple Memory**
replays the earlier messages into the prompt — the model itself remembers nothing between calls.
Raise or lower `contextWindowLength` on the memory node to see where that illusion breaks.

---

## Exercise — Gmail draft replies

[`gmail-draft-replies.json`](gmail-draft-replies.json) · 5 nodes · import straight into n8n

Every five minutes it checks my Gmail inbox for new unread mail, skips newsletters, notifications
and no-reply senders, and has an OpenAI agent write a short reply to whatever is left. The reply
is saved as a **draft** in the same thread, addressed to the sender.

It never sends anything. I read the drafts in Gmail and send, edit or delete them myself.

### Setup

1. Import the JSON into n8n (Workflows → Import from File).
2. In **Reply Writer**, replace `YOUR_NAME` at the end of the system message with the name to
   sign off with.
3. Connect two credentials, none of which are in this file:
   - Gmail OAuth2, on *New Unread Email* and *Create Draft Reply*
   - OpenAI, on the chat model
4. Execute once by hand before activating — with an unread test email from another account in
   the inbox — and check the draft that appears in that thread.

### How the filtering works

Two layers, both cheap, so the model only sees mail that plausibly wants a human reply:

- The trigger's Gmail search, `in:inbox -from:me -category:promotions -category:social
  -category:updates -category:forums`, drops anything Gmail has already sorted out of Primary.
- **Skip Newsletters & No-Reply** drops a message if the sender's address starts with
  `noreply`, `no-reply`, `newsletter`, `notifications`, `info`, `marketing` and the like, or if
  the message carries a `List-Unsubscribe` header, which mailing lists set and people don't.

The agent is told to leave `[placeholders]` rather than commit me to a date, price or meeting,
and to treat the email as content, not instructions — someone else wrote it, so it is untrusted
input to the prompt. The original stays unread, so it is still in front of me next time I open
Gmail.
