/**
 * EduBridge AI — Teacher dashboard: stats, student insights, roster.
 */
document.addEventListener("DOMContentLoaded", async () => {
  const user = Auth.requireRole(["teacher", "admin"]);
  if (!user) return;

  await Promise.all([loadTeacherStats(), loadInsights(), loadRoster()]);
});

async function loadTeacherStats() {
  const loadingEl = document.getElementById("stats-loading");
  const gridEl = document.getElementById("stats-grid");

  try {
    const stats = await Api.teacherDashboard();
    gridEl.innerHTML = `
      <div class="stat-card">
        <div class="stat-label">Total Students</div>
        <div class="stat-value">${stats.total_students}</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Class Average</div>
        <div class="stat-value">${stats.class_average}%</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Students Needing Attention</div>
        <div class="stat-value">${stats.students_needing_attention}</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Topics Needing Review</div>
        <div class="stat-value">${stats.topics_needing_review}</div>
      </div>
    `;
    loadingEl.classList.add("hidden");
    gridEl.classList.remove("hidden");
  } catch (err) {
    loadingEl.innerHTML = `<div class="state-block" style="grid-column:1/-1;">
      <p class="mb-0">We couldn't load dashboard stats. Please try again.</p>
    </div>`;
  }
}

async function loadInsights() {
  const loadingEl = document.getElementById("insights-loading");
  const listEl = document.getElementById("insights-list");

  try {
    const insights = await Api.teacherInsights();
    if (!insights || insights.length === 0) {
      listEl.innerHTML = `<div class="state-block card">
        <div class="state-icon">✅</div>
        <p class="mb-0">No students currently flagged for attention. Great work!</p>
      </div>`;
    } else {
      listEl.innerHTML = insights
        .map((s) => {
          const badgeClass = s.risk_level === "HIGH" ? "badge-high" : s.risk_level === "MEDIUM" ? "badge-medium" : "badge-low";
          return `
          <div class="card mt-2">
            <div class="flex justify-between items-center">
              <h4 class="mb-0">${escapeHtmlT(s.student_name)}</h4>
              <span class="badge ${badgeClass}">${s.risk_level}</span>
            </div>
            <p class="text-sm mt-2 mb-0">${s.evidence.map(escapeHtmlT).join(" · ")}</p>
            <p class="text-sm mt-2 mb-0" style="color:var(--growth-600); font-weight:600;">Recommended: ${escapeHtmlT(s.recommended_intervention)}</p>
          </div>`;
        })
        .join("");
    }
    loadingEl.classList.add("hidden");
    listEl.classList.remove("hidden");
  } catch (err) {
    loadingEl.innerHTML = `<div class="state-block card">
      <p class="mb-0">We couldn't load student insights. Please try again.</p>
    </div>`;
  }
}

async function loadRoster() {
  const loadingEl = document.getElementById("roster-loading");
  const tableEl = document.getElementById("roster-table");

  try {
    const students = await Api.teacherStudents();
    if (!students || students.length === 0) {
      tableEl.innerHTML = `<div class="state-block"><p class="mb-0">No students enrolled yet.</p></div>`;
    } else {
      tableEl.innerHTML = `
        <table class="data-table">
          <thead><tr><th>Name</th><th>Grade Level</th></tr></thead>
          <tbody>
            ${students.map((s) => `<tr><td>${escapeHtmlT(s.name)}</td><td>${escapeHtmlT(s.grade_level)}</td></tr>`).join("")}
          </tbody>
        </table>
      `;
    }
    loadingEl.classList.add("hidden");
    tableEl.classList.remove("hidden");
  } catch (err) {
    loadingEl.innerHTML = `<div class="state-block"><p class="mb-0">We couldn't load the class roster.</p></div>`;
  }
}

function escapeHtmlT(str) {
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}
