/**
 * EduBridge AI — Language selector logic shared by doubt-solver and dashboards.
 */
const SUPPORTED_LANGUAGES = ["English"];

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
    // If only one supported language, preselect it and hide the selector.
    if (SUPPORTED_LANGUAGES.length <= 1) {
      selectEl.innerHTML = `<option value="English">English</option>`;
      selectEl.value = "English";
      selectEl.disabled = true;
      selectEl.style.display = "none";
      this.set("English");
      return;
    }

    selectEl.innerHTML = SUPPORTED_LANGUAGES.map(
      (lang) => `<option value="${lang}">${lang}</option>`
    ).join("");
    selectEl.value = this.get();
    selectEl.addEventListener("change", () => this.set(selectEl.value));
  },
};
