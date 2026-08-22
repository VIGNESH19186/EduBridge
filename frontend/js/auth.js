/**
 * EduBridge AI — Auth handling for login.html / register.html and route guards.
 */
const Auth = {
  requireRole(roles) {
    const user = Api.currentUser();
    if (!user || !Api.token()) {
      window.location.href = "/login.html";
      return null;
    }
    if (roles && !roles.includes(user.role)) {
      window.location.href = "/index.html";
      return null;
    }
    return user;
  },

  logout() {
    Api.clearSession();
    window.location.href = "/index.html";
  },
};

function showFormError(formEl, message) {
  let errorBox = formEl.querySelector(".form-error-box");
  if (!errorBox) {
    errorBox = document.createElement("div");
    errorBox.className = "form-error-box";
    errorBox.style.cssText =
      "background:#FBE2E0;color:#C6403A;padding:12px 14px;border-radius:10px;margin-bottom:16px;font-size:0.88rem;";
    formEl.prepend(errorBox);
  }
  errorBox.textContent = message;
  errorBox.style.display = "block";
}

document.addEventListener("DOMContentLoaded", () => {
  const loginForm = document.getElementById("login-form");
  if (loginForm) {
    loginForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const submitBtn = loginForm.querySelector("button[type=submit]");
      submitBtn.disabled = true;
      submitBtn.textContent = "Signing in...";

      const email = loginForm.email.value.trim();
      const password = loginForm.password.value;

      try {
        const data = await Api.login({ email, password });
        Api.setSession(data.access_token, {
          id: data.user_id,
          name: data.name,
          role: data.role,
        });
        if (data.role === "teacher" || data.role === "admin") {
          window.location.href = "/teacher-dashboard.html";
        } else {
          window.location.href = "/student-dashboard.html";
        }
      } catch (err) {
        showFormError(loginForm, err.message);
        submitBtn.disabled = false;
        submitBtn.textContent = "Sign In";
      }
    });
  }

  const registerForm = document.getElementById("register-form");
  if (registerForm) {
    registerForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const submitBtn = registerForm.querySelector("button[type=submit]");
      submitBtn.disabled = true;
      submitBtn.textContent = "Creating account...";

      const roleTab = registerForm.querySelector(".auth-tab.active");
      const role = roleTab ? roleTab.dataset.role : "student";

      const payload = {
        name: registerForm.name.value.trim(),
        email: registerForm.email.value.trim(),
        password: registerForm.password.value,
        role,
        preferred_language: "English",
      };

      try {
        const data = await Api.register(payload);
        Api.setSession(data.access_token, { id: data.user_id, name: data.name, role: data.role });
        window.location.href = data.role === "teacher" ? "/teacher-dashboard.html" : "/student-dashboard.html";
      } catch (err) {
        showFormError(registerForm, err.message);
        submitBtn.disabled = false;
        submitBtn.textContent = "Create Account";
      }
    });

    registerForm.querySelectorAll(".auth-tab").forEach((tab) => {
      tab.addEventListener("click", () => {
        registerForm.querySelectorAll(".auth-tab").forEach((t) => t.classList.remove("active"));
        tab.classList.add("active");
      });
    });
  }

  const logoutBtn = document.getElementById("logout-btn");
  if (logoutBtn) {
    logoutBtn.addEventListener("click", (e) => {
      e.preventDefault();
      Auth.logout();
    });
  }

  // Populate sidebar user info if present on the page
  const user = Api.currentUser();
  if (user) {
    const nameEl = document.getElementById("sidebar-user-name");
    const roleEl = document.getElementById("sidebar-user-role");
    const avatarEl = document.getElementById("sidebar-avatar");
    if (nameEl) nameEl.textContent = user.name;
    if (roleEl) roleEl.textContent = user.role.charAt(0).toUpperCase() + user.role.slice(1);
    if (avatarEl) avatarEl.textContent = user.name.charAt(0).toUpperCase();
  }

  // Mobile sidebar drawer toggle
  const topbarToggle = document.querySelector(".topbar-toggle");
  const sidebar = document.querySelector(".sidebar");
  if (topbarToggle && sidebar) {
    topbarToggle.addEventListener("click", () => sidebar.classList.toggle("open"));
  }
});
