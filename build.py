# -*- coding: utf-8 -*-
"""Generates the English (/) and Polish (/pl/) versions of hirokifilmuje.
   Run:  python3 build.py"""
import os, html, json

ROOT = os.path.dirname(os.path.abspath(__file__))
BRAND = "Hiroki Filmuje"
EMAIL = "sebasuta@gmail.com"
PHONE_DISPLAY = "+48 516 849 121"
PHONE_RAW = "+48516849121"
INSTAGRAM = "https://www.instagram.com/hiroki_filmuje/"
IG_HANDLE = "@hiroki_filmuje"

PAGES = ["index", "work", "about", "offer", "contact"]

NAV = {
    "en": {"index": "Home", "work": "Work", "about": "About me", "offer": "Offer", "contact": "Contact"},
    "pl": {"index": "Start", "work": "Portfolio", "about": "O mnie", "offer": "Oferta", "contact": "Kontakt"},
}
TAG = {"en": "Wedding films &amp; photography", "pl": "Filmy i fotografia ślubna"}

# ---------------------------------------------------------------- photographs
# (file-stem, couple, orientation)
COUPLES = {
    "da": "Dominika &amp; Artur", "ja": "Julia &amp; Artsiom", "jd": "Julia &amp; Dominik",
    "nm": "Nadia &amp; Miguel", "na": "Nastyja &amp; Anton", "uc": "",
}
GALLERY_BY_COUPLE = {
    "da": ["da-29","da-31","da-9","da-12","da-20","da-26","da-3","da-32","da-34","da-39","da-42","da-23","da-11"],
    "ja": ["ja-40","ja-29","ja-4","ja-59","ja-31","ja-35","ja-44","ja-46","ja-49","ja-51","ja-55","ja-62","ja-69","ja-70","ja-10","ja-12","ja-15","ja-2"],
    "jd": ["jd-14","jd-13","jd-25","jd-20","jd-23","jd-3","jd-9","jd-10","jd-11","jd-17"],
    "nm": ["nm-11","nm-19","nm-28","nm-30","nm-13","nm-15","nm-20","nm-25","nm-33","nm-37","nm-39","nm-42","nm-44"],
    "na": ["na-10","na-3","na-8"],
    "uc": ["uc-4","uc-5","uc-7"],
}

def interleave(groups):
    """Round-robin so two frames from the same wedding never sit side by side."""
    out, keys, idx = [], list(groups.keys()), {k: 0 for k in groups}
    while True:
        placed = False
        for k in keys:
            if idx[k] < len(groups[k]):
                out.append((groups[k][idx[k]], k)); idx[k] += 1; placed = True
        if not placed:
            return out

GALLERY = interleave(GALLERY_BY_COUPLE)

HERO = ["da-29", "ja-40", "na-10", "nm-11"]           # four different weddings
STRIP = [("da-9","da"),("ja-29","ja"),("jd-14","jd"),("nm-28","nm"),("na-8","na"),("da-34","da")]

def alt(stem, lang):
    c = COUPLES.get(stem.split("-")[0], "")
    if lang == "pl":
        return ("Kadr ze ślubu — " + c) if c else "Kadr ze ślubu"
    return ("Wedding photograph — " + c) if c else "Wedding photograph"

# ---------------------------------------------------------------- testimonials
QUOTES = [
    {"who": "Barbara &amp; Michał",
     "pl": "Omg, to jest niesamowiteeee! Płakaliśmy, oglądając to. Piękny film. Zatwierdzone!!! Naprawdę wykonałeś najlepszą robotę.",
     "en": "Omg, this is amazing! We cried watching it. A beautiful film. Approved!!! You really did the best job."},
    {"who": "Monika &amp; Julien",
     "pl": "Dzięki, stary! Film wyszedł świetnie! Ma w sobie wszystko – urocze momenty, romantyzm i powagę! To była prawdziwa przyjemność pracować z Tobą.",
     "en": "Thanks, man! The film turned out great! It has it all — the sweet moments, the romance and the weight of the day. It was a real pleasure working with you."},
    {"who": "Julia &amp; Dominik",
     "pl": "Super współpraca, profesjonalizm i pozytywna atmosfera. Zdjęcia i filmy wyszły ekstra.",
     "en": "Great to work with, professional, and a good atmosphere all day. The photos and films came out brilliant."},
]

# ---------------------------------------------------------------- packages
PACKS = [
  {"n": "1", "price": "3 000 zł", "featured": False,
   "pl": {"name": "Klasyczny", "len": "Film 3–5 minut", "tag": "",
          "desc": "Kinowy highlight z całego dnia: montaż, color grading i jedna piosenka według Państwa wyboru."},
   "en": {"name": "Classic", "len": "Film 3–5 minutes", "tag": "",
          "desc": "A cinematic highlight of the whole day: edit, colour grading and one song of your choice."}},
  {"n": "2", "price": "3 500 zł", "featured": True,
   "pl": {"name": "Rozszerzony", "len": "Film 10–15 minut", "tag": "Najpopularniejszy",
          "desc": "Pełna dokumentacja ceremonii oraz rozbudowany highlight podzielony na rozdziały: przygotowania, ceremonia, wesele. Krótki Reel na Instagram (60 sek.) wliczony w cenę."},
   "en": {"name": "Extended", "len": "Film 10–15 minutes", "tag": "Most popular",
          "desc": "Full coverage of the ceremony plus a longer highlight split into chapters: preparations, ceremony, reception. A 60-second Instagram Reel is included."}},
  {"n": "3", "price": "4 000 zł", "featured": False,
   "pl": {"name": "Pełny dzień", "len": "Film 30–60 minut", "tag": "",
          "desc": "Kompletna dokumentacja całego dnia w formie filmowej, a do tego highlight 3–5 minut w cenie."},
   "en": {"name": "Full day", "len": "Film 30–60 minutes", "tag": "",
          "desc": "Complete documentary coverage of the entire day in cinematic form, with a 3–5 minute highlight included."}},
]

