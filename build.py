"""
Генератор сайту Pro Style Barbershop.
Запуск:  python build.py
Створює site/index.html (PT, основна), site/en/ (EN), site/de/ (DE) + sitemap.xml.
Демо-версія без індексації в Google:  python build.py --demo
Весь текст і дані — тут, у словниках нижче. Дизайн — site/assets/css/style.css, анімації — site/assets/js/main.js.
"""
import json
import sys
from html import escape
from pathlib import Path

# ---------------------------------------------------------------- базові дані (NAP)
BASE = "https://www.prostylebarbershop.pt"  # запропонований домен — змінити, коли буде куплено
BOOKSY = "https://prostyle38.booksy.com"
PHONE_DISPLAY = "939 135 742"
PHONE_INTL = "+351939135742"
MAPS_PLACE = "https://maps.app.goo.gl/f3qpy4afYyYAXmer7"
MAPS_CID = "https://maps.google.com/?cid=11358967857118036349"
MAPS_DIR = "https://www.google.com/maps/dir/?api=1&destination=Pro+Style+Barbershop%2C+Av.+da+Madalena+101%2C+9020-330+Funchal"
MAPS_EMBED = "https://www.google.com/maps?q=Pro+Style+Barbershop,+Av.+da+Madalena+101,+9020-330+Funchal&z=17&output=embed&hl="
LAT, LNG = 32.6607696, -16.9308653
STREET = "Av. da Madalena 101, Fração B"
POSTAL = "9020-330"
CITY = "Funchal"
REGION = "Madeira"
YEAR = 2026
DEMO = "--demo" in sys.argv  # демо на GitHub Pages: noindex, щоб Google не індексував чернетку
LANGS = [("pt", "/", "pt-PT"), ("en", "/en/", "en"), ("de", "/de/", "de")]
MAP_HL = {"pt": "pt-PT", "en": "en", "de": "de"}

TEAM = [
    {"id": "alvaro", "name": "Alvaro Wolf", "lead": True},
    {"id": "elias", "name": "Elias"},
    {"id": "junior", "name": "Junior JR"},
    {"id": "matheus", "name": "Matheus"},
]

# Ціни та тривалість — з Booksy (жовтень 2026)
SERVICES = [
    ("cuts", [
        ("Corte Simples", "Simple Cut", 15, "30 min", False),
        ("Corte Degradê", "Fade / Gradient Cut", 17, "30 min", True),
        ("Corte à Tesoura", "Scissors Cut", 19, "30 min", False),
        ("Corte à Tesoura — Médio / Longo", "Scissors Cut — Medium / Long", 27, "1 h", False),
        ("Degradê + Sobrancelha", "Fade + Eyebrow Shaping", 19, "30 min", True),
    ]),
    ("beard", [
        ("Barba Simples", "Simple Beard", 14, "30 min", False),
        ("Barba Pro Style", "Pro Style Beard", 30, "1 h", True),
        ("Barba + Pigmento", "Beard + Pigment", 26, "40 min", False),
    ]),
    ("combo", [
        ("Cabelo e Barba", "Hair & Beard", 24, "1 h", True),
        ("Cabelo e Barba Pro Style", "Hair & Beard Pro Style", 42, "1 h 30", False),
        ("Corte + Pigmento", "Cut + Pigment", 29, "40 min", False),
    ]),
    ("color", [
        ("Coloração", "Hair Colouring", 35, "1 h", False),
        ("Coloração + Corte", "Colouring + Haircut", 50, "1 h 30", False),
        ("Madeixas / Luzes", "Highlights / Lowlights", 60, "1 h 30", False),
        ("Platinado / Nevou", "Platinum / Snow Blonde", 70, "1 h 30", True),
    ]),
    ("extras", [
        ("Sobrancelha", "Eyebrows", 5, "15 min", False),
        ("Cera — Nariz", "Nose Waxing", 3, "10 min", False),
        ("Degradê + Cera Nariz", "Fade + Nose Waxing", 20, "30 min", False),
    ]),
]

SERVICES_DE = {
    "Corte Simples": "Einfacher Haarschnitt", "Corte Degradê": "Fade-Haarschnitt", "Corte à Tesoura": "Scherenschnitt",
    "Corte à Tesoura — Médio / Longo": "Scherenschnitt — mittel / lang", "Degradê + Sobrancelha": "Fade + Augenbrauen",
    "Barba Simples": "Bart einfach", "Barba Pro Style": "Pro Style Bart", "Barba + Pigmento": "Bart + Pigmentierung",
    "Cabelo e Barba": "Haare & Bart", "Cabelo e Barba Pro Style": "Haare & Bart Pro Style", "Corte + Pigmento": "Schnitt + Pigmentierung",
    "Coloração": "Färben", "Coloração + Corte": "Färben + Haarschnitt", "Madeixas / Luzes": "Strähnchen",
    "Platinado / Nevou": "Platinblond", "Sobrancelha": "Augenbrauen", "Cera — Nariz": "Nasenwachs", "Degradê + Cera Nariz": "Fade + Nasenwachs",
}


def svc_name(lang, pt, en):
    return {"pt": pt, "en": en, "de": SERVICES_DE.get(pt, en)}[lang]


# Справжні відгуки з Google Maps (оригінальною мовою автора)
REVIEWS = [
    {"name": "Diogo", "when": {"pt": "há 1 semana", "en": "1 week ago", "de": "vor 1 Woche"}, "lang": "PT",
     "text": "Experiência impecável do início ao fim! Fui recebido com um cafezinho logo à entrada, o que demonstra logo a atenção ao detalhe e o respeito pelo cliente. A equipa é super simpática, o ambiente é muito porreiro e o corte ficou perfeito. Recomendo vivamente!"},
    {"name": "Francisco Abreu", "when": {"pt": "há 3 meses", "en": "3 months ago", "de": "vor 3 Monaten"}, "lang": {"pt": "PT", "en": "EN"},
     "text": {
         "pt": "O Alvaro é, sem dúvida, o melhor barbeiro da Madeira. Já o seguimos há anos e ficámos muito contentes por saber que ele abriu o seu próprio espaço. Confio nele a 100% para cortar o meu cabelo e o dos meus dois filhos. Ele está sempre bem-disposto, é super sociável e faz com que toda a gente se sinta em casa logo que entra na barbearia.",
         "en": "Alvaro is easily the best barber in Madeira. We’ve been coming to him for years, so we were thrilled to hear he’s opened his own place. I trust him completely with my haircuts, as well as those for my two boys. He is always smiling, incredibly sociable, and makes everyone feel so welcome the moment they walk in.",
     }},
    {"name": "Pietro Manara", "when": {"pt": "há 1 mês", "en": "1 month ago", "de": "vor 1 Monat"}, "lang": "EN",
     "text": "Amazing guys, very friendly, clean and nice work! Great work with hair, beard, you can drink coffee, water, play with PlayStation 5, and enjoy some good time! 💪🏻"},
    {"name": "Troy", "when": {"pt": "há 4 meses", "en": "4 months ago", "de": "vor 4 Monaten"}, "lang": "PT",
     "text": "Um grande corte de cabelo pode mudar a forma como uma pessoa se apresenta ao mundo, e é exatamente isso que acontece sempre que me sento na cadeira do Alvaro."},
    {"name": "Luca Venturini", "when": {"pt": "há 1 mês", "en": "1 month ago", "de": "vor 1 Monat"}, "lang": "EN · IT",
     "text": "Best barber in Funchal, very professionale and good price! Per 🇮🇹 consigliato alla grande!"},
    {"name": "Samuel Pedroso", "when": {"pt": "há 4 meses", "en": "4 months ago", "de": "vor 4 Monaten"}, "lang": "PT",
     "text": "Top. Sem marcação, aguardei e done! Simpáticos e profissionais. A loja está bem decorada, fresca (AC) e possibilidade de “bater” uma play. Tooooop. 🤙🏻"},
    {"name": "David de Sousa", "when": {"pt": "há 2 meses", "en": "2 months ago", "de": "vor 2 Monaten"}, "lang": "FR",
     "text": "Au top, des pros, super team, ambiance de fou… Je recommande vivement. Merci encore"},
    {"name": "Ohi Farhin", "when": {"pt": "há 6 meses", "en": "6 months ago", "de": "vor 6 Monaten"}, "lang": "EN",
     "text": "Great barber shop around the corner. Worth to visit. Jolly and happy people."},
]

