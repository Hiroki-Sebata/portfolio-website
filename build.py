# -*- coding: utf-8 -*-
"""Builds the Hiroki Filmuje site into docs/ (which is what GitHub Pages serves).

    python3 build.py

Copy for both languages lives in copy.py. Photographs are read from
docs/assets/img/ and grouped into albums by their filename prefix.
"""
import os, re, json, random
from copy import COPY
from privacy import PRIVACY, PRIVACY_UPDATED

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(SRC_DIR, "docs")

BRAND = "Hiroki Filmuje"
EMAIL = "sebasuta@gmail.com"
PHONE_DISPLAY = "+48 516 849 121"
PHONE_RAW = "+48516849121"
INSTAGRAM = "https://www.instagram.com/hiroki_filmuje/"
IG_HANDLE = "@hiroki_filmuje"
# Every other page that is unmistakably this business. Google uses these to
# decide that the Instagram profile and this domain are one entity rather than
# two competing results. Add any directory listing you control.
SAME_AS = [
    INSTAGRAM,
    # "https://www.weselezklasa.pl/...",   <- paste your profile URL here
]
DOMAIN = "hiroki-filmuje.pl"
# Web3Forms delivers the enquiry form to EMAIL. This key is meant to be public:
# it sits in the page source, like every Web3Forms key. Rotate it at web3forms.com
# if it ever gets abused.
WEB3FORMS_KEY = "aa2ad116-3270-435b-9b0b-bd428f8ce67b"

# ---------------------------------------------------------------- Meta Pixel
# Paste the pixel ID from Meta Events Manager between the quotes (digits only).
# While this is empty no tracking code is written into the pages at all.
META_PIXEL_ID = "1143058494743549"
# True  -> the pixel loads only after a visitor accepts the cookie notice (EU/GDPR)
# False -> the pixel loads for everyone, immediately
META_PIXEL_ASK_CONSENT = True

PAGES = ["index", "work", "about", "offer", "contact"]
NAV = {
    "en": {"index": "Home", "work": "Work", "about": "About me", "offer": "Offer", "contact": "Contact"},
    "pl": {"index": "Start", "work": "Portfolio", "about": "O mnie", "offer": "Oferta", "contact": "Kontakt"},
}
TAG = {"en": "Wedding films &amp; photography", "pl": "Filmy i fotografia ślubna"}

# ---------------------------------------------------------------- albums
# prefix -> (file-slug, album page slug, display name EN, display name PL)
ALBUMS = [
    ("nm", "nadia-miguel",    "Nadia &amp; Miguel",    "Nadia &amp; Miguel"),
    ("na", "nastyja-anton",   "Nastyja &amp; Anton",   "Nastyja &amp; Anton"),
    ("da", "dominika-artur",  "Dominika &amp; Artur",  "Dominika &amp; Artur"),
    ("jd", "julia-dominik",   "Julia &amp; Dominik",   "Julia &amp; Dominik"),
    ("ja", "julia-artsiom",   "Julia &amp; Artsiom",   "Julia &amp; Artsiom"),
    ("ai", "agata-igor",      "Agata &amp; Igor",      "Agata &amp; Igor"),
]
ALBUM_BY_KEY = {a[0]: a for a in ALBUMS}

def album_name(key, lang):
    a = ALBUM_BY_KEY[key]
    return a[2] if lang == "en" else a[3]

def album_page(key):
    return "album-" + ALBUM_BY_KEY[key][1] + ".html"

def photos_for(key):
    """Every exported photograph for one wedding, in natural number order."""
    d = os.path.join(OUT, "assets/img/md")
    out = []
    for f in os.listdir(d):
        m = re.match(r"^" + key + r"-(\d+)\.jpg$", f)
        if m:
            out.append((int(m.group(1)), f[:-4]))
    return [s for _, s in sorted(out)]

PHOTOS = {k: photos_for(k) for k, *_ in ALBUMS}

# One shuffled run of every photograph, for the Work page. Seeded so the order
# is mixed but identical on every rebuild (no churn in git, no layout jumping).
ALL_SHUFFLED = [(s, k) for k in PHOTOS for s in PHOTOS[k]]
random.Random(20261006).shuffle(ALL_SHUFFLED)

# ---------------------------------------------------------------- picks
HERO = ["ja-48", "nm-39", "na-5", "da-33"]
# home strip: one frame per wedding, in the order you asked for, each linking to its album
# One frame per wedding, in the order you asked for; the last two follow so every
# album is reachable from the home page and the strip has something to scroll.
STRIP = [("nm-39", "nm"), ("na-10", "na"), ("da-9", "da"), ("jd-25", "jd"),
         ("ja-29", "ja"), ("ai-3", "ai")]
