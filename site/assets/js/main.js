/* Pro Style Barbershop — анімації та інтерактив */
(() => {
  const root = document.documentElement;
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const finePointer = matchMedia('(hover: hover) and (pointer: fine)').matches;
  const store = {
    get: k => { try { return sessionStorage.getItem(k); } catch (e) { return null; } },
    set: (k, v) => { try { sessionStorage.setItem(k, v); } catch (e) { /* приватний режим */ } },
    del: k => { try { sessionStorage.removeItem(k); } catch (e) { /* */ } },
  };

  /* ---------- Відкрито / зачинено (час Мадейри) ---------- */
  function madeiraNow() {
    const parts = new Intl.DateTimeFormat('en-GB', { timeZone: 'Atlantic/Madeira', weekday: 'short', hour: '2-digit', minute: '2-digit', hour12: false })
      .formatToParts(new Date()).reduce((o, p) => (o[p.type] = p.value, o), {});
    return { day: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].indexOf(parts.weekday), mins: (+parts.hour % 24) * 60 + +parts.minute };
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
      if (today) li.firstElementChild.dataset.today = li.parentElement.dataset.todayLabel; else delete li.firstElementChild.dataset.today;
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
    ind.style.height = tab.offsetHeight + 'px';
    ind.style.transform = `translate(${tab.offsetLeft}px, ${tab.offsetTop}px)`;
  };
  const setPhoto = cat => $$('.svc-photo figure').forEach(f => f.classList.toggle('is-active', f.dataset.cat === cat));
  tabs.forEach((tab, i) => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.setAttribute('aria-selected', t === tab));
      $$('.svc-panel').forEach(p => { p.hidden = p.id !== tab.getAttribute('aria-controls'); });
      moveInd(tab);
      setPhoto(tab.id.replace('tab-', ''));
      const bar = tab.parentElement;
      if (bar.scrollWidth > bar.clientWidth) bar.scrollTo({ left: tab.offsetLeft - 20, behavior: 'smooth' });
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
        gsap.to(body, { height: 0, duration: .5, ease: 'expo.out', onComplete: () => { d.open = false; body.style.height = ''; ScrollTrigger.refresh(); } });
      } else {
        d.open = true;
        gsap.fromTo(body, { height: 0 }, { height: body.scrollHeight, duration: .7, ease: 'expo.out', onComplete: () => { body.style.height = ''; ScrollTrigger.refresh(); } });
      }
    });
  });

  function fallback() {
    root.classList.remove('js');
    $$('.loader, .wipe').forEach(el => el.remove());
  }

  /* ---------- Розбиття тексту ---------- */
  function splitWords(el, cls = 'w') {
    el.setAttribute('aria-label', el.textContent.replace(/\s+/g, ' ').trim());
    const walk = node => {
      [...node.childNodes].forEach(n => {
        if (n.nodeType === 3) {
          const frag = document.createDocumentFragment();
          n.textContent.split(/(\s+)/).forEach(part => {
            if (!part) return;
            if (/^\s+$/.test(part)) { frag.appendChild(document.createTextNode(' ')); return; }
            const w = document.createElement('span'); w.className = cls;
            if (cls === 'w') { const i = document.createElement('span'); i.textContent = part; w.appendChild(i); }
            else w.textContent = part;
            frag.appendChild(w);
          });
          n.replaceWith(frag);
        } else if (n.nodeType === 1) walk(n);
      });
    };
    walk(el);
  }
  function splitChars(el) {
    const txt = el.textContent;
    el.textContent = '';
    [...txt].forEach((c, i) => {
      const s = document.createElement('span');
      s.className = 'ch'; s.style.setProperty('--i', i); s.textContent = c;
      el.appendChild(s);
    });
  }

  function init() {
    if (!window.gsap || !window.ScrollTrigger) return fallback();
    gsap.registerPlugin(ScrollTrigger);

    /* ---- Smooth scroll ---- */
    let lenis = null;
    if (!reduce && window.Lenis) {
      lenis = new Lenis({ duration: 1.15, easing: t => Math.min(1, 1.001 - Math.pow(2, -10 * t)) });
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
      lenis ? lenis.scrollTo(target, { offset: id === '#main' ? 0 : -10, duration: 1.4 }) : target.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth' });
    }));

    $$('.split').forEach(el => splitWords(el));
    $$('.ht-word').forEach(splitChars);
    const mText = $('.manifesto-text');
    mText && splitWords(mText, 'mw');

    if (reduce) { fallback(); $$('.ht-word').forEach(w => { w.style.visibility = 'visible'; }); return; }

    /* ---- Перехід між мовами ---- */
    const wipe = $('.wipe'), wGold = $('.wipe-gold'), wDark = $('.wipe-dark');
    $$('.lang a, .footer a[hreflang]').forEach(a => a.addEventListener('click', e => {
      if (e.metaKey || e.ctrlKey) return;
      e.preventDefault();
      store.set('ps-wipe', '1');
      gsap.set(wipe, { visibility: 'visible' });
      gsap.timeline({ onComplete: () => { location.href = a.href; } })
        .fromTo(wGold, { yPercent: 100 }, { yPercent: 0, duration: .55, ease: 'expo.in' })
        .fromTo(wDark, { yPercent: 100 }, { yPercent: 0, duration: .55, ease: 'expo.inOut' }, '-=.25');
    }));

    /* ---- Лоадер + інтро ---- */
    const clipFrom = 'inset(100% 0% 0% 0% round 999px 999px 18px 18px)', clipTo = 'inset(0% 0% 0% 0% round 999px 999px 18px 18px)';
    gsap.set('.hero-frame', { clipPath: clipFrom });
    gsap.set('.ht-word', { visibility: 'visible' });
    gsap.set('.ht-word .ch', { yPercent: 115, rotateX: -85, opacity: 0 });
    const intro = gsap.timeline({ paused: true, defaults: { ease: 'expo.out' } });
    intro
      .fromTo('.hero-frame', { clipPath: clipFrom }, { clipPath: clipTo, duration: 1.6, ease: 'expo.inOut', onComplete: () => gsap.set('.hero-frame', { clipPath: 'none' }) }, 0)
      .from('.hero-frame img', { scale: 1.4, duration: 2.2 }, .2)
      .to('.ht-word .ch', { yPercent: 0, rotateX: 0, opacity: 1, duration: 1.3, stagger: .05 }, .35)
      .fromTo('.ht-script', { opacity: 0, x: -40, rotate: -16, filter: 'blur(8px)' }, { opacity: 1, x: 0, rotate: -7, filter: 'blur(0px)', duration: 1.5 }, .95)
      .to('.hero-in', { opacity: 1, y: 0, duration: 1.1, stagger: .09 }, .8)
      .fromTo('.badge', { opacity: 0, scale: .4, rotate: -90 }, { opacity: 1, scale: 1, rotate: 0, duration: 1.6 }, 1.1)
      .fromTo('.hero-frame-shine', { xPercent: -120 }, { xPercent: 120, duration: 1.6, ease: 'power2.inOut' }, 1.4)
      .from('.header-in', { y: -30, opacity: 0, duration: 1 }, .6);

    const loader = $('.loader');
    if (store.get('ps-wipe')) {
      store.del('ps-wipe');
      loader && loader.remove();
      gsap.set(wipe, { visibility: 'visible' }); gsap.set([wGold, wDark], { yPercent: 0 });
      gsap.timeline({ onComplete: () => gsap.set(wipe, { visibility: 'hidden' }) })
        .to(wDark, { yPercent: -100, duration: .8, ease: 'expo.inOut' }, .1)
        .to(wGold, { yPercent: -100, duration: .8, ease: 'expo.inOut' }, .22)
        .add(() => intro.play(), .35);
    } else if (loader && !store.get('ps-loaded')) {
      store.set('ps-loaded', '1');
      lenis && lenis.stop();
      const c = { v: 0 }, count = $('.loader-count'), bar = $('.loader-bar i');
      gsap.timeline()
        .to(c, { v: 100, duration: 1.5, ease: 'power2.inOut', onUpdate: () => { count.textContent = Math.round(c.v); bar.style.transform = `scaleX(${c.v / 100})`; } }, .1)
        .to('.loader-inner', { y: -40, opacity: 0, duration: .6, ease: 'power3.in' }, '+=.1')
        .fromTo(loader, { clipPath: 'inset(0% 0% 0% 0%)' }, { clipPath: 'inset(0% 0% 100% 0%)', duration: 1, ease: 'expo.inOut' }, '-=.15')
        .add(() => { intro.play(); lenis && lenis.start(); }, '-=.55')
        .add(() => loader.remove());
    } else {
      loader && loader.remove();
      intro.play();
    }

    /* ---- Хедер, прогрес скролу, мобільна панель ---- */
    const header = $('.header'), mbar = $('.mbar'), prog = $('.progress i');
    let lastY = 0;
    ScrollTrigger.create({
      start: 0, end: 'max',
      onUpdate: self => {
        const y = self.scroll();
        header.classList.toggle('is-scrolled', y > 40);
        const menuOpen = burger.getAttribute('aria-expanded') === 'true';
        if (!menuOpen && y > 500 && y > lastY + 2) header.classList.add('is-hidden');
        else if (y < lastY - 2 || y <= 500) header.classList.remove('is-hidden');
        mbar && mbar.classList.toggle('is-visible', y > innerHeight * .6);
        prog.style.transform = `scaleX(${self.progress})`;
        lastY = y;
      }
    });

    /* ---- Активний пункт меню ---- */
    $$('.nav a').forEach(a => {
      const sec = $(a.getAttribute('href'));
      sec && ScrollTrigger.create({ trigger: sec, start: 'top 50%', end: 'bottom 50%', onToggle: s => a.classList.toggle('is-active', s.isActive) });
    });

    /* ---- Заголовки секцій: слова виїжджають ---- */
    $$('.split').forEach(el => {
      gsap.from($$('.w > span', el), {
        yPercent: 115, rotate: 5, duration: 1.2, ease: 'expo.out', stagger: .06,
        scrollTrigger: { trigger: el, start: 'top 88%' }
      });
    });
    $$('.kicker').forEach(k => gsap.from(k, { opacity: 0, x: -24, duration: 1, ease: 'expo.out', scrollTrigger: { trigger: k, start: 'top 92%' } }));

    /* ---- Поява блоків ---- */
    $$('.perk').forEach(p => p.classList.remove('reveal-up'));
    ScrollTrigger.batch('.reveal-up', {
      start: 'top 90%',
      onEnter: els => gsap.to(els, { opacity: 1, y: 0, duration: 1.1, ease: 'expo.out', stagger: .1, overwrite: true })
    });
    $$('.reveal-clip').forEach(el => {
      const img = $('img', el);
      const tl = gsap.timeline({ scrollTrigger: { trigger: el, start: 'top 88%' } });
      tl.fromTo(el, { clipPath: 'inset(100% 0% 0% 0%)' }, { clipPath: 'inset(0% 0% 0% 0%)', duration: 1.5, ease: 'expo.inOut', onComplete: () => gsap.set(el, { clipPath: 'none' }) });
      if (img && !el.classList.contains('svc-photo')) tl.from(img, { scale: 1.3, duration: 1.8, ease: 'expo.out' }, .2);
    });

    /* ---- Маніфест: слова підсвічуються під час скролу ---- */
    if (mText) {
      gsap.to($$('.mw', mText), {
        opacity: 1, stagger: .1, ease: 'none',
        scrollTrigger: { trigger: mText, start: 'top 80%', end: 'bottom 45%', scrub: .6 }
      });
    }

    /* ---- Паралакс ---- */
    const heroST = () => ({ trigger: '.hero', start: 'top top', end: 'bottom top', scrub: true });
    gsap.to('.hero-frame img', { yPercent: -12, ease: 'none', scrollTrigger: heroST() });
    gsap.to('.hero-copy', { yPercent: 14, opacity: .25, ease: 'none', scrollTrigger: heroST() });
    gsap.to('.hero-glow', { yPercent: 30, ease: 'none', scrollTrigger: heroST() });
    $$('.story-img img').forEach(img => gsap.fromTo(img, { yPercent: -8 }, { yPercent: 8, ease: 'none', scrollTrigger: { trigger: img.parentElement, start: 'top bottom', end: 'bottom top', scrub: true } }));
    gsap.fromTo('.story-logo', { y: 60, rotate: -14, scale: .85 }, { y: -30, rotate: 8, scale: 1, ease: 'none', scrollTrigger: { trigger: '.story', start: 'top bottom', end: 'bottom top', scrub: true } });
    gsap.fromTo('.cta-bg', { yPercent: -10, scale: 1.15 }, { yPercent: 10, scale: 1, ease: 'none', scrollTrigger: { trigger: '.cta', start: 'top bottom', end: 'bottom top', scrub: true } });
    gsap.from('.cta .crown', { y: -30, opacity: 0, rotate: -20, duration: 1.2, ease: 'expo.out', scrollTrigger: { trigger: '.cta', start: 'top 70%' } });

    /* ---- Бігучий рядок, що реагує на швидкість скролу ---- */
    const marquees = $$('.marquee').map((m, i) => ({ track: $('.marquee-track', m), x: 0, dir: i % 2 ? 1 : -1 }));
    let velBoost = 0;
    ScrollTrigger.create({ start: 0, end: 'max', onUpdate: s => { velBoost = gsap.utils.clamp(-14, 14, s.getVelocity() / 220); } });
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
      gsap.to(o, { v: to, duration: 2.2, ease: 'expo.out', scrollTrigger: { trigger: el, start: 'top 92%' }, onUpdate: () => { el.textContent = o.v.toFixed(dec); } });
    });

    /* ---- Каскадна поява карток ---- */
    gsap.from('.svc-panel:not([hidden]) .svc-row', { y: 30, opacity: 0, duration: .9, stagger: .07, ease: 'expo.out', scrollTrigger: { trigger: '.svc-panels', start: 'top 85%' } });
    gsap.from('.member', { y: 90, opacity: 0, duration: 1.4, stagger: .12, ease: 'expo.out', scrollTrigger: { trigger: '.team-grid', start: 'top 82%' } });
    gsap.from('.review', { y: 60, opacity: 0, rotate: () => gsap.utils.random(-3, 3), duration: 1.2, stagger: .08, ease: 'expo.out', scrollTrigger: { trigger: '.rev-grid', start: 'top 85%' } });
    gsap.from('.perk', { y: 50, opacity: 0, duration: 1.1, stagger: .1, ease: 'expo.out', scrollTrigger: { trigger: '.perks', start: 'top 85%' } });

    /* ---- Галерея: 1 екран + горизонтальний скрол (десктоп) ---- */
    const mm = gsap.matchMedia();
    const total = $$('.g-item').length, cur = $('.gal-cur'), gbar = $('.gal-bar i');
    mm.add('(min-width: 901px)', () => {
      const track = $('.gal-track');
      const dist = () => Math.max(0, track.scrollWidth - innerWidth);
      const skew = gsap.quickTo('.g-img', 'skewX', { duration: .5, ease: 'power3' });
      const tween = gsap.to(track, {
        x: () => -dist(), ease: 'none',
        scrollTrigger: {
          trigger: '.gal-pin', start: 'top top', end: () => '+=' + dist(), pin: true, scrub: 1, invalidateOnRefresh: true, anticipatePin: 1,
          onUpdate: s => {
            gbar.style.transform = `scaleX(${s.progress})`;
            cur.textContent = String(Math.min(total, Math.round(s.progress * (total - 1)) + 1)).padStart(2, '0');
            skew(gsap.utils.clamp(-6, 6, s.getVelocity() / -400));
          },
          onLeave: () => skew(0), onLeaveBack: () => skew(0)
        }
      });
      $$('.g-img img').forEach(img => gsap.fromTo(img, { xPercent: -5 }, { xPercent: 5, ease: 'none', scrollTrigger: { trigger: img.closest('.g-item'), containerAnimation: tween, start: 'left right', end: 'right left', scrub: true } }));
      return () => gsap.set(track, { x: 0 });
    });
    gsap.from('.g-item', { y: 80, opacity: 0, duration: 1.3, stagger: .08, ease: 'expo.out', scrollTrigger: { trigger: '.gallery', start: 'top 70%' } });

    /* ---- Футер: великі літери виїжджають по одній ---- */
    gsap.from('.footer-big span', { yPercent: 100, duration: 1.4, stagger: .06, ease: 'expo.out', scrollTrigger: { trigger: '.footer', start: 'top 85%' } });

    ScrollTrigger.refresh();
    addEventListener('load', () => ScrollTrigger.refresh());
    document.fonts && document.fonts.ready.then(() => ScrollTrigger.refresh());
  }

  /* ---------- Курсор, магніт, світіння, нахил, паралакс від миші ---------- */
  function pointerFx() {
    if (!finePointer || reduce || !window.gsap) return;
    root.classList.add('has-cursor');
    const cursor = $('.cursor'), dot = $('.cursor-dot'), ring = $('.cursor-ring'), label = $('.cursor-label');
    const book = { pt: 'Marcar', en: 'Book', de: 'Buchen' }[document.body.dataset.lang] || 'Book';
    const dx = gsap.quickTo(dot, 'x', { duration: .1 }), dy = gsap.quickTo(dot, 'y', { duration: .1 });
    const rx = gsap.quickTo(ring, 'x', { duration: .5, ease: 'expo.out' }), ry = gsap.quickTo(ring, 'y', { duration: .5, ease: 'expo.out' });
    let shown = false;
    addEventListener('pointermove', e => {
      if (!shown) { shown = true; gsap.set([dot, ring], { x: e.clientX, y: e.clientY }); gsap.to(cursor, { opacity: 1, duration: .3 }); }
      dx(e.clientX); dy(e.clientY); rx(e.clientX); ry(e.clientY);
    });
    document.addEventListener('pointerover', e => {
      const el = e.target.closest('[data-cursor], a, button, summary');
      cursor.classList.remove('is-hover', 'is-label');
      if (!el) return;
      if (el.dataset.cursor === 'book') { label.textContent = book; cursor.classList.add('is-label'); }
      else cursor.classList.add('is-hover');
    });
    root.addEventListener('pointerleave', () => gsap.to(cursor, { opacity: 0, duration: .3 }));
    root.addEventListener('pointerenter', () => shown && gsap.to(cursor, { opacity: 1, duration: .3 }));

    /* магнітні кнопки */
    $$('.magnetic').forEach(b => {
      const xTo = gsap.quickTo(b, 'x', { duration: .8, ease: 'elastic.out(1, .4)' }), yTo = gsap.quickTo(b, 'y', { duration: .8, ease: 'elastic.out(1, .4)' });
      b.addEventListener('pointermove', e => { const r = b.getBoundingClientRect(); xTo((e.clientX - r.left - r.width / 2) * .3); yTo((e.clientY - r.top - r.height / 2) * .4); });
      b.addEventListener('pointerleave', () => { xTo(0); yTo(0); });
    });

    /* світіння, що йде за курсором */
    $$('[data-spot]').forEach(p => p.addEventListener('pointermove', e => {
      const r = p.getBoundingClientRect();
      p.style.setProperty('--mx', (e.clientX - r.left) + 'px');
      p.style.setProperty('--my', (e.clientY - r.top) + 'px');
    }));

    /* 3D-нахил карток команди */
    $$('[data-tilt]').forEach(c => {
      const rX = gsap.quickTo(c, 'rotationX', { duration: .6, ease: 'power3' }), rY = gsap.quickTo(c, 'rotationY', { duration: .6, ease: 'power3' });
      gsap.set(c, { transformPerspective: 900 });
      c.addEventListener('pointermove', e => { const r = c.getBoundingClientRect(); rY(((e.clientX - r.left) / r.width - .5) * 12); rX(-((e.clientY - r.top) / r.height - .5) * 12); });
      c.addEventListener('pointerleave', () => { rX(0); rY(0); });
    });

    /* hero: шари рухаються за мишею + золотий прожектор */
    const hero = $('.hero');
    if (hero) {
      const spot = $('.hero-spot');
      const sx = gsap.quickTo(spot, 'x', { duration: .9, ease: 'power3' }), sy = gsap.quickTo(spot, 'y', { duration: .9, ease: 'power3' });
      const layers = [[$('.hero-frame'), 16], [$('.badge'), 34], [$('.ht-script'), -22]]
        .filter(l => l[0]).map(([el, k]) => ({ k, x: gsap.quickTo(el, 'x', { duration: 1.1, ease: 'power3' }), y: gsap.quickTo(el, 'y', { duration: 1.1, ease: 'power3' }) }));
      hero.addEventListener('pointermove', e => {
        const r = hero.getBoundingClientRect();
        sx(e.clientX - r.left); sy(e.clientY - r.top);
        const nx = e.clientX / innerWidth - .5, ny = e.clientY / innerHeight - .5;
        layers.forEach(l => { l.x(nx * l.k); l.y(ny * l.k); });
      });
      hero.addEventListener('pointerleave', () => layers.forEach(l => { l.x(0); l.y(0); }));
    }

    /* послуги: фото пливе біля курсора */
    const prev = $('.svc-preview'), panels = $('.svc-panels');
    if (prev && panels && getComputedStyle(prev).display !== 'none') {
      const imgs = $$('img', prev);
      const px = gsap.quickTo(prev, 'x', { duration: .6, ease: 'power3' }), py = gsap.quickTo(prev, 'y', { duration: .6, ease: 'power3' });
      const pr = gsap.quickTo(prev, 'rotation', { duration: .8, ease: 'power3' });
      let lx = 0;
      panels.addEventListener('pointerenter', e => { gsap.set(prev, { x: e.clientX + 170, y: e.clientY }); gsap.to(prev, { opacity: 1, scale: 1, duration: .5, ease: 'expo.out' }); });
      panels.addEventListener('pointerleave', () => gsap.to(prev, { opacity: 0, scale: .6, duration: .4, ease: 'power3.out' }));
      panels.addEventListener('pointermove', e => {
        px(e.clientX + 170); py(e.clientY);
        pr(gsap.utils.clamp(-14, 14, (e.clientX - lx) * .9)); lx = e.clientX;
        const row = e.target.closest('.svc-row');
        if (row) imgs.forEach(img => img.classList.toggle('is-active', img.dataset.cat === row.dataset.cat));
      });
    }
  }

  const start = () => { try { init(); pointerFx(); } catch (err) { console.error(err); fallback(); } };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start); else start();
})();