GALLERY = [
    ("interior", 1400, 874, "wide"),
    ("barber-at-work", 900, 1125, "tall"),
    ("logo-wall", 900, 1125, "tall"),
    ("sign-night", 1024, 682, "wide"),
    ("storefront", 900, 1125, "tall"),
    ("window", 900, 1125, "tall"),
]

# ---------------------------------------------------------------- тексти
T = {
    "pt": {
        "html_lang": "pt-PT", "og_locale": "pt_PT", "path": "/", "other": "en", "other_path": "/en/", "other_label": "EN",
        "title": "Pro Style Barbershop – Barbearia em Funchal, Madeira",
        "desc": "Barbearia na Av. da Madalena, Funchal. Degradês, barba e coloração desde 15 €. ★ 5.0 em 322 avaliações no Booksy. Seg–Sáb 10h–19h. Marca online.",
        "skip": "Saltar para o conteúdo",
        "nav": [("#servicos", "Serviços"), ("#equipa", "Equipa"), ("#galeria", "Galeria"), ("#avaliacoes", "Avaliações"), ("#contactos", "Contactos")],
        "ids": {"services": "servicos", "team": "equipa", "gallery": "galeria", "reviews": "avaliacoes", "contact": "contactos", "experience": "experiencia", "faq": "perguntas"},
        "book": "Marcar", "book_online": "Marcar online", "call": "Ligar",
        "menu": "Menu", "close": "Fechar",
        "status_open": "Aberto agora", "status_closes": "fecha às 19:00", "status_closed": "Fechado agora", "status_opens": "abre às 10:00",
        "hero_eyebrow": "Barbearia · Funchal, Madeira",
        "hero_h1_sr": "Pro Style Barbershop — barbearia em Funchal, Madeira",
        "hero_sub": "Barbearia em Funchal",
        "hero_lead": "Degradês ao milímetro, barbas esculpidas e um café à tua espera. Na Avenida da Madalena, de segunda a sábado.",
        "rating_booksy": "322 avaliações no Booksy", "rating_google": "no Google",
        "scroll": "Desce",
        "badge": "PRO STYLE • BARBERSHOP • FUNCHAL • MADEIRA • ",
        "marquee1": ["Degradê", "Barba Pro Style", "Corte à Tesoura", "Platinado", "Pigmentação", "Sobrancelha"],
        "marquee2": ["Funchal", "Madeira", "Av. da Madalena", "Seg–Sáb 10h–19h", "Walk-ins bem-vindos"],
        "exp_kicker": "A experiência",
        "exp_title": "Mais do que <em>um corte.</em>",
        "exp_lead": "Entras para cortar o cabelo e sais com o dia melhor. É assim que os nossos clientes descrevem a Pro Style.",
        "perks": [
            ("coffee", "Café à chegada", "Recebemos-te com um café ou água fresca. Detalhes que fazem a diferença."),
            ("ps5", "PlayStation 5", "À espera da tua vez? Pega no comando e joga uma partida."),
            ("snow", "Ar condicionado", "Espaço fresco e confortável, mesmo nos dias mais quentes da Madeira."),
            ("walk", "Com ou sem marcação", "Marca online em segundos ou aparece — atendemos sempre que houver vaga."),
        ],
        "stats": [("5.0", "Avaliação média no Booksy", "★"), ("322", "Avaliações de clientes", "+"), ("4", "Barbeiros na equipa", ""), ("6", "Dias por semana", "")],
        "svc_kicker": "Serviços & preços",
        "svc_title": "Escolhe o teu <em>estilo.</em>",
        "svc_lead": "Preços transparentes, sem surpresas. Reserva o serviço diretamente no Booksy — demora menos de um minuto.",
        "svc_cats": {"cuts": "Cortes", "beard": "Barba", "combo": "Combos", "color": "Cor", "extras": "Extras"},
        "popular": "Popular", "reserve": "Reservar", "from": "desde",
        "svc_note": "Preços em euros, IVA incluído. Tabela atualizada a partir do Booksy.",
        "team_kicker": "A equipa",
        "team_title": "As mãos por trás <em>do estilo.</em>",
        "team_lead": "Quatro barbeiros, um padrão: precisão, simpatia e atenção a cada detalhe.",
        "role_lead": "Fundador · Master Barber", "role": "Barbeiro",
        "book_with": "Marcar com",
        "story_kicker": "A nossa história",
        "story_title": "Anos de cadeira. <em>Agora, casa própria.</em>",
        "story_p1": "A Pro Style nasceu do sonho de Alvaro Wolf: depois de anos a cortar cabelo na Madeira e a construir uma clientela fiel, abriu o seu próprio espaço na Avenida da Madalena, em Funchal.",
        "story_p2": "Aqui o corte é levado a sério, mas o ambiente é descontraído: boa música, café, PlayStation e uma equipa que te trata pelo nome. De miúdos a graúdos, todos saem daqui com estilo.",
        "story_quote": "O Alvaro é, sem dúvida, o melhor barbeiro da Madeira.",
        "story_quote_by": "Francisco Abreu, cliente há anos",
        "gal_kicker": "Galeria",
        "gal_title": "Entra no <em>espaço.</em>",
        "gal_alts": {
            "interior": "Interior da barbearia Pro Style em Funchal com cadeiras de barbeiro",
            "barber-at-work": "Barbeiro da Pro Style a cortar cabelo em Funchal",
            "logo-wall": "Parede com o logótipo Pro Style Barbershop",
            "sign-night": "Logótipo iluminado da Pro Style Barbershop",
            "storefront": "Fachada da Pro Style Barbershop na Av. da Madalena, Funchal",
            "window": "Montra da barbearia Pro Style, Funchal",
        },
        "gal_caps": {"interior": "O espaço", "barber-at-work": "Mãos à obra", "logo-wall": "A marca", "sign-night": "Pro Style", "storefront": "Av. da Madalena 101", "window": "Funchal"},
        "drag": "Arrasta",
        "rev_kicker": "Avaliações",
        "rev_title": "Não acredites <em>só em nós.</em>",
        "rev_booksy": "Booksy · 322 avaliações", "rev_google": "Google · avaliações",
        "rev_more_google": "Ver no Google", "rev_more_booksy": "Ver no Booksy",
        "rev_src": "Avaliação Google",
        "loc_kicker": "Contactos",
        "loc_title": "Encontra-nos <em>em Funchal.</em>",
        "addr_label": "Morada", "hours_label": "Horário", "phone_label": "Telefone", "book_label": "Marcações",
        "days": ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"],
        "closed": "Encerrado", "today": "Hoje",
        "directions": "Como chegar",
        "map_title": "Mapa: Pro Style Barbershop, Av. da Madalena 101, Funchal",
        "faq_kicker": "Perguntas frequentes",
        "faq_title": "Tudo o que <em>precisas de saber.</em>",
        "faq": [
            ("Preciso de marcação na Pro Style Barbershop?", "Recomendamos marcar online no Booksy para garantires o teu horário, mas clientes sem marcação são bem-vindos sempre que houver disponibilidade."),
            ("Quanto custa um corte de cabelo em Funchal na Pro Style?", "Um corte simples custa 15 €, o corte degradê 17 € e o combo cabelo e barba 24 €. Consulta a tabela completa de preços acima."),
            ("Qual é o horário da barbearia?", "Estamos abertos de segunda a sábado, das 10:00 às 19:00. Ao domingo estamos encerrados."),
            ("Onde fica a Pro Style Barbershop?", "Na Av. da Madalena 101, Fração B, 9020-330 Funchal, Madeira. Toca em “Como chegar” para abrir o percurso no Google Maps."),
            ("Cortam cabelo a crianças?", "Sim. Cortamos cabelo a clientes de todas as idades — muitos pais vêm com os filhos."),
            ("Fazem coloração, madeixas e platinado?", "Sim. Coloração a partir de 35 €, madeixas/luzes 60 € e platinado (nevou) 70 €."),
        ],
        "cta_title": "Pronto para o <em>próximo corte?</em>",
        "cta_lead": "Escolhe o barbeiro, o serviço e a hora. Em menos de um minuto está feito.",
        "footer_tag": "Barbearia em Funchal, Madeira. Degradês, barba e coloração com estilo.",
        "footer_nav": "Navegação", "footer_visit": "Visita-nos", "footer_follow": "Online",
        "rights": "Todos os direitos reservados.",
        "bar_call": "Ligar", "bar_book": "Marcar", "bar_map": "Mapa",
        "loader": "A preparar a cadeira",
        "price_alt": "Preço",
    },
    "en": {
        "html_lang": "en", "og_locale": "en_GB", "path": "/en/", "other": "pt", "other_path": "/", "other_label": "PT",
        "title": "Pro Style Barbershop – Barber Shop in Funchal, Madeira",
        "desc": "Barber shop on Av. da Madalena, Funchal. Fades, beard trims and colour from €15. ★ 5.0 from 322 Booksy reviews. Mon–Sat 10am–7pm. Book online.",
        "skip": "Skip to content",
        "nav": [("#services", "Services"), ("#team", "Team"), ("#gallery", "Gallery"), ("#reviews", "Reviews"), ("#contact", "Contact")],
        "ids": {"services": "services", "team": "team", "gallery": "gallery", "reviews": "reviews", "contact": "contact", "experience": "experience", "faq": "faq"},
        "book": "Book", "book_online": "Book online", "call": "Call",
        "menu": "Menu", "close": "Close",
        "status_open": "Open now", "status_closes": "closes at 7pm", "status_closed": "Closed now", "status_opens": "opens at 10am",
        "hero_eyebrow": "Barber shop · Funchal, Madeira",
        "hero_h1_sr": "Pro Style Barbershop — barber shop in Funchal, Madeira",
        "hero_sub": "Barber shop in Funchal",
        "hero_lead": "Razor-sharp fades, sculpted beards and a coffee waiting for you. On Avenida da Madalena, Monday to Saturday.",
        "rating_booksy": "322 reviews on Booksy", "rating_google": "on Google",
        "scroll": "Scroll",
        "badge": "PRO STYLE • BARBERSHOP • FUNCHAL • MADEIRA • ",
        "marquee1": ["Skin Fade", "Pro Style Beard", "Scissor Cut", "Platinum", "Pigmentation", "Eyebrows"],
        "marquee2": ["Funchal", "Madeira", "Av. da Madalena", "Mon–Sat 10am–7pm", "Walk-ins welcome"],
        "exp_kicker": "The experience",
        "exp_title": "More than <em>a haircut.</em>",
        "exp_lead": "You come in for a cut and leave with a better day. That’s how our clients describe Pro Style.",
        "perks": [
            ("coffee", "Coffee on arrival", "We welcome you with a coffee or a cold water. Small details, big difference."),
            ("ps5", "PlayStation 5", "Waiting for your turn? Grab the controller and play a round."),
            ("snow", "Air-conditioned", "A cool, comfortable space — even on the hottest Madeira days."),
            ("walk", "Walk-ins welcome", "Book online in seconds or just drop by — we’ll fit you in whenever there’s a free chair."),
        ],
        "stats": [("5.0", "Average rating on Booksy", "★"), ("322", "Client reviews", "+"), ("4", "Barbers on the team", ""), ("6", "Days a week", "")],
        "svc_kicker": "Services & prices",
        "svc_title": "Choose your <em>style.</em>",
        "svc_lead": "Clear prices, no surprises. Book your service directly on Booksy — it takes less than a minute.",
        "svc_cats": {"cuts": "Haircuts", "beard": "Beard", "combo": "Combos", "color": "Colour", "extras": "Extras"},
        "popular": "Popular", "reserve": "Book", "from": "from",
        "svc_note": "Prices in euros, VAT included. Price list synced from Booksy.",
        "team_kicker": "The team",
        "team_title": "The hands behind <em>the style.</em>",
        "team_lead": "Four barbers, one standard: precision, good vibes and attention to every detail.",
        "role_lead": "Founder · Master Barber", "role": "Barber",
        "book_with": "Book with",
        "story_kicker": "Our story",
        "story_title": "Years behind the chair. <em>Now, his own place.</em>",
        "story_p1": "Pro Style is Alvaro Wolf’s dream come true: after years of cutting hair in Madeira and building a loyal clientele, he opened his own shop on Avenida da Madalena in Funchal.",
        "story_p2": "The craft is taken seriously, the vibe is relaxed: good music, coffee, PlayStation and a team that knows your name. From kids to grandads, everyone leaves in style.",
        "story_quote": "Alvaro is easily the best barber in Madeira.",
        "story_quote_by": "Francisco Abreu, client for years",
        "gal_kicker": "Gallery",
        "gal_title": "Step <em>inside.</em>",
        "gal_alts": {
            "interior": "Inside Pro Style barber shop in Funchal with barber chairs",
            "barber-at-work": "Pro Style barber cutting hair in Funchal",
            "logo-wall": "Wall with the Pro Style Barbershop logo",
            "sign-night": "Illuminated Pro Style Barbershop logo",
            "storefront": "Pro Style Barbershop storefront on Av. da Madalena, Funchal",
            "window": "Pro Style barber shop window, Funchal",
        },
        "gal_caps": {"interior": "The space", "barber-at-work": "At work", "logo-wall": "The brand", "sign-night": "Pro Style", "storefront": "Av. da Madalena 101", "window": "Funchal"},
        "drag": "Drag",
        "rev_kicker": "Reviews",
        "rev_title": "Don’t just <em>take our word.</em>",
        "rev_booksy": "Booksy · 322 reviews", "rev_google": "Google · reviews",
        "rev_more_google": "See on Google", "rev_more_booksy": "See on Booksy",
        "rev_src": "Google review",
        "loc_kicker": "Contact",
        "loc_title": "Find us <em>in Funchal.</em>",
        "addr_label": "Address", "hours_label": "Opening hours", "phone_label": "Phone", "book_label": "Bookings",
        "days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        "closed": "Closed", "today": "Today",
        "directions": "Get directions",
        "map_title": "Map: Pro Style Barbershop, Av. da Madalena 101, Funchal",
        "faq_kicker": "FAQ",
        "faq_title": "Everything <em>you need to know.</em>",
        "faq": [
            ("Do I need an appointment at Pro Style Barbershop?", "We recommend booking online on Booksy to secure your time, but walk-ins are welcome whenever a chair is free."),
            ("How much is a haircut in Funchal at Pro Style?", "A simple cut is €15, a fade €17 and the hair & beard combo €24. See the full price list above."),
            ("What are the opening hours?", "We’re open Monday to Saturday, 10:00 to 19:00. Closed on Sundays."),
            ("Where is Pro Style Barbershop?", "Av. da Madalena 101, Fração B, 9020-330 Funchal, Madeira, Portugal. Tap “Get directions” to open the route in Google Maps."),
            ("Do you cut kids’ hair?", "Yes. We cut hair for clients of all ages — lots of dads bring their sons along."),
            ("Do you do colouring, highlights and platinum?", "Yes. Colouring from €35, highlights/lowlights €60 and platinum (snow blonde) €70."),
        ],
        "cta_title": "Ready for your <em>next cut?</em>",
        "cta_lead": "Pick your barber, your service and your time. Done in under a minute.",
        "footer_tag": "Barber shop in Funchal, Madeira. Fades, beards and colour — with style.",
        "footer_nav": "Navigate", "footer_visit": "Visit us", "footer_follow": "Online",
        "rights": "All rights reserved.",
        "bar_call": "Call", "bar_book": "Book", "bar_map": "Map",
        "loader": "Getting the chair ready",
        "price_alt": "Price",
    },
}

