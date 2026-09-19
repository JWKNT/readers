(() => {
  "use strict";

  const storageKey = "jehlp-theme";
  const legacyKeys = ["jwknt-theme", "bst-reader-theme", "solverTheme"];
  const media = window.matchMedia("(prefers-color-scheme: dark)");
  const root = document.documentElement;
  let followsSystem = true;

  function savedTheme() {
    try {
      const saved = localStorage.getItem(storageKey);
      if (saved === "dark" || saved === "light") return saved;
      for (const key of legacyKeys) {
        const legacy = localStorage.getItem(key);
        if (legacy === "dark" || legacy === "light") {
          try { localStorage.setItem(storageKey, legacy); } catch {}
          return legacy;
        }
      }
    } catch {}
    return "";
  }

  function updateControls(theme) {
    const dark = theme === "dark";
    const label = dark ? "Use light theme" : "Use dark theme";
    const meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.content = dark ? "#131412" : "#fbfaf7";
    document.querySelectorAll("[data-theme-toggle]").forEach((button) => {
      button.setAttribute("aria-pressed", String(dark));
      button.setAttribute("aria-label", label);
      button.dataset.themeTarget = dark ? "light" : "dark";
      button.title = label;
    });
  }

  function applyTheme(theme) {
    const dark = theme === "dark";
    root.dataset.theme = theme;
    root.classList.toggle("dark", dark);
    root.style.colorScheme = theme;
    updateControls(theme);
    const detail = { detail: { theme } };
    window.dispatchEvent(new CustomEvent("jehlp:themechange", detail));
    window.dispatchEvent(new CustomEvent("jwknt:themechange", detail));
  }

  function createControl() {
    if (document.querySelector("[data-theme-toggle]")) return;
    const button = document.createElement("button");
    button.className = "theme-toggle";
    button.type = "button";
    button.dataset.themeToggle = "";
    button.textContent = "◐";
    const slot = document.querySelector("[data-theme-toggle-slot], .site-header nav, header nav, .toolbar, .detail-nav");
    if (slot) slot.append(button);
    else {
      button.classList.add("theme-toggle--floating");
      document.body.prepend(button);
    }
  }

  const stored = savedTheme();
  followsSystem = !stored;
  applyTheme(stored || (media.matches ? "dark" : "light"));

  function setup() {
    createControl();
    updateControls(root.dataset.theme);
    document.querySelectorAll("[data-theme-toggle]").forEach((button) => {
      if (button.dataset.themeBound) return;
      button.dataset.themeBound = "true";
      button.addEventListener("click", () => {
        const next = root.dataset.theme === "dark" ? "light" : "dark";
        followsSystem = false;
        try { localStorage.setItem(storageKey, next); } catch {}
        applyTheme(next);
      });
    });
  }

  const followSystem = (event) => {
    if (followsSystem) applyTheme(event.matches ? "dark" : "light");
  };
  if (typeof media.addEventListener === "function") media.addEventListener("change", followSystem);
  else media.addListener(followSystem);

  // Same-origin pages share the preference; clearing it resumes system mode.
  // A storage event is not written back, avoiding a cross-tab feedback loop.
  window.addEventListener("storage", (event) => {
    try { if (event.storageArea && event.storageArea !== localStorage) return; } catch { return; }
    if (event.key !== storageKey && event.key !== null) return;
    const value = event.newValue;
    const valid = value === "dark" || value === "light";
    followsSystem = !valid;
    applyTheme(valid ? value : (media.matches ? "dark" : "light"));
  });

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", setup, { once: true });
  else setup();
})();
