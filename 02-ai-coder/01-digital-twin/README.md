# Project 1 — Digital twin

AI Coder, week 1 · Next.js personal website with an AI digital twin on OpenRouter

A one-page personal site — hero, about, experience, projects, contact — with a "Talk to my
digital twin" panel. Visitors ask questions and the twin answers as me, in the first person, from
my profile and nothing else. If the answer isn't in the profile it says "I'd rather you ask me
directly" and points at the contact links.

Everything on the page and everything the twin knows comes from one file,
[`content/profile.ts`](content/profile.ts). Right now it holds placeholders ("Your Name",
"Example Company", two sample projects) — swap in your own.

## Running this

Node 20.9 or newer, and an [OpenRouter](https://openrouter.ai/keys) key for the chat.

```bash
npm install
cp .env.example .env.local   # then put your key in OPENROUTER_API_KEY
npm run dev                  # http://localhost:3000
```

The site renders without a key. The chat panel just tells you the twin is offline until
`OPENROUTER_API_KEY` is set.

`OPENROUTER_MODEL` is optional. Blank means `openai/gpt-4.1-nano`; any OpenRouter model id works.

Checks:

```bash
npm run lint
npm run typecheck
npm test
npm run build
```

## Editing the profile

Open `content/profile.ts` and replace each placeholder. The fields map straight onto the page:
`about` is paragraphs, `experience` and `projects` are lists, `contact` drives the buttons at the
bottom (leave one out and its button disappears). `twinNotes` is for things the twin may talk
about that don't need a section on the page — what I'm looking for, interests, how I like to work.

Whatever is in that file the twin can repeat to anyone, so don't put anything in it that
shouldn't be public.

## How the twin works

The browser posts the conversation to `/api/chat`. The route checks it, builds a system prompt from
the profile, and streams the answer back from OpenRouter as plain text.

- **Only from the profile.** The system prompt ([`lib/twin.ts`](lib/twin.ts)) tells the model to
  answer in the first person from the profile, keep it short, say "I'd rather you ask me directly"
  when it doesn't know, and refuse anything private or off-topic.
- **Caps, on the server.** 1,000 characters per message, 12 questions per conversation, and a
  400-token answer. The client can't send its own `system` message.
- **No key, no crash.** Missing `OPENROUTER_API_KEY` returns a clear 503; the page is still static.
- **Key stays server-side.** It is only read in the route handler, never sent to the browser.

The prompt builder, the input validation and the stream parser are pure functions with tests
(`lib/*.test.ts`); the route is tested with a stubbed `fetch`, so no test calls OpenRouter.

## Deploying to Vercel

1. Push the repo, then import it in Vercel and set the root directory to
   `02-ai-coder/01-digital-twin`.
2. Add `OPENROUTER_API_KEY` (and `OPENROUTER_MODEL` if you want another model) under
   Settings → Environment Variables.
3. Deploy. Every push to the branch redeploys.

## Cost

Next to nothing. `gpt-4.1-nano` on OpenRouter is about $0.10 per million input tokens and $0.40 per
million output tokens. Each question sends the profile (a couple of thousand tokens at most) plus
the conversation, so a full 12-question chat is well under a cent.

There is no per-visitor rate limit — the caps are per conversation, and a refresh starts a new
one. So put a credit limit on the OpenRouter key before the site goes public.

## How it was built

This follows the vibe-coding method from the course rather than writing it line by line:

1. **Context first.** [`AGENTS.md`](AGENTS.md) describes the stack, the commands, the layout and
   the don'ts, so a coding agent starts every session knowing the rules of the project.
2. **Agent mode, small steps.** A coding agent in an IDE's agent mode (the course uses Cursor)
   builds the site, then the chat route, one feature at a time, with lint, tests and a build after
   each.
3. **Be the boss.** I decide the scope and the guardrails — profile-only answers, server-side
   caps, no key in the browser — and check the result rather than trusting it.
4. **Second opinion.** A different model reviews the code before it's called done, because a
   model is worst at spotting its own mistakes.
