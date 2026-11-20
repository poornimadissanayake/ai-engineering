"use client";

import { useEffect, useRef, useState, type FormEvent } from "react";
import { MAX_MESSAGE_CHARS, MAX_USER_TURNS, type ChatMessage } from "@/lib/twin";

const SUGGESTIONS = ["What do you work on?", "Tell me about a project", "How can I reach you?"];

export default function Chat({ name }: { name: string }) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const bottomRef = useRef<HTMLDivElement>(null);

  const userTurns = messages.filter((m) => m.role === "user").length;
  const limitReached = userTurns >= MAX_USER_TURNS;

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }, [messages]);

  async function send(text: string) {
    const content = text.trim();
    if (!content || loading || limitReached) return;

    const history: ChatMessage[] = [...messages, { role: "user", content }];
    setMessages(history);
    setInput("");
    setError(null);
    setLoading(true);

    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ messages: history }),
      });

      if (!res.ok || !res.body) {
        const data = await res.json().catch(() => null);
        throw new Error(data?.error ?? `Something went wrong (${res.status}).`);
      }

      setMessages([...history, { role: "assistant", content: "" }]);
      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      let answer = "";
      for (;;) {
        const { value, done } = await reader.read();
        if (done) break;
        answer += decoder.decode(value, { stream: true });
        setMessages([...history, { role: "assistant", content: answer }]);
      }
      if (!answer.trim()) {
        setMessages(history);
        throw new Error("No answer came back. Please try again.");
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong.");
    } finally {
      setLoading(false);
    }
  }

  function onSubmit(e: FormEvent) {
    e.preventDefault();
    void send(input);
  }

  return (
    <div className="rounded-2xl border border-zinc-200 bg-white shadow-sm dark:border-zinc-800 dark:bg-zinc-900">
      <div className="max-h-96 min-h-48 space-y-3 overflow-y-auto p-4" aria-live="polite">
        {messages.length === 0 && (
          <div className="space-y-3 text-sm text-zinc-500 dark:text-zinc-400">
            <p>
              Ask me anything about my work. I&apos;m an AI twin of {name} and I only know what&apos;s on
              this page.
            </p>
            <div className="flex flex-wrap gap-2">
              {SUGGESTIONS.map((s) => (
                <button
                  key={s}
                  type="button"
                  onClick={() => void send(s)}
                  className="rounded-full border border-zinc-300 px-3 py-1 text-zinc-700 hover:bg-zinc-100 dark:border-zinc-700 dark:text-zinc-300 dark:hover:bg-zinc-800"
                >
                  {s}
                </button>
              ))}
            </div>
          </div>
        )}
        {messages.map((m, i) => (
          <div key={i} className={m.role === "user" ? "flex justify-end" : "flex justify-start"}>
            <p
              className={
                "max-w-[85%] whitespace-pre-wrap rounded-2xl px-4 py-2 text-sm " +
                (m.role === "user"
                  ? "bg-zinc-900 text-white dark:bg-zinc-100 dark:text-zinc-900"
                  : "bg-zinc-100 text-zinc-800 dark:bg-zinc-800 dark:text-zinc-100")
              }
            >
              {m.content || (loading && i === messages.length - 1 ? "…" : "")}
            </p>
          </div>
        ))}
        {loading && messages[messages.length - 1]?.role === "user" && (
          <p className="text-sm text-zinc-400">Thinking…</p>
        )}
        <div ref={bottomRef} />
      </div>

      {error && (
        <p role="alert" className="border-t border-zinc-200 px-4 py-2 text-sm text-red-600 dark:border-zinc-800 dark:text-red-400">
          {error}
        </p>
      )}

      <form onSubmit={onSubmit} className="flex gap-2 border-t border-zinc-200 p-3 dark:border-zinc-800">
        <label htmlFor="twin-input" className="sr-only">
          Your question
        </label>
        <input
          id="twin-input"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          maxLength={MAX_MESSAGE_CHARS}
          disabled={loading || limitReached}
          placeholder={limitReached ? "Question limit reached — refresh to start again" : "Ask a question…"}
          className="flex-1 rounded-lg border border-zinc-300 bg-transparent px-3 py-2 text-sm outline-none focus:border-zinc-500 disabled:opacity-60 dark:border-zinc-700"
        />
        <button
          type="submit"
          disabled={loading || limitReached || !input.trim()}
          className="rounded-lg bg-zinc-900 px-4 py-2 text-sm font-medium text-white disabled:opacity-40 dark:bg-zinc-100 dark:text-zinc-900"
        >
          Send
        </button>
      </form>
    </div>
  );
}