CTA_IMG = {"index": "ja-59", "work": "nm-11", "about": "da-3", "offer": "na-10"}

# Where to anchor a photograph when a wide screen crops it. A laptop window is
# much wider than it is tall, so a portrait frame loses its top and bottom; with
# the default centre anchor that cuts faces off. These pull the crop upwards.
# Format: "horizontal vertical" — smaller vertical = more of the top kept.
FOCUS_DEFAULT = "50% 20%"
FOCUS = {
    "ja-48": "50% 8%",    # extreme close-up; pull right up so the eyes stay in
    "nm-39": "50% 20%",   # both heads in the upper third
    "na-5":  "50% 50%",   # wide crop already centred on their faces
    "da-33": "50% 28%",   # bouquet and veil are the subject, not a face
    "ja-59": "50% 50%",   # dedicated 3.5:1 band slice, centred on their faces
    "nm-11": "50% 38%",
    "da-3":  "50% 50%",   # flat-lay of shoes, nothing to cut off
    "na-10": "55% 45%",   # candlelit couple sit centre-right
}

def focus(stem):
    return FOCUS.get(stem, FOCUS_DEFAULT)

_SIZE_CACHE = {}


def img_size(path):
    """Intrinsic pixel size of a JPEG, read straight from its header.

    srcset needs each file's real width. Our photographs are a mix of portrait
    and landscape, so the width of a '900px' file is 900 for one and 600 for the
    other — guessing would make the browser pick the wrong file."""
    if path in _SIZE_CACHE:
        return _SIZE_CACHE[path]
    try:
        with open(path, "rb") as fh:
            data = fh.read()
    except OSError:
        return None
    i, n = 2, len(data)
    while i < n - 9:
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        if marker in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
                      0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
            h = (data[i + 5] << 8) + data[i + 6]
            w = (data[i + 7] << 8) + data[i + 8]
            _SIZE_CACHE[path] = (w, h)
            return (w, h)
        if marker in (0xD8, 0xD9) or 0xD0 <= marker <= 0xD7:
            i += 2
            continue
        seg = (data[i + 2] << 8) + data[i + 3]
        i += 2 + seg
    return None


def srcset_for(stem):
    """md + lg as a srcset, with each file's true width."""
    parts = []
    for size in ("md", "lg"):
        p = os.path.join(OUT, "assets/img", size, stem + ".jpg")
        wh = img_size(p)
        if wh:
            parts.append("@@assets/img/%s/%s.jpg %dw" % (size, stem, wh[0]))
    return ", ".join(parts)   # srcset candidates are comma separated


def alt(stem, lang):
    key = stem.split("-")[0]
    name = album_name(key, lang).replace("&amp;", "&") if key in ALBUM_BY_KEY else ""
    if lang == "pl":
        return ("Fotografia ślubna — " + name) if name else "Fotografia ślubna"
    return ("Wedding photograph — " + name) if name else "Wedding photograph"

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
def page_url(lang, page):
    """The one canonical address for a page."""
    base = "https://%s/" % DOMAIN
    if lang == "pl":
        base += "pl/"
    return base if page == "index" else base + page + ".html"


