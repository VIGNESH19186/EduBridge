/**
 * EduBridge AI — Knowledge Base page: upload, ingest, browse, search.
 */
document.addEventListener("DOMContentLoaded", async () => {
  const user = Auth.requireRole(["student", "teacher", "admin"]);
  if (!user) return;

  renderNav(user.role);

  const isTeacherOrAdmin = user.role === "teacher" || user.role === "admin";
  const uploadCard = document.getElementById("upload-card");
  if (!isTeacherOrAdmin) uploadCard.classList.add("hidden");

  await loadResources();

  document.getElementById("upload-form").addEventListener("submit", handleUpload);
  document.getElementById("search-btn").addEventListener("click", handleSearch);
});

function renderNav(role) {
  const navEl = document.getElementById("nav-links");
  if (role === "student") {
    navEl.innerHTML = `
      <a href="/student-dashboard.html" class="sidebar-link">📊 Dashboard</a>
      <a href="/doubt-solver.html" class="sidebar-link">💬 Ask AI</a>
      <a href="/practice.html" class="sidebar-link">📝 Practice</a>
      <a href="/analytics.html" class="sidebar-link">📈 Progress</a>
      <a href="/knowledge-base.html" class="sidebar-link active">📚 Knowledge Base</a>
    `;
  } else {
    navEl.innerHTML = `
      <a href="/teacher-dashboard.html" class="sidebar-link">📊 Dashboard</a>
      <a href="/teacher-dashboard.html#insights" class="sidebar-link">🚨 Student Insights</a>
      <a href="/knowledge-base.html" class="sidebar-link active">📚 Knowledge Base</a>
    `;
  }
}

async function loadResources() {
  const loadingEl = document.getElementById("resources-loading");
  const gridEl = document.getElementById("resources-grid");

  try {
    const data = await Api.knowledgeResources();
    const entries = Object.entries(data.by_subject || {});
    if (entries.length === 0) {
      gridEl.innerHTML = `<div class="state-block" style="grid-column:1/-1;">
        <div class="state-icon">📚</div>
        <p class="mb-0">No resources uploaded yet.</p>
      </div>`;
    } else {
      gridEl.innerHTML = entries
        .map(
          ([subject, count]) => `
        <div class="stat-card">
          <div class="stat-label">${escapeHtmlK(subject)}</div>
          <div class="stat-value">${count}</div>
          <div class="stat-sub">resource${count !== 1 ? "s" : ""}</div>
        </div>`
        )
        .join("");
    }
    loadingEl.classList.add("hidden");
    gridEl.classList.remove("hidden");
  } catch (err) {
    loadingEl.innerHTML = `<div class="state-block" style="grid-column:1/-1;">
      <p class="mb-0">We couldn't load resources. Please try again.</p>
    </div>`;
  }
}

async function handleUpload(e) {
  e.preventDefault();
  const statusEl = document.getElementById("upload-status");
  const fileInput = document.getElementById("file-input");
  const file = fileInput.files[0];
  if (!file) return;

  statusEl.textContent = "Uploading...";

  const formData = new FormData();
  formData.append("file", file);
  formData.append("subject", document.getElementById("subject-input").value);
  formData.append("topic", document.getElementById("topic-input").value);
  formData.append("title", document.getElementById("title-input").value);
  formData.append("author", document.getElementById("author-input").value);
  formData.append("url", document.getElementById("url-input").value);
  formData.append("license", document.getElementById("license-input").value);

  try {
    const uploadRes = await fetch(`${window.location.origin}/api/knowledge/upload`, {
      method: "POST",
      headers: { Authorization: `Bearer ${Api.token()}` },
      body: formData,
    });
    const uploadData = await uploadRes.json();
    if (!uploadRes.ok) throw new Error(uploadData.detail || "Upload failed");

    statusEl.textContent = "Uploaded. Indexing document...";

    const ingestRes = await fetch(
      `${window.location.origin}/api/knowledge/ingest?document_id=${uploadData.document_id}`,
      { method: "POST", headers: { Authorization: `Bearer ${Api.token()}` } }
    );
    const ingestData = await ingestRes.json();
    if (!ingestRes.ok) throw new Error(ingestData.detail || "Ingestion failed");

    statusEl.textContent = `✓ ${ingestData.message}`;
    document.getElementById("upload-form").reset();
    await loadResources();
  } catch (err) {
    statusEl.textContent = `Error: ${err.message}`;
  }
}

async function handleSearch() {
  const query = document.getElementById("search-input").value.trim();
  const resultsEl = document.getElementById("search-results");
  if (!query) return;

  resultsEl.innerHTML = `<div class="skeleton" style="height:60px;"></div>`;

  try {
    const results = await Api.knowledgeSearch(query);
    if (!results || results.length === 0) {
      resultsEl.innerHTML = `<div class="state-block">
        <p class="mb-0">No matching sources found in the knowledge base for this query.</p>
      </div>`;
      return;
    }
    resultsEl.innerHTML = results
      .map(
        (r) => `
      <div class="card-flat mt-2">
        <strong>${escapeHtmlK(r.title)}</strong> — ${escapeHtmlK(r.section)}
        <p class="text-sm mt-2 mb-0 text-muted">${escapeHtmlK(r.content.slice(0, 220))}...</p>
      </div>`
      )
      .join("");
  } catch (err) {
    resultsEl.innerHTML = `<div class="state-block"><p class="mb-0">Search failed. Please try again.</p></div>`;
  }
}

function escapeHtmlK(str) {
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}
