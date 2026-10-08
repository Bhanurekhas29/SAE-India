(function () {
  'use strict';

  /* ---------- sticky header shadow + mobile menu ---------- */
  var header = document.querySelector('[data-header]');
  var toggle = document.querySelector('[data-nav-toggle]');
  var nav = document.getElementById('main-nav');

  function onScroll() {
    if (header) header.classList.toggle('scrolled', window.scrollY > 8);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      toggle.querySelector('.material-symbols-outlined').textContent = open ? 'close' : 'menu';
    });
    nav.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') {
        nav.classList.remove('open');
        toggle.setAttribute('aria-expanded', 'false');
        toggle.querySelector('.material-symbols-outlined').textContent = 'menu';
      }
    });
  }

  /* ---------- highlight the active menu item while scrolling ---------- */
  var navLinks = nav ? Array.prototype.slice.call(nav.querySelectorAll('a[href^="#"]')) : [];
  var spy = navLinks.map(function (a) {
    var id = a.getAttribute('href').slice(1);
    return { link: a, target: id ? document.getElementById(id) : null };
  }).filter(function (x) { return x.target; });

  function updateActive() {
    if (!spy.length) return;
    var offset = (header ? header.offsetHeight : 80) + 48;
    var current = null;
    var best = -Infinity;
    spy.forEach(function (x) {
      var top = x.target.getBoundingClientRect().top;
      if (top <= offset && top > best) { best = top; current = x; }
    });
    if (window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 4) {
      current = spy.reduce(function (a, b) { return b.target.getBoundingClientRect().top > a.target.getBoundingClientRect().top ? b : a; });
    }
    spy.forEach(function (x) {
      var on = x === current;
      x.link.classList.toggle('active', on);
      if (on) x.link.setAttribute('aria-current', 'true'); else x.link.removeAttribute('aria-current');
    });
  }
  var spyTick = false;
  window.addEventListener('scroll', function () {
    if (spyTick) return;
    spyTick = true;
    requestAnimationFrame(function () { updateActive(); spyTick = false; });
  }, { passive: true });
  window.addEventListener('resize', updateActive);
  updateActive();

  /* ---------- soft scroll-in animation ---------- */
  var revealEls = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
      });
    }, { threshold: 0.12 });
    revealEls.forEach(function (el) { io.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add('in'); });
  }

  /* ---------- hero countdown ---------- */
  var cd = document.querySelector('[data-countdown]');
  if (cd) {
    var target = new Date(cd.getAttribute('data-countdown')).getTime();
    var parts = {
      days: cd.querySelector('[data-cd="days"]'), hours: cd.querySelector('[data-cd="hours"]'),
      minutes: cd.querySelector('[data-cd="minutes"]'), seconds: cd.querySelector('[data-cd="seconds"]')
    };
    var pad = function (n) { return String(n).padStart(2, '0'); };
    var tick = function () {
      var diff = target - Date.now();
      if (isNaN(target)) return;
      if (diff <= 0) {
        cd.classList.add('ended');
        cd.textContent = cd.getAttribute('data-ended') || '';
        clearInterval(timer);
        return;
      }
      var s = Math.floor(diff / 1000);
      parts.days.textContent = pad(Math.floor(s / 86400));
      parts.hours.textContent = pad(Math.floor(s % 86400 / 3600));
      parts.minutes.textContent = pad(Math.floor(s % 3600 / 60));
      parts.seconds.textContent = pad(s % 60);
    };
    var timer = setInterval(tick, 1000);
    tick();
  }

  /* ---------- stats count-up ---------- */
  var counters = document.querySelectorAll('[data-count]');
  function animateCount(el) {
    var raw = el.getAttribute('data-count');
    var end = parseInt(raw.replace(/[^0-9]/g, ''), 10);
    if (isNaN(end)) return;
    var withComma = raw.indexOf(',') !== -1;
    var start = performance.now(), dur = 1400;
    (function step(now) {
      var p = Math.min((now - start) / dur, 1);
      var v = Math.round(end * (1 - Math.pow(1 - p, 3)));
      el.textContent = withComma ? v.toLocaleString('en-US') : String(v);
      if (p < 1) requestAnimationFrame(step);
    })(start);
  }
  if ('IntersectionObserver' in window) {
    var co = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { animateCount(en.target); co.unobserve(en.target); }
      });
    }, { threshold: 0.6 });
    counters.forEach(function (el) { co.observe(el); });
  }

  /* ---------- partners carousel: always loops, pauses on hover, arrows nudge ---------- */
  document.querySelectorAll('[data-carousel]').forEach(function (car) {
    var viewport = car.querySelector('[data-viewport]');
    var track = car.querySelector('[data-track]');
    var originals = Array.prototype.slice.call(track.children);
    if (!originals.length) return;
    var autoplay = car.getAttribute('data-autoplay') === '1';
    var seconds = parseFloat(car.getAttribute('data-seconds')) || 30;
    var paused = false, last = null, pos = 0, half = 0;

    function clones(count) {
      for (var i = 0; i < count; i++) {
        originals.forEach(function (n) {
          var c = n.cloneNode(true);
          c.setAttribute('data-clone', '');
          c.setAttribute('aria-hidden', 'true');
          Array.prototype.forEach.call(c.querySelectorAll('a'), function (a) { a.tabIndex = -1; });
          track.appendChild(c);
        });
      }
    }

    function build() {
      Array.prototype.slice.call(track.querySelectorAll('[data-clone]')).forEach(function (n) { n.remove(); });
      track.style.width = 'max-content';
      var gap = parseFloat(getComputedStyle(track).columnGap) || 0;
      var setW = originals.reduce(function (w, n) { return w + n.getBoundingClientRect().width + gap; }, 0);
      var reps = Math.max(1, Math.ceil(viewport.clientWidth / setW));
      clones(reps * 2 - 1);          // two identical groups, each at least as wide as the viewport
      half = setW * reps;
      pos = 0;
      viewport.scrollLeft = 0;
    }
    build();

    function frame(ts) {
      if (autoplay && !paused && half) {
        if (last !== null) pos += (half / seconds) * ((ts - last) / 1000);
        if (pos >= half) pos -= half;
        viewport.scrollLeft = pos;
      }
      last = ts;
      requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);

    ['mouseenter', 'focusin', 'touchstart'].forEach(function (ev) { car.addEventListener(ev, function () { paused = true; }, { passive: true }); });
    ['mouseleave', 'focusout', 'touchend'].forEach(function (ev) { car.addEventListener(ev, function () { pos = viewport.scrollLeft; paused = false; }, { passive: true }); });

    function nudge(dir) {
      var step = viewport.clientWidth * 0.6;
      pos = viewport.scrollLeft + dir * step;
      if (pos < 0) pos += half;
      if (pos >= half) pos -= half;
      viewport.scrollTo({ left: pos, behavior: 'smooth' });
    }
    var prev = car.querySelector('.car-prev'), next = car.querySelector('.car-next');
    if (prev) prev.addEventListener('click', function () { nudge(-1); });
    if (next) next.addEventListener('click', function () { nudge(1); });

    var rt;
    window.addEventListener('resize', function () { clearTimeout(rt); rt = setTimeout(build, 200); });
  });

  /* ---------- gallery lightbox ---------- */
  document.querySelectorAll('[data-lightbox]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      e.preventDefault();
      var box = document.createElement('div');
      box.className = 'lightbox';
      box.setAttribute('role', 'dialog');
      var img = document.createElement('img'); img.src = a.href; img.alt = a.getAttribute('data-caption') || '';
      var wrap = document.createElement('div');
      wrap.appendChild(img);
      var cap = a.getAttribute('data-caption');
      if (cap) { var p = document.createElement('p'); p.textContent = cap; wrap.appendChild(p); }
      var close = document.createElement('button'); close.type = 'button'; close.setAttribute('aria-label', 'Close'); close.innerHTML = '&times;';
      box.appendChild(wrap); box.appendChild(close);
      function shut() { box.remove(); document.removeEventListener('keydown', onKey); }
      function onKey(ev) { if (ev.key === 'Escape') shut(); }
      box.addEventListener('click', function (ev) { if (ev.target !== img) shut(); });
      document.addEventListener('keydown', onKey);
      document.body.appendChild(box);
    });
  });
})();
