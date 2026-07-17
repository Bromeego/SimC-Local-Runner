(function () {
  const toggle = document.getElementById("theme-toggle");
  if (!toggle) return;

  function currentTheme() {
    return document.documentElement.dataset.theme === "light" ? "light" : "dark";
  }

  function updateLabel() {
    toggle.textContent = currentTheme() === "dark" ? "Light theme" : "Dark theme";
  }

  toggle.addEventListener("click", function () {
    const nextTheme = currentTheme() === "dark" ? "light" : "dark";
    document.documentElement.dataset.theme = nextTheme;
    try {
      localStorage.setItem("simc-theme", nextTheme);
    } catch (_error) {
      // The selected theme still applies for this page view.
    }
    updateLabel();
  });

  updateLabel();
})();