def seo_head(lang, page, title, desc):
    """Canonical, language alternates, social cards and structured data.

    The structured data matters more than anything else here: sameAs is what
    tells Google the Instagram profile and this domain are the same business,
    which is how a site stops competing with its own social profiles.
    """
    url_self = page_url(lang, page)
    url_en = page_url("en", page)
    url_pl = page_url("pl", page)
    og_locale = "pl_PL" if lang == "pl" else "en_GB"
    bits = [
        '<link rel="canonical" href="%s">' % url_self,
        '<link rel="alternate" hreflang="en" href="%s">' % url_en,
        '<link rel="alternate" hreflang="pl" href="%s">' % url_pl,
        '<link rel="alternate" hreflang="x-default" href="%s">' % url_en,
        '<meta property="og:url" content="%s">' % url_self,
        '<meta property="og:site_name" content="%s">' % BRAND,
        '<meta property="og:locale" content="%s">' % og_locale,
        '<meta name="twitter:card" content="summary_large_image">',
    ]

    business = {
        "@type": "ProfessionalService",
        "@id": "https://%s/#business" % DOMAIN,
        "name": BRAND,
        "alternateName": "Hiroki Sebata",
        "url": "https://%s/" % DOMAIN,
        "image": "https://%s/assets/img/xl/%s.jpg" % (DOMAIN, HERO[0]),
        "email": EMAIL,
        "telephone": PHONE_RAW,
        "priceRange": "3000–4000 PLN",
        "currenciesAccepted": "PLN",
        "paymentAccepted": "Cash",
        "areaServed": {"@type": "Country", "name": "Poland"},
        "knowsLanguage": ["pl", "en"],
        "sameAs": SAME_AS,
        "description": ("Filmy i fotografia ślubna. Pracuję solo — od pierwszego kadru "
                        "do gotowego filmu." if lang == "pl" else
                        "Wedding films and photography. I work solo — from the first "
                        "frame to the finished film."),
    }
    graph = [business, {
        "@type": "WebSite",
        "@id": "https://%s/#website" % DOMAIN,
        "url": "https://%s/" % DOMAIN,
        "name": BRAND,
        "inLanguage": "pl-PL" if lang == "pl" else "en-GB",
        "publisher": {"@id": "https://%s/#business" % DOMAIN},
    }, {
        "@type": "WebPage",
        "@id": url_self + "#webpage",
        "url": url_self,
        "name": title,
        "description": desc,
        "inLanguage": "pl-PL" if lang == "pl" else "en-GB",
        "isPartOf": {"@id": "https://%s/#website" % DOMAIN},
        "about": {"@id": "https://%s/#business" % DOMAIN},
    }]
    ld = {"@context": "https://schema.org", "@graph": graph}
    bits.append('<script type="application/ld+json">%s</script>'
                % json.dumps(ld, ensure_ascii=False, separators=(",", ":")))
    return "\n".join(bits)


def head(lang, page, title, desc, base):
    seo = seo_head(lang, page, title, desc)
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
<meta property="og:image" content="https://{DOMAIN}/assets/img/lg/{HERO[0]}.jpg">
<meta name="theme-color" content="#0c0e0d">
<link rel="icon" href="{base}assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,opsz,wght@0,6..96,400;0,6..96,500;1,6..96,400&family=Archivo:wght@300;400;500&family=IBM+Plex+Mono:wght@300;400&display=swap">
<link rel="stylesheet" href="{base}assets/css/site.css">
{seo}
</head>
<body data-page="{page}">"""

def header(lang, page, base):
    nav = NAV[lang]
    # pages outside the menu (privacy) must not light up a menu item
    cur = page if page in PAGES else ""
    inline = "\n          ".join(
        '<a href="%s.html"%s>%s</a>' % (p, ' aria-current="page"' if p == cur else '', nav[p])
        for p in PAGES if p != "contact")
    drawer_links = "\n        ".join('<a href="%s.html">%s</a>' % (p, nav[p]) for p in PAGES)
    # the language switch should stay on the same page, menu or not
    target = page if page in PAGES or page == "privacy" else "work"
    en_href = ("../" if lang == "pl" else "") + target + ".html"
    pl_href = ("" if lang == "pl" else "pl/") + target + ".html"
    skip = "Skip to content" if lang == "en" else "Przejdź do treści"
    close = "Close" if lang == "en" else "Zamknij"
    tpl = """<a class="skip" href="#main">{skip}</a>
<header class="site-head">
  <div class="wrap site-head-in">
    <a class="brand" href="index.html">{brand}<small>{tagline}</small></a>
    <div class="head-right">
      <nav class="nav-inline" aria-label="Menu">
          {inline}
      </nav>
      <span class="lang">
        <a href="{pl_href}" hreflang="pl"{pl_cur}>PL</a><i>/</i><a href="{en_href}" hreflang="en"{en_cur}>EN</a>
      </span>
      <a class="btn" href="contact.html">{cta}</a>
      <button class="menu-btn" type="button" data-drawer-open aria-controls="drawer" aria-label="Menu"><i></i><i></i></button>
    </div>
  </div>
</header>

<div class="drawer" id="drawer" role="dialog" aria-modal="true" aria-label="Menu" data-open="false">
  <div class="drawer-pane">
    <div class="drawer-top">
      <span class="eyebrow">{brand}</span>
      <button class="drawer-close" type="button" data-drawer-close>{close}</button>
    </div>
    <nav class="drawer-nav" aria-label="Menu">
        {drawer_links}
    </nav>
    <div class="drawer-meta">
      <a href="mailto:{email}">{email}</a>
      <a href="tel:{phone_raw}">{phone}</a>
      <a href="{ig}" target="_blank" rel="noopener">Instagram {ig_handle}</a>
    </div>
  </div>
  <div class="drawer-art"><img src="{base}assets/img/md/{drawer_img}.jpg" srcset="{drawer_srcset}" sizes="50vw" alt="" loading="lazy"></div>
