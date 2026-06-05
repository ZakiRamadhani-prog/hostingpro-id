document.addEventListener("DOMContentLoaded", () => {
  // Dark/light theme toggle based on data-bs-theme
  const btn = document.getElementById("themeToggle");
  const root = document.documentElement;

  // Apply theme ASAP before the user sees the page (best-effort)
  try {
    const initial = localStorage.getItem("theme");
    if (initial === "light" || initial === "dark") {
      root.setAttribute("data-bs-theme", initial);
    }
  } catch (e) {}

  if (btn) {
    const applyTheme = (theme) => {
      root.setAttribute("data-bs-theme", theme);
      try {
        localStorage.setItem("theme", theme);
      } catch (e) {}
    };

    const initial = (() => {
      try {
        return localStorage.getItem("theme");
      } catch (e) {
        return null;
      }
    })();

    if (initial === "light" || initial === "dark") {
      applyTheme(initial);
    }

    btn.addEventListener("click", () => {
      const current = root.getAttribute("data-bs-theme") || "dark";
      applyTheme(current === "dark" ? "light" : "dark");
    });
  }

  // Reveal on scroll
  const revealEls = document.querySelectorAll(".reveal");
  const obs = new IntersectionObserver(
    (entries) => {
      entries.forEach((e) => {
        if (e.isIntersecting) e.target.classList.add("is-visible");
      });
    },
    { threshold: 0.12 },
  );

  revealEls.forEach((el) => obs.observe(el));
});
