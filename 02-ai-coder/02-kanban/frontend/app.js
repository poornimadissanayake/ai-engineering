// Kanban Chat front end. No build step: plain DOM, HTML5 drag and drop, fetch.

const state = {
  board: { columns: [] },
  chat: [],          // {role, content} sent to /api/chat as history
  dragId: null,      // id of the card being dragged
  editing: null,     // card open in the dialog
};

const $ = (sel) => document.querySelector(sel);

async function api(path, options = {}) {
  const response = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...options,
    body: options.body === undefined ? undefined : JSON.stringify(options.body),
  });
  if (!response.ok) {
    let detail = response.statusText;
    try {
      const data = await response.json();
      detail = typeof data.detail === "string" ? data.detail : JSON.stringify(data.detail);
    } catch { /* not JSON */ }
    const error = new Error(detail);
    error.status = response.status;
    throw error;
  }
  return response.status === 204 ? null : response.json();
}

function flash(message) {
  const el = $("#status");
  el.textContent = message;
  clearTimeout(flash.timer);
  flash.timer = setTimeout(() => { el.textContent = ""; }, 4000);
}

async function loadBoard() {
  try {
    state.board = await api("/api/board");
    renderBoard();
  } catch (err) {
    flash(`Could not load the board: ${err.message}`);
  }
}

// ---------- board ----------

function renderBoard() {
  const board = $("#board");
  board.replaceChildren(...state.board.columns.map(renderColumn));
}

function renderColumn(column) {
  const el = $("#column-template").content.firstElementChild.cloneNode(true);
  el.dataset.column = column.id;
  el.querySelector("h2").textContent = column.name;
  el.querySelector(".count").textContent = column.cards.length;

  const list = el.querySelector(".cards");
  list.append(...column.cards.map(renderCard));
  wireDropZone(el, list, column.id);

  el.querySelector(".add-card").addEventListener("submit", async (event) => {
    event.preventDefault();
    const input = event.target.elements.title;
    const title = input.value.trim();
    if (!title) return;
    try {
      await api("/api/cards", { method: "POST", body: { title, column: column.id } });
      input.value = "";
      await loadBoard();
      $(`[data-column="${column.id}"] .add-card input`)?.focus();
    } catch (err) {
      flash(err.message);
    }
  });
  return el;
}

function renderCard(card) {
  const li = document.createElement("li");
  li.className = "card";
  li.draggable = true;
  li.tabIndex = 0;
  li.dataset.id = card.id;

  const title = document.createElement("div");
  title.className = "card-title";
  title.textContent = card.title;
  li.append(title);
  if (card.description) {
    const desc = document.createElement("div");
    desc.className = "card-desc";
    desc.textContent = card.description;
    li.append(desc);
  }

  li.addEventListener("click", () => openEditor(card));
  li.addEventListener("keydown", (event) => { if (event.key === "Enter") openEditor(card); });
  li.addEventListener("dragstart", (event) => {
    state.dragId = card.id;
    event.dataTransfer.effectAllowed = "move";
    event.dataTransfer.setData("text/plain", String(card.id));
    // Add the class after the browser has taken its drag snapshot.
    requestAnimationFrame(() => li.classList.add("dragging"));
  });
  li.addEventListener("dragend", () => {
    state.dragId = null;
    li.classList.remove("dragging");
    clearDropMarkers();
  });
  return li;
}

// Where in `list` would a drop at clientY land? Counted without the dragged card,
// which is exactly how the API reads `position`.
function dropIndex(list, clientY) {
  const cards = [...list.querySelectorAll(".card:not(.dragging)")];
  const index = cards.findIndex((card) => {
    const box = card.getBoundingClientRect();
    return clientY < box.top + box.height / 2;
  });
  return { index: index === -1 ? cards.length : index, cards };
}

function clearDropMarkers() {
  document.querySelectorAll(".drop-marker").forEach((m) => m.remove());
  document.querySelectorAll(".column.drag-over").forEach((c) => c.classList.remove("drag-over"));
}