# ================================================================= chrome
def head(lang, page, title, desc):
    other = "pl" if lang == "en" else "en"
    base = "" if lang == "en" else "../"
    url_self = ("" if lang == "en" else "pl/") + page + ".html"
    url_other = ("pl/" if lang == "en" else "") + page + ".html"
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:image" content="{base}assets/img/lg/da-29.jpg">
<meta name="theme-color" content="#0c0e0d">
<link rel="icon" href="{base}assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,opsz,wght@0,6..96,400;0,6..96,500;1,6..96,400&family=Archivo:wght@300;400;500&family=IBM+Plex+Mono:wght@300;400&display=swap">
<link rel="stylesheet" href="{base}assets/css/site.css">
</head>
<body>"""

def header(lang, page):
    base = "" if lang == "en" else "../"
    nav = NAV[lang]
    inline = "\n          ".join(
        f'<a href="{p}.html"{" aria-current=\"page\"" if p == page else ""}>{nav[p]}</a>'
        for p in PAGES if p != "contact")
    drawer_links = "\n        ".join(f'<a href="{p}.html">{nav[p]}</a>' for p in PAGES)
    en_href = ("../" if lang == "pl" else "") + page + ".html"
    pl_href = ("" if lang == "pl" else "pl/") + page + ".html"
    skip = "Skip to content" if lang == "en" else "Przejdź do treści"
    menu = "Menu"
    close = "Close" if lang == "en" else "Zamknij"
    cta = NAV[lang]["contact"]
    return f"""<a class="skip" href="#main">{skip}</a>
<header class="site-head">
  <div class="wrap site-head-in">
    <a class="brand" href="index.html">{BRAND}<small>{TAG[lang]}</small></a>
    <div class="head-right">
      <nav class="nav-inline" aria-label="{menu}">
          {inline}
      </nav>
      <span class="lang">
        <a href="{pl_href}" hreflang="pl"{' aria-current="true"' if lang=="pl" else ''}>PL</a><i>/</i><a href="{en_href}" hreflang="en"{' aria-current="true"' if lang=="en" else ''}>EN</a>
      </span>
      <a class="btn" href="contact.html">{cta}</a>
      <button class="menu-btn" type="button" data-drawer-open aria-controls="drawer" aria-label="{menu}"><i></i><i></i></button>
    </div>
  </div>
</header>

<div class="drawer" id="drawer" role="dialog" aria-modal="true" aria-label="{menu}" data-open="false">
  <div class="drawer-pane">
    <div class="drawer-top">
      <span class="eyebrow">{BRAND}</span>
      <button class="drawer-close" type="button" data-drawer-close>{close}</button>
    </div>
    <nav class="drawer-nav" aria-label="{menu}">
        {drawer_links}
    </nav>
    <div class="drawer-meta">
      <a href="mailto:{EMAIL}">{EMAIL}</a>
      <a href="tel:{PHONE_RAW}">{PHONE_DISPLAY}</a>
      <a href="{INSTAGRAM}" target="_blank" rel="noopener">Instagram {IG_HANDLE}</a>
    </div>
  </div>
  <div class="drawer-art"><img src="{base}assets/img/md/ja-40.jpg" alt="" loading="lazy"></div>
</div>"""

def footer(lang):
    base = "" if lang == "en" else "../"
    nav = NAV[lang]
    links = "\n            ".join(f'<li><a href="{p}.html">{nav[p]}</a></li>' for p in PAGES)
    if lang == "pl":
        blurb = "Filmy i fotografia ślubna. Pracuję solo — od pierwszego kadru do gotowego filmu."
        h_pages, h_contact, rights = "Strony", "Kontakt", "Wszelkie prawa zastrzeżone"
        made = "Zdjęcia i filmy: " + BRAND
    else:
        blurb = "Wedding films and photography. I work solo — from the first frame to the finished film."
        h_pages, h_contact, rights = "Pages", "Contact", "All rights reserved"
        made = "Photographs and films: " + BRAND
    return f"""<footer class="site-foot">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <h4>{BRAND}</h4>
        <p class="dim" style="max-width:34ch;margin:0">{blurb}</p>
      </div>
      <div>
        <h4>{h_pages}</h4>
        <ul class="foot-list">
            {links}
        </ul>
      </div>
      <div>
        <h4>{h_contact}</h4>
        <ul class="foot-list">
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li><a href="tel:{PHONE_RAW}">{PHONE_DISPLAY}</a></li>
          <li><a href="{INSTAGRAM}" target="_blank" rel="noopener">Instagram</a></li>
        </ul>
      </div>
    </div>
    <div class="foot-bottom">
      <span>© <span id="yr">2026</span> {BRAND} · {rights}</span>
      <span>{made}</span>
    </div>
  </div>
