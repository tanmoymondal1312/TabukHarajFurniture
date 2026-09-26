(function () {
  "use strict";

  /* ---- Mobile sidebar ---- */
  var sidebar = document.getElementById("sidebar");
  var overlay = document.getElementById("sidebar-overlay");
  var toggle = document.getElementById("sidebar-toggle");

  function setSidebar(open) {
    if (!sidebar) return;
    sidebar.classList.toggle("is-open", open);
    if (overlay) overlay.hidden = !open;
    if (toggle) toggle.setAttribute("aria-expanded", open ? "true" : "false");
  }

  if (toggle) {
    toggle.addEventListener("click", function () {
      setSidebar(!sidebar.classList.contains("is-open"));
    });
  }
  if (overlay) {
    overlay.addEventListener("click", function () { setSidebar(false); });
  }

  /* ---- Delete confirm ---- */
  document.querySelectorAll("form[data-confirm]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      if (!window.confirm(form.getAttribute("data-confirm"))) {
        e.preventDefault();
      }
    });
  });

  /* ---- Image live preview ---- */
  var fileInput = document.querySelector(".input--file");
  var preview = document.getElementById("photo-preview");
  if (fileInput && preview) {
    fileInput.addEventListener("change", function () {
      var file = fileInput.files && fileInput.files[0];
      if (!file) return;
      var img = preview.querySelector("img") || document.createElement("img");
      img.src = URL.createObjectURL(file);
      img.alt = "Preview";
      if (!img.parentNode) preview.innerHTML = "", preview.appendChild(img);
    });
  }

  /* ---- Auto-hide flash messages ---- */
  document.querySelectorAll(".alert--success").forEach(function (el) {
    setTimeout(function () {
      el.style.transition = "opacity .4s";
      el.style.opacity = "0";
      setTimeout(function () { el.remove(); }, 450);
    }, 4000);
  });

  /* ---- Close alerts ---- */
  document.querySelectorAll(".alert__close").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var alert = btn.closest(".alert");
      if (alert) alert.remove();
    });
  });
})();
