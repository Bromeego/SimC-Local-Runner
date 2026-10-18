(function () {
  const toggle = document.getElementById("theme-toggle");
  if (!toggle) return;

  function currentTheme() {
    return document.documentElement.dataset.theme === "light" ? "light" : "dark";
  }

  function updateThemeColor() {
    const themeColor = document.querySelector('meta[name="theme-color"]');
    if (!themeColor) return;
    themeColor.setAttribute(
      "content",
      currentTheme() === "light" ? "#f0efec" : "#111315"
    );
  }

  function updateLabel() {
    toggle.textContent = currentTheme() === "dark" ? "Light theme" : "Dark theme";
    updateThemeColor();
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
