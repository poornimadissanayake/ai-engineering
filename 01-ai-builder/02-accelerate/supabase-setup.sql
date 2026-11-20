-- Supabase setup for the voice agent's RAG store.
-- Run once in the Supabase SQL editor (SQL Editor -> New query -> paste -> Run).
--
-- This is the shape n8n's Supabase Vector Store node expects: a `documents`
-- table with content / metadata / embedding, and a `match_documents` function
-- it calls for similarity search. vector(1536) matches OpenAI's
-- text-embedding-3-small. Use a different embedding model and the 1536 has to
-- change in all three places below.

-- 1. pgvector
create extension if not exists vector;

-- 2. The chunks, one row each
create table if not exists documents (
  id bigserial primary key,
  content text,          -- the chunk text (Document.pageContent)
  metadata jsonb,        -- file_name, file_id, loader metadata
  embedding vector(1536) -- OpenAI text-embedding-3-small
);

-- 3. Similarity search. n8n passes the query embedding, how many rows to
--    return, and a metadata filter (an empty object matches everything).
create or replace function match_documents (
  query_embedding vector(1536),
  match_count int default null,
  filter jsonb default '{}'
) returns table (
  id bigint,
  content text,
  metadata jsonb,
  similarity float
)
language plpgsql
as $$
#variable_conflict use_column
begin
  return query
  select
    id,
    content,
    metadata,
    1 - (documents.embedding <=> query_embedding) as similarity
  from documents
  where metadata @> filter
  order by documents.embedding <=> query_embedding
  limit match_count;
end;
$$;

-- 4. Index for cosine distance. Not needed for a handful of documents, but
--    free to add now.
create index if not exists documents_embedding_idx
  on documents using hnsw (embedding vector_cosine_ops);

-- 5. Lock the table down. With RLS on and no policies, the public anon key
--    can't read or write it; n8n connects with the service_role key, which
--    bypasses RLS.
alter table documents enable row level security;

-- Starting over (e.g. after re-ingesting the same files):
-- truncate table documents;