function wireDropZone(columnEl, list, columnId) {
  columnEl.addEventListener("dragover", (event) => {
    if (state.dragId === null) return;
    event.preventDefault();  // required, or the drop event never fires
    event.dataTransfer.dropEffect = "move";
    columnEl.classList.add("drag-over");

    const { index, cards } = dropIndex(list, event.clientY);
    let marker = list.querySelector(".drop-marker");
    if (!marker) {
      document.querySelectorAll(".drop-marker").forEach((m) => m.remove());
      marker = document.createElement("li");
      marker.className = "drop-marker";
    }
    const before = cards[index] || null;
    if (marker.nextElementSibling !== before || marker.parentNode !== list) {
      list.insertBefore(marker, before);
    }
  });

  columnEl.addEventListener("dragleave", (event) => {
    // dragleave also fires when moving onto a child; only clear when leaving the column.
    if (!columnEl.contains(event.relatedTarget)) {
      columnEl.classList.remove("drag-over");
      list.querySelector(".drop-marker")?.remove();
    }
  });

  columnEl.addEventListener("drop", async (event) => {
    event.preventDefault();
    const id = Number(event.dataTransfer.getData("text/plain") || state.dragId);
    const { index } = dropIndex(list, event.clientY);
    clearDropMarkers();
    if (!id) return;
    try {
      await api(`/api/cards/${id}/move`, { method: "POST", body: { column: columnId, position: index } });
    } catch (err) {
      flash(`Move failed: ${err.message}`);
    }
    await loadBoard();
  });
}

// ---------- edit dialog ----------

function openEditor(card) {
  state.editing = card;
  const form = $("#card-form");
  form.elements.title.value = card.title;
  form.elements.description.value = card.description;
  $("#card-dialog").showModal();
  form.elements.title.focus();
}

$("#card-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = event.target;
  try {
    await api(`/api/cards/${state.editing.id}`, {
      method: "PATCH",
      body: { title: form.elements.title.value.trim(), description: form.elements.description.value },
    });
    $("#card-dialog").close();
    await loadBoard();
  } catch (err) {
    flash(err.message);
  }
});

$("#cancel-card").addEventListener("click", () => $("#card-dialog").close());

$("#delete-card").addEventListener("click", async () => {
  if (!confirm(`Delete "${state.editing.title}"?`)) return;
  try {
    await api(`/api/cards/${state.editing.id}`, { method: "DELETE" });
    $("#card-dialog").close();
    await loadBoard();
  } catch (err) {
    flash(err.message);
  }
});

// ---------- chat ----------

function addMessage(kind, text, extra) {
  const p = document.createElement("p");
  p.className = `msg ${kind}`;
  p.textContent = text;
  if (extra) {
    const small = document.createElement("small");
    small.textContent = extra;
    p.append(small);
  }
  const log = $("#chat-log");
  log.append(p);
  log.scrollTop = log.scrollHeight;
  return p;
}

$("#chat-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const input = $("#chat-input");
  const text = input.value.trim();
  if (!text) return;
  input.value = "";

  state.chat.push({ role: "user", content: text });
  addMessage("user", text);
  const pending = addMessage("assistant pending", "Thinking…");
  const button = event.target.querySelector("button");
  button.disabled = true;

  try {
    const data = await api("/api/chat", { method: "POST", body: { messages: state.chat } });
    pending.remove();
    state.chat.push({ role: "assistant", content: data.reply });
    const tools = data.actions.map((a) => a.ok ? a.tool : `${a.tool} (failed)`).join(", ");
    addMessage("assistant", data.reply, tools ? `tools: ${tools}` : "");
    if (data.board_changed) await loadBoard();
  } catch (err) {
    pending.remove();
    state.chat.pop();  // keep failed turns out of the history
    addMessage("note error", err.message);
  } finally {
    button.disabled = false;
    input.focus();
  }
});

$("#chat-input").addEventListener("keydown", (event) => {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    $("#chat-form").requestSubmit();
  }
});

loadBoard();