T["de"] = {
    "html_lang": "de", "og_locale": "de_DE", "path": "/de/",
    "title": "Pro Style Barbershop – Barbershop in Funchal, Madeira",
    "desc": "Barbershop in der Av. da Madalena, Funchal. Fades, Bart und Färben ab 15 €. ★ 5.0 bei 322 Booksy-Bewertungen. Mo–Sa 10–19 Uhr. Online buchen.",
    "skip": "Zum Inhalt springen",
    "nav": [("#leistungen", "Leistungen"), ("#team", "Team"), ("#galerie", "Galerie"), ("#bewertungen", "Bewertungen"), ("#kontakt", "Kontakt")],
    "ids": {"services": "leistungen", "team": "team", "gallery": "galerie", "reviews": "bewertungen", "contact": "kontakt", "experience": "erlebnis", "faq": "faq"},
    "book": "Buchen", "book_online": "Online buchen", "call": "Anrufen",
    "menu": "Menü", "close": "Schließen",
    "status_open": "Jetzt geöffnet", "status_closes": "schließt um 19 Uhr", "status_closed": "Jetzt geschlossen", "status_opens": "öffnet um 10 Uhr",
    "hero_eyebrow": "Barbershop · Funchal, Madeira",
    "hero_h1_sr": "Pro Style Barbershop — Barbershop in Funchal, Madeira",
    "hero_sub": "Barbershop in Funchal",
    "hero_lead": "Millimetergenaue Fades, perfekt geformte Bärte und ein Kaffee, der schon auf dich wartet. In der Avenida da Madalena, Montag bis Samstag.",
    "rating_booksy": "322 Bewertungen auf Booksy", "rating_google": "auf Google",
    "scroll": "Scrollen",
    "badge": "PRO STYLE • BARBERSHOP • FUNCHAL • MADEIRA • ",
    "marquee1": ["Skin Fade", "Pro Style Bart", "Scherenschnitt", "Platinblond", "Pigmentierung", "Augenbrauen"],
    "marquee2": ["Funchal", "Madeira", "Av. da Madalena", "Mo–Sa 10–19 Uhr", "Ohne Termin willkommen"],
    "exp_kicker": "Das Erlebnis",
    "exp_title": "Mehr als <em>ein Haarschnitt.</em>",
    "exp_lead": "Du kommst für einen Schnitt und gehst mit einem besseren Tag. So beschreiben unsere Kunden Pro Style.",
    "perks": [
        ("coffee", "Kaffee zur Begrüßung", "Wir empfangen dich mit einem Kaffee oder kaltem Wasser. Kleine Details, großer Unterschied."),
        ("ps5", "PlayStation 5", "Du wartest auf deinen Termin? Schnapp dir den Controller und spiel eine Runde."),
        ("snow", "Klimatisiert", "Ein kühler, angenehmer Raum – selbst an den heißesten Tagen auf Madeira."),
        ("walk", "Ohne Termin willkommen", "Buche in Sekunden online oder komm einfach vorbei – wir nehmen dich dran, sobald ein Stuhl frei ist."),
    ],
    "stats": [("5.0", "Durchschnittsbewertung auf Booksy", "★"), ("322", "Kundenbewertungen", "+"), ("4", "Barbiere im Team", ""), ("6", "Tage pro Woche", "")],
    "svc_kicker": "Leistungen & Preise",
    "svc_title": "Wähle deinen <em>Style.</em>",
    "svc_lead": "Klare Preise, keine Überraschungen. Buche deine Leistung direkt auf Booksy – das dauert weniger als eine Minute.",
    "svc_cats": {"cuts": "Haarschnitte", "beard": "Bart", "combo": "Kombis", "color": "Farbe", "extras": "Extras"},
    "popular": "Beliebt", "reserve": "Buchen", "from": "ab",
    "svc_note": "Preise in Euro inkl. MwSt. Preisliste von Booksy übernommen.",
    "team_kicker": "Das Team",
    "team_title": "Die Hände hinter <em>dem Style.</em>",
    "team_lead": "Vier Barbiere, ein Anspruch: Präzision, gute Stimmung und Liebe zum Detail.",
    "role_lead": "Gründer · Master Barber", "role": "Barbier",
    "book_with": "Buchen bei",
    "story_kicker": "Unsere Geschichte",
    "story_title": "Jahre am Stuhl. <em>Jetzt der eigene Laden.</em>",
    "story_p1": "Mit Pro Style hat sich Alvaro Wolf seinen Traum erfüllt: Nach Jahren als Barbier auf Madeira und mit einer treuen Stammkundschaft eröffnete er seinen eigenen Shop in der Avenida da Madalena in Funchal.",
    "story_p2": "Das Handwerk wird ernst genommen, die Atmosphäre ist entspannt: gute Musik, Kaffee, PlayStation und ein Team, das dich beim Namen kennt. Vom Kind bis zum Opa – alle gehen mit Style nach Hause.",
    "story_quote": "Alvaro is easily the best barber in Madeira.",
    "story_quote_by": "Francisco Abreu, seit Jahren Kunde",
    "gal_kicker": "Galerie",
    "gal_title": "Tritt <em>ein.</em>",
    "gal_alts": {
        "interior": "Innenraum von Pro Style Barbershop in Funchal mit Barberstühlen",
        "barber-at-work": "Barbier von Pro Style beim Haareschneiden in Funchal",
        "logo-wall": "Wand mit dem Logo von Pro Style Barbershop",
        "sign-night": "Beleuchtetes Logo von Pro Style Barbershop",
        "storefront": "Ladenfront von Pro Style Barbershop in der Av. da Madalena, Funchal",
        "window": "Schaufenster von Pro Style Barbershop, Funchal",
    },
    "gal_caps": {"interior": "Der Laden", "barber-at-work": "Bei der Arbeit", "logo-wall": "Die Marke", "sign-night": "Pro Style", "storefront": "Av. da Madalena 101", "window": "Funchal"},
    "drag": "Ziehen",
    "rev_kicker": "Bewertungen",
    "rev_title": "Glaub nicht <em>nur uns.</em>",
    "rev_booksy": "Booksy · 322 Bewertungen", "rev_google": "Google · Bewertungen",
    "rev_more_google": "Auf Google ansehen", "rev_more_booksy": "Auf Booksy ansehen",
    "rev_src": "Google-Bewertung",
    "loc_kicker": "Kontakt",
    "loc_title": "Finde uns <em>in Funchal.</em>",
    "addr_label": "Adresse", "hours_label": "Öffnungszeiten", "phone_label": "Telefon", "book_label": "Termine",
    "days": ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"],
    "closed": "Geschlossen", "today": "Heute",
    "directions": "Route planen",
    "map_title": "Karte: Pro Style Barbershop, Av. da Madalena 101, Funchal",
    "faq_kicker": "Häufige Fragen",
    "faq_title": "Alles, was du <em>wissen musst.</em>",
    "faq": [
        ("Brauche ich bei Pro Style Barbershop einen Termin?", "Wir empfehlen, online über Booksy zu buchen, um deine Wunschzeit zu sichern. Kunden ohne Termin sind aber willkommen, sobald ein Stuhl frei ist."),
        ("Was kostet ein Haarschnitt in Funchal bei Pro Style?", "Ein einfacher Haarschnitt kostet 15 €, ein Fade 17 € und die Kombi Haare & Bart 24 €. Die vollständige Preisliste findest du oben."),
        ("Wie sind die Öffnungszeiten?", "Wir haben Montag bis Samstag von 10:00 bis 19:00 Uhr geöffnet. Sonntags ist geschlossen."),
        ("Wo befindet sich Pro Style Barbershop?", "Av. da Madalena 101, Fração B, 9020-330 Funchal, Madeira, Portugal. Tippe auf „Route planen“, um den Weg in Google Maps zu öffnen."),
        ("Schneidet ihr auch Kindern die Haare?", "Ja. Wir schneiden Haare für Kunden jeden Alters – viele Väter bringen ihre Söhne gleich mit."),
        ("Bietet ihr Färben, Strähnchen und Platinblond an?", "Ja. Färben ab 35 €, Strähnchen 60 € und Platinblond 70 €."),
    ],
    "cta_title": "Bereit für deinen <em>nächsten Schnitt?</em>",
    "cta_lead": "Wähle Barbier, Leistung und Uhrzeit. In unter einer Minute erledigt.",
    "footer_tag": "Barbershop in Funchal, Madeira. Fades, Bärte und Farbe – mit Style.",
    "footer_nav": "Navigation", "footer_visit": "Besuch uns", "footer_follow": "Online",
    "rights": "Alle Rechte vorbehalten.",
    "bar_call": "Anrufen", "bar_book": "Buchen", "bar_map": "Karte",
    "loader": "Der Stuhl wird vorbereitet",
    "price_alt": "Preis",
}

