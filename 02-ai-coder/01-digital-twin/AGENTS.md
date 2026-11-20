# AGENTS.md — Digital twin website

Personal website with a chat panel that answers as the site owner, from their profile only.

## Stack

- Next.js 16 (App Router), React 19, TypeScript (strict), Tailwind CSS v4
- OpenRouter chat completions via plain `fetch` (OpenAI-compatible API, streamed)
- Vitest for unit tests, ESLint (`eslint-config-next`) for lint
- Node 20.9+

## Commands

```bash
npm install
npm run dev        # http://localhost:3000
npm run lint
npm run typecheck
npm test           # vitest run
npm run build
```

Before saying a change is done: `npm run lint && npm run typecheck && npm test && npm run build` all pass.

## Layout

- `content/profile.ts` — the ONLY source of personal content. Page and twin both read it.
- `app/page.tsx` — hero, about, experience, projects, twin, contact. Server component.
- `app/api/chat/route.ts` — POST handler: key check → size check → `validateChatRequest` → OpenRouter → plain-text stream.
- `components/Chat.tsx` — client chat panel, reads the text stream.
- `lib/twin.ts` — pure: `buildSystemPrompt`, `validateChatRequest`, limits, default model.
- `lib/sse.ts` — pure: parses OpenRouter's SSE stream into text deltas.
- Tests sit next to the code as `*.test.ts`.

## Conventions

- Keep `lib/` pure (no env, no network) so it stays unit-testable. Env and `fetch` live in the route.
- Limits live in `lib/twin.ts` and are enforced server-side; the client only mirrors them for UX.
- Personal content goes in `content/profile.ts`, never hard-coded in components.
- Tailwind utility classes only; zinc palette; support dark mode with `dark:` variants.
- Small, focused changes. Add or update a test when changing `lib/` or the route.

## Don'ts

- Don't commit `.env.local` or any key. `OPENROUTER_API_KEY` is read on the server only — never `NEXT_PUBLIC_`.
- Don't let the page depend on the key: it must render and build with no key set; the route returns 503.
- Don't accept `system` messages from the client, and don't loosen the length or turn caps without a reason.
- Don't make the twin answer beyond the profile; changes to the system prompt keep the "only from the profile" rules and the tests for them.
- Don't add dependencies (an SDK, a UI kit) for something `fetch` or Tailwind already does.
- Don't invent facts about the owner in placeholder content.
