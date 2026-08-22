/**
 * EduBridge AI — Language selector logic shared by doubt-solver and dashboards.
 */
const SUPPORTED_LANGUAGES = ["English", "हिन्दी", "ಕನ್ನಡ", "தமிழ்", "తెలుగు"];

const LanguageManager = {
  STORAGE_KEY: "edubridge_language",

  get() {
    return localStorage.getItem(this.STORAGE_KEY) || "English";
  },

  set(lang) {
    localStorage.setItem(this.STORAGE_KEY, lang);
  },

  bindSelector(selectEl) {
    if (!selectEl) return;
    selectEl.innerHTML = SUPPORTED_LANGUAGES.map(
      (lang) => `<option value="${lang}">${lang}</option>`
    ).join("");
    selectEl.value = this.get();
    selectEl.addEventListener("change", () => this.set(selectEl.value));
  },
};