</div>"""
    return tpl.format(
        skip=skip, brand=BRAND, tagline=TAG[lang], inline=inline,
        pl_href=pl_href, en_href=en_href,
        pl_cur=' aria-current="true"' if lang == "pl" else "",
        en_cur=' aria-current="true"' if lang == "en" else "",
        cta=nav["contact"], close=close, drawer_links=drawer_links,
        email=EMAIL, phone_raw=PHONE_RAW, phone=PHONE_DISPLAY,
        ig=INSTAGRAM, ig_handle=IG_HANDLE, base=base, drawer_img=HERO[1],
        drawer_srcset=srcset_for(HERO[1]).replace('@@', base))


PIXEL_BASE = """<!-- Meta Pixel -->
<script>
!function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;
n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,
document,'script','https://connect.facebook.net/en_US/fbevents.js');
fbq('init','{id}');fbq('track','PageView');
</script>
<noscript><img height="1" width="1" style="display:none" alt=""
src="https://www.facebook.com/tr?id={id}&ev=PageView&noscript=1"></noscript>
<!-- End Meta Pixel -->"""

CONSENT_BAR = """<script>window.HF_PIXEL_ID="{id}";</script>
<div class="consent" id="consent" hidden>
  <p class="consent-text">{text} <a href="{privacy_href}">{privacy_label}</a></p>
  <div class="consent-actions">
    <button class="btn btn-sm" type="button" data-consent="no">{no}</button>
    <button class="btn btn-sm btn-solid" type="button" data-consent="yes">{yes}</button>
  </div>
</div>"""


def meta_pixel(lang):
    """Meta Pixel. Writes nothing at all while META_PIXEL_ID is empty.

    When META_PIXEL_ASK_CONSENT is on, the page only carries the id and the
    notice; site.js fetches Facebook's script after the visitor accepts, and
    never before. The no-JavaScript <noscript> fallback cannot be gated, so it
    is only used when consent is not required.
    """
    if not META_PIXEL_ID:
        return ""
    if not META_PIXEL_ASK_CONSENT:
        return PIXEL_BASE.replace("{id}", META_PIXEL_ID)
    c = COPY[lang]
    return (CONSENT_BAR.replace("{id}", META_PIXEL_ID)
            .replace("{privacy_href}", "privacy.html")
            .replace("{privacy_label}", "Polityka prywatności" if lang == "pl" else "Privacy policy")
            .replace("{text}", c["consent_text"])
            .replace("{yes}", c["consent_yes"])
            .replace("{no}", c["consent_no"]))


def footer(lang, base, page=""):
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
    privacy_label = "Polityka prywatności" if lang == "pl" else "Privacy policy"
    totop = "Wróć na górę" if lang == "pl" else "Back to top"
    # The Work page is long enough that halfway is a long way down, so there the
    # button appears after a fixed amount of scrolling instead.
    totop_mode = "distance" if page == "work" else "half"
    pixel = meta_pixel(lang)
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
      <span><a href="privacy.html" class="foot-legal">{privacy_label}</a> · {made}</span>
    </div>
  </div>
</footer>
<button class="to-top" type="button" id="to-top" aria-label="{totop}" data-mode="{totop_mode}">
  <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 19V5M5 12l7-7 7 7"/></svg>
</button>
{pixel}
<script src="{base}assets/js/films.js"></script>
<script src="{base}assets/js/site.js"></script>
<script>document.getElementById('yr').textContent=new Date().getFullYear();</script>
</body>
</html>
"""

def lightbox(lang):
    label = "Zdjęcia" if lang == "pl" else "Photographs"
    return f"""  <div class="lb" id="lightbox" hidden role="dialog" aria-modal="true" aria-label="{label}">
    <button class="lb-btn lb-close" type="button" aria-label="&#10005;">&#10005;</button>
    <button class="lb-btn lb-prev" type="button" aria-label="&#8592;">&#8592;</button>
    <button class="lb-btn lb-next" type="button" aria-label="&#8594;">&#8594;</button>
    <img src="" alt="">
    <p class="lb-cap"></p>
  </div>"""