</footer>
<script src="{base}assets/js/films.js"></script>
<script src="{base}assets/js/site.js"></script>
<script>document.getElementById('yr').textContent=new Date().getFullYear();</script>
</body>
</html>
"""

def write(lang, page, title, desc, body):
    base = "" if lang == "en" else "../"
    out = head(lang, page, title, desc) + "\n" + header(lang, page) + \
          '\n<main id="main">\n' + body.replace("@@", base) + "\n</main>\n" + footer(lang)
    d = ROOT if lang == "en" else os.path.join(ROOT, "pl")
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, page + ".html"), "w", encoding="utf-8").write(out)


# ================================================================= content
COPY = {
 "en": {
  "home_title": "Hiroki Filmuje — wedding films and photography",
  "home_desc": "Wedding films and photography. One person, the whole day, no posing drills. Films ready within 14 days.",
  "hero_eyebrow": "Wedding films &amp; photography",
  "hero_h1": 'The day as it<br><span class="ital">actually</span> happened',
  "hero_lede": "I work alone, quietly, with a camera in my hands all day. No posing drills — your wedding, kept the way it felt.",
  "hero_cta1": "Check your date", "hero_cta2": "See the work",
  "s1_rail1": "01 — Approach", "s1_rail2": "Solo",
  "s1_h": "One person, one eye, the whole day.",
  "s1_p1": "Working solo means the film and the photographs come from the same pair of eyes. The colour, the rhythm, the moments I go after — all of it stays consistent from the first frame to the last.",
  "s1_p2": "I stay out of the way. Wide and quiet for most of the day, close only when something is happening that deserves it. The one thing I ask for is a short walk near golden hour.",
  "spec": [("Coverage","Film and photography"),("Crew","Solo"),("Film ready","Within 14 days"),("Delivery","WeTransfer or Google Drive")],
  "s2_rail1": "02 — Selected", "s2_rail2": "Recent",
  "s2_h": "Frames from recent weddings", "s2_btn": "Full portfolio",
  "strip_note": "Drag or scroll sideways",
  "s3_eyebrow": "03 — Behind the camera",
  "s3_h": "Hi, I'm Hiroki.",
  "s3_p1": "I film and photograph weddings in Poland. I came to this work because I like watching people forget the camera is there — and because a wedding is one of the few days when everyone in the room is telling the truth.",
  "s3_p2": "I cover the whole day myself: the preparations, the ceremony, the party until the dance floor finds its level. Then I cut it into a film you will actually rewatch.",
  "s3_btn": "More about me",
  "s4_eyebrow": "04 — In their words",
  "quote_note": "Translated from the original Polish messages.",
  "cta_h": "Dates book well ahead. Tell me when and where.",
  "cta_btn": "Start an enquiry",

  "work_title": "Work — Hiroki Filmuje",
  "work_desc": "Wedding films and photographs from recent weddings.",
  "work_h1": "Work",
  "work_lede": "Films and photographs from recent weddings. Press any photograph to open it full size.",
  "tab_all": "Everything", "tab_film": "Films", "tab_photo": "Photographs",
  "films_h": "Films", "photos_h": "Photographs",
  "work_rail1": "Portfolio", "work_rail2": "Film &amp; stills",

  "about_title": "About me — Hiroki Filmuje",
  "about_desc": "Hiroki Filmuje — wedding filmmaker and photographer working solo across Poland.",
  "about_h1": "About me",
  "about_eyebrow": "Behind the camera",
  "about_lede": "I'm Hiroki. I film and photograph weddings, and I do both myself.",
  "about_p1": "Working solo is a deliberate choice, not a limitation. One person carrying both the camera and the stills means the film and the photographs share a look: the same colour, the same instinct about when to step closer and when to leave people alone.",
  "about_p2": "I am not interested in a wedding that has been arranged for the lens. The parts worth keeping tend to happen on their own — someone's father going quiet during the speeches, the half-second before a first dance starts, a room that has been laughing for an hour and does not realise it. My job is to be there for those, and to be unobtrusive enough that they still happen.",
  "about_p3": "In practice that means I am there from the preparations through to the dancing. I shoot in the light the day gives me. I ask for one short walk near golden hour, and that is the only part of the day I will direct.",
  "about_p4": "Afterwards I edit everything myself. The film is with you within 14 days, delivered as a download link over WeTransfer or Google Drive.",
  "about_steps_h": "How a day runs",
  "about_steps": [
    ("A message and a call", "Tell me the date and the place. We talk for twenty minutes about how the day is shaped — no sales pitch."),
    ("The date is held", "A signed agreement and a 30% deposit take the date out of the calendar."),
    ("The wedding day", "I arrive during the preparations and stay through the ceremony and the reception. One short portrait walk, timed to the light."),
    ("Edit and delivery", "I cut, grade and finish the film myself. It reaches you within 14 days by WeTransfer or Google Drive."),
  ],

  "offer_title": "Offer — Hiroki Filmuje",
  "offer_desc": "Wedding film packages from 3 000 zł. Highlight films, full-day coverage, drone, Instagram Reel.",
  "offer_h1": "Offer",
  "offer_lede": "Three film packages. Every one of them is shot, edited and graded by me.",
  "offer_rail1": "Packages", "offer_rail2": "Prices in zł",
  "extras_h": "Extras",
  "extras": [("Drone", "+500 zł — aerial shots cut into the final film"),
             ("Additional outdoor session", "Quoted individually")],
  "general_h": "The practical part",
  "general": [("Crew","I work solo — one consistent style across the whole film"),
              ("Turnaround","Finished film within 14 days of the wedding"),
              ("Delivery","Download link via WeTransfer or Google Drive"),
              ("Travel","Depends on the distance — ask me for a figure")],
  "pay_h": "Payment",
  "pay_intro": "Cash, in three parts:",
  "pay": [("30%","On signing the agreement — this reserves your date"),
          ("50%","On the wedding day"),
          ("20%","After the finished film is delivered")],
  "offer_close": "Happy to send more examples of my work or answer anything that is not covered here.",

  "contact_title": "Contact — Hiroki Filmuje",
  "contact_desc": "Enquire about your wedding date. Email sebasuta@gmail.com or +48 516 849 121.",
  "contact_h1": "Let's talk",
  "contact_lede": "The date and the place are enough to start. Everything else we can work out on a call.",
  "contact_rail1": "Enquire", "contact_rail2": "Usually a reply within 2 days",
  "f_name": "Your names", "f_name_ph": "both of you, if you like",
  "f_email": "Email", "f_email_ph": "where I should reply",
  "f_date": "Wedding date", "f_date_note": "Leave blank if it is not fixed yet",
  "f_place": "Where", "f_place_ph": "venue, town, or just the region",
  "f_cov": "What you are after",
  "f_cov_opts": ["Choose one","Film only","Film and photography","Photography only","Not sure yet"],
  "f_notes": "Anything else", "f_notes_ph": "How the day runs, what matters most, anything you are worried about.",
  "f_send": "Prepare my enquiry",
  "form_note": "This form does not send email on its own. It checks what you have written and lays it out so you can copy it into a message — the address is just below.",
  "direct_h": "Or reach me directly",
  "l_email": "Email", "l_phone": "Phone", "l_ig": "Instagram",
  "copy": "Copy",
  "faq_h": "Before you ask",
  "faq": [
    ("How far do you travel?", "Travel is quoted according to distance, so tell me where the wedding is and I will give you a figure with the package price."),
    ("How long until we get the film?", "Within 14 days of the wedding. You get a download link over WeTransfer or Google Drive."),
    ("Do you work alone?", "Yes. One person for the film and the photographs, which is what keeps the style consistent across the whole day."),
    ("Can we choose the music?", "Yes — one song of your choice is part of every package."),
    ("How do we book?", "A signed agreement and a 30% deposit reserve the date. 50% is paid on the wedding day and the last 20% once the finished film is delivered."),
  ],
 },

 "pl": {
  "home_title": "Hiroki Filmuje — filmy i fotografia ślubna",
  "home_desc": "Filmy i fotografia ślubna. Jedna osoba, cały dzień, bez sztucznego pozowania. Gotowy film do 14 dni.",
  "hero_eyebrow": "Filmy i fotografia ślubna",
  "hero_h1": 'Dzień taki,<br>jaki był <span class="ital">naprawdę</span>',
  "hero_lede": "Pracuję sam, po cichu, z aparatem w ręku przez cały dzień. Bez sztucznego pozowania — zostaje Wasz ślub taki, jaki był.",
  "hero_cta1": "Sprawdź termin", "hero_cta2": "Zobacz prace",
  "s1_rail1": "01 — Podejście", "s1_rail2": "Solo",
  "s1_h": "Jedna osoba, jedno spojrzenie, cały dzień.",
  "s1_p1": "Pracuję solo, więc film i zdjęcia powstają z tej samej perspektywy. Kolor, rytm, wyłapywane momenty — wszystko jest spójne od pierwszego do ostatniego kadru.",
  "s1_p2": "Nie wchodzę w drogę. Przez większość dnia jestem z boku, podchodzę bliżej tylko wtedy, gdy dzieje się coś, co na to zasługuje. Proszę jedynie o krótki spacer o złotej godzinie.",
  "spec": [("Zakres","Film i fotografia"),("Obsada","Solo"),("Gotowy film","Do 14 dni"),("Dostawa","WeTransfer lub Google Drive")],
  "s2_rail1": "02 — Wybrane", "s2_rail2": "Ostatnie",
  "s2_h": "Kadry z ostatnich ślubów", "s2_btn": "Całe portfolio",
  "strip_note": "Przeciągnij lub przewiń w bok",
  "s3_eyebrow": "03 — Za kamerą",
  "s3_h": "Cześć, jestem Hiroki.",
  "s3_p1": "Filmuję i fotografuję śluby w Polsce. Zajmuję się tym, bo lubię patrzeć, jak ludzie zapominają o kamerze — i dlatego, że ślub jest jednym z niewielu dni, kiedy wszyscy na sali są prawdziwi.",
  "s3_p2": "Cały dzień obsługuję sam: przygotowania, ceremonię i wesele, aż parkiet złapie swój rytm. Potem montuję z tego film, do którego naprawdę się wraca.",
  "s3_btn": "Poznaj mnie",
  "s4_eyebrow": "04 — Opinie",
  "quote_note": "Oryginalne wiadomości od par młodych.",
  "cta_h": "Terminy rezerwują się z dużym wyprzedzeniem. Napiszcie, kiedy i gdzie.",
  "cta_btn": "Napisz do mnie",

  "work_title": "Portfolio — Hiroki Filmuje",
  "work_desc": "Filmy i zdjęcia z ostatnich ślubów.",
  "work_h1": "Portfolio",
  "work_lede": "Filmy i zdjęcia z ostatnich ślubów. Kliknijcie zdjęcie, aby otworzyć je w pełnym rozmiarze.",
  "tab_all": "Wszystko", "tab_film": "Filmy", "tab_photo": "Zdjęcia",
  "films_h": "Filmy", "photos_h": "Zdjęcia",
  "work_rail1": "Portfolio", "work_rail2": "Film i zdjęcia",

  "about_title": "O mnie — Hiroki Filmuje",
  "about_desc": "Hiroki Filmuje — filmy i fotografia ślubna. Pracuję solo, w całej Polsce.",
  "about_h1": "O mnie",
  "about_eyebrow": "Za kamerą",
  "about_lede": "Jestem Hiroki. Filmuję i fotografuję śluby — jedno i drugie robię osobiście.",
  "about_p1": "Praca solo to świadomy wybór, nie ograniczenie. Jedna osoba z kamerą i aparatem oznacza, że film i zdjęcia mają ten sam charakter: ten sam kolor i to samo wyczucie, kiedy podejść bliżej, a kiedy zostawić ludziom przestrzeń.",
  "about_p2": "Nie interesuje mnie ślub ustawiony pod obiektyw. To, co warto zatrzymać, dzieje się samo — tata, który milknie w trakcie przemówienia, pół sekundy przed pierwszym tańcem, sala, która śmieje się od godziny i nawet tego nie zauważa. Moim zadaniem jest przy tym być i nie przeszkadzać, żeby to dalej się działo.",
  "about_p3": "W praktyce jestem z Wami od przygotowań aż po tańce. Pracuję w świetle, które daje dzień. Proszę o jeden krótki spacer o złotej godzinie — i to jedyny moment, który reżyseruję.",
  "about_p4": "Całość montuję sam. Gotowy film trafia do Was w ciągu 14 dni, jako link do pobrania przez WeTransfer lub Google Drive.",
  "about_steps_h": "Jak wygląda współpraca",
  "about_steps": [
    ("Wiadomość i rozmowa", "Napiszcie termin i miejsce. Rozmawiamy dwadzieścia minut o tym, jak wygląda Wasz dzień — bez sprzedażowego gadania."),
    ("Rezerwacja terminu", "Podpisana umowa i 30% zaliczki blokują termin w kalendarzu."),
    ("Dzień ślubu", "Przyjeżdżam na przygotowania i zostaję przez ceremonię i wesele. Jeden krótki plener, dopasowany do światła."),
    ("Montaż i dostawa", "Montuję, koloruję i kończę film osobiście. Dostajecie go do 14 dni przez WeTransfer lub Google Drive."),
  ],

  "offer_title": "Oferta — Hiroki Filmuje",
  "offer_desc": "Pakiety filmów ślubnych od 3 000 zł. Highlight, pełny dzień, dron, Reel na Instagram.",
  "offer_h1": "Oferta",
  "offer_lede": "Trzy pakiety filmowe. Każdy z nich nagrywam, montuję i koloruję osobiście.",
  "offer_rail1": "Pakiety", "offer_rail2": "Ceny w zł",
  "extras_h": "Dodatki",
  "extras": [("Dron", "+500 zł — ujęcia lotnicze zmontowane w finalny film"),
             ("Dodatkowa sesja plenerowa", "Wycena indywidualna")],
  "general_h": "Informacje ogólne",
  "general": [("Obsada","Pracuję solo — pełna spójność stylu i estetyki przez cały film"),
              ("Czas realizacji","Gotowy film do 14 dni od ślubu"),
              ("Forma dostawy","Link do pobrania przez WeTransfer lub Google Drive"),
              ("Dojazd","Zależny od odległości — napiszcie, gdzie się odbywa ślub")],
  "pay_h": "Płatność",
  "pay_intro": "Gotówka, w trzech częściach:",
  "pay": [("30%","Przy podpisaniu umowy — rezerwacja terminu"),
          ("50%","W dniu ślubu"),
          ("20%","Po dostarczeniu gotowego materiału")],
  "offer_close": "Chętnie prześlę przykłady mojej pracy lub odpowiem na dodatkowe pytania.",

  "contact_title": "Kontakt — Hiroki Filmuje",
  "contact_desc": "Zapytaj o termin. E-mail sebasuta@gmail.com lub +48 516 849 121.",
  "contact_h1": "Napiszcie do mnie",
  "contact_lede": "Termin i miejsce w zupełności wystarczą na początek. Resztę ustalimy na rozmowie.",
  "contact_rail1": "Kontakt", "contact_rail2": "Odpowiadam zwykle w 2 dni",
  "f_name": "Wasze imiona", "f_name_ph": "najlepiej oboje",
  "f_email": "E-mail", "f_email_ph": "adres, na który mam odpowiedzieć",
  "f_date": "Data ślubu", "f_date_note": "Zostawcie puste, jeśli termin nie jest jeszcze ustalony",
  "f_place": "Miejsce", "f_place_ph": "sala, miasto albo sam region",
  "f_cov": "Czego potrzebujecie",
  "f_cov_opts": ["Wybierzcie","Tylko film","Film i zdjęcia","Tylko zdjęcia","Jeszcze nie wiemy"],
  "f_notes": "Coś jeszcze", "f_notes_ph": "Jak wygląda dzień, co jest dla Was najważniejsze, o co się martwicie.",
  "f_send": "Przygotuj zapytanie",
  "form_note": "Ten formularz nie wysyła wiadomości samodzielnie. Sprawdza to, co wpisaliście, i układa w gotowy tekst do skopiowania — adres e-mail znajdziecie niżej.",
  "direct_h": "Albo bezpośrednio",
  "l_email": "E-mail", "l_phone": "Telefon", "l_ig": "Instagram",
  "copy": "Kopiuj",
  "faq_h": "Zanim zapytacie",
  "faq": [
    ("Jak daleko dojeżdżasz?", "Dojazd wyceniam według odległości — napiszcie, gdzie odbywa się ślub, a podam kwotę razem z ceną pakietu."),
    ("Kiedy dostaniemy film?", "Do 14 dni od ślubu. Dostajecie link do pobrania przez WeTransfer lub Google Drive."),
    ("Pracujesz sam?", "Tak. Jedna osoba do filmu i do zdjęć — dzięki temu całość jest spójna stylistycznie."),
    ("Czy możemy wybrać muzykę?", "Tak — jedna piosenka według Waszego wyboru wchodzi w skład każdego pakietu."),
    ("Jak zarezerwować termin?", "Podpisana umowa i 30% zaliczki rezerwują termin. 50% płatne w dniu ślubu, ostatnie 20% po dostarczeniu gotowego filmu."),
  ],
 },
}

# ================================================================= pages
def img(stem, size, lang, cls="", lazy=True, sizes=""):
    return (f'<img src="@@assets/img/{size}/{stem}.jpg" alt="{alt(stem, lang)}"'
            f'{" loading=\"lazy\"" if lazy else ""} decoding="async"{cls}>')

def build(lang):
    c = COPY[lang]
    nav = NAV[lang]

    # ---------------------------------------------------------------- home
    hero_imgs = "\n        ".join(
        f'<img src="@@assets/img/lg/{s}.jpg" alt="{alt(s, lang)}"'
        f'{"" if i == 0 else " loading=\"lazy\""} decoding="async">' for i, s in enumerate(HERO))
    strip = "\n        ".join(
        f'<figure><div class="ph r45">{img(s,"md",lang)}</div>'
        f'<figcaption><span>{COUPLES[k] or ""}</span><span>{i+1:02d}</span></figcaption></figure>'
        for i, (s, k) in enumerate(STRIP))
    specs = "\n            ".join(f'<li><span>{a}</span><span>{b}</span></li>' for a, b in c["spec"])
    quotes = "\n          ".join(
        f'<div class="quote"><blockquote>{q[lang]}</blockquote><cite>{q["who"]}</cite></div>' for q in QUOTES)

    home = f"""  <section class="hero">
    <div class="hero-stack" data-stack aria-hidden="true">
        {hero_imgs}
    </div>
    <p class="hero-index"><span data-stack-count>01 / 0{len(HERO)}</span></p>
    <div class="wrap hero-body">
      <p class="eyebrow">{c["hero_eyebrow"]}</p>
      <h1 class="h-xl">{c["hero_h1"]}</h1>
      <p class="lede">{c["hero_lede"]}</p>
      <div class="hero-cta">
        <a class="btn btn-solid btn-lg" href="contact.html">{c["hero_cta1"]}</a>
        <a class="btn btn-lg" href="work.html">{c["hero_cta2"]}</a>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap railed">
      <div class="rail reveal"><span>{c["s1_rail1"]}</span><span>{c["s1_rail2"]}</span></div>
      <div class="reveal">
        <h2 class="h-lg">{c["s1_h"]}</h2>
        <div class="prose dim" style="margin-top:1.6em"><p>{c["s1_p1"]}</p><p>{c["s1_p2"]}</p></div>
        <ul class="specs" style="margin-top:2.4em;max-width:48ch">
            {specs}
        </ul>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap" style="margin-bottom:clamp(26px,4vw,48px)">
      <div class="railed">
        <div class="rail reveal"><span>{c["s2_rail1"]}</span><span>{c["s2_rail2"]}</span></div>
        <div class="reveal" style="display:flex;flex-wrap:wrap;gap:18px;align-items:end;justify-content:space-between">
          <h2 class="h-lg" style="max-width:22ch">{c["s2_h"]}</h2>
          <a class="btn" href="work.html">{c["s2_btn"]}</a>
        </div>
      </div>
    </div>
    <div class="strip" data-strip>
        {strip}
    </div>
    <div class="wrap"><p class="field-note" style="margin-top:14px">{c["strip_note"]}</p></div>
  </section>

  <section class="section">
    <div class="wrap split">
      <div class="reveal"><div class="ph r45"><img src="@@assets/img/md/hiroki.jpg" alt="Hiroki" loading="lazy" decoding="async"></div></div>
      <div class="reveal">
        <p class="eyebrow">{c["s3_eyebrow"]}</p>
        <h2 class="h-lg" style="margin-top:.7em">{c["s3_h"]}</h2>
        <div class="prose dim" style="margin-top:1.4em"><p>{c["s3_p1"]}</p><p>{c["s3_p2"]}</p></div>
        <a class="btn" href="about.html" style="margin-top:2em">{c["s3_btn"]}</a>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="quotes" data-quotes>
        <p class="eyebrow" style="margin-bottom:2.4em">{c["s4_eyebrow"]}</p>
          {quotes}
        <div class="quote-nav">
          <button type="button" data-quote-prev aria-label="&#8592;">&#8592;</button>
          <span class="quote-count" data-quote-count>01 / 03</span>
          <button type="button" data-quote-next aria-label="&#8594;">&#8594;</button>
        </div>
      </div>
      <p class="field-note" style="text-align:center;margin-top:2.4em">{c["quote_note"]}</p>
    </div>
  </section>

  <section class="cta-band">
    <img src="@@assets/img/lg/ja-59.jpg" alt="" loading="lazy" decoding="async">
    <div class="wrap">
      <h2 class="h-lg" style="max-width:26ch;margin-inline:auto">{c["cta_h"]}</h2>
      <a class="btn btn-solid btn-lg" href="contact.html" style="margin-top:2.2em">{c["cta_btn"]}</a>
    </div>
  </section>"""
    write(lang, "index", c["home_title"], c["home_desc"], home)

    # ---------------------------------------------------------------- work
    gal = "\n        ".join(
        f'<figure><button type="button" data-full="@@assets/img/lg/{s}.jpg" data-cap="{COUPLES[k] or ""}">'
        f'{img(s,"md",lang)}</button>'
        + (f'<figcaption>{COUPLES[k]}</figcaption>' if COUPLES[k] else '')
        + '</figure>' for s, k in GALLERY)
    work = f"""  <section class="section">
    <div class="wrap railed">
      <div class="rail"><span>{c["work_rail1"]}</span><span>{c["work_rail2"]}</span></div>
      <div>
        <h1 class="h-xl">{c["work_h1"]}</h1>
        <p class="lede dim" style="max-width:44ch;margin-top:1em">{c["work_lede"]}</p>
        <div class="tabs" data-tabs role="tablist">
          <button type="button" data-tab="all" role="tab" aria-selected="true">{c["tab_all"]}</button>
          <button type="button" data-tab="film" role="tab" aria-selected="false">{c["tab_film"]}</button>
          <button type="button" data-tab="photo" role="tab" aria-selected="false">{c["tab_photo"]}</button>
        </div>
      </div>
    </div>
  </section>

  <section class="section" data-panel="film">
    <div class="wrap">
      <h2 class="h-md" style="margin-bottom:clamp(22px,3vw,38px)">{c["films_h"]}</h2>
      <div class="films" data-films></div>
    </div>
  </section>

  <section class="section" data-panel="photo">
    <div class="wrap">
      <h2 class="h-md" style="margin-bottom:clamp(22px,3vw,38px)">{c["photos_h"]}</h2>
      <div class="gallery" data-gallery>
        {gal}
      </div>
    </div>
  </section>

  <div class="lb" id="lightbox" hidden role="dialog" aria-modal="true" aria-label="{c["photos_h"]}">
    <button class="lb-btn lb-close" type="button" aria-label="&#10005;">&#10005;</button>
    <button class="lb-btn lb-prev" type="button" aria-label="&#8592;">&#8592;</button>
    <button class="lb-btn lb-next" type="button" aria-label="&#8594;">&#8594;</button>
    <img src="" alt="">
    <p class="lb-cap"></p>
  </div>

  <section class="cta-band">
    <img src="@@assets/img/lg/nm-11.jpg" alt="" loading="lazy" decoding="async">
    <div class="wrap">
      <h2 class="h-lg" style="max-width:26ch;margin-inline:auto">{c["cta_h"]}</h2>
      <a class="btn btn-solid btn-lg" href="contact.html" style="margin-top:2.2em">{c["cta_btn"]}</a>
    </div>
  </section>"""
    write(lang, "work", c["work_title"], c["work_desc"], work)

    # ---------------------------------------------------------------- about
    steps = "\n          ".join(
        f'<li><h3>{t}</h3><p>{p}</p></li>' for t, p in c["about_steps"])
    about = f"""  <section class="section">
    <div class="wrap split">
      <div>
        <p class="eyebrow">{c["about_eyebrow"]}</p>
        <h1 class="h-xl" style="margin-top:.5em">{c["about_h1"]}</h1>
        <p class="lede dim" style="margin-top:1.2em;max-width:34ch">{c["about_lede"]}</p>
      </div>
      <div class="ph r45"><img src="@@assets/img/lg/hiroki.jpg" alt="Hiroki" decoding="async"></div>
    </div>
  </section>

  <section class="section">
    <div class="wrap railed">
      <div class="rail"><span>{c["about_eyebrow"]}</span><span>{BRAND}</span></div>
      <div class="prose dim">
        <p>{c["about_p1"]}</p><p>{c["about_p2"]}</p><p>{c["about_p3"]}</p><p>{c["about_p4"]}</p>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap grid g2">
      <div class="ph r32 reveal">{img("da-39","md",lang)}</div>
      <div class="ph r32 reveal offset">{img("nm-30","md",lang)}</div>
    </div>
  </section>

  <section class="section">
    <div class="wrap railed">
      <div class="rail"><span>{c["about_steps_h"]}</span><span>01 — 04</span></div>
      <div>
        <h2 class="h-lg">{c["about_steps_h"]}</h2>
        <ol class="steps">
          {steps}
        </ol>
      </div>
    </div>
  </section>

  <section class="cta-band">
    <img src="@@assets/img/lg/jd-14.jpg" alt="" loading="lazy" decoding="async">
    <div class="wrap">
      <h2 class="h-lg" style="max-width:26ch;margin-inline:auto">{c["cta_h"]}</h2>
      <a class="btn btn-solid btn-lg" href="contact.html" style="margin-top:2.2em">{c["cta_btn"]}</a>
    </div>
  </section>"""
    write(lang, "about", c["about_title"], c["about_desc"], about)

    # ---------------------------------------------------------------- offer
    packs = "\n        ".join(
        f'<article class="pack reveal" data-featured="{"true" if p["featured"] else "false"}">'
        + (f'<p class="pack-tag">★ {p[lang]["tag"]}</p>' if p[lang]["tag"] else '<p class="pack-tag">0' + p["n"] + '</p>')
        + f'<h3>{p[lang]["name"]}</h3>'
          f'<p class="pack-len">{p[lang]["len"]}</p>'
          f'<p>{p[lang]["desc"]}</p>'
          f'<p class="pack-price">{p["price"]}</p></article>' for p in PACKS)
    extras = "\n            ".join(f'<li><span>{a}</span><span>{b}</span></li>' for a, b in c["extras"])
    general = "\n            ".join(f'<li><span>{a}</span><span>{b}</span></li>' for a, b in c["general"])
    pay = "\n            ".join(f'<li><span>{a}</span><span>{b}</span></li>' for a, b in c["pay"])
    offer = f"""  <section class="section">
    <div class="wrap railed">
      <div class="rail"><span>{c["offer_rail1"]}</span><span>{c["offer_rail2"]}</span></div>
      <div>
        <h1 class="h-xl">{c["offer_h1"]}</h1>
        <p class="lede dim" style="max-width:40ch;margin-top:1em">{c["offer_lede"]}</p>
      </div>
    </div>
    <div class="wrap">
      <div class="packs">
        {packs}
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap railed">
      <div class="rail"><span>{c["extras_h"]}</span></div>
      <div>
        <h2 class="h-lg">{c["extras_h"]}</h2>
        <ul class="specs" style="margin-top:1.8em;max-width:60ch">
            {extras}
        </ul>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap railed">
      <div class="rail"><span>{c["general_h"]}</span></div>
      <div>
        <h2 class="h-lg">{c["general_h"]}</h2>
        <ul class="specs" style="margin-top:1.8em;max-width:60ch">
            {general}
        </ul>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap railed">
      <div class="rail"><span>{c["pay_h"]}</span></div>
      <div>
        <h2 class="h-lg">{c["pay_h"]}</h2>
        <p class="dim" style="margin-top:1.2em">{c["pay_intro"]}</p>
        <ul class="specs" style="margin-top:1.2em;max-width:60ch">
            {pay}
        </ul>
        <p class="prose dim" style="margin-top:2.4em">{c["offer_close"]}</p>
        <a class="btn btn-solid" href="contact.html" style="margin-top:1.6em">{c["cta_btn"]}</a>
      </div>
    </div>
  </section>

  <section class="cta-band">
    <img src="@@assets/img/lg/na-10.jpg" alt="" loading="lazy" decoding="async">
    <div class="wrap">
      <h2 class="h-lg" style="max-width:26ch;margin-inline:auto">{c["cta_h"]}</h2>
      <a class="btn btn-solid btn-lg" href="contact.html" style="margin-top:2.2em">{c["cta_btn"]}</a>
    </div>
  </section>"""
    write(lang, "offer", c["offer_title"], c["offer_desc"], offer)

    # ---------------------------------------------------------------- contact
    opts = "\n                ".join(
        f'<option{" value=\"\"" if i == 0 else ""}>{o}</option>' for i, o in enumerate(c["f_cov_opts"]))
    faq = "\n            ".join(
        f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in c["faq"])
    contact = f"""  <section class="section">
    <div class="wrap railed">
      <div class="rail"><span>{c["contact_rail1"]}</span><span>{c["contact_rail2"]}</span></div>
      <div>
        <h1 class="h-xl">{c["contact_h1"]}</h1>
        <p class="lede dim" style="max-width:40ch;margin-top:1em">{c["contact_lede"]}</p>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap railed">
      <div class="rail"><span>{NAV[lang]["contact"]}</span></div>
      <div>
        <p class="note" style="max-width:58ch;margin-bottom:2.6em">{c["form_note"]}</p>
        <form class="form" id="enquiry" data-mailto="{EMAIL}" novalidate>
          <div class="field">
            <label for="f-name">{c["f_name"]}</label>
            <input id="f-name" name="name" type="text" autocomplete="name" placeholder="{c["f_name_ph"]}" data-required>
            <p class="field-err" id="f-name-err" aria-live="polite"></p>
          </div>
          <div class="field">
            <label for="f-email">{c["f_email"]}</label>
            <input id="f-email" name="email" type="email" autocomplete="email" placeholder="{c["f_email_ph"]}" data-required>
            <p class="field-err" id="f-email-err" aria-live="polite"></p>
          </div>
          <div class="field">
            <label for="f-date">{c["f_date"]}</label>
            <input id="f-date" name="date" type="date">
            <p class="field-note">{c["f_date_note"]}</p>
          </div>
          <div class="field">
            <label for="f-place">{c["f_place"]}</label>
            <input id="f-place" name="place" type="text" placeholder="{c["f_place_ph"]}">
          </div>
          <div class="field">
            <label for="f-coverage">{c["f_cov"]}</label>
            <select id="f-coverage" name="coverage">
                {opts}
            </select>
          </div>
          <div class="field">
            <label for="f-notes">{c["f_notes"]}</label>
            <textarea id="f-notes" name="notes" placeholder="{c["f_notes_ph"]}"></textarea>
          </div>
          <div><button class="btn btn-solid btn-lg" type="submit">{c["f_send"]}</button></div>
          <div class="form-status" id="enquiry-status" tabindex="-1" role="status" hidden></div>
        </form>

        <div class="contact-lines">
          <h2 class="h-sm" style="margin-top:clamp(28px,4vw,46px)">{c["direct_h"]}</h2>
          <p class="cline"><b>{c["l_email"]}</b>
            <code id="c-mail">{EMAIL}</code>
            <button class="copy-btn" type="button" data-copy="{EMAIL}" data-copy-target="c-mail">{c["copy"]}</button></p>
          <p class="cline"><b>{c["l_phone"]}</b>
            <code id="c-tel">{PHONE_DISPLAY}</code>
            <button class="copy-btn" type="button" data-copy="{PHONE_RAW}" data-copy-target="c-tel">{c["copy"]}</button></p>
          <p class="cline"><b>{c["l_ig"]}</b>
            <a class="plain" href="{INSTAGRAM}" target="_blank" rel="noopener">{IG_HANDLE}</a></p>
        </div>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap railed">
      <div class="rail"><span>FAQ</span></div>
      <div>
        <h2 class="h-lg">{c["faq_h"]}</h2>
        <div class="faq">
            {faq}
        </div>
      </div>
    </div>
  </section>"""
    write(lang, "contact", c["contact_title"], c["contact_desc"], contact)

for lg in ("en", "pl"):
    build(lg)
print("built EN + PL")
