/* ==========================================================================
   MBC Consultancy — site behaviour
   No dependencies. Everything here is progressive enhancement: if this file
   fails to parse or run, every page stays fully readable and navigable.

   Replaces the prototype's GSAP + ScrollTrigger motion system. The two bugs
   the prototype kept hitting are structurally impossible here:
     - Content stranded invisible: the hidden state lives in CSS behind `.js`
       and is cleared by a guaranteed failsafe, never set by script.
     - Broken page hand-off: the departure wipe always navigates, even if the
       transition never fires, and is reset on bfcache restore.
   ========================================================================== */
(function () {
  'use strict';

  var reduceMotion = false;
  try {
    reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  } catch (e) {}

  function ready(fn) {
    if (document.readyState !== 'loading') fn();
    else document.addEventListener('DOMContentLoaded', fn);
  }

  function all(sel, root) {
    return Array.prototype.slice.call((root || document).querySelectorAll(sel));
  }

  /* Reveal everything, unconditionally. The safety net for every motion bug. */
  function revealAll() {
    all('[data-reveal],[data-rise]').forEach(function (el) {
      el.classList.add('is-in');
    });
    all('.authitem').forEach(function (el) {
      el.classList.add('is-lit');
    });
  }

  /* ------------------------------------------------------------------------
     Header height -> --header-h-live, so anchor targets clear the sticky bar.
     The prototype hard-coded scroll-margin-top:140px, which was wrong on
     mobile where the header is a different height.
     ------------------------------------------------------------------------ */
  function trackHeaderHeight() {
    var header = document.querySelector('.header');
    if (!header) return;

    function apply() {
      var h = Math.round(header.getBoundingClientRect().height);
      document.documentElement.style.setProperty('--header-h-live', h + 16 + 'px');
    }

    apply();
    window.addEventListener('resize', apply);
    if (window.ResizeObserver) {
      try {
        new ResizeObserver(apply).observe(header);
      } catch (e) {}
    }
    // Re-measure once webfonts land, since the pills change size.
    if (document.fonts && document.fonts.ready) {
      document.fonts.ready.then(apply).catch(function () {});
    }
  }

  /* ------------------------------------------------------------------------
     Nav pill carousel
     The strip scrolls horizontally whenever it overflows — no breakpoint, it
     reacts to actual measured width. Chevrons are a pointer affordance only
     and stay out of the accessibility tree; keyboard users tab the links.
     ------------------------------------------------------------------------ */
  function initNav() {
    var nav = document.querySelector('.nav');
    var scroller = document.querySelector('.nav__scroller');
    if (!nav || !scroller) return;

    var prev = nav.querySelector('.nav__arrow--prev');
    var next = nav.querySelector('.nav__arrow--next');

    function update() {
      var overflow = scroller.scrollWidth - scroller.clientWidth;
      var scrollable = overflow > 2;
      nav.classList.toggle('nav--scrollable', scrollable);

      var x = scroller.scrollLeft;
      nav.classList.toggle('nav--at-start', x <= 2);
      nav.classList.toggle('nav--at-end', x >= overflow - 2);

      if (prev) prev.disabled = !scrollable || x <= 2;
      if (next) next.disabled = !scrollable || x >= overflow - 2;
    }

    function nudge(dir) {
      var step = Math.max(140, Math.round(scroller.clientWidth * 0.7));
      scroller.scrollBy({ left: dir * step, behavior: reduceMotion ? 'auto' : 'smooth' });
    }

    if (prev) prev.addEventListener('click', function () { nudge(-1); });
    if (next) next.addEventListener('click', function () { nudge(1); });

    // Bring the current page's pill fully into view, so you can see where you
    // are without swiping. Scrolls the minimum distance that clears it —
    // anchoring its left edge would leave a wide pill clipped on the right,
    // which is exactly what happens to "Book a consultation".
    //
    // Must run again after the webfont swaps: the pills are measurably
    // narrower in the fallback face, so a position computed at DOMContentLoaded
    // under-scrolls and leaves the current pill hanging off the edge.
    var current = scroller.querySelector('[aria-current="page"]');

    function showCurrent() {
      if (!current) return;
      var pad = 16;
      var left = current.offsetLeft;
      var right = left + current.offsetWidth;
      var maxScroll = scroller.scrollWidth - scroller.clientWidth;
      if (maxScroll <= 0) return;
      if (right > scroller.clientWidth - pad) {
        scroller.scrollLeft = Math.min(right - scroller.clientWidth + pad, maxScroll);
      } else if (left < pad) {
        scroller.scrollLeft = 0;
      }
    }

    function sync() {
      showCurrent();
      update();
    }

    scroller.addEventListener('scroll', update, { passive: true });
    window.addEventListener('resize', sync);
    if (document.fonts && document.fonts.ready) {
      document.fonts.ready.then(sync).catch(function () {});
    }

    sync();
  }

  /* ------------------------------------------------------------------------
     Scroll reveal + hero rise
     ------------------------------------------------------------------------ */
  function initReveal() {
    if (reduceMotion || !('IntersectionObserver' in window)) {
      revealAll();
      return;
    }

    // Hero lines rise immediately on load, staggered.
    var rise = all('[data-rise]');
    rise.forEach(function (el, i) {
      el.style.transitionDelay = i * 90 + 'ms';
    });
    requestAnimationFrame(function () {
      requestAnimationFrame(function () {
        rise.forEach(function (el) {
          el.classList.add('is-in');
        });
      });
    });

    var targets = all('[data-reveal]');
    if (!targets.length) return;

    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          entry.target.classList.add('is-in');
          io.unobserve(entry.target);
        });
      },
      { rootMargin: '0px 0px -6% 0px', threshold: 0.01 }
    );

    targets.forEach(function (el) {
      // Anything already on screen at load reveals without waiting.
      var top = el.getBoundingClientRect().top;
      if (top < window.innerHeight * 0.94) {
        el.classList.add('is-in');
      } else {
        io.observe(el);
      }
    });
  }

  /* ------------------------------------------------------------------------
     Counters — roll a number up once it enters view.
     The element's markup already contains the final value, so with no JS or a
     failed observer the correct figure is simply there.
     ------------------------------------------------------------------------ */
  function initCounters() {
    var els = all('[data-count]');
    if (!els.length || reduceMotion || !('IntersectionObserver' in window)) return;

    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          run(entry.target);
          io.unobserve(entry.target);
        });
      },
      { threshold: 0.4 }
    );

    els.forEach(function (el) {
      io.observe(el);
    });

    function run(el) {
      var target = parseFloat(el.getAttribute('data-count'));
      if (isNaN(target)) return;
      var prefix = el.getAttribute('data-prefix') || '';
      var suffix = el.getAttribute('data-suffix') || '';
      var final = prefix + target + suffix;
      var start = 0;
      var dur = 1100;
      var t0 = null;

      function frame(ts) {
        if (t0 === null) t0 = ts;
        var p = Math.min(1, (ts - t0) / dur);
        var eased = 1 - Math.pow(1 - p, 3);
        el.textContent = prefix + Math.round(start + (target - start) * eased) + suffix;
        if (p < 1) requestAnimationFrame(frame);
        else el.textContent = final;
      }
      requestAnimationFrame(frame);
    }
  }

  /* ------------------------------------------------------------------------
     Authorities scene — a sticky pinned section whose scroll progress lights
     each authority in turn and drives the cyan-to-rose progress bar.

     Built on position:sticky rather than a scroll library: the browser owns
     the pinning, so it cannot desync, and it degrades to a plain section.
     ------------------------------------------------------------------------ */
  function initAuthScene() {
    var stage = document.querySelector('.authstage');
    if (!stage) return;

    var sticky = stage.querySelector('.authstage__sticky');
    var items = all('.authitem', stage);
    var fill = stage.querySelector('.authbar__fill');
    if (!sticky || !items.length) return;

    var active = false;
    var raf = null;

    function enable() {
      if (active) return;
      active = true;
      document.documentElement.classList.add('js-scene');
      sticky.style.position = 'sticky';
      sticky.style.top = 'var(--header-h-live, var(--header-h))';
      // Runway: one viewport to read it, plus a beat per authority.
      stage.style.height = 'calc(100vh + ' + items.length * 200 + 'px)';
      onScroll();
    }

    function disable() {
      if (!active) return;
      active = false;
      document.documentElement.classList.remove('js-scene');
      sticky.style.position = '';
      sticky.style.top = '';
      stage.style.height = '';
      items.forEach(function (el) {
        el.classList.add('is-lit');
      });
      if (fill) fill.style.setProperty('--p', '1');
    }

    function onScroll() {
      if (!active) return;
      if (raf) return;
      raf = requestAnimationFrame(function () {
        raf = null;
        var rect = stage.getBoundingClientRect();
        var travel = rect.height - window.innerHeight;
        if (travel <= 0) return;
        var p = Math.min(1, Math.max(0, -rect.top / travel));

        // All lit by 85% of the runway, leaving a beat before release.
        var span = 0.85;
        items.forEach(function (el, i) {
          var at = (i / items.length) * span;
          el.classList.toggle('is-lit', p >= at);
        });
        if (fill) {
          fill.style.setProperty('--p', String(Math.min(1, p / span)));
        }
      });
    }

    function decide() {
      // Desktop only, matching the prototype, and never under reduced motion.
      if (!reduceMotion && window.innerWidth > 1040) enable();
      else disable();
    }

    decide();
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', decide);
  }

  /* ------------------------------------------------------------------------
     Page transition — teal wipe covers, then navigates. The arrival curtain
     on the next page is pure CSS, so the two halves read as one move.
     ------------------------------------------------------------------------ */
  function initTransition() {
    var wipe = document.querySelector('.wipe');
    if (!wipe || reduceMotion) return;

    // A restored bfcache page would otherwise come back still covered.
    window.addEventListener('pageshow', function () {
      wipe.classList.remove('is-covering');
    });

    document.addEventListener('click', function (e) {
      if (e.defaultPrevented) return;
      if (e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;

      var a = e.target.closest ? e.target.closest('a[href]') : null;
      if (!a) return;
      if (a.target && a.target !== '_self') return;
      if (a.hasAttribute('download')) return;

      var href = a.getAttribute('href') || '';
      // Same-page anchors, mail, phone and WhatsApp all navigate normally.
      if (!href || href.charAt(0) === '#') return;
      if (/^(mailto:|tel:|sms:|javascript:)/i.test(href)) return;

      var url;
      try {
        url = new URL(a.href, location.href);
      } catch (err) {
        return;
      }
      if (url.origin !== location.origin) return;
      // A hash link into the page we are already on is a scroll, not a nav.
      if (url.pathname === location.pathname && url.hash) return;

      e.preventDefault();
      var done = false;
      function go() {
        if (done) return;
        done = true;
        location.href = a.href;
      }
      // Navigate on transition end, but never depend on it firing.
      wipe.addEventListener('transitionend', go, { once: true });
      setTimeout(go, 520);
      wipe.classList.add('is-covering');
    });
  }

  /* ------------------------------------------------------------------------
     Contact form
     Posts to the form's own action so it works without JS. With JS it submits
     in place, reports status in a live region, and if the endpoint is
     unreachable it hands off to WhatsApp with the enquiry pre-filled rather
     than losing what the visitor typed.
     ------------------------------------------------------------------------ */
  function initForm() {
    var form = document.querySelector('form[data-enhance]');
    if (!form) return;

    var status = form.querySelector('.form__status');
    var submit = form.querySelector('[type="submit"]');
    var wa = form.getAttribute('data-whatsapp') || '';

    function setStatus(kind, html) {
      if (!status) return;
      status.className = 'form__status form__status--' + kind;
      status.innerHTML = html;
    }

    // Carry context in from the page that sent them here: the package cards
    // link with ?enquiry=…, and a no-JavaScript post that failed comes back
    // with ?error=1 so the visitor still sees what happened.
    var params = null;
    try {
      params = new URLSearchParams(location.search);
    } catch (e) {}

    if (params) {
      var from = params.get('enquiry');
      var hidden = form.querySelector('input[name="enquiry"]');
      if (from && hidden) hidden.value = from.slice(0, 80);
      if (params.get('error')) {
        setStatus(
          'err',
          '<strong>That did not send.</strong><br>Please try again, or reach us on ' +
            '<a href="https://wa.me/263774121012" target="_blank" rel="noopener">WhatsApp</a> ' +
            'or <a href="mailto:mmazha800@gmail.com">mmazha800@gmail.com</a>.'
        );
      }
    }

    function fieldError(input, msg) {
      var wrapper = input.closest('.field') || input.parentNode;
      var slot = wrapper.querySelector('.field__error');
      if (slot) slot.textContent = msg || '';
      if (msg) input.setAttribute('aria-invalid', 'true');
      else input.removeAttribute('aria-invalid');
    }

    function validate() {
      var firstBad = null;
      all('[required]', form).forEach(function (input) {
        var val = (input.value || '').trim();
        var msg = '';
        if (!val) {
          msg = 'This one is needed.';
        } else if (input.type === 'email' && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(val)) {
          msg = 'Check the email address.';
        }
        fieldError(input, msg);
        if (msg && !firstBad) firstBad = input;
      });
      return firstBad;
    }

    // Clear a field's error as soon as the visitor starts fixing it.
    all('[required]', form).forEach(function (input) {
      input.addEventListener('input', function () {
        if (input.getAttribute('aria-invalid')) fieldError(input, '');
      });
    });

    function whatsappHref() {
      if (!wa) return '';
      var d = new FormData(form);
      var lines = [];
      var name = d.get('name');
      var company = d.get('company');
      var email = d.get('email');
      var needs = d.getAll('services');
      var message = d.get('message');
      if (name) lines.push('Name: ' + name);
      if (company) lines.push('Company: ' + company);
      if (email) lines.push('Email: ' + email);
      if (needs.length) lines.push('Needs: ' + needs.join(', '));
      if (message) lines.push('', message);
      return 'https://wa.me/' + wa + '?text=' + encodeURIComponent(lines.join('\n'));
    }

    form.addEventListener('submit', function (e) {
      // Silently accept and drop anything that filled the honeypot.
      var hp = form.querySelector('input[name="_gotcha"]');
      if (hp && hp.value) {
        e.preventDefault();
        setStatus('ok', 'Thank you — your enquiry is with us.');
        return;
      }

      var bad = validate();
      if (bad) {
        e.preventDefault();
        setStatus('err', 'Please check the highlighted fields.');
        bad.focus();
        return;
      }

      // No fetch support: let the browser do the plain POST.
      if (!window.fetch) return;

      e.preventDefault();
      if (submit) {
        submit.disabled = true;
        submit.dataset.label = submit.textContent;
        submit.textContent = 'Sending…';
      }
      setStatus('ok', 'Sending your enquiry…');

      fetch(form.action, {
        method: 'POST',
        body: new FormData(form),
        headers: { Accept: 'application/json' }
      })
        .then(function (res) {
          if (!res.ok) throw new Error('HTTP ' + res.status);
          form.reset();
          setStatus(
            'ok',
            '<strong>Thank you — your enquiry is with us.</strong><br>' +
              'We aim to reply within one working day. If it is urgent, ' +
              'WhatsApp is quickest.'
          );
          if (submit) submit.remove();
        })
        .catch(function () {
          var href = whatsappHref();
          setStatus(
            'err',
            '<strong>That did not send.</strong><br>Nothing you typed is lost. ' +
              (href
                ? 'You can <a href="' +
                  href +
                  '" target="_blank" rel="noopener"><strong>send it on WhatsApp instead</strong></a>, or email '
                : 'Please email ') +
              '<a href="mailto:mmazha800@gmail.com">mmazha800@gmail.com</a>.'
          );
          if (submit) {
            submit.disabled = false;
            submit.textContent = submit.dataset.label || 'Send enquiry';
          }
        });
    });
  }

  /* ------------------------------------------------------------------------
     Footer year — so the copyright never goes stale.
     ------------------------------------------------------------------------ */
  function initYear() {
    all('[data-year]').forEach(function (el) {
      el.textContent = String(new Date().getFullYear());
    });
  }

  /* ------------------------------------------------------------------------
     Boot. Each module is isolated so one failure cannot take down the rest,
     and a hard failsafe guarantees nothing is left hidden.
     ------------------------------------------------------------------------ */
  ready(function () {
    [
      trackHeaderHeight,
      initNav,
      initReveal,
      initCounters,
      initAuthScene,
      initTransition,
      initForm,
      initYear
    ].forEach(function (fn) {
      try {
        fn();
      } catch (e) {
        if (window.console) console.error('[mbc] ' + fn.name + ' failed', e);
      }
    });

    // Whatever happened above, no content stays invisible.
    setTimeout(function () {
      all('[data-reveal],[data-rise]').forEach(function (el) {
        if (!el.classList.contains('is-in')) el.classList.add('is-in');
      });
    }, 2500);
  });

  window.addEventListener('error', function () {
    try {
      revealAll();
    } catch (e) {}
  });
})();
