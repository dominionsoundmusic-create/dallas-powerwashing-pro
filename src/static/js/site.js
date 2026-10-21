/* Dallas Power Washing Pro: header menu, submenus, EN/ES toggle and click-to-play video.
   The site works without this file; it only adds menu toggles, translation and video loading. */
(function () {
  "use strict";
  // YouTube click-to-play: the iframe is only created after the visitor presses play.
  document.querySelectorAll(".video[data-yt]").forEach(function (box) {
    var btn = box.querySelector(".video__play");
    if (!btn) return;
    btn.addEventListener("click", function () {
      var f = document.createElement("iframe");
      f.src = "https://www.youtube-nocookie.com/embed/" + box.getAttribute("data-yt") + "?autoplay=1&rel=0";
      f.title = btn.getAttribute("aria-label").replace(/^Play video: /, "");
      f.allow = "accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture";
      f.allowFullscreen = true;
      box.innerHTML = "";
      box.appendChild(f);
    });
  });

  var header = document.querySelector(".site-header");
  if (!header) return;

  // Mobile menu
  var toggle = header.querySelector(".nav-toggle");
  if (toggle) {
    toggle.addEventListener("click", function () {
      var open = header.classList.toggle("nav-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  // Submenus (click / keyboard)
  var subToggles = header.querySelectorAll(".sub-toggle");
  function closeAll(except) {
    subToggles.forEach(function (b) {
      if (b === except) return;
      b.setAttribute("aria-expanded", "false");
      b.closest(".has-sub").classList.remove("sub-open");
    });
  }
  subToggles.forEach(function (btn) {
    btn.addEventListener("click", function (e) {
      e.stopPropagation();
      var li = btn.closest(".has-sub");
      var open = !li.classList.contains("sub-open");
      closeAll(btn);
      li.classList.toggle("sub-open", open);
      btn.setAttribute("aria-expanded", open ? "true" : "false");
    });
  });
  document.addEventListener("click", function (e) {
    if (!header.contains(e.target)) closeAll(null);
  });
  document.addEventListener("keydown", function (e) {
    if (e.key !== "Escape") return;
    var openBtn = header.querySelector('.sub-toggle[aria-expanded="true"]');
    closeAll(null);
    if (openBtn) openBtn.focus();
    if (header.classList.contains("nav-open")) {
      header.classList.remove("nav-open");
      toggle.setAttribute("aria-expanded", "false");
      toggle.focus();
    }
  });
  header.querySelectorAll(".has-sub").forEach(function (li) {
    li.addEventListener("focusout", function (e) {
      if (!li.contains(e.relatedTarget)) {
        li.classList.remove("sub-open");
        var b = li.querySelector(".sub-toggle");
        if (b) b.setAttribute("aria-expanded", "false");
      }
    });
  });

  // EN / ES toggle using Google Translate
  var host = location.hostname;
  function setCookie(val) {
    var exp = val ? "" : "; expires=Thu, 01 Jan 1970 00:00:00 GMT";
    document.cookie = "googtrans=" + val + "; path=/" + exp;
    if (host.indexOf(".") > -1) {
      var root = host.split(".").slice(-2).join(".");
      document.cookie = "googtrans=" + val + "; path=/; domain=." + root + exp;
    }
  }
  function currentLang() {
    return /googtrans=\/en\/es/.test(document.cookie) ? "es" : "en";
  }
  function loadTranslate() {
    if (window.__gtLoaded) return;
    window.__gtLoaded = true;
    window.googleTranslateElementInit = function () {
      /* global google */
      new google.translate.TranslateElement(
        { pageLanguage: "en", includedLanguages: "es", autoDisplay: false },
        "google_translate_element"
      );
    };
    var s = document.createElement("script");
    s.src = "https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit";
    s.async = true;
    document.body.appendChild(s);
  }
  var lang = currentLang();
  header.querySelectorAll(".lang__btn").forEach(function (b) {
    b.setAttribute("aria-pressed", b.getAttribute("data-lang") === lang ? "true" : "false");
    b.addEventListener("click", function () {
      var want = b.getAttribute("data-lang");
      if (want === currentLang()) return;
      if (want === "es") setCookie("/en/es");
      else setCookie("");
      location.reload();
    });
  });
  if (lang === "es") {
    document.documentElement.lang = "es";
    loadTranslate();
  }
})();
