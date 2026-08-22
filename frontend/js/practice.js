/**
 * EduBridge AI — Practice page logic: generate questions, answer, submit, show results.
 */
let currentQuestions = [];
let currentIndex = 0;
let userAnswers = [];

document.addEventListener("DOMContentLoaded", () => {
  const user = Auth.requireRole(["student"]);
  if (!user) return;

  const params = new URLSearchParams(window.location.search);
  const topicParam = params.get("topic");
  if (topicParam) {
    document.getElementById("topic-input").value = topicParam;
  }

  document.getElementById("generate-btn").addEventListener("click", generateQuestions);

  // Auto-generate if a topic was passed in via the URL (from a recommendation)
  if (topicParam) generateQuestions();
  else {
    document.getElementById("practice-subtitle").textContent =
      "Enter a topic above, or leave blank for a mixed set based on your recent performance.";
  }
});

async function generateQuestions() {
  const topic = document.getElementById("topic-input").value.trim();
  const count = parseInt(document.getElementById("count-input").value, 10) || 5;
  const areaEl = document.getElementById("practice-area");

  areaEl.innerHTML = `<div class="skeleton" style="height:220px;"></div>`;
  document.getElementById("practice-subtitle").textContent = "Loading your recommended questions...";

  try {
    const questions = await Api.generatePractice({ topic: topic || null, count });
    if (!questions || questions.length === 0) {
      areaEl.innerHTML = `<div class="state-block card">
        <div class="state-icon">📭</div>
        <h4>No questions found</h4>
        <p class="mb-0">We don't have practice questions for that topic yet. Try "Quadratic Equations", "Differential Calculus", "Fractions", "Newton's Laws of Motion", "Photosynthesis", or "Algorithms & Control Flow".</p>
      </div>`;
      document.getElementById("practice-subtitle").textContent = "";
      return;
    }
    currentQuestions = questions;
    currentIndex = 0;
    userAnswers = [];
    document.getElementById("practice-subtitle").textContent = `Topic: ${questions[0].topic} · Level: ${questions[0].difficulty}`;
    renderQuestion();
  } catch (err) {
    areaEl.innerHTML = `<div class="state-block card">
      <p class="mb-0">We couldn't load practice questions. Please try again.</p>
    </div>`;
  }
}

function renderQuestion() {
  const areaEl = document.getElementById("practice-area");
  const q = currentQuestions[currentIndex];

  areaEl.innerHTML = `
    <div class="card question-card">
      <div class="question-progress">Question ${currentIndex + 1} / ${currentQuestions.length}</div>
      <h3>${escapeHtmlP(q.prompt)}</h3>
      <div id="options-container" class="mt-4"></div>
    </div>
  `;

  const optionsContainer = document.getElementById("options-container");
  q.options.forEach((opt) => {
    const btn = document.createElement("button");
    btn.className = "option-btn";
    btn.textContent = opt;
    btn.addEventListener("click", () => selectOption(opt, btn));
    optionsContainer.appendChild(btn);
  });
}

function selectOption(answer, btnEl) {
  document.querySelectorAll(".option-btn").forEach((b) => b.classList.remove("selected"));
  btnEl.classList.add("selected");

  userAnswers.push({
    question_id: currentQuestions[currentIndex].id,
    given_answer: answer,
  });

  setTimeout(() => {
    if (currentIndex < currentQuestions.length - 1) {
      currentIndex++;
      renderQuestion();
    } else {
      submitPractice();
    }
  }, 300);
}

async function submitPractice() {
  const areaEl = document.getElementById("practice-area");
  areaEl.innerHTML = `<div class="skeleton" style="height:220px;"></div>`;

  try {
    const result = await Api.submitPractice({ answers: userAnswers });
    renderResults(result);
  } catch (err) {
    areaEl.innerHTML = `<div class="state-block card">
      <p class="mb-0">We couldn't submit your practice results. Please try again.</p>
    </div>`;
  }
}

function renderResults(result) {
  const areaEl = document.getElementById("practice-area");
  const resultsHtml = result.results
    .map(
      (r, i) => `
      <div class="card-flat mt-2">
        <div class="flex justify-between items-center">
          <strong>${r.is_correct ? "✓ Correct" : "✗ Incorrect"}</strong>
          <span class="text-sm text-muted">Q${i + 1}</span>
        </div>
        <p class="text-sm mt-2 mb-0">Correct answer: <strong>${escapeHtmlP(r.correct_answer)}</strong></p>
        <p class="text-sm mt-2 mb-0">Learning Tip: ${escapeHtmlP(r.explanation)}</p>
      </div>`
    )
    .join("");

  areaEl.innerHTML = `
    <div class="card">
      <h3>Results</h3>
      <div class="stat-grid" style="grid-template-columns: repeat(2, 1fr);">
        <div class="stat-card">
          <div class="stat-label">Score</div>
          <div class="stat-value">${result.score_percent}%</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">Next Difficulty</div>
          <div class="stat-value" style="font-size:1.4rem; text-transform:capitalize;">${result.new_difficulty_recommendation}</div>
        </div>
      </div>
      <div class="mt-4">${resultsHtml}</div>
      <button class="btn btn-accent mt-4" onclick="location.reload()">Practice Again</button>
    </div>
  `;
}

function escapeHtmlP(str) {
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}