HERO_ALT = {"pt": "Equipa da Pro Style Barbershop em Funchal", "en": "The Pro Style Barbershop team in Funchal", "de": "Das Team von Pro Style Barbershop in Funchal"}
LANG_NAMES = {"pt": "Português", "en": "English", "de": "Deutsch"}


def lang_href(cur, target):
    """відносне посилання з однієї мовної версії на іншу"""
    path = {l: p for l, p, _ in LANGS}[target].lstrip("/")
    return rel(cur, path) or "./"


ICONS = {
    "coffee": '<path d="M5 10h12v4a6 6 0 0 1-6 6h0a6 6 0 0 1-6-6v-4Z"/><path d="M17 11h1.5a2.5 2.5 0 0 1 0 5H17"/><path d="M8 3c0 1.5 1 1.5 1 3M12 3c0 1.5 1 1.5 1 3"/>',
    "ps5": '<path d="M6.5 8h11a4 4 0 0 1 3.9 4.8l-.8 4a2.4 2.4 0 0 1-4.2 1L15 16H9l-1.4 1.8a2.4 2.4 0 0 1-4.2-1l-.8-4A4 4 0 0 1 6.5 8Z"/><path d="M8 11v3M6.5 12.5h3"/><circle cx="16" cy="11.5" r=".6"/><circle cx="17.5" cy="13.5" r=".6"/>',
    "snow": '<path d="M12 2v20M4.9 6.5l14.2 11M4.9 17.5l14.2-11"/><path d="m9 3.5 3 2 3-2M9 20.5l3-2 3 2"/>',
    "walk": '<rect x="3.5" y="4.5" width="17" height="16" rx="2.5"/><path d="M3.5 9.5h17M8 2.5v4M16 2.5v4"/><path d="m9 15 2 2 4-4"/>',
    "phone": '<path d="M5 3.5h3.2l1.6 4-2 1.3a10 10 0 0 0 4.4 4.4l1.3-2 4 1.6V16a2 2 0 0 1-2 2A13.5 13.5 0 0 1 3 5.5a2 2 0 0 1 2-2Z"/>',
    "pin": '<path d="M12 21s-6.5-6-6.5-11a6.5 6.5 0 0 1 13 0c0 5-6.5 11-6.5 11Z"/><circle cx="12" cy="10" r="2.3"/>',
    "clock": '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>',
    "cal": '<rect x="3.5" y="4.5" width="17" height="16" rx="2.5"/><path d="M3.5 9.5h17M8 2.5v4M16 2.5v4"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "star": '<path d="m12 3 2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1L3.2 9.5l6.1-.9L12 3Z"/>',
}


