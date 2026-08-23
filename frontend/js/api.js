/**
 * EduBridge AI — API client
 * Central wrapper around fetch() for all backend REST calls.
 * All frontend pages use this instead of hard-coded fetch calls.
 */
const API_BASE = window.location.origin;

const Api = {
  token() {
    return localStorage.getItem("edubridge_token");
  },

  setSession(token, user) {
    localStorage.setItem("edubridge_token", token);
    localStorage.setItem("edubridge_user", JSON.stringify(user));
  },

  clearSession() {
    localStorage.removeItem("edubridge_token");
    localStorage.removeItem("edubridge_user");
  },

  currentUser() {
    const raw = localStorage.getItem("edubridge_user");
    return raw ? JSON.parse(raw) : null;
  },

  async request(path, { method = "GET", body = null, auth = true } = {}) {
    const headers = { "Content-Type": "application/json", "Accept-Language": "en" };
    if (auth && this.token()) {
      headers["Authorization"] = `Bearer ${this.token()}`;
    }

    let response;
    try {
      response = await fetch(`${API_BASE}${path}`, {
        method,
        headers,
        body: body ? JSON.stringify(body) : undefined,
      });
    } catch (networkErr) {
      throw new Error("Network error — please check your connection and try again.");
    }

    if (response.status === 401) {
      this.clearSession();
      if (!path.includes("/auth/login")) {
        window.location.href = "/login.html";
      }
    }

    let data = null;
    try {
      data = await response.json();
    } catch (_) {
      data = null;
    }

    if (!response.ok) {
      const message = (data && data.detail) || "Something went wrong. Please try again.";
      throw new Error(typeof message === "string" ? message : JSON.stringify(message));
    }

    return data;
  },

  // ---- Auth ----
  register: (payload) => Api.request("/api/auth/register", { method: "POST", body: payload, auth: false }),
  login: (payload) => Api.request("/api/auth/login", { method: "POST", body: payload, auth: false }),
  me: () => Api.request("/api/auth/me"),

  // ---- Students ----
  studentMe: () => Api.request("/api/students/me"),
  studentProgress: () => Api.request("/api/students/progress"),

  // ---- Doubts ----
  askDoubt: (payload) => Api.request("/api/doubts", { method: "POST", body: payload }),
  doubtHistory: () => Api.request("/api/doubts/history"),

  // ---- Practice ----
  generatePractice: (payload) => Api.request("/api/practice/generate", { method: "POST", body: payload }),
  submitPractice: (payload) => Api.request("/api/practice/submit", { method: "POST", body: payload }),

  // ---- Recommendations ----
  recommendations: () => Api.request("/api/recommendations"),

  // ---- Analytics ----
  studentAnalytics: () => Api.request("/api/analytics/student"),

  // ---- Teachers ----
  teacherDashboard: () => Api.request("/api/teachers/dashboard"),
  teacherStudents: () => Api.request("/api/teachers/students"),
  teacherInsights: () => Api.request("/api/teachers/insights"),

  // ---- Knowledge base ----
  knowledgeSearch: (query) => Api.request(`/api/knowledge/search?query=${encodeURIComponent(query)}`),
  knowledgeResources: () => Api.request("/api/knowledge/resources"),
};
