# Module 2 — Accelerate

25 lectures · 3hr 42min · weeks 4–5

Voice agents and RAG. The ElevenLabs Agent Platform — agent tools, widgets, multi-agent voice
workflows — wired to n8n over webhooks. Then RAG properly: embeddings, vector search, and agentic
vs. traditional retrieval, built on a Supabase vector store with OpenAI embeddings. Ends with a
voice agent that answers from that store over a real Twilio phone number.

**Projects:** Voice agent — ElevenLabs and Twilio conversational agent, answering from Supabase RAG

## Running this

n8n Cloud plus an ElevenLabs agent and a Supabase project. Import the workflow JSON, reconnect
credentials in n8n, point the ElevenLabs agent at the n8n webhook, then activate.

Accounts this module needs: ElevenLabs, Supabase, Twilio, OpenAI or Gemini for embeddings.

---

## Project — Voice agent over a Supabase RAG store

A phone line for a small business that answers callers' questions from its own documents. The
business is made up — Harbour Dental Clinic — so the knowledge base can be specific without being
anyone's real data.

```
caller → Twilio → ElevenLabs agent → server tool → n8n webhook → agent + Supabase → answer
```

ElevenLabs handles the call: speech to text, the conversation, text to speech. When the caller
asks something about the clinic, the ElevenLabs agent calls a server tool, which is an n8n
webhook. n8n searches the Supabase vector store, writes a one-to-three-sentence answer from what
it finds, and returns `{"answer": "…"}`. ElevenLabs reads that out.

Five pieces, set up in this order:

| File | What it is |
|---|---|
| [`supabase-setup.sql`](supabase-setup.sql) | pgvector, the `documents` table and the `match_documents` search function |
| [`knowledge-base/`](knowledge-base/) | two short markdown docs for the fictional clinic — hours, prices, booking policy |
| [`rag-ingest.json`](rag-ingest.json) | n8n: new file in a Drive folder → chunks → embeddings → Supabase |
| [`voice-agent-backend.json`](voice-agent-backend.json) | n8n: webhook → agent that searches Supabase → spoken-style answer |
| [`elevenlabs-agent.md`](elevenlabs-agent.md) | the ElevenLabs agent's prompt, server tool and Twilio steps |

Accounts: n8n Cloud, Supabase, OpenAI (embeddings and chat), Google Drive, ElevenLabs, Twilio.

### 1. Supabase

Create a Supabase project, open the SQL editor, paste [`supabase-setup.sql`](supabase-setup.sql)
and run it. It enables pgvector, creates `documents` (`id`, `content`, `metadata`,
`embedding vector(1536)`) and `match_documents(query_embedding, match_count, filter)` — the
table and function names n8n's Supabase Vector Store node looks for by default. 1536 is the
dimension of OpenAI's `text-embedding-3-small`; a different embedding model means changing it.

RLS is switched on with no policies, so the table is closed to the public anon key. n8n connects
with the **service_role** key (Project Settings → API), which goes into n8n's credential store
and nowhere else.

### 2. Ingest — `rag-ingest.json`

[`rag-ingest.json`](rag-ingest.json) · 6 nodes

When a file lands in one Google Drive folder, it downloads it, splits it into ~800-character
chunks along markdown headings, embeds each chunk with `text-embedding-3-small`, and inserts the
chunks into `documents` with the file's name and id in `metadata`.

Setup:

1. Make a Drive folder for the knowledge base and copy its id from the URL
   (`drive.google.com/drive/folders/<this part>`).
2. Import the JSON and put the folder id into **New File in Folder** — it says
   `YOUR_DRIVE_FOLDER_ID`.
3. Connect three credentials, none of which are in this file:
   - Google Drive OAuth2, on *New File in Folder* and *Download File*
   - OpenAI, on *Embeddings OpenAI*
   - Supabase (project URL + service_role key), on *Supabase Vector Store*
4. Upload one file from [`knowledge-base/`](knowledge-base/) to the folder and execute once by
   hand before activating — the trigger's test fetch picks up the newest file — then check the
   rows in Supabase's table editor.
5. Activate it and upload the other file. From then on, anything dropped in the folder is
   ingested within a minute or so.

How it works: the **Default Data Loader** reads the downloaded file as plain text and hands it
to the **Recursive Character Text Splitter**; the vector store node calls the embeddings node
once per chunk. The loader is set to the text loader because the knowledge base is markdown — for
PDFs, switch it to the PDF loader (or "Automatically Detect by Mime Type"). A Google Doc dropped
in the folder is exported as plain text on download.

It only inserts. Uploading a new version of a file adds a second copy of its chunks rather than
replacing the first, so to re-ingest I clear the table (`truncate table documents;`) and upload
again.

### 3. Backend — `voice-agent-backend.json`

[`voice-agent-backend.json`](voice-agent-backend.json) · 8 nodes

A POST webhook at `/webhook/voice-agent-query`, guarded by a header secret, takes
`{"question": "…"}` from the ElevenLabs agent. An AI Agent with the Supabase store attached as a
tool (`knowledge_base`, top 4 chunks) searches it, answers only from what comes back, and replies
`{"answer": "…"}` in one to three sentences written to be spoken — no lists, no symbols, numbers
in words. If the knowledge base doesn't cover it, the answer says so instead of guessing. A
request with no question gets a polite "didn't catch that" rather than an error.

Setup:

1. Import the JSON.
2. Connect four credentials, none of which are in this file:
   - **Header Auth** on *ElevenLabs Tool Call*, with name `X-Voice-Agent-Key` and a long random
     string as the value — the same string goes into ElevenLabs as a secret
   - OpenAI, on *OpenAI Chat Model* and *Embeddings OpenAI*
   - Supabase, on *Knowledge Base*
3. Execute once by hand before activating: click **Listen for test event** on the webhook and
   send it a question from a terminal:

   ```bash
   curl -X POST "https://YOUR_N8N_SUBDOMAIN.app.n8n.cloud/webhook-test/voice-agent-query" \
     -H "X-Voice-Agent-Key: YOUR_SHARED_SECRET" \
     -H "Content-Type: application/json" \
     -d '{"question": "What time do you close on Friday?"}'
   ```

4. Activate it, and copy the webhook's **Production URL** for the ElevenLabs tool.

The embeddings model here has to be the same one used at ingest, or the query vectors and the
stored vectors live in different spaces and the search returns noise.

### 4. ElevenLabs and Twilio — `elevenlabs-agent.md`

[`elevenlabs-agent.md`](elevenlabs-agent.md) has the agent's first message and system prompt,
the `knowledge_base` server tool (POST to the production webhook URL, header secret, body
`{question: string}`), and the steps to import a Twilio number into ElevenLabs (Phone Numbers →
Import number → From Twilio). The Twilio Account SID and auth token are entered in ElevenLabs
only — they are not in this repo.

### Why the split

ElevenLabs owns the conversation and n8n owns the facts. The voice agent's prompt says to call
the tool for every clinic question and never answer from its own knowledge; the n8n agent's
prompt says to answer only from what Supabase returns. That is two places where "I don't know"
is the required answer for anything outside the documents — which is the whole point of putting
a front desk on RAG instead of a bare model.

Built against n8n 2.x node versions. On an older instance n8n flags the version on import and
you can pin it down from there.
