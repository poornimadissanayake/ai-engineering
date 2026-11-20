import { describe, expect, it } from "vitest";
import { parseSseChunk } from "./sse";

const event = (content: string) => `data: ${JSON.stringify({ choices: [{ delta: { content } }] })}\n`;

describe("parseSseChunk", () => {
  it("extracts content deltas and skips comments and blank lines", () => {
    const result = parseSseChunk(`: OPENROUTER PROCESSING\n\n${event("Hel")}\n${event("lo")}\n`);
    expect(result.deltas).toEqual(["Hel", "lo"]);
    expect(result.rest).toBe("");
    expect(result.done).toBe(false);
  });

  it("keeps an incomplete trailing line for the next chunk", () => {
    const full = event("Hello");
    const first = parseSseChunk(full.slice(0, 20));
    expect(first.deltas).toEqual([]);
    const second = parseSseChunk(first.rest + full.slice(20));
    expect(second.deltas).toEqual(["Hello"]);
  });

  it("recognises the end of the stream", () => {
    expect(parseSseChunk("data: [DONE]\n").done).toBe(true);
  });

  it("reports an error event", () => {
    const result = parseSseChunk(`data: ${JSON.stringify({ error: { message: "rate limited" } })}\n`);
    expect(result.error).toBe("rate limited");
  });

  it("ignores malformed events", () => {
    expect(parseSseChunk("data: {not json\n").deltas).toEqual([]);
  });
});
