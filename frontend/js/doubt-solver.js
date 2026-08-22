/**
 * EduBridge AI — Doubt Solver chat interface logic.
 */
let lastQuestionText = "";

document.addEventListener("DOMContentLoaded", () => {
  const user = Auth.requireRole(["student"]);
  if (!user) return;

  LanguageManager.bindSelector(document.getElementById("language-select"));

  const sendBtn = document.getElementById("send-btn");
  const input = document.getElementById("doubt-input");

  sendBtn.addEventListener("click", handleAsk);
  input.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleAsk();
    }
  });

  input.addEventListener("input", () => {
    input.style.height = "auto";
    input.style.height = Math.min(input.scrollHeight, 160) + "px";
  });
});

function appendMessage({ role, html }) {
  const container = document.getElementById("chat-messages");
  const empty = document.getElementById("chat-empty");
  if (empty) empty.remove();

  const msgEl = document.createElement("div");
  msgEl.className = `msg msg-${role}`;
  msgEl.innerHTML = html;
  container.appendChild(msgEl);
  container.scrollTop = container.scrollHeight;
  return msgEl;
}

async function handleAsk() {
  const input = document.getElementById("doubt-input");
  const text = input.value.trim();
  if (!text) return;

  lastQuestionText = text;
  appendMessage({ role: "student", html: `<div class="msg-bubble">${escapeHtml(text)}</div>` });
  input.value = "";
  input.style.height = "auto";

  const loadingMsg = appendMessage({
    role: "ai",
    html: `<div class="msg-bubble"><span class="skeleton" style="display:inline-block;width:220px;height:14px;"></span></div>`,
  });

  const language = document.getElementById("language-select").value;
  const level = document.getElementById("level-select").value;

  try {
    const result = await Api.askDoubt({
      question_text: text,
      language,
      explanation_level: level,
    });
    renderAiResponse(loadingMsg, result);
  } catch (err) {
    loadingMsg.querySelector(".msg-bubble").innerHTML =
      `We couldn't process your question right now. Please try again. <span class="text-sm text-muted">(${escapeHtml(err.message)})</span>`;
  }
}

function renderAiResponse(msgEl, result) {
  const groundedBadge = result.grounded
    ? `<span class="badge badge-low">Grounded</span>`
    : `<span class="badge badge-medium">No source found</span>`;

  const citationsHtml =
    result.citations && result.citations.length > 0
      ? `<div class="msg-sources">
          <strong>Sources</strong>
          ${result.citations.map((c) => `${escapeHtml(c.title)} — ${escapeHtml(c.section)}`).join("<br/>")}
        </div>`
      : "";

  msgEl.innerHTML = `
    <div class="msg-bubble">
      <div class="flex gap-2 mt-2" style="flex-wrap:wrap; margin-bottom:10px;">
        <span class="badge badge-low">${escapeHtml(result.detected_subject)}</span>
        <span class="badge badge-medium">${escapeHtml(result.detected_topic)}</span>
        ${groundedBadge}
      </div>
      ${escapeHtml(result.explanation).replace(/\n/g, "<br/>")}
      ${citationsHtml}
      <div class="card-flat mt-4" style="background:var(--insight-100); border:none;">
        <strong class="text-sm">Quick Check</strong>
        <p class="mb-0 text-sm mt-2">${escapeHtml(result.quick_check_question)}</p>
      </div>
    </div>
    <div class="msg-actions">
      <button class="btn btn-outline btn-sm" onclick="requestVariation('simpler')">Explain Simpler</button>
      <button class="btn btn-outline btn-sm" onclick="requestVariation('example')">Give Example</button>
      <button class="btn btn-outline btn-sm" onclick="requestVariation('translate')">Translate</button>
      <a href="/practice.html?topic=${encodeURIComponent(result.detected_topic)}" class="btn btn-accent btn-sm">Practice This</a>
    </div>
  `;
}

async function requestVariation(type) {
  if (!lastQuestionText) return;
  const level = type === "simpler" ? "simpler" : document.getElementById("level-select").value;
  const language = type === "translate" ? document.getElementById("language-select").value : "English";

  const loadingMsg = appendMessage({
    role: "ai",
    html: `<div class="msg-bubble"><span class="skeleton" style="display:inline-block;width:220px;height:14px;"></span></div>`,
  });

  try {
    const result = await Api.askDoubt({
      question_text: lastQuestionText,
      language,
      explanation_level: level,
    });
    renderAiResponse(loadingMsg, result);
  } catch (err) {
    loadingMsg.querySelector(".msg-bubble").innerHTML = "We couldn't process that request. Please try again.";
  }
}

function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}