def icon(name, cls="ico"):
    return f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>'


STAR_FILL = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="m12 3 2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1L3.2 9.5l6.1-.9L12 3Z"/></svg>'
STARS5 = '<span class="stars" aria-hidden="true">' + STAR_FILL * 5 + "</span>"

CROWN = '<svg class="crown" viewBox="0 0 64 44" aria-hidden="true"><path class="crown-path" d="M4 14l12 10L32 4l16 20 12-10-5 22H9L4 14Z" fill="none" stroke="currentColor" stroke-width="3" stroke-linejoin="round"/><path class="crown-base" d="M9 39h46" stroke="currentColor" stroke-width="3.4" stroke-linecap="round"/></svg>'


def wordmark(extra=""):
    return f'<span class="wordmark {extra}">{CROWN}<span class="wm-text"><span class="wm-pro">PRO STYLE</span><span class="wm-script">Barbershop</span></span></span>'


def rel(lang, path):
    """шлях до assets відносно сторінки"""
    return ("" if lang == "pt" else "../") + path


def schema(lang, t):
    url = BASE + t["path"]
    offers = []
    for cat, items in SERVICES:
        for pt, en, price, dur, _ in items:
            offers.append({
                "@type": "Offer",
                "price": f"{price:.2f}",
                "priceCurrency": "EUR",
                "itemOffered": {"@type": "Service", "name": svc_name(lang, pt, en)},
            })
    biz = {
        "@context": "https://schema.org",
        "@type": "BarberShop",
        "@id": BASE + "/#barbershop",
        "name": "Pro Style Barbershop",
        "alternateName": "Pro Style Barber Shop",
        "description": t["desc"],
        "url": url,
        "logo": BASE + "/icon-512.png",
        "image": [BASE + "/assets/img/og-image.jpg", BASE + "/assets/img/hero-team.webp", BASE + "/assets/img/interior.webp"],
        "telephone": PHONE_INTL,
        "priceRange": "€€",
        "currenciesAccepted": "EUR",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": STREET,
            "addressLocality": CITY,
            "addressRegion": REGION,
            "postalCode": POSTAL,
            "addressCountry": "PT",
        },
        "geo": {"@type": "GeoCoordinates", "latitude": LAT, "longitude": LNG},
        "hasMap": MAPS_CID,
        "areaServed": [{"@type": "City", "name": "Funchal"}, {"@type": "AdministrativeArea", "name": "Madeira"}],
        "openingHoursSpecification": [{
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
            "opens": "10:00", "closes": "19:00",
        }],
        "founder": {"@type": "Person", "name": "Alvaro Wolf"},
        "employee": [{"@type": "Person", "name": m["name"], "jobTitle": "Barber"} for m in TEAM],
        "sameAs": [BOOKSY, MAPS_CID],
        "potentialAction": {"@type": "ReserveAction", "target": BOOKSY, "name": t["book_online"]},
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": t["svc_kicker"], "itemListElement": offers},
        "amenityFeature": [
            {"@type": "LocationFeatureSpecification", "name": n, "value": True}
            for n in (["Air conditioning", "Free coffee", "PlayStation 5", "Walk-ins welcome"])
        ],
    }
    faq = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in t["faq"]],
    }
    site = {"@context": "https://schema.org", "@type": "WebSite", "name": "Pro Style Barbershop", "url": BASE + "/", "inLanguage": t["html_lang"]}
    return "\n".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in (biz, faq, site))


