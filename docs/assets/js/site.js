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
      noDate: 'nie podano', of: 'z', play: 'Obejrzyj film',
      sending: 'Wysyłanie…',
      sentOk: 'Dziękuję — zapytanie zostało wysłane.',
      sentOkSub: 'Odpowiadam w ciągu dwóch dni, zwykle szybciej.',
      failed: 'Nie udało się wysłać wiadomości.',
      failedSub: 'Coś poszło nie tak po drodze. Proszę napisać bezpośrednio na adres'
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
      noDate: 'not given', of: 'of', play: 'Watch the film',
      sending: 'Sending…',
      sentOk: 'Thank you — your enquiry is on its way.',
      sentOkSub: 'I reply within two days, usually sooner.',
      failed: 'The message could not be sent.',
      failedSub: 'Something went wrong on the way. Please email me directly at'
    }
  }[LANG];

  /* ---- Meta Pixel, behind a consent notice -------------------------------
     Nothing from Facebook is requested until the visitor accepts. The choice is
     remembered per browser; clearing site data brings the notice back.          */
  var PIXEL_ID = window.HF_PIXEL_ID || '';
  var CONSENT_KEY = 'hf_consent';

  function readConsent() {
    try { return localStorage.getItem(CONSENT_KEY); } catch (e) { return null; }
  }
  function writeConsent(v) {
    try { localStorage.setItem(CONSENT_KEY, v); } catch (e) {}
  }
  function loadPixel() {
    if (!PIXEL_ID || window.fbq) return;
    /* Meta's standard base code */
    !function (f, b, e, v, n, t, s) {
      if (f.fbq) return; n = f.fbq = function () {
        n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments);
      };
      if (!f._fbq) f._fbq = n; n.push = n; n.loaded = !0; n.version = '2.0'; n.queue = [];
      t = b.createElement(e); t.async = !0; t.src = v;
      s = b.getElementsByTagName(e)[0]; s.parentNode.insertBefore(t, s);
    }(window, doc, 'script', 'https://connect.facebook.net/en_US/fbevents.js');
    window.fbq('init', PIXEL_ID);
    trackPage();
  }

  /* What gets reported to Meta once consent is given.

     PageView alone cannot tell you which page someone looked at — Events
     Manager has no per-URL report. So each page also sends a named event, and
     those appear in Events Manager by name with no extra setup:

       ViewPortfolio   the Work page
       ViewAlbum       one wedding's album (carries which one)
       ViewOffer       the prices
       ViewAbout       About me
       ViewContact     the contact page, before anything is typed
       PlayFilm        a film was actually opened and started
       Lead            an enquiry was completed and sent

     Together those read as a funnel: looked -> watched -> checked the price ->
     got in touch.                                                            */
  function trackPage() {
    if (!window.fbq) return;
    var page = (doc.body.getAttribute('data-page') || '').toLowerCase();
    var lang = doc.documentElement.lang === 'pl' ? 'pl' : 'en';
    window.fbq('track', 'PageView');

    if (page.indexOf('album-') === 0) {
      window.fbq('trackCustom', 'ViewAlbum', { album: page.slice(6), lang: lang });
      return;
    }
    var named = {
      work: 'ViewPortfolio',
      offer: 'ViewOffer',
      about: 'ViewAbout',
      contact: 'ViewContact'
    }[page];
    if (named) window.fbq('trackCustom', named, { lang: lang });
  }

  window.hfTrackFilm = function (couple) {
    if (window.fbq) {
      try { window.fbq('trackCustom', 'PlayFilm', { film: couple || '' }); } catch (e) {}
    }
  };

  var consentBar = doc.getElementById('consent');
  if (PIXEL_ID) {
    var choice = readConsent();
    if (choice === 'yes') {
      loadPixel();
    } else if (choice !== 'no' && consentBar) {
      consentBar.hidden = false;
      setTimeout(function () { consentBar.classList.add('is-shown'); }, 20);
    }
    if (consentBar) {
      consentBar.addEventListener('click', function (e) {
        var b = e.target.closest('[data-consent]');
        if (!b) return;
        var yes = b.getAttribute('data-consent') === 'yes';
        writeConsent(yes ? 'yes' : 'no');
        consentBar.classList.remove('is-shown');
        setTimeout(function () { consentBar.hidden = true; }, 350);
        if (yes) loadPixel();
      });
    }
  }

  /* Withdrawing consent has to be as easy as giving it (privacy page button). */
  var consentReset = doc.getElementById('consent-reset');
  if (consentReset) {
    consentReset.addEventListener('click', function () {
      try { localStorage.removeItem(CONSENT_KEY); } catch (e) {}
      var done = doc.getElementById('consent-reset-done');
      if (done) done.hidden = false;
      if (consentBar) {
        consentBar.hidden = false;
        setTimeout(function () { consentBar.classList.add('is-shown'); }, 20);
      } else {
        setTimeout(function () { location.reload(); }, 900);
      }
    });
  }

  /* Reports a completed enquiry, so ad spend can be measured against real
     enquiries and not only visits. Silent when the pixel was never loaded. */
  window.hfTrackLead = function () {
    if (window.fbq) { try { window.fbq('track', 'Lead'); } catch (e) {} }
  };

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

    // Advance on its own every 5s, but never while someone is reading it:
    // hovering, focusing or pressing an arrow all hold it where it is.
    var qTimer = null;
    function qStart() {
      if (reduce || items.length < 2) return;
      qStop();
      qTimer = setInterval(function () { show(q + 1); }, 5000);
    }
    function qStop() { if (qTimer) { clearInterval(qTimer); qTimer = null; } }
    function qNudge() { qStop(); qStart(); }

    if (p) p.addEventListener('click', function () { show(q - 1); qNudge(); });
    if (nx) nx.addEventListener('click', function () { show(q + 1); qNudge(); });
    quotes.addEventListener('mouseenter', qStop);
    quotes.addEventListener('mouseleave', qStart);
    quotes.addEventListener('focusin', qStop);
    quotes.addEventListener('focusout', qStart);
    doc.addEventListener('visibilitychange', function () { doc.hidden ? qStop() : qStart(); });
    qStart();
  }

  /* ---- strips: drag to scroll, with arrows as the obvious alternative ---- */
  doc.querySelectorAll('[data-strip]').forEach(function (strip) {
    var down = false, startX = 0, startLeft = 0, moved = 0, pid = null;

    // The browser's native image/link dragging would otherwise swallow the gesture.
    strip.addEventListener('dragstart', function (e) { e.preventDefault(); });

    strip.addEventListener('pointerdown', function (e) {
      if (e.pointerType === 'touch' || e.button !== 0) return;   // touch scrolls natively
      down = true; moved = 0; pid = e.pointerId;
      startX = e.clientX; startLeft = strip.scrollLeft;
      e.preventDefault();
    });
    strip.addEventListener('pointermove', function (e) {
      if (!down || e.pointerId !== pid) return;
      var dx = e.clientX - startX;
      if (!moved && Math.abs(dx) < 4) return;                    // let small wobbles be clicks
      if (!moved) {
        strip.classList.add('is-drag');
        try { strip.setPointerCapture(pid); } catch (err) {}
      }
      moved = Math.abs(dx);
      strip.scrollLeft = startLeft - dx;
    });
    function release() {
      if (!down) return;
      down = false;
      if (pid !== null) { try { strip.releasePointerCapture(pid); } catch (err) {} }
      pid = null;
      strip.classList.remove('is-drag');
    }
    strip.addEventListener('pointerup', release);
    strip.addEventListener('pointercancel', release);
    window.addEventListener('blur', release);
    // a drag that ends on a card must not also follow its link
    strip.addEventListener('click', function (e) { if (moved > 4) { e.preventDefault(); e.stopPropagation(); } }, true);

    var nav = doc.querySelector('[data-strip-nav]');
    var prev = nav && nav.querySelector('[data-strip-prev]');
    var next = nav && nav.querySelector('[data-strip-next]');

    function step() {
      var card = strip.querySelector('figure');
      return card ? card.getBoundingClientRect().width + 16 : strip.clientWidth * 0.8;
    }
    function maxScroll() { return strip.scrollWidth - strip.clientWidth - 2; }
    function sync() {
      if (prev) prev.disabled = strip.scrollLeft <= 2;
      if (next) next.disabled = strip.scrollLeft >= maxScroll();
    }
    var navTimer = null;
    function scrollToX(x) {
      // Scroll snapping cancels an animated scroll and pulls the strip back to
      // where it started, so turn it off for the length of the animation.
      strip.classList.add('is-nav');
      strip.scrollTo({ left: x, behavior: reduce ? 'auto' : 'smooth' });
      clearTimeout(navTimer);
      navTimer = setTimeout(function () { strip.classList.remove('is-nav'); }, 700);
    }
    function go(dir) { scrollToX(strip.scrollLeft + dir * step()); }

    if (prev) prev.addEventListener('click', function () { go(-1); nudge(); });
    if (next) next.addEventListener('click', function () { go(1); nudge(); });
    strip.addEventListener('scroll', sync, { passive: true });
    window.addEventListener('resize', sync, { passive: true });
    sync();

    // Drift one card to the right every 5s, returning to the start at the end.
    // Holds still while the pointer is over it, while dragging, while any card
    // has keyboard focus, and while the tab is in the background.
    var autoTimer = null, held = false;
    function tick() {
      if (held || strip.scrollWidth <= strip.clientWidth) return;
      scrollToX(strip.scrollLeft >= maxScroll() ? 0 : strip.scrollLeft + step());
    }
    function start() {
      if (reduce) return;
      stop();
      autoTimer = setInterval(tick, 5000);
    }
    function stop() { if (autoTimer) { clearInterval(autoTimer); autoTimer = null; } }
    function nudge() { stop(); start(); }
    function hold(v) { held = v; }

    strip.addEventListener('mouseenter', function () { hold(true); });
    strip.addEventListener('mouseleave', function () { hold(false); });
    strip.addEventListener('focusin', function () { hold(true); });
    strip.addEventListener('focusout', function () { hold(false); });
    strip.addEventListener('pointerdown', function () { hold(true); });
    window.addEventListener('pointerup', function () { hold(false); nudge(); });
    if (nav) {
      nav.addEventListener('mouseenter', function () { hold(true); });
      nav.addEventListener('mouseleave', function () { hold(false); });
    }
    doc.addEventListener('visibilitychange', function () { doc.hidden ? stop() : start(); });
    start();
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

  /* ---- films: alternating rows, played in a window over the page ---- */
  var filmWrap = doc.querySelector('[data-films]');
  var filmModal = doc.getElementById('film-modal');
  if (filmWrap) {
    var films = (window.HF_FILMS || []).filter(function (f) { return f && f.id && f.type; });
    if (!films.length) {
      filmWrap.innerHTML = '<p class="note"><b>' + T.films + '</b><br>' + T.filmsHint + '</p>';
    } else {
      filmWrap.innerHTML = films.map(function (f, i) {
        var title = (LANG === 'pl' ? f.titlePl : f.titleEn) || '';
        var text = (LANG === 'pl' ? f.textPl : f.textEn) || '';
        var poster = 'assets/img/film/' + f.poster + '.jpg';
        if (doc.documentElement.lang === 'pl') poster = '../' + poster;
        return '<article class="film-row" data-flip="' + (i % 2 ? 'true' : 'false') + '">' +
          '<button class="film-frame" type="button" data-film="' + i + '" aria-label="' +
              T.play + ' — ' + (f.couple || title).replace(/"/g, '') + '">' +
            '<img src="' + poster + '" alt="" loading="lazy" decoding="async">' +
            '<span class="film-play" aria-hidden="true"></span>' +
          '</button>' +
          '<div class="film-words">' +
            '<p class="eyebrow">' + title + '</p>' +
            '<h3 class="h-md">' + (f.couple || '') + '</h3>' +
            '<p class="film-text">' + text + '</p>' +
            '<button class="btn film-cue" type="button" data-film="' + i + '">' + T.play + '</button>' +
          '</div>' +
        '</article>';
      }).join('');

      var lastFilmFocus = null;
      function srcFor(f) {
        return f.type === 'drive'
          ? 'https://drive.google.com/file/d/' + f.id + '/preview'
          : 'https://www.youtube-nocookie.com/embed/' + f.id + '?autoplay=1&rel=0';
      }
      function openFilm(i) {
        var f = films[i];
        if (!f || !filmModal) return;
        lastFilmFocus = doc.activeElement;
        if (window.hfTrackFilm) window.hfTrackFilm(f.couple);
        var holder = filmModal.querySelector('.film-modal-frame');
        var cap = filmModal.querySelector('.film-modal-cap');
        holder.innerHTML = '';
        var fr = doc.createElement('iframe');
        fr.src = srcFor(f);
        fr.title = f.couple || 'Film';
        fr.setAttribute('allow', 'accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture');
        fr.setAttribute('allowfullscreen', '');
        holder.appendChild(fr);
        cap.textContent = (f.couple || '') + ((LANG === 'pl' ? f.titlePl : f.titleEn) ? '  ·  ' + (LANG === 'pl' ? f.titlePl : f.titleEn) : '');
        filmModal.hidden = false;
        doc.body.style.overflow = 'hidden';
        filmModal.querySelector('.film-modal-close').focus();
      }
      function closeFilm() {
        if (!filmModal || filmModal.hidden) return;
        filmModal.querySelector('.film-modal-frame').innerHTML = '';  // stops playback
        filmModal.hidden = true;
        doc.body.style.overflow = '';
        if (lastFilmFocus) lastFilmFocus.focus();
      }
      filmWrap.addEventListener('click', function (e) {
        var b = e.target.closest('[data-film]');
        if (b) openFilm(parseInt(b.getAttribute('data-film'), 10));
      });
      if (filmModal) {
        filmModal.querySelector('.film-modal-close').addEventListener('click', closeFilm);
        filmModal.addEventListener('click', function (e) { if (e.target === filmModal) closeFilm(); });
        doc.addEventListener('keydown', function (e) {
          if (e.key === 'Escape' && !filmModal.hidden) closeFilm();
        });
      }
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

  /* ---- back to top: appears once past halfway ---- */
  var toTop = doc.getElementById('to-top');
  if (toTop) {
    var ticking = false;
    function checkTop() {
      ticking = false;
      var doch = doc.documentElement;
      var scrollable = (doc.body.scrollHeight || 0) - window.innerHeight;
      var y = window.scrollY || doch.scrollTop;
      // Nothing to go back to on a page that barely scrolls.
      // "distance" is for very long pages, where halfway is a long way down:
      // the button turns up after about a screen and a half of scrolling.
      var past = scrollable > 400 && (toTop.getAttribute('data-mode') === 'distance'
        ? y > window.innerHeight * 1.5
        : y > scrollable * 0.5);
      toTop.classList.toggle('is-shown', past);
    }
    window.addEventListener('scroll', function () {
      if (!ticking) { ticking = true; window.requestAnimationFrame(checkTop); }
    }, { passive: true });
    window.addEventListener('resize', checkTop, { passive: true });
    toTop.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' });
      var skip = doc.querySelector('.skip');
      if (skip) skip.focus({ preventScroll: true });
    });
    checkTop();
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

  /* ---- enquiry form: posted to Web3Forms, which emails it on ---- */
  var form = doc.getElementById('enquiry');
  if (form) {
    var status = doc.getElementById('enquiry-status');
    var mail = form.getAttribute('data-mailto') || '';

    function say(html) {
      status.hidden = false;
      status.innerHTML = html;
    }
    function esc(v) {
      return String(v == null ? '' : v).replace(/[<>&]/g, function (ch) {
        return { '<': '&lt;', '>': '&gt;', '&': '&amp;' }[ch];
      });
    }

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
        say('<strong>' + T.invalid + '</strong> ' + T.invalidBody);
        return;
      }

      var btn = form.querySelector('button[type="submit"]');
      var btnText = btn ? btn.textContent : '';
      if (btn) { btn.disabled = true; btn.textContent = T.sending; }
      say('<strong>' + T.sending + '</strong>');

      var data = Object.fromEntries(new FormData(form).entries());
      fetch('https://api.web3forms.com/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify(data)
      })
        .then(function (r) { return r.json().catch(function () { return { success: r.ok }; }); })
        .then(function (res) {
          if (!res || !res.success) throw new Error((res && res.message) || 'failed');
          form.reset();
          if (window.hfTrackLead) window.hfTrackLead();
          say('<strong>' + T.sentOk + '</strong><br>' + T.sentOkSub);
        })
        .catch(function () {
          // Nothing is lost: show what they wrote so it can be copied into an email.
          function val(id) { var el = doc.getElementById(id); return el && el.value.trim() ? el.value.trim() : T.noDate; }
          var lines = [val('f-name'), val('f-email'), val('f-date'), val('f-place'),
                       val('f-coverage'), val('f-notes')];
          say('<strong>' + T.failed + '</strong> ' + T.failedSub +
              ' <code style="user-select:all">' + esc(mail) + '</code>.' +
              '<br><br><span class="field-note" style="text-transform:none;letter-spacing:0;font-size:.8rem;line-height:1.7">' +
              lines.map(esc).join('<br>') + '</span>');
        })
        .then(function () {
          if (btn) { btn.disabled = false; btn.textContent = btnText; }
          status.focus();
        });
    });
  }
})();
