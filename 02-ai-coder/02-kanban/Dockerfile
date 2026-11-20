FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:0.7.17 /uv /bin/uv

WORKDIR /app
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH" \
    KANBAN_DB=/data/kanban.db

# Dependencies first so code edits don't re-install them. uv.lock is used if present.
COPY pyproject.toml uv.lock* ./
RUN uv sync --no-dev

COPY backend ./backend
COPY frontend ./frontend

RUN mkdir -p /data
VOLUME ["/data"]
EXPOSE 8000

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
