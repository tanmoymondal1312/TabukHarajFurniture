(function () {
  "use strict";

  var toggle = document.getElementById("nav-toggle");
  var nav = document.getElementById("site-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    });
  }

  document.querySelectorAll("img[data-fallback]").forEach(function (img) {
    img.addEventListener(
      "error",
      function () {
        img.src = img.dataset.fallback;
      },
      { once: true }
    );
  });

  var root = document.querySelector("[data-carousel]");
  if (!root) return;

  var slides = Array.prototype.slice.call(root.querySelectorAll(".hero__slide"));
  var dotsWrap = document.querySelector("[data-carousel-dots]");
  var prevBtn = document.querySelector("[data-carousel-prev]");
  var nextBtn = document.querySelector("[data-carousel-next]");
  var index = 0;

  function render() {
    slides.forEach(function (slide, i) {
      slide.classList.toggle("is-active", i === index);
    });
    if (dotsWrap) {
      Array.prototype.forEach.call(dotsWrap.children, function (dot, i) {
        dot.classList.toggle("is-active", i === index);
        dot.setAttribute("aria-current", i === index ? "true" : "false");
      });
    }
  }

  if (dotsWrap && slides.length) {
    slides.forEach(function (_, i) {
      var dot = document.createElement("button");
      dot.type = "button";
      dot.className = "hero__dot" + (i === 0 ? " is-active" : "");
      dot.setAttribute("aria-label", "Go to slide " + (i + 1));
      dot.addEventListener("click", function () {
        index = i;
        render();
      });
      dotsWrap.appendChild(dot);
    });
  }

  function go(delta) {
    if (!slides.length) return;
    index = (index + delta + slides.length) % slides.length;
    render();
  }

  if (prevBtn) prevBtn.addEventListener("click", function () { go(-1); });
  if (nextBtn) nextBtn.addEventListener("click", function () { go(1); });

  render();
})();
