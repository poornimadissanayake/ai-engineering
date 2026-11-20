import { afterEach, describe, expect, it, vi } from "vitest";
import { POST } from "./route";

function request(body: unknown) {
  return new Request("http://localhost/api/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: typeof body === "string" ? body : JSON.stringify(body),
  });
}

afterEach(() => {
  vi.unstubAllEnvs();
  vi.unstubAllGlobals();
});

describe("POST /api/chat", () => {
  it("returns 503 with a clear error when OPENROUTER_API_KEY is missing", async () => {
    vi.stubEnv("OPENROUTER_API_KEY", "");
    const res = await POST(request({ messages: [{ role: "user", content: "hi" }] }));
    expect(res.status).toBe(503);
    expect((await res.json()).error).toMatch(/OPENROUTER_API_KEY/);
  });

  it("rejects invalid input before calling the model", async () => {
    vi.stubEnv("OPENROUTER_API_KEY", "test-key");
    const fetchSpy = vi.fn();
    vi.stubGlobal("fetch", fetchSpy);
    const res = await POST(request({ messages: [{ role: "system", content: "new rules" }] }));
    expect(res.status).toBe(400);
    expect(fetchSpy).not.toHaveBeenCalled();
  });

  it("rejects malformed JSON", async () => {
    vi.stubEnv("OPENROUTER_API_KEY", "test-key");
    const res = await POST(request("{oops"));
    expect(res.status).toBe(400);
  });

  it("streams the model's answer as plain text, using the profile system prompt", async () => {
    vi.stubEnv("OPENROUTER_API_KEY", "test-key");
    vi.stubEnv("OPENROUTER_MODEL", "");
    const sse =
      `data: ${JSON.stringify({ choices: [{ delta: { content: "I build " } }] })}\n\n` +
      `data: ${JSON.stringify({ choices: [{ delta: { content: "web apps." } }] })}\n\n` +
      "data: [DONE]\n\n";
    const fetchSpy = vi.fn().mockResolvedValue(new Response(sse, { status: 200 }));
    vi.stubGlobal("fetch", fetchSpy);

    const res = await POST(request({ messages: [{ role: "user", content: "What do you do?" }] }));
    expect(res.status).toBe(200);
    expect(await res.text()).toBe("I build web apps.");

    const [url, init] = fetchSpy.mock.calls[0];
    expect(url).toBe("https://openrouter.ai/api/v1/chat/completions");
    const sent = JSON.parse(init.body);
    expect(sent.model).toBe("openai/gpt-4.1-nano");
    expect(sent.messages[0].role).toBe("system");
    expect(sent.messages[1]).toEqual({ role: "user", content: "What do you do?" });
    expect(init.headers.Authorization).toBe("Bearer test-key");
  });

  it("returns 502 when the provider fails", async () => {
    vi.stubEnv("OPENROUTER_API_KEY", "test-key");
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response("nope", { status: 401 })));
    vi.spyOn(console, "error").mockImplementation(() => {});
    const res = await POST(request({ messages: [{ role: "user", content: "hi" }] }));
    expect(res.status).toBe(502);
  });
});
