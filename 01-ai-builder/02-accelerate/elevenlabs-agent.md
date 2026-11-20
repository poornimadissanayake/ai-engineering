# ElevenLabs agent — configuration

Everything to paste into the ElevenLabs Agent Platform for the Harbour Dental Clinic front desk.
The agent does the talking; the facts come from the n8n webhook in
[`voice-agent-backend.json`](voice-agent-backend.json), which searches the Supabase store.

No keys, phone numbers or account ids live in this file. The webhook secret goes into
ElevenLabs' own secret store, and the Twilio SID and auth token are typed into ElevenLabs
directly.

```
caller → Twilio number → ElevenLabs agent → server tool (knowledge_base) → n8n webhook → agent + Supabase → {"answer": "…"} → spoken reply
```

## 1. Create the agent

ElevenLabs → Agents → Create agent → Blank template. Name it `Harbour Dental front desk`.

### First message

```
Hi, you've reached Harbour Dental Clinic. I'm the clinic's virtual assistant — I can tell you
about our opening hours, services, prices and booking policy. What can I help you with?
```

### System prompt

```
You are the virtual front-desk assistant for Harbour Dental Clinic, a small family dental
practice. You are speaking with a caller on the phone.

How to answer:
- For ANY question about the clinic — hours, services, prices, payment, booking, cancellations,
  emergencies, location, parking, staff — call the knowledge_base tool first and answer only
  from what it returns. Pass the caller's question as the `question` parameter.
- Never answer clinic questions from your own general knowledge, and never make up a price, a
  time, a policy or a name.
- If the tool's answer says the information isn't available, tell the caller plainly that you
  don't have that information and offer to take a message for the front desk to call back.
- You cannot book, move or cancel appointments. Explain that the front desk does that, and
  offer to take a message.
- You do not give medical or dental advice. For severe pain, heavy bleeding, swelling that
  affects breathing or swallowing, or a facial injury, tell the caller to go to the hospital
  emergency department.

How to speak:
- Short, warm, natural sentences — this is a phone call. One or two sentences per turn.
- No lists, no reading out symbols or web addresses.
- While the tool is working, say something brief like "One moment, let me check that."

Taking a message:
- Ask for the caller's first name, a good time to call back, and what it's about. Repeat it
  back to confirm. Do not ask for dates of birth, card numbers or any medical history.
```

### Voice and model

- Voice: any calm, clear voice from the library.
- LLM: a fast model (the default is fine). The heavy lifting is in n8n.
- Language: English.

## 2. The server tool

Agent → Tools → Add tool → Webhook.

| Field | Value |
|---|---|
| Name | `knowledge_base` |
| Description | `Look up Harbour Dental Clinic information — opening hours, services, prices, payment, booking and cancellation policy, emergencies, location and parking. Call this for every question about the clinic. Returns a short answer to read to the caller.` |
| Method | `POST` |
| URL | `https://YOUR_N8N_SUBDOMAIN.app.n8n.cloud/webhook/voice-agent-query` |
| Response timeout | 20 seconds |

The URL is the **Production URL** from the *ElevenLabs Tool Call* webhook node in n8n (not the
Test URL — that one only listens while the editor is waiting for a test event).

### Headers

| Header | Value |
|---|---|
| `X-Voice-Agent-Key` | a **secret**: Workspace → Secrets → Add secret, paste the same random string as in the n8n Header Auth credential, then pick that secret here |

### Body parameters

Body description: `The caller's question about the clinic.`

| Property | Type | Required | Description (what the LLM is told to fill in) |
|---|---|---|---|
| `question` | string | yes | `The caller's question, as a full sentence in plain English, e.g. "What time do you close on Friday?"` |

That produces this request body, which the n8n workflow reads as `body.question`:

```json
{ "question": "What time do you close on Friday?" }
```

and expects this back:

```json
{ "answer": "We close at three in the afternoon on Fridays." }
```

## 3. Try it in the browser first

Agent → Test AI agent. Ask a couple of things the knowledge base covers ("How much is a
check-up?", "Can I cancel the day before?") and one it doesn't ("Do you take dogs in the waiting
room?"). The last one should come back as "I don't have that information", not an invention. The n8n execution log shows each tool call.

## 4. Attach a Twilio phone number

Prerequisite: a Twilio account with a voice-capable phone number.

1. In the Twilio console, copy the **Account SID** and **Auth Token** from the account dashboard.
   They go into ElevenLabs only — never into n8n, this repo, or a chat message.
2. ElevenLabs → Phone Numbers → **Import number** → **From Twilio**.
3. Fill in a label (`Harbour Dental front desk`), the Twilio phone number, the Account SID and
   the Auth Token, then Import. ElevenLabs configures the number's voice webhook in Twilio for
   you.
4. On the imported number, set **Agent** to `Harbour Dental front desk`.
5. Call the number. The first message should play, and questions should show up as executions
   of the *Voice Agent Backend* workflow in n8n.

To take the number off the agent, unassign it in ElevenLabs → Phone Numbers. Deleting the
imported number there does not release it in Twilio.