def render(lang):
    t = T[lang]
    a = lambda p: rel(lang, p)
    ids = t["ids"]
    url = BASE + t["path"]

    nav_links = "".join(f'<li><a href="{h}" data-cursor="hover">{escape(l)}</a></li>' for h, l in t["nav"])

    def marquee(words, cls):
        chunk = "".join(f'<span>{escape(w)}</span><i aria-hidden="true">✦</i>' for w in words)
        return f'<div class="marquee {cls}" aria-hidden="true"><div class="marquee-track">{chunk * 4}</div></div>'

    perks = "".join(
        f'''<article class="perk reveal-up">
              <span class="perk-num">0{i+1}</span>
              <div class="perk-ico">{icon(k)}</div>
              <h3>{escape(h)}</h3>
              <p>{escape(p)}</p>
            </article>''' for i, (k, h, p) in enumerate(t["perks"]))

    stats = "".join(
        f'''<div class="stat reveal-up"><div class="stat-num"><span class="count" data-to="{n}">{n}</span><sup>{s}</sup></div><p>{escape(l)}</p></div>'''
        for n, l, s in t["stats"])

    tabs, panels = [], []
    for i, (cat, items) in enumerate(SERVICES):
        sel = "true" if i == 0 else "false"
        tabs.append(f'<button class="svc-tab" role="tab" id="tab-{cat}" aria-controls="panel-{cat}" aria-selected="{sel}" data-cursor="hover">{escape(t["svc_cats"][cat])}<span class="svc-count">{len(items):02d}</span></button>')
        rows = []
        for pt, en, price, dur, pop in items:
            name = svc_name(lang, pt, en)
            sub = en if lang == "pt" else pt
            badge = f'<span class="pop">{escape(t["popular"])}</span>' if pop else ""
            rows.append(f'''<li class="svc-row">
                <a href="{BOOKSY}" target="_blank" rel="noopener" data-cursor="book">
                  <span class="svc-name"><strong>{escape(name)}</strong>{badge}<small>{escape(sub)} · {dur}</small></span>
                  <span class="svc-dots" aria-hidden="true"></span>
                  <span class="svc-price">{price}<em>€</em></span>
                  <span class="svc-go" aria-hidden="true">{escape(t["reserve"])} {icon("arrow")}</span>
                </a></li>''')
        hidden = "" if i == 0 else " hidden"
        panels.append(f'<ul class="svc-panel" role="tabpanel" id="panel-{cat}" aria-labelledby="tab-{cat}"{hidden}>{"".join(rows)}</ul>')

    team = "".join(
        f'''<article class="member" data-tilt>
              <div class="member-img">
                <img src="{a(f"assets/img/team-{m['id']}.webp")}" alt="{escape(m['name'])} — {escape(t['role_lead'] if m.get('lead') else t['role'])}, Pro Style Barbershop Funchal" width="544" height="544" loading="lazy" decoding="async">
                <span class="member-idx">0{i+1}</span>
              </div>
              <div class="member-info">
                <h3>{escape(m['name'])}</h3>
                <p>{escape(t['role_lead'] if m.get('lead') else t['role'])}</p>
                <a class="member-book" href="{BOOKSY}" target="_blank" rel="noopener" data-cursor="book">{escape(t['book_with'])} {escape(m['name'].split()[0])} {icon("arrow")}</a>
              </div>
            </article>''' for i, m in enumerate(TEAM))

    gallery = "".join(
        f'''<figure class="g-item g-{shape}">
              <div class="g-img"><img src="{a(f"assets/img/{n}.webp")}" alt="{escape(t['gal_alts'][n])}" width="{w}" height="{h}" loading="lazy" decoding="async"></div>
              <figcaption><span>0{i+1}</span>{escape(t['gal_caps'][n])}</figcaption>
            </figure>''' for i, (n, w, h, shape) in enumerate(GALLERY))

    def rv(r, k):
        v = r[k]
        return v.get(lang, v['en']) if isinstance(v, dict) else v

    reviews = "".join(
        f'''<article class="review">
              <div class="review-top">{STARS5}<span class="review-lang">{escape(rv(r, 'lang'))}</span></div>
              <blockquote><p>{escape(rv(r, 'text'))}</p></blockquote>
              <footer><span class="avatar" aria-hidden="true">{escape(r['name'][0])}</span><span><strong>{escape(r['name'])}</strong><small>{escape(t['rev_src'])} · {escape(rv(r, 'when'))}</small></span></footer>
            </article>''' for r in REVIEWS)

    hours = "".join(
        f'<li data-day="{(i + 1) % 7}"><span>{escape(d)}</span><span>{"10:00 – 19:00" if i < 6 else escape(t["closed"])}</span></li>'
        for i, d in enumerate(t["days"]))

    faq = "".join(
        f'''<details class="faq-item reveal-up">
              <summary data-cursor="hover"><span>{escape(q)}</span><i aria-hidden="true"></i></summary>
              <div class="faq-a"><p>{escape(ans)}</p></div>
            </details>''' for q, ans in t["faq"])

    footer_nav = "".join(f'<li><a href="{h}">{escape(l)}</a></li>' for h, l in t["nav"])

    hreflangs = "\n".join(f'<link rel="alternate" hreflang="{hl}" href="{BASE}{pth}">' for _, pth, hl in LANGS)
    lang_switch = '<span class="lang-sep">/</span>'.join(
        f'<span class="lang-cur" aria-current="true">{l.upper()}</span>' if l == lang else
        f'<a href="{lang_href(lang, l)}" hreflang="{l}" lang="{l}" title="{LANG_NAMES[l]}" data-cursor="hover">{l.upper()}</a>'
        for l, _, _ in LANGS)
    footer_langs = "".join(f'<li><a href="{lang_href(lang, l)}" hreflang="{l}" lang="{l}">{LANG_NAMES[l]}</a></li>' for l, _, _ in LANGS if l != lang)
    robots = "noindex, nofollow" if DEMO else "index, follow, max-image-preview:large"
    return f'''<!doctype html>
<html lang="{t['html_lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{escape(t['title'])}</title>
<meta name="description" content="{escape(t['desc'])}">
<link rel="canonical" href="{url}">
{hreflangs}
<link rel="alternate" hreflang="x-default" href="{BASE}/">
<meta name="robots" content="{robots}">
<meta name="theme-color" content="#0d0d0b">
<meta name="geo.region" content="PT-30">
<meta name="geo.placename" content="Funchal, Madeira">
<meta name="geo.position" content="{LAT};{LNG}">
<meta name="ICBM" content="{LAT}, {LNG}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Pro Style Barbershop">
<meta property="og:locale" content="{t['og_locale']}">
<meta property="og:title" content="{escape(t['title'])}">
<meta property="og:description" content="{escape(t['desc'])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}/assets/img/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="629">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" sizes="32x32" href="{a('favicon-32.png')}">
<link rel="apple-touch-icon" href="{a('apple-touch-icon.png')}">
<link rel="manifest" href="{a('site.webmanifest')}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@500;700;800;900&family=Instrument+Serif:ital@0;1&family=Manrope:wght@400;500;600;700&family=Yellowtail&display=swap">
<link rel="preload" as="image" href="{a('assets/img/hero-team.webp')}" imagesrcset="{a('assets/img/hero-team-sm.webp')} 640w, {a('assets/img/hero-team.webp')} 1100w" imagesizes="(max-width: 900px) 100vw, 45vw">
<link rel="stylesheet" href="{a('assets/css/style.css')}">
<script>document.documentElement.classList.add('js');</script>
{schema(lang, t)}
</head>
<body data-lang="{lang}">
<a class="skip" href="#main">{escape(t['skip'])}</a>

<div class="loader" aria-hidden="true">
  <div class="loader-inner">
    {CROWN}
    <div class="loader-word"><span>P</span><span>R</span><span>O</span><span>&nbsp;</span><span>S</span><span>T</span><span>Y</span><span>L</span><span>E</span></div>
    <div class="loader-bar"><i></i></div>
    <p class="loader-sub">{escape(t['loader'])}</p>
  </div>
</div>

<div class="cursor" aria-hidden="true"><div class="cursor-dot"></div><div class="cursor-ring"><span class="cursor-label"></span></div></div>
<div class="grain" aria-hidden="true"></div>

<header class="header">
  <div class="header-in">
    <a class="brand" href="{a('') or './'}" aria-label="Pro Style Barbershop — {escape(t['hero_sub'])}" data-cursor="hover">{wordmark()}</a>
    <nav class="nav" aria-label="Menu">
      <ul>{nav_links}</ul>
    </nav>
    <div class="header-actions">
      <div class="lang" role="group" aria-label="Language">{lang_switch}</div>
      <a class="btn btn-gold btn-sm magnetic" href="{BOOKSY}" target="_blank" rel="noopener" data-cursor="book"><span>{escape(t['book'])}</span></a>
      <button class="burger" aria-expanded="false" aria-controls="mnav" aria-label="{escape(t['menu'])}"><i></i><i></i></button>
    </div>
  </div>
</header>

<div class="mnav" id="mnav" hidden>
  <ul>{''.join(f'<li><a href="{h}"><span>0{i+1}</span>{escape(l)}</a></li>' for i, (h, l) in enumerate(t['nav']))}</ul>
  <div class="mnav-foot">
    <a href="tel:{PHONE_INTL}">{icon('phone')} {PHONE_DISPLAY}</a>
    <a href="{MAPS_DIR}" target="_blank" rel="noopener">{icon('pin')} Av. da Madalena 101, Funchal</a>
  </div>
</div>

<main id="main">

<section class="hero" aria-labelledby="hero-title">
  <div class="hero-bg" aria-hidden="true"><div class="hero-glow"></div><div class="hero-lines"></div></div>
  <div class="container hero-grid">
    <div class="hero-copy">
      <p class="eyebrow hero-in"><span class="status" data-status><i></i><b data-open="{escape(t['status_open'])}" data-closed="{escape(t['status_closed'])}">{escape(t['status_open'])}</b><span class="status-sub" data-open="{escape(t['status_closes'])}" data-closed="{escape(t['status_opens'])}">{escape(t['status_closes'])}</span></span><span class="eyebrow-txt">{escape(t['hero_eyebrow'])}</span></p>
      <h1 id="hero-title" class="hero-title">
        <span class="sr-only">{escape(t['hero_h1_sr'])}</span>
        <span class="ht-line" aria-hidden="true"><span class="ht-word">PRO</span></span>
        <span class="ht-line" aria-hidden="true"><span class="ht-word ht-outline">STYLE</span></span>
        <span class="ht-script" aria-hidden="true">Barbershop</span>
      </h1>
      <p class="hero-lead hero-in">{escape(t['hero_lead'])}</p>
      <div class="hero-ctas hero-in">
        <a class="btn btn-gold magnetic" href="{BOOKSY}" target="_blank" rel="noopener" data-cursor="book"><span>{escape(t['book_online'])}</span>{icon('arrow')}</a>
        <a class="btn btn-ghost magnetic" href="tel:{PHONE_INTL}" data-cursor="hover">{icon('phone')}<span>{PHONE_DISPLAY}</span></a>
      </div>
      <div class="hero-ratings hero-in">
        <a href="{BOOKSY}" target="_blank" rel="noopener" class="rating" data-cursor="hover"><strong>5.0</strong>{STARS5}<small>{escape(t['rating_booksy'])}</small></a>
        <span class="rating-sep" aria-hidden="true"></span>
        <a href="{MAPS_PLACE}" target="_blank" rel="noopener" class="rating" data-cursor="hover"><strong>4.8</strong>{STARS5}<small>{escape(t['rating_google'])}</small></a>
      </div>
    </div>
    <div class="hero-media">
      <div class="hero-frame">
        <img src="{a('assets/img/hero-team.webp')}" srcset="{a('assets/img/hero-team-sm.webp')} 640w, {a('assets/img/hero-team.webp')} 1100w" sizes="(max-width: 900px) 100vw, 45vw" alt="{escape(HERO_ALT[lang])}" width="1100" height="1650" fetchpriority="high">
      </div>
      <div class="badge" aria-hidden="true">
        <svg viewBox="0 0 200 200"><defs><path id="circ-{lang}" d="M100,100 m-78,0 a78,78 0 1,1 156,0 a78,78 0 1,1 -156,0"/></defs><text><textPath href="#circ-{lang}">{escape(t['badge'])}</textPath></text></svg>
        {CROWN}
      </div>
      <p class="hero-loc"><span>32.6607° N</span><span>16.9308° W</span></p>
    </div>
  </div>
  <a class="scroll-cue" href="#{ids['experience']}" data-cursor="hover"><span>{escape(t['scroll'])}</span><i></i></a>
</section>

<section class="ticker" aria-hidden="true">
  {marquee(t['marquee1'], 'mq-a')}
  {marquee(t['marquee2'], 'mq-b')}
</section>

<section class="section experience" id="{ids['experience']}">
  <div class="container">
    <div class="sec-head sec-head-row">
      <div>
        <p class="kicker">{escape(t['exp_kicker'])}</p>
        <h2 class="sec-title split">{t['exp_title']}</h2>
      </div>
      <p class="sec-lead reveal-up">{escape(t['exp_lead'])}</p>
    </div>
    <div class="perks">{perks}</div>
    <div class="stats">{stats}</div>
  </div>
</section>

<section class="section services" id="{ids['services']}">
  <div class="container svc-grid">
    <div class="svc-side">
      <p class="kicker">{escape(t['svc_kicker'])}</p>
      <h2 class="sec-title split">{t['svc_title']}</h2>
      <p class="sec-lead reveal-up">{escape(t['svc_lead'])}</p>
      <a class="btn btn-gold magnetic reveal-up" href="{BOOKSY}" target="_blank" rel="noopener" data-cursor="book"><span>{escape(t['book_online'])}</span>{icon('arrow')}</a>
      <div class="svc-photo reveal-clip"><img src="{a('assets/img/barber-at-work.webp')}" alt="{escape(t['gal_alts']['barber-at-work'])}" width="900" height="1125" loading="lazy" decoding="async"></div>
    </div>
    <div class="svc-main">
      <div class="svc-tabs" role="tablist" aria-label="{escape(t['svc_kicker'])}">{''.join(tabs)}<span class="svc-ind" aria-hidden="true"></span></div>
      <div class="svc-panels">{''.join(panels)}</div>
      <p class="svc-note">{escape(t['svc_note'])}</p>
    </div>
  </div>
</section>

<section class="section team" id="{ids['team']}">
  <div class="container">
    <div class="sec-head sec-head-row">
      <div>
        <p class="kicker">{escape(t['team_kicker'])}</p>
        <h2 class="sec-title split">{t['team_title']}</h2>
      </div>
      <p class="sec-lead reveal-up">{escape(t['team_lead'])}</p>
    </div>
    <div class="team-grid">{team}</div>
  </div>
</section>

<section class="section story">
  <div class="container story-grid">
    <div class="story-media">
      <div class="story-img reveal-clip"><img src="{a('assets/img/sign-night.webp')}" alt="{escape(t['gal_alts']['sign-night'])}" width="1024" height="682" loading="lazy" decoding="async"></div>
      <div class="story-logo reveal-clip"><img src="{a('assets/img/logo-3d.webp')}" alt="Pro Style Barbershop logo" width="600" height="600" loading="lazy" decoding="async"></div>
    </div>
    <div class="story-copy">
      <p class="kicker">{escape(t['story_kicker'])}</p>
      <h2 class="sec-title split">{t['story_title']}</h2>
      <p class="reveal-up">{escape(t['story_p1'])}</p>
      <p class="reveal-up">{escape(t['story_p2'])}</p>
      <figure class="story-quote reveal-up">
        <blockquote><p>“{escape(t['story_quote'])}”</p></blockquote>
        <figcaption>— {escape(t['story_quote_by'])}</figcaption>
      </figure>
    </div>
  </div>
</section>

<section class="section gallery" id="{ids['gallery']}">
  <div class="gallery-pin">
    <div class="container gal-head">
      <div>
        <p class="kicker">{escape(t['gal_kicker'])}</p>
        <h2 class="sec-title split">{t['gal_title']}</h2>
      </div>
      <p class="gal-hint" aria-hidden="true"><span>{escape(t['drag'])}</span><i></i></p>
    </div>
    <div class="gal-track" data-cursor="drag" data-cursor-label="{escape(t['drag'])}">{gallery}</div>
  </div>
</section>

<section class="section reviews" id="{ids['reviews']}">
  <div class="container">
    <div class="sec-head sec-head-row">
      <div>
        <p class="kicker">{escape(t['rev_kicker'])}</p>
        <h2 class="sec-title split">{t['rev_title']}</h2>
      </div>
      <div class="rev-scores reveal-up">
        <a href="{BOOKSY}" target="_blank" rel="noopener" class="score" data-cursor="hover"><strong>5.0</strong><span>{STARS5}<small>{escape(t['rev_booksy'])}</small></span></a>
        <a href="{MAPS_PLACE}" target="_blank" rel="noopener" class="score" data-cursor="hover"><strong>4.8</strong><span>{STARS5}<small>{escape(t['rev_google'])}</small></span></a>
      </div>
    </div>
  </div>
  <div class="rev-marquee" data-cursor="drag" data-cursor-label="{escape(t['drag'])}">
    <div class="rev-track">{reviews}</div>
  </div>
  <div class="container rev-links">
    <a class="link-arrow" href="{MAPS_PLACE}" target="_blank" rel="noopener" data-cursor="hover">{escape(t['rev_more_google'])} {icon('arrow')}</a>
    <a class="link-arrow" href="{BOOKSY}" target="_blank" rel="noopener" data-cursor="hover">{escape(t['rev_more_booksy'])} {icon('arrow')}</a>
  </div>
</section>

<section class="section location" id="{ids['contact']}">
  <div class="container">
    <div class="sec-head">
      <p class="kicker">{escape(t['loc_kicker'])}</p>
      <h2 class="sec-title split">{t['loc_title']}</h2>
    </div>
    <div class="loc-grid">
      <div class="loc-info" itemscope itemtype="https://schema.org/BarberShop">
        <meta itemprop="name" content="Pro Style Barbershop">
        <div class="loc-block reveal-up">
          <h3>{icon('pin')}{escape(t['addr_label'])}</h3>
          <address itemprop="address" itemscope itemtype="https://schema.org/PostalAddress">
            <span itemprop="streetAddress">{STREET}</span><br>
            <span itemprop="postalCode">{POSTAL}</span> <span itemprop="addressLocality">{CITY}</span>, <span itemprop="addressRegion">{REGION}</span>, Portugal
          </address>
          <a class="link-arrow" href="{MAPS_DIR}" target="_blank" rel="noopener" data-cursor="hover">{escape(t['directions'])} {icon('arrow')}</a>
        </div>
        <div class="loc-block reveal-up">
          <h3>{icon('clock')}{escape(t['hours_label'])}</h3>
          <ul class="hours" data-today-label="{escape(t['today'])}">{hours}</ul>
        </div>
        <div class="loc-row reveal-up">
          <div class="loc-block">
            <h3>{icon('phone')}{escape(t['phone_label'])}</h3>
            <a class="big-link" href="tel:{PHONE_INTL}" itemprop="telephone" content="{PHONE_INTL}" data-cursor="hover">{PHONE_DISPLAY}</a>
          </div>
          <div class="loc-block">
            <h3>{icon('cal')}{escape(t['book_label'])}</h3>
            <a class="big-link" href="{BOOKSY}" target="_blank" rel="noopener" data-cursor="book">Booksy ↗</a>
          </div>
        </div>
      </div>
      <div class="loc-map reveal-clip">
        <iframe title="{escape(t['map_title'])}" src="{MAPS_EMBED}{MAP_HL[lang]}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
        <a class="map-pin-card" href="{MAPS_DIR}" target="_blank" rel="noopener" data-cursor="hover">
          <span class="map-pin-ico">{CROWN}</span>
          <span><strong>Pro Style Barbershop</strong><small>Av. da Madalena 101 · Funchal</small></span>
          {icon('arrow')}
        </a>
      </div>
    </div>
  </div>
</section>

<section class="section faq" id="{ids['faq']}">
  <div class="container faq-grid">
    <div>
      <p class="kicker">{escape(t['faq_kicker'])}</p>
      <h2 class="sec-title split">{t['faq_title']}</h2>
    </div>
    <div class="faq-list">{faq}</div>
  </div>
</section>

<section class="cta">
  <div class="cta-bg" aria-hidden="true"><img src="{a('assets/img/interior.webp')}" alt="" width="1400" height="874" loading="lazy" decoding="async"></div>
  <div class="container cta-in">
    {CROWN}
    <h2 class="cta-title split">{t['cta_title']}</h2>
    <p class="reveal-up">{escape(t['cta_lead'])}</p>
    <div class="hero-ctas reveal-up">
      <a class="btn btn-gold btn-lg magnetic" href="{BOOKSY}" target="_blank" rel="noopener" data-cursor="book"><span>{escape(t['book_online'])}</span>{icon('arrow')}</a>
      <a class="btn btn-ghost btn-lg magnetic" href="tel:{PHONE_INTL}" data-cursor="hover">{icon('phone')}<span>{escape(t['call'])}</span></a>
    </div>
  </div>
</section>

</main>

<footer class="footer">
  <div class="container">
    <div class="footer-big" aria-hidden="true">PRO STYLE</div>
    <div class="footer-grid">
      <div class="footer-brand">
        {wordmark('wm-lg')}
        <p>{escape(t['footer_tag'])}</p>
      </div>
      <div>
        <h4>{escape(t['footer_nav'])}</h4>
        <ul>{footer_nav}</ul>
      </div>
      <div>
        <h4>{escape(t['footer_visit'])}</h4>
        <p>{STREET}<br>{POSTAL} {CITY}, {REGION}</p>
        <p>{escape(t['days'][0][:3])}–{escape(t['days'][5][:3])} · 10:00–19:00</p>
        <p><a href="tel:{PHONE_INTL}">{PHONE_DISPLAY}</a></p>
      </div>
      <div>
        <h4>{escape(t['footer_follow'])}</h4>
        <ul>
          <li><a href="{BOOKSY}" target="_blank" rel="noopener">Booksy</a></li>
          <li><a href="{MAPS_PLACE}" target="_blank" rel="noopener">Google Maps</a></li>
          {footer_langs}
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <p>© {YEAR} Pro Style Barbershop · {escape(t['hero_sub'])}. {escape(t['rights'])}</p>
      <a href="#main" class="to-top" data-cursor="hover">↑ Top</a>
    </div>
  </div>
</footer>

<nav class="mbar" aria-label="{escape(t['book'])}">
  <a href="tel:{PHONE_INTL}">{icon('phone')}<span>{escape(t['bar_call'])}</span></a>
  <a class="mbar-main" href="{BOOKSY}" target="_blank" rel="noopener">{icon('cal')}<span>{escape(t['bar_book'])}</span></a>
  <a href="{MAPS_DIR}" target="_blank" rel="noopener">{icon('pin')}<span>{escape(t['bar_map'])}</span></a>
</nav>

<script src="{a('assets/vendor/gsap.min.js')}" defer></script>
<script src="{a('assets/vendor/ScrollTrigger.min.js')}" defer></script>
<script src="{a('assets/vendor/lenis.min.js')}" defer></script>
<script src="{a('assets/js/main.js')}" defer></script>
</body>
</html>
'''