def cta_band(lang, page, base):
    c = COPY[lang]
    stem = CTA_IMG.get(page, "nm-11")
    return f"""  <section class="cta-band">
    <picture>
      <source media="(min-width:900px)" srcset="{base}assets/img/xl/{stem}.jpg">
      <img src="{base}assets/img/lg/{stem}.jpg" alt="" loading="lazy" decoding="async" style="object-position:{focus(stem)}">
    </picture>
    <div class="wrap">
      <h2 class="h-lg" style="max-width:26ch;margin-inline:auto">{c["cta_h"]}</h2>
      <a class="btn btn-solid btn-lg" href="contact.html" style="margin-top:2.2em">{c["cta_btn"]}</a>
    </div>
  </section>"""

def write(lang, page, title, desc, body):
    base = "" if lang == "en" else "../"
    out = (head(lang, page, title, desc, base) + "\n" + header(lang, page, base) +
           '\n<main id="main">\n' + body.replace("@@", base) + "\n</main>\n" + footer(lang, base, page))
    d = OUT if lang == "en" else os.path.join(OUT, "pl")
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, page + ".html"), "w", encoding="utf-8").write(out)

# ================================================================= pages
# column count by width: 1 under 620, 2 under 1040, 3 under 1400, then 4
# Measured, not guessed: the container caps at 1320px with a 72px gutter, so a
# four-column tile is ~285px, not 23vw. Overstating this makes the browser fetch
# the 1600px file for a 285px slot, and 70 of those on one album page is enough
# decoded bitmap that the browser starts re-rasterising tiles at low resolution.
GALLERY_SIZES = ("(min-width:1400px) 285px, (min-width:1040px) 29vw, "
                 "(min-width:620px) 44vw, 90vw")
STRIP_SIZES = "(min-width:460px) 340px, 74vw"


def fig(stem, key, lang, with_caption=True):
    """One gallery tile. data-album scopes the lightbox to that wedding."""
    name = album_name(key, lang)
    cap = f'<figcaption>{name}</figcaption>' if (with_caption and name) else ''
    return (f'<figure><button type="button" data-full="@@assets/img/lg/{stem}.jpg" '
            f'data-album="{key}" data-cap="{name}">'
            f'<img src="@@assets/img/md/{stem}.jpg" srcset="{srcset_for(stem)}" '
            f'sizes="{GALLERY_SIZES}" alt="{alt(stem, lang)}" loading="lazy" decoding="async">'
            f'</button>{cap}</figure>')

def build(lang):
    c = COPY[lang]

    # ---------------------------------------------------------------- home
    # A portrait photograph stretched across a wide screen is a 2.7x upscale and
    # looks soft, so wide screens get a 2560px landscape crop cut at the same
    # focal point. Phones keep the portrait frame, which fits a tall screen.
    hero_imgs = "\n        ".join(
        '<picture>'
        f'<source media="(min-width:900px)" srcset="@@assets/img/xl/{s}.jpg">'
        f'<img src="@@assets/img/lg/{s}.jpg" alt="{alt(s, lang)}"'
        + ('' if i == 0 else ' loading="lazy"')
        + f' decoding="async" style="object-position:{focus(s)}">'
        '</picture>'
        for i, s in enumerate(HERO))
    strip = "\n        ".join(
        f'<figure><a href="{album_page(k)}" aria-label="{album_name(k, lang)}">'
        f'<div class="ph r45"><img src="@@assets/img/md/{s}.jpg" srcset="{srcset_for(s)}" '
        f'sizes="{STRIP_SIZES}" alt="{alt(s, lang)}" loading="lazy" decoding="async"></div>'
        f'<figcaption><span>{album_name(k, lang)}</span><span>{len(PHOTOS[k])} {c["photos_count"]}</span></figcaption>'
        f'</a></figure>' for s, k in STRIP)
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
        <div class="prose dim" style="margin-top:1.2em"><p>{c["s1_p1"]}</p><p>{c["s1_p2"]}</p></div>
        <ul class="specs" style="margin-top:1.6em;max-width:48ch">
            {specs}
        </ul>
      </div>
    </div>
  </section>

  <section class="section tight-bottom">
    <div class="wrap" style="margin-bottom:clamp(18px,2.4vw,32px)">
      <div class="railed">
        <div class="rail reveal"><span>{c["s2_rail1"]}</span><span>{c["s2_rail2"]}</span></div>
        <div class="reveal" style="display:flex;flex-wrap:wrap;gap:18px;align-items:end;justify-content:space-between">
          <h2 class="h-lg" style="max-width:22ch">{c["s2_h"]}</h2>
          <div style="display:flex;align-items:center;gap:12px">
            <div class="strip-nav" data-strip-nav>
              <button type="button" data-strip-prev aria-label="{c["strip_prev"]}">
                <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 19l-7-7 7-7"/></svg>
              </button>
              <button type="button" data-strip-next aria-label="{c["strip_next"]}">
                <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 5l7 7-7 7"/></svg>
              </button>
            </div>
            <a class="btn" href="work.html">{c["s2_btn"]}</a>
          </div>
        </div>
      </div>
    </div>
    <div class="strip strip-links" data-strip>
        {strip}
    </div>
    <div class="wrap"><p class="field-note" style="margin-top:14px">{c["work_album_hint"]}</p></div>
  </section>

  <section class="section tight-top">
    <div class="wrap">
      <div class="quotes" data-quotes>
        <p class="eyebrow" style="margin-bottom:1.5em">{c["s4_eyebrow"]}</p>
          {quotes}
        <div class="quote-nav">
          <button type="button" data-quote-prev aria-label="&#8592;">&#8592;</button>
          <span class="quote-count" data-quote-count>01 / 03</span>
          <button type="button" data-quote-next aria-label="&#8594;">&#8594;</button>
        </div>
      </div>
      <p class="field-note" style="text-align:center;margin-top:1.6em">{c["quote_note"]}</p>
    </div>
  </section>

  <section class="section">
    <div class="wrap split">
      <div class="reveal"><div class="ph r45"><img src="@@assets/img/md/hiroki.jpg" srcset="{srcset_for("hiroki")}" sizes="(min-width:880px) 48vw, 92vw" alt="Hiroki" loading="lazy" decoding="async"></div></div>
      <div class="reveal">
        <p class="eyebrow">{c["s3_eyebrow"]}</p>
        <h2 class="h-lg" style="margin-top:.7em">{c["s3_h"]}</h2>
        <div class="prose dim" style="margin-top:1.4em"><p>{c["s3_p1"]}</p><p>{c["s3_p2"]}</p></div>
        <a class="btn" href="about.html" style="margin-top:2em">{c["s3_btn"]}</a>
      </div>
    </div>
  </section>

