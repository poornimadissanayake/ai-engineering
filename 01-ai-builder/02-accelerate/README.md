# Module 2 — Accelerate

Voice agents and RAG. The ElevenLabs Agent Platform — agent tools, widgets, multi-agent voice
workflows — wired to n8n over webhooks. Then RAG properly: embeddings, vector search, and agentic
vs. traditional retrieval, built on a Supabase vector store with OpenAI embeddings. Ends with a
voice agent that answers from that store over a real Twilio phone number.

**Projects:** Voice agent — ElevenLabs and Twilio conversational agent, answering from Supabase RAG

## Running this

n8n Cloud plus an ElevenLabs agent and a Supabase project. Import the workflow JSON, reconnect
credentials in n8n, point the ElevenLabs agent at the n8n webhook, then activate.

Accounts this module needs: ElevenLabs, Supabase, Twilio, OpenAI or Gemini for embeddings.

Setup notes per project go here as they are built.
