/**
 * EduBridge AI — Student analytics/progress charts.
 */
document.addEventListener("DOMContentLoaded", async () => {
  const user = Auth.requireRole(["student"]);
  if (!user) return;

  try {
    const data = await Api.studentAnalytics();
    renderSubjectChart(data.subject_mastery);
    renderWeeklyChart(data.weekly_activity);
    renderTopicChart(data.topic_performance);
    document.getElementById("quiz-accuracy-value").textContent = `${data.quiz_accuracy}%`;
  } catch (err) {
    document.querySelector("main").innerHTML = `<div class="state-block card">
      <div class="state-icon">⚠️</div>
      <p class="mb-0">We couldn't load your analytics. Please try again.</p>
    </div>`;
  }
});

const CHART_COLORS = ["#0F9B8E", "#E8A33D", "#2A3358", "#C6403A", "#A7ADC9", "#0B7D72"];

function renderSubjectChart(subjectMastery) {
  const ctx = document.getElementById("subject-chart");
  if (!subjectMastery || subjectMastery.length === 0) {
    ctx.parentElement.innerHTML += `<p class="text-sm text-muted mt-2">No subject data yet.</p>`;
    return;
  }
  new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: subjectMastery.map((s) => s.topic),
      datasets: [{ data: subjectMastery.map((s) => s.mastery_percent), backgroundColor: CHART_COLORS }],
    },
    options: { plugins: { legend: { position: "bottom" } } },
  });
}

function renderWeeklyChart(weeklyActivity) {
  const ctx = document.getElementById("weekly-chart");
  if (!weeklyActivity || weeklyActivity.length === 0) {
    ctx.parentElement.innerHTML += `<p class="text-sm text-muted mt-2">No activity data yet.</p>`;
    return;
  }
  new Chart(ctx, {
    type: "bar",
    data: {
      labels: weeklyActivity.map((d) => d.day),
      datasets: [{ label: "Questions Solved", data: weeklyActivity.map((d) => d.questions_solved), backgroundColor: "#0F9B8E", borderRadius: 6 }],
    },
    options: { plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true, ticks: { precision: 0 } } } },
  });
}

function renderTopicChart(topicPerformance) {
  const ctx = document.getElementById("topic-chart");
  if (!topicPerformance || topicPerformance.length === 0) {
    ctx.parentElement.innerHTML += `<p class="text-sm text-muted mt-2">No topic data yet.</p>`;
    return;
  }
  new Chart(ctx, {
    type: "bar",
    data: {
      labels: topicPerformance.map((t) => t.topic),
      datasets: [{ label: "Mastery %", data: topicPerformance.map((t) => t.mastery_percent), backgroundColor: "#E8A33D", borderRadius: 6 }],
    },
    options: {
      indexAxis: "y",
      plugins: { legend: { display: false } },
      scales: { x: { beginAtZero: true, max: 100 } },
    },
  });
}