{cta_band(lang, "index", "@@")}"""
    write(lang, "index", c["home_title"], c["home_desc"], home)

    # ---------------------------------------------------------------- work
    gal = "\n        ".join(fig(s, k, lang) for s, k in ALL_SHUFFLED)
    album_links = "\n          ".join(
        f'<a class="btn btn-sm" href="{album_page(k)}">{album_name(k, lang)}</a>' for k, *_ in ALBUMS)
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
      <h2 class="h-md" style="margin-bottom:clamp(16px,2.2vw,28px)">{c["films_h"]}</h2>
      <div class="films" data-films></div>
    </div>
  </section>

  <div class="film-modal" id="film-modal" hidden role="dialog" aria-modal="true" aria-label="Film">
    <button class="film-modal-close" type="button" aria-label="&#10005;">&#10005;</button>
    <div class="film-modal-inner">
      <div class="film-modal-frame"></div>
      <p class="film-modal-cap"></p>
    </div>
  </div>

  <section class="section" data-panel="photo">
    <div class="wrap">
      <div style="display:flex;flex-wrap:wrap;gap:16px;align-items:baseline;justify-content:space-between;margin-bottom:clamp(14px,2vw,24px)">
        <h2 class="h-md">{c["photos_h"]}</h2>
        <p class="field-note" style="margin:0">{c["work_album_hint"]}</p>
      </div>
      <div class="album-links">
          {album_links}
      </div>
      <div class="gallery" data-gallery style="margin-top:clamp(16px,2.2vw,28px)">
        {gal}
      </div>
    </div>
  </section>

{lightbox(lang)}

{cta_band(lang, "work", "@@")}"""
    write(lang, "work", c["work_title"], c["work_desc"], work)

    # ---------------------------------------------------------------- albums
    for key, slug, *_ in ALBUMS:
        name = album_name(key, lang)
        shots = PHOTOS[key]
        tiles = "\n        ".join(fig(s, key, lang, with_caption=False) for s in shots)
        others = "\n          ".join(
            f'<a class="btn btn-sm" href="{album_page(k)}">{album_name(k, lang)}</a>'
            for k, *_ in ALBUMS if k != key)
        plain = name.replace("&amp;", "&")
        body = f"""  <section class="section">
    <div class="wrap railed">
      <div class="rail"><span>{c["album_eyebrow"]}</span><span>{len(shots)} {c["photos_count"]}</span></div>
      <div>
        <p class="eyebrow"><a href="work.html" style="text-decoration:none">&#8592; {c["album_back"]}</a></p>
        <h1 class="h-xl" style="margin-top:.5em">{name}</h1>
        <p class="lede dim" style="max-width:44ch;margin-top:1em">{c["album_lede"]}</p>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="gallery" data-gallery>
        {tiles}
      </div>
    </div>
  </section>

{lightbox(lang)}

  <section class="section">
    <div class="wrap railed">
      <div class="rail"><span>{c["albums_h"]}</span></div>
      <div>
        <h2 class="h-lg">{c["albums_h"]}</h2>
        <div class="album-links" style="margin-top:1.6em">
          {others}
        </div>
      </div>
    </div>
  </section>

{cta_band(lang, "album", "@@")}"""
        title = f"{plain} — {BRAND}"
        desc = (f"Zdjęcia ślubne — {plain}." if lang == "pl" else f"Wedding photographs — {plain}.")
        write(lang, "album-" + slug, title, desc, body)

    # ---------------------------------------------------------------- about
    steps = "\n          ".join(f'<li><h3>{t}</h3><p>{p}</p></li>' for t, p in c["about_steps"])
    about = f"""  <section class="section">
    <div class="wrap split">
      <div>
        <p class="eyebrow">{c["about_eyebrow"]}</p>
        <h1 class="h-xl" style="margin-top:.5em">{c["about_h1"]}</h1>
        <p class="lede dim" style="margin-top:1.2em;max-width:34ch">{c["about_lede"]}</p>
      </div>
      <div class="ph r45"><img src="@@assets/img/lg/hiroki.jpg" srcset="{srcset_for("hiroki")}" sizes="(min-width:880px) 45vw, 92vw" alt="Hiroki" decoding="async"></div>
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
      <div class="ph r32 reveal"><img src="@@assets/img/md/da-39.jpg" srcset="{srcset_for("da-39")}" sizes="(min-width:720px) 47vw, 92vw" alt="{alt("da-39", lang)}" loading="lazy" decoding="async"></div>
      <div class="ph r32 reveal offset"><img src="@@assets/img/md/nm-30.jpg" srcset="{srcset_for("nm-30")}" sizes="(min-width:720px) 47vw, 92vw" alt="{alt("nm-30", lang)}" loading="lazy" decoding="async"></div>
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

{cta_band(lang, "about", "@@")}"""
    write(lang, "about", c["about_title"], c["about_desc"], about)

    # ---------------------------------------------------------------- offer
    packs = "\n        ".join(
        f'<article class="pack reveal" data-featured="{"true" if p["featured"] else "false"}">'
        + (f'<p class="pack-tag">★ {p[lang]["tag"]}</p>' if p[lang]["tag"] else f'<p class="pack-tag">0{p["n"]}</p>')
        + f'<h3>{p[lang]["name"]}</h3><p class="pack-len">{p[lang]["len"]}</p>'
          f'<p>{p[lang]["desc"]}</p><p class="pack-price">{p["price"]}</p></article>' for p in PACKS)
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
    <div class="wrap"><div class="packs">
        {packs}
    </div></div>
  </section>

  <section class="section">
    <div class="wrap railed">
      <div class="rail"><span>{c["extras_h"]}</span></div>
      <div><h2 class="h-lg">{c["extras_h"]}</h2>
        <ul class="specs" style="margin-top:1.3em;max-width:60ch">
            {extras}
        </ul></div>
    </div>
  </section>

  <section class="section">
    <div class="wrap railed">
      <div class="rail"><span>{c["general_h"]}</span></div>
      <div><h2 class="h-lg">{c["general_h"]}</h2>
        <ul class="specs" style="margin-top:1.8em;max-width:60ch">
            {general}
        </ul></div>
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

