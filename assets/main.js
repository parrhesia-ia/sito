// ParrhesIA — interazioni del sito
(function () {
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // Menu mobile
  var burger = document.querySelector(".burger"), nav = document.querySelector(".nav");
  if (burger && nav) burger.addEventListener("click", function () {
    var open = nav.classList.toggle("open");
    burger.setAttribute("aria-expanded", open ? "true" : "false");
  });

  // Parola greca che compare lettera per lettera
  var greek = document.querySelector(".greek");
  if (greek) {
    var word = greek.getAttribute("data-word") || "";
    greek.textContent = "";
    var spans = word.split("").map(function (ch) {
      var s = document.createElement("span"); s.textContent = ch; greek.appendChild(s); return s;
    });
    spans.forEach(function (s, i) { setTimeout(function () { s.classList.add("on"); }, reduce ? 0 : 200 + i * 140); });
  }

  // Titolo con parola che cambia
  var rot = document.querySelector(".rot");
  if (rot) {
    var words = (rot.getAttribute("data-words") || "").split("|");
    if (reduce || words.length < 2) { rot.textContent = words[0]; }
    else {
      var wi = 0, ci = words[0].length, del = false;
      rot.textContent = words[0];
      var tick = function () {
        var w = words[wi];
        if (!del) {
          if (ci < w.length) { ci++; rot.textContent = w.slice(0, ci); setTimeout(tick, 80); }
          else { del = true; setTimeout(tick, 1800); }
        } else {
          if (ci > 0) { ci--; rot.textContent = w.slice(0, ci); setTimeout(tick, 40); }
          else { del = false; wi = (wi + 1) % words.length; setTimeout(tick, 200); }
        }
      };
      setTimeout(function () { del = true; tick(); }, 2600);
    }
  }

  // Comparsa allo scorrimento
  var io = "IntersectionObserver" in window ? new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) {
        e.target.classList.add("in");
        e.target.querySelectorAll("[data-w]").forEach(function (b) { b.style.width = b.getAttribute("data-w"); });
        io.unobserve(e.target);
      }
    });
  }, { threshold: 0.15 }) : null;
  var watch = function (el) { if (io) io.observe(el); else { el.classList.add("in"); el.querySelectorAll("[data-w]").forEach(function (b) { b.style.width = b.getAttribute("data-w"); }); } };
  document.querySelectorAll(".reveal").forEach(watch);

  // Articoli dalla lista
  var list = document.querySelector("[data-articoli]");
  if (list) {
    var base = list.getAttribute("data-base") || "";
    var limit = parseInt(list.getAttribute("data-limit") || "0", 10);
    fetch(base + "data/articoli.json").then(function (r) { return r.json(); }).then(function (items) {
      if (limit) items = items.slice(0, limit);
      list.innerHTML = "";
      items.forEach(function (a) {
        var el = document.createElement(a.url ? "a" : "div");
        el.className = "card reveal" + (a.url ? "" : " soon");
        if (a.url) el.href = base + a.url;
        el.innerHTML = '<span class="fmt"></span><h3></h3><p></p><span class="meta"></span>';
        el.querySelector(".fmt").textContent = a.formato;
        el.querySelector("h3").textContent = a.titolo;
        el.querySelector("p").textContent = a.sommario;
        el.querySelector(".meta").textContent = a.url ? a.data_testo : "In arrivo · " + a.data_testo;
        list.appendChild(el); watch(el);
      });
    }).catch(function () {
      list.innerHTML = '<p style="color:var(--muted)">Gli articoli non si sono caricati. Riprova tra poco.</p>';
    });
  }

  // Ieri e oggi: schede
  var tabs = document.querySelectorAll(".tab");
  tabs.forEach(function (t) {
    t.addEventListener("click", function () {
      tabs.forEach(function (x) { x.setAttribute("aria-selected", x === t ? "true" : "false"); });
      document.querySelectorAll("[data-pair]").forEach(function (p) { p.hidden = p.getAttribute("data-pair") !== t.getAttribute("data-target"); });
    });
  });
})();