def main():
    site = Path("site")
    for lang, path, _ in LANGS:
        out = site / path.strip("/") / "index.html" if path != "/" else site / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render(lang), encoding="utf-8")

    alt = "\n".join(f'    <xhtml:link rel="alternate" hreflang="{hl}" href="{BASE}{pth}"/>' for _, pth, hl in LANGS)
    alt += f'\n    <xhtml:link rel="alternate" hreflang="x-default" href="{BASE}/"/>'
    urls = "".join(
        f"  <url>\n    <loc>{BASE}{pth}</loc>\n{alt}\n    <changefreq>monthly</changefreq><priority>{'1.0' if pth == '/' else '0.8'}</priority>\n  </url>\n"
        for _, pth, _ in LANGS)
    (site / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        f"{urls}</urlset>\n", encoding="utf-8")
    (site / "robots.txt").write_text("User-agent: *\nDisallow: /\n" if DEMO else f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n", encoding="utf-8")
    (site / "site.webmanifest").write_text(json.dumps({
        "name": "Pro Style Barbershop", "short_name": "Pro Style",
        "icons": [{"src": "apple-touch-icon.png", "sizes": "180x180", "type": "image/png"},
                  {"src": "icon-512.png", "sizes": "512x512", "type": "image/png"}],
        "theme_color": "#0d0d0b", "background_color": "#0d0d0b", "display": "standalone", "start_url": "./",
    }, indent=2), encoding="utf-8")
    print("OK: PT / EN / DE, sitemap.xml, robots.txt" + ("  [DEMO: noindex]" if DEMO else ""))


if __name__ == "__main__":
    main()