{cta_band(lang, "offer", "@@")}"""
    write(lang, "offer", c["offer_title"], c["offer_desc"], offer)

    # ---------------------------------------------------------------- contact
    opts = "\n                ".join(
        (f'<option value="">{o}</option>' if i == 0 else f'<option>{o}</option>')
        for i, o in enumerate(c["f_cov_opts"]))
    subject = ("Nowe zapytanie ze strony " if lang == "pl" else "New enquiry from ") + DOMAIN
    faq = "\n            ".join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in c["faq"])
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
        <p class="note" style="max-width:58ch;margin-bottom:1.8em">{c["form_note"]}</p>
        <form class="form" id="enquiry" data-mailto="{EMAIL}" novalidate
              action="https://api.web3forms.com/submit" method="POST">
          <input type="hidden" name="access_key" value="{WEB3FORMS_KEY}">
          <input type="hidden" name="subject" value="{subject}">
          <input type="hidden" name="from_name" value="{BRAND}">
          <label class="sr" aria-hidden="true">
            <input type="checkbox" name="botcheck" tabindex="-1" autocomplete="off">
          </label>
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

        <div class="contact-lines" style="margin-top:clamp(20px,2.6vw,32px)">
          <h2 class="h-sm" style="margin-top:clamp(20px,2.6vw,34px)">{c["direct_h"]}</h2>
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


def build_privacy(lang):
    """A page of its own, deliberately not in the menu — reached from the
    footer link and from the cookie notice."""
    d = PRIVACY[lang]
    c = COPY[lang]
    out = []
    for heading, blocks in d["sections"]:
        out.append('      <section class="legal-block">')
        out.append('        <h2 class="h-sm">%s</h2>' % heading)
        for b in blocks:
            if isinstance(b, tuple) and b[0] == "list":
                out.append('        <ul class="legal-list">')
                out.extend('          <li>%s</li>' % i for i in b[1])
                out.append('        </ul>')
            elif isinstance(b, tuple) and b[0] == "consent-reset":
                out.append('        <p><button class="btn" type="button" '
                           'id="consent-reset">%s</button></p>' % c["consent_reset"])
                out.append('        <p class="field-note" id="consent-reset-done" hidden>%s</p>'
                           % c["consent_reset_done"])
            else:
                out.append('        <p>%s</p>' % b)
        out.append('      </section>')
    body = """  <section class="section">
    <div class="wrap railed">
      <div class="rail"><span>{eyebrow}</span><span>{updated}</span></div>
      <div>
        <h1 class="h-xl">{title}</h1>
        <p class="lede dim" style="max-width:46ch;margin-top:1em">{lede}</p>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap railed">
      <div class="rail"><span>{eyebrow}</span></div>
      <div class="legal">
{blocks}
      </div>
    </div>
  </section>""".format(
        eyebrow=("Polityka prywatności" if lang == "pl" else "Privacy policy"),
        updated=(("Aktualizacja: " if lang == "pl" else "Updated ") + PRIVACY_UPDATED[lang]),
        title=d["title"], lede=d["lede"], blocks="\n".join(out))
    title = "%s — %s" % (d["title"], BRAND)
    desc = ("Jakie dane zbiera ta strona, po co i jak je usunąć."
            if lang == "pl" else
            "What this site collects, why, and how to have it removed.")
    write(lang, "privacy", title, desc, body)


def sitemap():
    """Every page, in both languages, each declaring its counterpart.

    Without the hreflang pairs Google treats the Polish and English versions as
    rivals for the same queries instead of as one site in two languages."""
    import datetime
    today = datetime.date.today().isoformat()
    slugs = PAGES + ["privacy"] + ["album-" + s for _, s, *_ in ALBUMS]
    entries = []
    for lang in ("en", "pl"):
        for slug in slugs:
            loc = page_url(lang, slug)
            alts = "".join(
                '\n    <xhtml:link rel="alternate" hreflang="%s" href="%s"/>' % (lg, page_url(lg, slug))
                for lg in ("en", "pl"))
            alts += ('\n    <xhtml:link rel="alternate" hreflang="x-default" href="%s"/>'
                     % page_url("en", slug))
            prio = "1.0" if slug == "index" else ("0.8" if slug in PAGES else "0.6")
            entries.append(
                "  <url>\n    <loc>%s</loc>%s\n    <lastmod>%s</lastmod>"
                "\n    <priority>%s</priority>\n  </url>" % (loc, alts, today, prio))
    open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
        '        xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        + "\n".join(entries) + "\n</urlset>\n")
    open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8").write(
        f"User-agent: *\nAllow: /\nSitemap: https://{DOMAIN}/sitemap.xml\n")
    # GitHub's Pages settings screen rewrites this file without a trailing
    # newline whenever the custom domain is re-saved. Match that, so rebuilding
    # does not produce a pointless diff every time.
    open(os.path.join(OUT, "CNAME"), "w", encoding="utf-8").write(DOMAIN)
    open(os.path.join(OUT, ".nojekyll"), "w").write("")


if __name__ == "__main__":
    for lg in ("en", "pl"):
        build(lg)
        build_privacy(lg)
    sitemap()
    total = sum(len(v) for v in PHOTOS.values())
    print(f"built EN + PL · {len(ALBUMS)} albums · {total} photographs")
