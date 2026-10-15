/* Pro Style Barbershop — анімації та інтерактив */
(() => {
  const root = document.documentElement;
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const finePointer = matchMedia('(pointer: fine)').matches;
  const isDesktop = () => innerWidth > 900;

  /* ---------- Відкрито / зачинено (час Мадейри) ---------- */
  function madeiraNow() {
    const parts = new Intl.DateTimeFormat('en-GB', { timeZone: 'Atlantic/Madeira', weekday: 'short', hour: '2-digit', minute: '2-digit', hour12: false })
      .formatToParts(new Date()).reduce((o, p) => (o[p.type] = p.value, o), {});
    const day = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].indexOf(parts.weekday);
    return { day, mins: (+parts.hour % 24) * 60 + +parts.minute };
  }
  function updateStatus() {
    const { day, mins } = madeiraNow();
    const open = day >= 1 && day <= 6 && mins >= 600 && mins < 1140;
    $$('[data-status]').forEach(el => {
      el.classList.toggle('is-closed', !open);
      $$('[data-open]', el).forEach(n => { n.textContent = open ? n.dataset.open : n.dataset.closed; });
    });
    $$('.hours li').forEach(li => {
      const today = +li.dataset.day === day;
      li.classList.toggle('is-today', today);
      const label = li.parentElement.dataset.todayLabel;
      if (today) li.firstElementChild.dataset.today = label; else delete li.firstElementChild.dataset.today;
    });
  }
  updateStatus();
  setInterval(updateStatus, 60000);

  /* ---------- Мобільне меню ---------- */
  const burger = $('.burger'), mnav = $('#mnav');
  const setMenu = open => {
    burger.setAttribute('aria-expanded', open);
    if (open) { mnav.hidden = false; requestAnimationFrame(() => mnav.classList.add('is-open')); }
    else { mnav.classList.remove('is-open'); setTimeout(() => { if (!mnav.classList.contains('is-open')) mnav.hidden = true; }, 800); }
    document.body.style.overflow = open ? 'hidden' : '';
    window.__lenis && (open ? window.__lenis.stop() : window.__lenis.start());
  };
  burger.addEventListener('click', () => setMenu(burger.getAttribute('aria-expanded') !== 'true'));
  $$('a', mnav).forEach(a => a.addEventListener('click', () => setMenu(false)));
  addEventListener('keydown', e => { if (e.key === 'Escape' && burger.getAttribute('aria-expanded') === 'true') setMenu(false); });

  /* ---------- Вкладки послуг ---------- */
  const tabs = $$('.svc-tab'), ind = $('.svc-ind');
  const moveInd = tab => {
    if (!tab || !ind) return;
    ind.style.width = tab.offsetWidth + 'px';
    ind.style.transform = `translate(${tab.offsetLeft - 6}px, ${tab.offsetTop - 6}px)`;
  };
  tabs.forEach((tab, i) => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.setAttribute('aria-selected', t === tab));
      $$('.svc-panel').forEach(p => { p.hidden = p.id !== tab.getAttribute('aria-controls'); });
      moveInd(tab);
      tab.scrollIntoView({ block: 'nearest', inline: 'center', behavior: 'smooth' });
      const panel = $('#' + tab.getAttribute('aria-controls'));
      if (window.gsap && !reduce) gsap.fromTo($$('.svc-row', panel), { y: 24, opacity: 0 }, { y: 0, opacity: 1, duration: .7, stagger: .06, ease: 'expo.out' });
      window.ScrollTrigger && ScrollTrigger.refresh();
    });
    tab.addEventListener('keydown', e => {
      const d = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
      if (d) { const n = tabs[(i + d + tabs.length) % tabs.length]; n.focus(); n.click(); }
    });
  });
  const syncInd = () => moveInd($('.svc-tab[aria-selected="true"]'));
  addEventListener('resize', syncInd);
  document.fonts && document.fonts.ready.then(syncInd);
  syncInd();

  /* ---------- FAQ: плавне відкриття ---------- */
  $$('.faq-item').forEach(d => {
    const sum = $('summary', d), body = $('.faq-a', d);
    sum.addEventListener('click', e => {
      if (!window.gsap || reduce) return;
      e.preventDefault();
      if (d.open) {
        gsap.to(body, { height: 0, duration: .5, ease: 'expo.out', onComplete: () => { d.open = false; body.style.height = ''; window.ScrollTrigger && ScrollTrigger.refresh(); } });
      } else {
        d.open = true;
        gsap.fromTo(body, { height: 0 }, { height: body.scrollHeight, duration: .7, ease: 'expo.out', onComplete: () => { body.style.height = ''; window.ScrollTrigger && ScrollTrigger.refresh(); } });
      }
    });
  });

  /* ---------- Якщо GSAP не завантажився — показуємо все без анімацій ---------- */
  function fallback() {
    root.classList.remove('js');
    const l = $('.loader'); l && l.remove();
  }

  function init() {
    if (!window.gsap || !window.ScrollTrigger) return fallback();
    gsap.registerPlugin(ScrollTrigger);

    /* ---- Smooth scroll ---- */
    let lenis = null;
    if (!reduce && window.Lenis) {
      lenis = new Lenis({ duration: 1.15, easing: t => Math.min(1, 1.001 - Math.pow(2, -10 * t)), smoothTouch: false });
      window.__lenis = lenis;
      lenis.on('scroll', ScrollTrigger.update);
      gsap.ticker.add(t => lenis.raf(t * 1000));
      gsap.ticker.lagSmoothing(0);
    }
    $$('a[href^="#"]').forEach(a => a.addEventListener('click', e => {
      const id = a.getAttribute('href');
      const target = id.length > 1 ? $(id) : null;
      if (!target) return;
      e.preventDefault();
      lenis ? lenis.scrollTo(target, { offset: id === '#main' ? 0 : -70, duration: 1.4 }) : target.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth' });
    }));

    /* ---- Розбиття заголовків на слова ---- */
    $$('.split').forEach(el => {
      const walk = node => {
        [...node.childNodes].forEach(n => {
          if (n.nodeType === 3) {
            const frag = document.createDocumentFragment();
            n.textContent.split(/(\s+)/).forEach(part => {
              if (!part) return;
              if (/^\s+$/.test(part)) { frag.appendChild(document.createTextNode(' ')); return; }
              const w = document.createElement('span'); w.className = 'w';
              const i = document.createElement('span'); i.textContent = part;
              w.appendChild(i); frag.appendChild(w);
            });
            n.replaceWith(frag);
          } else if (n.nodeType === 1) walk(n);
        });
      };
      walk(el);
      el.setAttribute('aria-label', el.textContent.replace(/\s+/g, ' ').trim());
    });

    if (reduce) { root.classList.remove('js'); const l = $('.loader'); l && l.remove(); return; }

    /* ---- Лоадер + інтро ---- */
    const seen = sessionStorageGet('ps-loaded');
    const loader = $('.loader');
    const heroR = isDesktop() ? 220 : 160;
    gsap.set('.hero-frame', { clipPath: `inset(100% 0% 0% 0% round ${heroR}px ${heroR}px 18px 18px)` });
    const intro = gsap.timeline({ paused: true, defaults: { ease: 'expo.out' } });
    intro
      .fromTo('.hero-frame', { clipPath: `inset(100% 0% 0% 0% round ${heroR}px ${heroR}px 18px 18px)` }, { clipPath: `inset(0% 0% 0% 0% round ${heroR}px ${heroR}px 18px 18px)`, duration: 1.6, ease: 'expo.inOut', onComplete: () => gsap.set('.hero-frame', { clipPath: 'none' }) }, 0)
      .from('.hero-frame img', { scale: 1.35, duration: 2, ease: 'expo.out' }, .3)
      .to('.ht-word', { y: 0, duration: 1.3, stagger: .12 }, .35)
      .fromTo('.ht-script', { opacity: 0, x: -30, rotate: -14 }, { opacity: 1, x: 0, rotate: -7, duration: 1.4 }, .9)
      .to('.hero-in', { opacity: 1, y: 0, duration: 1.1, stagger: .09 }, .75)
      .to('.badge', { opacity: 1, scale: 1, rotate: 0, duration: 1.4 }, 1.1)
      .from('.header-in', { y: -30, opacity: 0, duration: 1 }, .6);

    if (loader && !seen) {
      sessionStorageSet('ps-loaded', '1');
      lenis && lenis.stop();
      gsap.timeline({ delay: 1.55 })
        .to('.loader-inner', { y: -40, opacity: 0, duration: .6, ease: 'power3.in' })
        .fromTo(loader, { clipPath: 'inset(0% 0% 0% 0%)' }, { clipPath: 'inset(0% 0% 100% 0%)', duration: 1, ease: 'expo.inOut' }, '-=.15')
        .add(() => { intro.play(); lenis && lenis.start(); }, '-=.55')
        .add(() => loader.remove());
    } else {
      loader && loader.remove();
      intro.play();
    }

    /* ---- Хедер: фон при скролі, ховається вниз / показується вгору ---- */
    const header = $('.header'), mbar = $('.mbar');
    let lastY = 0;
    ScrollTrigger.create({
      start: 0, end: 'max',
      onUpdate: self => {
        const y = self.scroll();
        header.classList.toggle('is-scrolled', y > 40);
        const menuOpen = burger.getAttribute('aria-expanded') === 'true';
        header.classList.toggle('is-hidden', !menuOpen && y > 500 && y > lastY);
        mbar && mbar.classList.toggle('is-visible', y > innerHeight * .6);
        lastY = y;
      }
    });

    /* ---- Активний пункт меню ---- */
    $$('.nav a').forEach(a => {
      const sec = $(a.getAttribute('href'));
      sec && ScrollTrigger.create({ trigger: sec, start: 'top 50%', end: 'bottom 50%', onToggle: s => a.classList.toggle('is-active', s.isActive) });
    });

    /* ---- Заголовки секцій ---- */
    $$('.split').forEach(el => {
      if (el.closest('.hero')) return;
      gsap.from($$('.w > span', el), {
        yPercent: 110, rotate: 4, duration: 1.2, ease: 'expo.out', stagger: .06,
        scrollTrigger: { trigger: el, start: 'top 85%' }
      });
    });
    $$('.kicker').forEach(k => gsap.from(k, { opacity: 0, x: -20, duration: 1, ease: 'expo.out', scrollTrigger: { trigger: k, start: 'top 90%' } }));

    /* ---- Поява блоків ---- */
    ScrollTrigger.batch('.reveal-up', {
      start: 'top 88%',
      onEnter: els => gsap.to(els, { opacity: 1, y: 0, duration: 1.1, ease: 'expo.out', stagger: .1, overwrite: true })
    });
    $$('.reveal-clip').forEach(el => {
      const img = $('img, iframe', el);
      const tl = gsap.timeline({ scrollTrigger: { trigger: el, start: 'top 85%' } });
      tl.fromTo(el, { clipPath: 'inset(100% 0% 0% 0%)' }, { clipPath: 'inset(0% 0% 0% 0%)', duration: 1.5, ease: 'expo.inOut', onComplete: () => gsap.set(el, { clipPath: 'none' }) });
      if (img && img.tagName === 'IMG') tl.from(img, { scale: 1.3, duration: 1.8, ease: 'expo.out' }, .2);
    });

    /* ---- Паралакс ---- */
    gsap.to('.hero-frame img', { yPercent: -12, ease: 'none', scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: true } });
    gsap.to('.hero-title', { yPercent: 18, ease: 'none', scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: true } });
    gsap.to('.hero-glow', { yPercent: 30, ease: 'none', scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: true } });
    $$('.svc-photo img, .story-img img').forEach(img => gsap.fromTo(img, { yPercent: -8 }, { yPercent: 8, ease: 'none', scrollTrigger: { trigger: img.parentElement, start: 'top bottom', end: 'bottom top', scrub: true } }));
    gsap.fromTo('.story-logo', { y: 60, rotate: -8 }, { y: -40, rotate: 6, ease: 'none', scrollTrigger: { trigger: '.story', start: 'top bottom', end: 'bottom top', scrub: true } });
    gsap.fromTo('.cta-bg', { yPercent: -10 }, { yPercent: 10, ease: 'none', scrollTrigger: { trigger: '.cta', start: 'top bottom', end: 'bottom top', scrub: true } });
    gsap.from('.footer-big', { yPercent: 40, opacity: 0, ease: 'none', scrollTrigger: { trigger: '.footer', start: 'top bottom', end: 'top 40%', scrub: true } });

    /* ---- Бігучий рядок, що реагує на швидкість скролу ---- */
    const marquees = $$('.marquee').map((m, i) => ({ track: $('.marquee-track', m), x: 0, dir: i % 2 ? 1 : -1 }));
    let velBoost = 0;
    ScrollTrigger.create({ start: 0, end: 'max', onUpdate: s => { velBoost = gsap.utils.clamp(-12, 12, s.getVelocity() / 250); } });
    gsap.ticker.add((t, dt) => {
      velBoost *= .93;
      marquees.forEach(m => {
        const half = m.track.scrollWidth / 2;
        if (!half) return;
        m.x += (m.dir * (0.6 + Math.abs(velBoost))) * (dt / 16.7);
        if (m.x <= -half) m.x += half;
        if (m.x > 0) m.x -= half;
        m.track.style.transform = `translate3d(${m.x}px,0,0)`;
      });
    });

    /* ---- Лічильники ---- */
    $$('.count').forEach(el => {
      const to = parseFloat(el.dataset.to), dec = (el.dataset.to.split('.')[1] || '').length;
      const o = { v: 0 };
      el.textContent = (0).toFixed(dec);
      gsap.to(o, { v: to, duration: 2.2, ease: 'expo.out', scrollTrigger: { trigger: el, start: 'top 90%' }, onUpdate: () => { el.textContent = o.v.toFixed(dec); } });
    });

    /* ---- Ряди послуг ---- */
    ScrollTrigger.batch('.svc-panel:not([hidden]) .svc-row', {
      start: 'top 92%',
      onEnter: els => gsap.from(els, { y: 30, opacity: 0, duration: .9, stagger: .07, ease: 'expo.out' })
    });

    /* ---- Команда: поява ---- */
    gsap.from('.member', { y: 100, opacity: 0, duration: 1.4, stagger: .12, ease: 'expo.out', scrollTrigger: { trigger: '.team-grid', start: 'top 80%' } });

    /* ---- Галерея: горизонтальний скрол із закріпленням (десктоп) ---- */
    const mm = gsap.matchMedia();
    mm.add('(min-width: 901px)', () => {
      const track = $('.gal-track');
      const dist = () => Math.max(0, track.scrollWidth - innerWidth);
      const tween = gsap.to(track, {
        x: () => -dist(), ease: 'none',
        scrollTrigger: { trigger: '.gallery-pin', start: 'top top', end: () => '+=' + dist(), pin: true, scrub: 1, invalidateOnRefresh: true, anticipatePin: 1 }
      });
      $$('.g-img img').forEach(img => gsap.fromTo(img, { xPercent: -6 }, { xPercent: 6, ease: 'none', scrollTrigger: { trigger: img.closest('.g-item'), containerAnimation: tween, start: 'left right', end: 'right left', scrub: true } }));
      return () => gsap.set(track, { x: 0 });
    });
    gsap.from('.g-item', { y: 80, opacity: 0, duration: 1.3, stagger: .08, ease: 'expo.out', scrollTrigger: { trigger: '.gallery', start: 'top 70%' } });

    /* ---- Відгуки: безкінечна стрічка + перетягування ---- */
    reviewsMarquee();

    ScrollTrigger.refresh();
    addEventListener('load', () => ScrollTrigger.refresh());
  }

  function reviewsMarquee() {
    const wrap = $('.rev-marquee'), track = $('.rev-track');
    if (!wrap || !track) return;
    $$('.review', track).forEach(c => { const cl = c.cloneNode(true); cl.setAttribute('aria-hidden', 'true'); track.appendChild(cl); });
    let x = 0, drag = false, startX = 0, startPos = 0, hover = false, vel = 0, lastX = 0;
    const speed = .45;
    const half = () => track.scrollWidth / 2;
    const wrapX = () => { const h = half(); if (x <= -h) x += h; if (x > 0) x -= h; };
    wrap.addEventListener('pointerenter', () => hover = true);
    wrap.addEventListener('pointerleave', () => { hover = false; drag = false; wrap.classList.remove('is-drag'); });
    wrap.addEventListener('pointerdown', e => { drag = true; startX = lastX = e.clientX; startPos = x; vel = 0; wrap.classList.add('is-drag'); wrap.setPointerCapture(e.pointerId); });
    wrap.addEventListener('pointermove', e => { if (!drag) return; x = startPos + (e.clientX - startX); vel = e.clientX - lastX; lastX = e.clientX; wrapX(); });
    const end = () => { drag = false; wrap.classList.remove('is-drag'); };
    wrap.addEventListener('pointerup', end);
    wrap.addEventListener('pointercancel', end);
    gsap.ticker.add((t, dt) => {
      if (!drag) {
        vel *= .94;
        x += vel - (hover ? speed * .25 : speed) * (dt / 16.7);
        wrapX();
      }
      track.style.transform = `translate3d(${x}px,0,0)`;
    });
  }

  function sessionStorageGet(k) { try { return sessionStorage.getItem(k); } catch (e) { return null; } }
  function sessionStorageSet(k, v) { try { sessionStorage.setItem(k, v); } catch (e) { /* приватний режим */ } }

  /* ---------- Курсор, магнітні кнопки, світіння, нахил (тільки миша) ---------- */
  function pointerFx() {
    if (!finePointer || reduce || !window.gsap) return;
    root.classList.add('has-cursor');
    const cursor = $('.cursor'), dot = $('.cursor-dot'), ring = $('.cursor-ring'), label = $('.cursor-label');
    const book = { pt: 'Marcar', en: 'Book', de: 'Buchen' }[document.body.dataset.lang] || 'Book';
    const dx = gsap.quickTo(dot, 'x', { duration: .1 }), dy = gsap.quickTo(dot, 'y', { duration: .1 });
    const rx = gsap.quickTo(ring, 'x', { duration: .5, ease: 'expo.out' }), ry = gsap.quickTo(ring, 'y', { duration: .5, ease: 'expo.out' });
    let shown = false;
    addEventListener('pointermove', e => { if (!shown) { shown = true; gsap.set([dot, ring], { x: e.clientX, y: e.clientY }); gsap.to(cursor, { opacity: 1, duration: .3 }); } dx(e.clientX); dy(e.clientY); rx(e.clientX); ry(e.clientY); });
    document.addEventListener('pointerover', e => {
      const el = e.target.closest('[data-cursor], a, button, summary');
      cursor.classList.remove('is-hover', 'is-label');
      if (!el) return;
      const type = el.dataset.cursor;
      if (type === 'book') { label.textContent = book; cursor.classList.add('is-label'); }
      else if (type === 'drag') { label.textContent = el.dataset.cursorLabel || 'Drag'; cursor.classList.add('is-label'); }
      else cursor.classList.add('is-hover');
    });
    document.addEventListener('pointerleave', () => gsap.to(cursor, { opacity: 0, duration: .3 }));
    document.addEventListener('pointerenter', () => gsap.to(cursor, { opacity: 1, duration: .3 }));

    $$('.magnetic').forEach(b => {
      const xTo = gsap.quickTo(b, 'x', { duration: .8, ease: 'elastic.out(1, .4)' }), yTo = gsap.quickTo(b, 'y', { duration: .8, ease: 'elastic.out(1, .4)' });
      b.addEventListener('pointermove', e => { const r = b.getBoundingClientRect(); xTo((e.clientX - r.left - r.width / 2) * .3); yTo((e.clientY - r.top - r.height / 2) * .4); });
      b.addEventListener('pointerleave', () => { xTo(0); yTo(0); });
    });

    $$('.perk').forEach(p => p.addEventListener('pointermove', e => {
      const r = p.getBoundingClientRect();
      p.style.setProperty('--mx', (e.clientX - r.left) + 'px');
      p.style.setProperty('--my', (e.clientY - r.top) + 'px');
    }));

    $$('[data-tilt]').forEach(c => {
      const rX = gsap.quickTo(c, 'rotationX', { duration: .6, ease: 'power3' }), rY = gsap.quickTo(c, 'rotationY', { duration: .6, ease: 'power3' });
      gsap.set(c, { transformPerspective: 900 });
      c.addEventListener('pointermove', e => { const r = c.getBoundingClientRect(); rY(((e.clientX - r.left) / r.width - .5) * 10); rX(-((e.clientY - r.top) / r.height - .5) * 10); });
      c.addEventListener('pointerleave', () => { rX(0); rY(0); });
    });
  }

  const start = () => { try { init(); pointerFx(); } catch (err) { console.error(err); fallback(); } };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start); else start();
})();
