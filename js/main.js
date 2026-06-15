(function () {
  "use strict";

  const navToggle = document.querySelector(".nav-toggle");
  const navLinks = document.querySelector(".nav-links");
  const siteHeader = document.querySelector(".site-header");
  const backToTop = document.getElementById("back-to-top");
  const themeToggle = document.getElementById("theme-toggle");
  const yearEl = document.getElementById("year");
  const THEME_KEY = "theme";
  const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

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

  if (siteHeader) {
    function updateHeaderOnScroll() {
      const scrolled = window.scrollY > 12;
      siteHeader.classList.toggle("is-scrolled", scrolled);

      if (backToTop) {
        backToTop.classList.toggle("is-visible", window.scrollY > 400);
        backToTop.hidden = window.scrollY <= 400;
      }
    }

    updateHeaderOnScroll();
    window.addEventListener("scroll", updateHeaderOnScroll, { passive: true });
  }

  if (backToTop) {
    backToTop.addEventListener("click", function () {
      window.scrollTo({ top: 0, behavior: prefersReducedMotion ? "auto" : "smooth" });
    });
  }

  function initScrollReveal() {
    if (prefersReducedMotion || !("IntersectionObserver" in window)) {
      return;
    }

    const revealGroups = [
      { parent: ".about-grid", selector: ":scope > *", stagger: 100 },
      { parent: ".timeline", selector: ".timeline-item", stagger: 120 },
      { parent: ".skills-showcase", selector: ".skills-core", stagger: 0 },
      { parent: ".skills-cards", selector: ".skill-card", stagger: 80 },
      { parent: ".skills-footer", selector: ".skill-card", stagger: 100 },
      { parent: ".edu-grid", selector: ".edu-block", stagger: 100 },
      { parent: ".awards-list", selector: "li", stagger: 70 },
    ];

    const revealElements = [];

    document.querySelectorAll(".section-title").forEach(function (title) {
      title.classList.add("reveal");
      revealElements.push(title);
    });

    revealGroups.forEach(function (group) {
      document.querySelectorAll(group.parent).forEach(function (parent) {
        parent.querySelectorAll(group.selector).forEach(function (element, index) {
          element.classList.add("reveal");
          element.style.setProperty("--reveal-delay", String(index * group.stagger) + "ms");
          revealElements.push(element);
        });
      });
    });

    if (!revealElements.length) {
      return;
    }

    const revealObserver = new IntersectionObserver(
      function (entries, observer) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) {
            return;
          }

          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        });
      },
      { rootMargin: "0px 0px -8% 0px", threshold: 0.12 }
    );

    revealElements.forEach(function (element) {
      revealObserver.observe(element);
    });
  }

  initScrollReveal();

  const sections = document.querySelectorAll("section[id]");
  const navAnchors = document.querySelectorAll(".nav-links a");

  if (sections.length && navAnchors.length && "IntersectionObserver" in window) {
    const navObserver = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            const id = entry.target.getAttribute("id");
            navAnchors.forEach(function (anchor) {
              anchor.classList.toggle("is-active", anchor.getAttribute("href") === "#" + id);
            });
          }
        });
      },
      { rootMargin: "-40% 0px -50% 0px", threshold: 0 }
    );

    sections.forEach(function (section) {
      navObserver.observe(section);
    });
  }
})();
