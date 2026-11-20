// Parses OpenRouter's streaming (server-sent events) response into plain text deltas.
// Pure: feed it the text received so far, keep `rest` for the next chunk.

export type SseParseResult = {
  deltas: string[];
  rest: string; // an incomplete trailing line, to prepend to the next chunk
  done: boolean;
  error?: string;
};

export function parseSseChunk(buffer: string): SseParseResult {
  const lines = buffer.split("\n");
  const rest = lines.pop() ?? "";
  const result: SseParseResult = { deltas: [], rest, done: false };

  for (const rawLine of lines) {
    const line = rawLine.trim();
    // Blank lines separate events; lines starting with ":" are keep-alive comments.
    if (!line.startsWith("data:")) continue;

    const payload = line.slice("data:".length).trim();
    if (payload === "[DONE]") {
      result.done = true;
      continue;
    }

    try {
      const event = JSON.parse(payload);
      if (event?.error) {
        result.error = String(event.error.message ?? "Upstream error");
        continue;
      }
      const content = event?.choices?.[0]?.delta?.content;
      if (typeof content === "string" && content) result.deltas.push(content);
    } catch {
      // Ignore a malformed event rather than failing the whole answer.
    }
  }

  return result;
}
