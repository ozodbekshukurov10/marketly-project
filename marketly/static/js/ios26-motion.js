document.addEventListener("DOMContentLoaded", () => {
  const motionTargets = document.querySelectorAll(
    ".navbar, .hero-content, .step-card, .profile-card, .service-card, .service-row, .card, .product-card, .promo-banner, .category-card, .stat-card, .stat, .panel, .info-section, .add-product-section, .top-bar, .feed-info, .product-grid, .sidebar, .main-content, .login-card"
  );

  motionTargets.forEach((element, index) => {
    element.classList.add("motion-item");
    if (index % 3 === 0) {
      element.classList.add("floaty");
    }
    element.style.transitionDelay = `${Math.min(index * 45, 420)}ms`;
  });

  const reveal = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          reveal.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.12 }
  );

  motionTargets.forEach((element) => reveal.observe(element));

  document.querySelectorAll("button, .btn-primary, .btn-secondary, .product-card, .card, .panel, .stat, .stat-card").forEach((element) => {
    element.addEventListener("pointermove", (event) => {
      if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
        return;
      }

      const rect = element.getBoundingClientRect();
      const x = ((event.clientX - rect.left) / rect.width - 0.5) * 6;
      const y = ((event.clientY - rect.top) / rect.height - 0.5) * -6;
      element.style.transform = `perspective(900px) rotateX(${y}deg) rotateY(${x}deg) translateY(-2px)`;
    });

    element.addEventListener("pointerleave", () => {
      element.style.transform = "";
    });
  });
});
