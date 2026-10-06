(function () {
  var doc = document;
  doc.documentElement.classList.add('js');
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var LANG = doc.documentElement.lang === 'pl' ? 'pl' : 'en';
  var T = {
    pl: {
      films: 'Filmy pojawią się tutaj wkrótce.',
      filmsHint: 'Linki do YouTube nie zostały jeszcze dodane.',
      sent: 'Formularz jest poprawny, ale wiadomość nie została wysłana.',
      sentBody: 'Ta strona nie ma serwera, który mógłby wysłać e-mail. Proszę skopiować poniższe podsumowanie i wysłać je na adres ',
      invalid: 'Nie wysłano.',
      invalidBody: 'Proszę uzupełnić zaznaczone pola.',
      reqName: 'To pole jest wymagane',
      reqMail: 'Proszę podać adres e-mail, na który mogę odpowiedzieć',
      copied: 'Skopiowano',
      selectCopy: 'Zaznacz i skopiuj',
      noDate: 'nie podano', of: 'z'
    },
    en: {
      films: 'Films will appear here shortly.',
      filmsHint: 'The YouTube links have not been added yet.',
      sent: 'The form is valid, but nothing was sent.',
      sentBody: 'This site has no server that can send email. Copy the summary below and send it to ',
      invalid: 'Not sent.',
      invalidBody: 'Please fill in the highlighted fields.',
      reqName: 'This field is required',
      reqMail: 'Enter an email address I can reply to',
      copied: 'Copied',
      selectCopy: 'Select + copy',
      noDate: 'not given', of: 'of'
    }
  }[LANG];

  /* ---- drawer ---- */
  var drawer = doc.getElementById('drawer');
  if (drawer) {
    var lastFocus = null;
    function setDrawer(open) {
      drawer.setAttribute('data-open', open ? 'true' : 'false');
      drawer.setAttribute('aria-hidden', open ? 'false' : 'true');
      doc.body.style.overflow = open ? 'hidden' : '';
      if (open) { lastFocus = doc.activeElement; var f = drawer.querySelector('a,button'); if (f) f.focus(); }
      else if (lastFocus) { lastFocus.focus(); }
    }
    setDrawer(false);
    doc.querySelectorAll('[data-drawer-open]').forEach(function (b) { b.addEventListener('click', function () { setDrawer(true); }); });
    drawer.querySelectorAll('[data-drawer-close]').forEach(function (b) { b.addEventListener('click', function () { setDrawer(false); }); });
    drawer.querySelectorAll('a[href]').forEach(function (a) { a.addEventListener('click', function () { setDrawer(false); }); });
    doc.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && drawer.getAttribute('data-open') === 'true') setDrawer(false);
    });
  }

  /* ---- hero crossfade ---- */
  var stack = doc.querySelector('[data-stack]');
  if (stack) {
    var shots = [].slice.call(stack.querySelectorAll('img'));
    var counter = doc.querySelector('[data-stack-count]');
    var i = 0;
    function paint() {
      shots.forEach(function (s, n) { s.setAttribute('data-active', n === i ? 'true' : 'false'); });
      if (counter) counter.textContent = pad(i + 1) + ' / ' + pad(shots.length);
    }
    paint();
    if (shots.length > 1 && !reduce) setInterval(function () { i = (i + 1) % shots.length; paint(); }, 5200);
  }
  function pad(n) { return String(n).padStart(2, '0'); }

  /* ---- quotes ---- */
  var quotes = doc.querySelector('[data-quotes]');
  if (quotes) {
    var items = [].slice.call(quotes.querySelectorAll('.quote'));
    var qc = quotes.querySelector('[data-quote-count]');
    var q = 0;
    function show(n) {
      q = (n + items.length) % items.length;
      items.forEach(function (el, k) { el.setAttribute('data-active', k === q ? 'true' : 'false'); });
      if (qc) qc.textContent = pad(q + 1) + ' / ' + pad(items.length);
    }
    show(0);
    var p = quotes.querySelector('[data-quote-prev]'), nx = quotes.querySelector('[data-quote-next]');
    if (p) p.addEventListener('click', function () { show(q - 1); });
    if (nx) nx.addEventListener('click', function () { show(q + 1); });
  }

  /* ---- drag strips ---- */
  doc.querySelectorAll('[data-strip]').forEach(function (strip) {
    var down = false, startX = 0, startLeft = 0, moved = 0;
    strip.addEventListener('pointerdown', function (e) {
      if (e.pointerType === 'touch') return;
      down = true; moved = 0; startX = e.clientX; startLeft = strip.scrollLeft;
      strip.classList.add('is-drag');
    });
    window.addEventListener('pointermove', function (e) {
      if (!down) return;
      var dx = e.clientX - startX; moved = Math.abs(dx); strip.scrollLeft = startLeft - dx;
    });
    window.addEventListener('pointerup', function () { if (down) { down = false; strip.classList.remove('is-drag'); } });
    strip.addEventListener('click', function (e) { if (moved > 6) e.preventDefault(); }, true);
  });

  /* ---- work page tabs ---- */
  var tabs = doc.querySelector('[data-tabs]');
  if (tabs) {
    var panels = {};
    doc.querySelectorAll('[data-panel]').forEach(function (p) { panels[p.getAttribute('data-panel')] = p; });
    function select(key) {
      tabs.querySelectorAll('button[data-tab]').forEach(function (b) {
        b.setAttribute('aria-selected', b.getAttribute('data-tab') === key ? 'true' : 'false');
      });
      Object.keys(panels).forEach(function (k) {
        panels[k].hidden = !(key === 'all' || key === k);
      });
    }
    tabs.addEventListener('click', function (e) {
      var b = e.target.closest('button[data-tab]');
      if (b) select(b.getAttribute('data-tab'));
    });
    select('all');
  }

  /* ---- films from assets/js/films.js ---- */
  var filmWrap = doc.querySelector('[data-films]');
  if (filmWrap) {
    var list = (window.HF_FILMS || []).filter(function (f) {
      return f && typeof f.id === 'string' && /^[A-Za-z0-9_-]{11}$/.test(f.id);
    });
    if (!list.length) {
      filmWrap.innerHTML = '<p class="note" style="grid-column:1/-1"><b>' + T.films + '</b><br>' + T.filmsHint + '</p>';
    } else {
      filmWrap.innerHTML = list.map(function (f) {
        var thumb = 'https://i.ytimg.com/vi/' + f.id + '/hqdefault.jpg';
        var place = (LANG === 'pl' ? (f.titlePl || f.placePl) : (f.titleEn || f.placeEn)) || f.place || '';
        var label = (f.couple || place || 'Film').replace(/"/g, '');
        return '<figure class="film">' +
          '<button class="film-frame" type="button" data-yt="' + f.id + '" aria-label="' + label + '">' +
            '<img src="' + thumb + '" alt="" loading="lazy">' +
            '<span class="film-play" aria-hidden="true"></span>' +
          '</button>' +
          '<figcaption><span>' + (f.couple || '') + '</span><span>' + place +
            (f.len ? ' · ' + f.len : '') + '</span></figcaption>' +
        '</figure>';
      }).join('');
      filmWrap.addEventListener('click', function (e) {
        var b = e.target.closest('[data-yt]');
        if (!b) return;
        var id = b.getAttribute('data-yt');
        var f = doc.createElement('iframe');
        f.src = 'https://www.youtube-nocookie.com/embed/' + id + '?autoplay=1&rel=0';
        f.title = b.getAttribute('aria-label') || 'Film';
        f.allow = 'accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture';
        f.allowFullscreen = true;
        b.replaceWith(f);
      });
    }
  }

  /* ---- lightbox ---- */
  var gal = doc.querySelector('[data-gallery]');
  var lb = doc.getElementById('lightbox');
  if (gal && lb) {
    var allShots = [].slice.call(gal.querySelectorAll('button[data-full]'));
    var shots2 = allShots;
    var lbImg = lb.querySelector('img'), lbCap = lb.querySelector('.lb-cap');
    var cur = 0, opener = null;
    function open(n) {
      cur = (n + shots2.length) % shots2.length;
      var b = shots2[cur];
      lbImg.src = b.getAttribute('data-full');
      lbImg.alt = b.querySelector('img') ? b.querySelector('img').alt : '';
      lbCap.textContent = (b.getAttribute('data-cap') || '') + '  ·  ' + (cur + 1) + ' ' + T.of + ' ' + shots2.length;
      lb.hidden = false;
      doc.body.style.overflow = 'hidden';
      lb.querySelector('.lb-close').focus();
    }
    function close() {
      lb.hidden = true; doc.body.style.overflow = ''; lbImg.removeAttribute('src');
      if (opener) opener.focus();
    }
    gal.addEventListener('click', function (e) {
      var b = e.target.closest('button[data-full]');
      if (!b) return;
      // Page only through the wedding that was clicked, never a mix of couples.
      var album = b.getAttribute('data-album');
      shots2 = album
        ? allShots.filter(function (x) { return x.getAttribute('data-album') === album; })
        : allShots;
      opener = b; open(shots2.indexOf(b));
    });
    lb.querySelector('.lb-close').addEventListener('click', close);
    lb.querySelector('.lb-prev').addEventListener('click', function () { open(cur - 1); });
    lb.querySelector('.lb-next').addEventListener('click', function () { open(cur + 1); });
    lb.addEventListener('click', function (e) { if (e.target === lb) close(); });
    doc.addEventListener('keydown', function (e) {
      if (lb.hidden) return;
      if (e.key === 'Escape') close();
      if (e.key === 'ArrowLeft') open(cur - 1);
      if (e.key === 'ArrowRight') open(cur + 1);
    });
  }

  /* ---- reveal ---- */
  var targets = doc.querySelectorAll('.reveal');
  if (targets.length && 'IntersectionObserver' in window && !reduce) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('is-in'); io.unobserve(en.target); } });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    targets.forEach(function (t) { io.observe(t); });
  } else {
    targets.forEach(function (t) { t.classList.add('is-in'); });
  }

  /* ---- copy buttons ---- */
  doc.querySelectorAll('[data-copy]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var text = btn.getAttribute('data-copy');
      function done() { var o = btn.textContent; btn.textContent = T.copied; setTimeout(function () { btn.textContent = o; }, 1600); }
      function fallback() {
        var el = doc.getElementById(btn.getAttribute('data-copy-target') || '');
        if (!el) return;
        var r = doc.createRange(); r.selectNodeContents(el);
        var s = window.getSelection(); s.removeAllRanges(); s.addRange(r);
        btn.textContent = T.selectCopy;
      }
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(done, fallback);
      } else { fallback(); }
    });
  });

  /* ---- enquiry form (no backend; see README) ---- */
  var form = doc.getElementById('enquiry');
  if (form) {
    var status = doc.getElementById('enquiry-status');
    var mail = form.getAttribute('data-mailto') || '';
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var ok = true, firstBad = null;
      form.querySelectorAll('[data-required]').forEach(function (input) {
        var err = doc.getElementById(input.id + '-err');
        var v = input.value.trim();
        var bad = !v || (input.type === 'email' && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v));
        if (err) err.textContent = bad ? (input.type === 'email' ? T.reqMail : T.reqName) : '';
        input.setAttribute('aria-invalid', bad ? 'true' : 'false');
        if (bad) { ok = false; if (!firstBad) firstBad = input; }
      });
      if (!ok) {
        if (firstBad) firstBad.focus();
        status.hidden = false;
        status.innerHTML = '<strong>' + T.invalid + '</strong> ' + T.invalidBody;
        return;
      }
      function val(id) { var el = doc.getElementById(id); return el && el.value.trim() ? el.value.trim() : T.noDate; }
      var lines = [
        val('f-name'), val('f-email'), val('f-date'), val('f-place'), val('f-coverage'), val('f-notes')
      ];
      status.hidden = false;
      status.innerHTML = '<strong>' + T.sent + '</strong> ' + T.sentBody +
        '<code style="user-select:all">' + mail + '</code>.' +
        '<br><br><span class="field-note" style="text-transform:none;letter-spacing:0;font-size:.8rem;line-height:1.7">' +
        lines.map(function (l) { return String(l).replace(/[<>]/g, ''); }).join('<br>') + '</span>';
      status.focus();
    });
  }
})();
