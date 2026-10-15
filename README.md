# Pro Style Barbershop — сайт (демо для пропозиції)

## Як відкрити
- Онлайн-демо: https://nexgen-fullstack.github.io/prostyle-barbershop/
- Локально: двічі клікнути `site/index.html` (PT), `site/en/index.html` (EN) або `site/de/index.html` (DE).
- Для шрифтів і карти потрібен інтернет. Анімації працюють і без нього.

## Структура
- `site/` — готовий сайт. Саме цю папку треба завантажувати на хостинг (Netlify, Vercel, cPanel).
- `build.py` — усі тексти, ціни, відгуки, команда. Після змін запустити `python build.py`.
- `tools_images.py` — обробка фото з `img/raw` у WebP.
- `site/assets/css/style.css` — дизайн, `site/assets/js/main.js` — анімації.

## Перед запуском у продакшн
1. Купити домен і замінити `BASE` у `build.py` (зараз стоїть `https://www.prostylebarbershop.pt`), потім `python build.py` (БЕЗ `--demo`).
   Демо на GitHub зібране командою `python build.py --demo` — воно закрите від Google (noindex), щоб не створювати дублікат.
2. Взяти в барбершопу свої фото робіт (стрижки крупним планом) і посилання на Instagram/TikTok.
3. Додати сайт у Google Business Profile (поле «Веб-сайт»), відправити `sitemap.xml` у Google Search Console.
4. Перевірити з власником: ролі барберів, «з/без запису», стрижки дітям.
