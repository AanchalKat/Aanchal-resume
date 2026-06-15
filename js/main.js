(function () {
  "use strict";

  const navToggle = document.querySelector(".nav-toggle");
  const navLinks = document.querySelector(".nav-links");
  const themeToggle = document.getElementById("theme-toggle");
  const yearEl = document.getElementById("year");
  const THEME_KEY = "theme";

  if (yearEl) {
    yearEl.textContent = new Date().getFullYear();
  }

  function getTheme() {
    return document.documentElement.getAttribute("data-theme") === "light" ? "light" : "dark";
  }

  function updateThemeToggle(theme) {
    if (!themeToggle) {
      return;
    }

    const isDark = theme === "dark";
    themeToggle.setAttribute("aria-label", isDark ? "Switch to light theme" : "Switch to dark theme");
    const label = themeToggle.querySelector(".theme-toggle-label");
    if (label) {
      label.textContent = isDark ? "Light" : "Dark";
    }
  }

  function setTheme(theme) {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem(THEME_KEY, theme);
    updateThemeToggle(theme);
  }

  updateThemeToggle(getTheme());

  if (themeToggle) {
    themeToggle.addEventListener("click", function () {
      setTheme(getTheme() === "dark" ? "light" : "dark");
    });
  }

  if (navToggle && navLinks) {
    navToggle.addEventListener("click", function () {
      const isOpen = document.body.classList.toggle("nav-open");
      navToggle.setAttribute("aria-expanded", String(isOpen));
    });

    navLinks.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        document.body.classList.remove("nav-open");
        navToggle.setAttribute("aria-expanded", "false");
      });
    });
  }

  const sections = document.querySelectorAll("section[id]");
  const navAnchors = document.querySelectorAll(".nav-links a");

  if (sections.length && navAnchors.length && "IntersectionObserver" in window) {
    const observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            const id = entry.target.getAttribute("id");
            navAnchors.forEach(function (anchor) {
              const isActive = anchor.getAttribute("href") === "#" + id;
              anchor.style.color = isActive ? "var(--color-text)" : "";
            });
          }
        });
      },
      { rootMargin: "-40% 0px -50% 0px", threshold: 0 }
    );

    sections.forEach(function (section) {
      observer.observe(section);
    });
  }
})();
