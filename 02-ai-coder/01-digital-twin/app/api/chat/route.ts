import { profile } from "@/content/profile";
import { parseSseChunk } from "@/lib/sse";
import { DEFAULT_MODEL, MAX_BODY_CHARS, buildSystemPrompt, validateChatRequest } from "@/lib/twin";

const OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions";

export const dynamic = "force-dynamic";

function errorResponse(error: string, status: number) {
  return Response.json({ error }, { status });
}

export async function POST(req: Request) {
  const apiKey = process.env.OPENROUTER_API_KEY?.trim();
  if (!apiKey) {
    return errorResponse(
      "The digital twin is offline: OPENROUTER_API_KEY is not set on the server.",
      503,
    );
  }

  const raw = await req.text();
  if (raw.length > MAX_BODY_CHARS) {
    return errorResponse("Request is too large.", 413);
  }

  let body: unknown;
  try {
    body = JSON.parse(raw);
  } catch {
    return errorResponse("Request body must be valid JSON.", 400);
  }

  const check = validateChatRequest(body);
  if (!check.ok) {
    return errorResponse(check.error, check.status);
  }

  const model = process.env.OPENROUTER_MODEL?.trim() || DEFAULT_MODEL;

  let upstream: Response;
  try {
    upstream = await fetch(OPENROUTER_URL, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${apiKey}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        model,
        stream: true,
        max_tokens: 400,
        temperature: 0.4,
        messages: [{ role: "system", content: buildSystemPrompt(profile) }, ...check.messages],
      }),
      signal: req.signal,
    });
  } catch {
    return errorResponse("Could not reach the model provider. Try again in a moment.", 502);
  }

  if (!upstream.ok || !upstream.body) {
    console.error(`OpenRouter returned ${upstream.status}`);
    return errorResponse("The model provider returned an error. Try again in a moment.", 502);
  }

  const reader = upstream.body.getReader();
  const decoder = new TextDecoder();
  const encoder = new TextEncoder();
  let buffer = "";

  const stream = new ReadableStream<Uint8Array>({
    async pull(controller) {
      const { value, done } = await reader.read();
      if (done) {
        controller.close();
        return;
      }
      buffer += decoder.decode(value, { stream: true });
      const parsed = parseSseChunk(buffer);
      buffer = parsed.rest;
      for (const delta of parsed.deltas) controller.enqueue(encoder.encode(delta));
      if (parsed.error) {
        console.error(`OpenRouter stream error: ${parsed.error}`);
        controller.enqueue(encoder.encode("\n\n(Sorry, the answer was cut off. Please try again.)"));
      }
      if (parsed.done || parsed.error) {
        await reader.cancel();
        controller.close();
      }
    },
    async cancel() {
      await reader.cancel();
    },
  });

  return new Response(stream, {
    headers: {
      "Content-Type": "text/plain; charset=utf-8",
      "Cache-Control": "no-store",
    },
  });
}
