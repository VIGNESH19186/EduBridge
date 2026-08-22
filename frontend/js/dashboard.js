/**
 * EduBridge AI — Student dashboard data loading.
 */
document.addEventListener("DOMContentLoaded", async () => {
  const user = Auth.requireRole(["student"]);
  if (!user) return;

  const hour = new Date().getHours();
  const greetingEl = document.getElementById("greeting");
  if (greetingEl) {
    const timeOfDay = hour < 12 ? "Morning" : hour < 18 ? "Afternoon" : "Evening";
    greetingEl.textContent = `Good ${timeOfDay}, ${user.name.split(" ")[0]} 👋`;
  }

  await Promise.all([loadStats(), loadRecommendations()]);
});

async function loadStats() {
  const loadingEl = document.getElementById("stats-loading");
  const gridEl = document.getElementById("stats-grid");
  const weakLoadingEl = document.getElementById("weak-topics-loading");
  const weakEl = document.getElementById("weak-topics");

  try {
    const profile = await Api.studentMe();

    gridEl.innerHTML = `
      <div class="stat-card">
        <div class="stat-label">Learning Progress</div>
        <div class="stat-value">${profile.overall_mastery}%</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Questions Solved</div>
        <div class="stat-value">${profile.questions_solved}</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Accuracy</div>
        <div class="stat-value">${profile.accuracy}%</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Learning Streak</div>
        <div class="stat-value">${profile.learning_streak_days}d</div>
      </div>
    `;
    loadingEl.classList.add("hidden");
    gridEl.classList.remove("hidden");

    if (profile.weak_topics && profile.weak_topics.length > 0) {
      weakEl.innerHTML = profile.weak_topics
        .map((t) => {
          const cls = t.mastery_percent < 50 ? "weak" : t.mastery_percent < 75 ? "mid" : "";
          return `
            <div class="topic-bar-row">
              <span class="topic-bar-label">${t.topic}</span>
              <div class="topic-bar-track"><div class="topic-bar-fill ${cls}" style="width:${t.mastery_percent}%"></div></div>
              <span class="topic-bar-value">${t.mastery_percent}%</span>
            </div>`;
        })
        .join("");
    } else {
      weakEl.innerHTML = `<div class="state-block">
        <div class="state-icon">🌱</div>
        <p class="mb-0">No practice data yet. Ask your first doubt or try a practice set to get started!</p>
      </div>`;
    }
    weakLoadingEl.classList.add("hidden");
    weakEl.classList.remove("hidden");
  } catch (err) {
    loadingEl.innerHTML = `<div class="state-block" style="grid-column:1/-1;">
      <div class="state-icon">⚠️</div>
      <p class="mb-0">We couldn't load your dashboard stats. Please try again.</p>
    </div>`;
    weakLoadingEl.innerHTML = `<div class="state-block"><p class="mb-0">We couldn't load your weak topics.</p></div>`;
  }
}

async function loadRecommendations() {
  const loadingEl = document.getElementById("recommendations-loading");
  const listEl = document.getElementById("recommendations-list");

  try {
    const recs = await Api.recommendations();
    if (!recs || recs.length === 0) {
      listEl.innerHTML = `<div class="state-block">
        <div class="state-icon">🎯</div>
        <p class="mb-0">Solve a few practice questions and we'll build your personalized learning path.</p>
      </div>`;
    } else {
      listEl.innerHTML = recs
        .map(
          (r) => `
        <div class="rec-card">
          <div class="rec-info">
            <h4>${r.topic_name}</h4>
            <p class="mb-0 text-sm text-muted">${r.reason}</p>
            <div class="rec-meta mt-2">
              <span>⏱ ${r.estimated_minutes} min</span>
              <span>📶 ${r.difficulty}</span>
            </div>
          </div>
          <a href="/practice.html?topic=${encodeURIComponent(r.topic_name)}" class="btn btn-outline btn-sm">Start</a>
        </div>`
        )
        .join("");
    }
    loadingEl.classList.add("hidden");
    listEl.classList.remove("hidden");
  } catch (err) {
    loadingEl.innerHTML = `<div class="state-block">
      <p class="mb-0">We couldn't load your recommendations. Please try again.</p>
    </div>`;
  }
}
