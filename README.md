# Hiroki Filmuje — website

Static site. **GitHub Pages serves the `docs/` folder on `main`** — that is the
setting already chosen in the repo, so everything published lives in `docs/`.

```
build.py                 generates every page; run it after any change
copy.py                  ALL wording, Polish and English — edit here
docs/                    <- this folder is the live website
  index.html work.html about.html offer.html contact.html        English
  album-*.html                                                   one per wedding
  pl/...                                                         Polish, same names
  assets/css/site.css    styling
  assets/js/site.js      menu, hero, gallery, lightbox, tabs, form
  assets/js/films.js     >>> YOUR YOUTUBE LINKS <<<
  assets/img/lg/         photographs, long edge 1600px (lightbox, hero)
  assets/img/md/         photographs, long edge 900px (grids)
  CNAME                  hiroki-filmuje.pl
  sitemap.xml robots.txt
```

Rebuild after editing `copy.py` or `build.py`:

```bash
python3 build.py
```

## Adding a film

`docs/assets/js/films.js`. You only need the video ID — the part of the YouTube
URL after `v=` or after `youtu.be/`:

```js
{ id: "XPw7D7KUssw", couple: "Monika & Julien", titleEn: "A Celebration of Love",
  titlePl: "A Celebration of Love", len: "" },
```

Both languages read this one file. Films load only when someone presses play, so
the page stays fast, and the embed uses `youtube-nocookie.com`.

## Adding a wedding

1. Export the photographs as `<key>-<number>.jpg` into **both** `docs/assets/img/lg/`
   and `docs/assets/img/md/` (1600px and 900px long edge).
2. Add the wedding to the `ALBUMS` list in `build.py`:
   `("key", "page-slug", "Name EN", "Name PL")`.
3. Optionally put one of its frames in `STRIP` in `build.py` to show it on the
   home page.
4. `python3 build.py`.

The Work page picks up every photograph automatically and shuffles them with a
fixed seed, so the mix looks random but does not reshuffle on every rebuild. The
lightbox only ever pages through the wedding that was clicked.

Photographs are resized and have all EXIF metadata, including GPS, stripped.

## The contact form

It validates what a visitor types and formats it for copying — it does **not**
send email. GitHub Pages serves files only; it cannot run code, so there is
nothing on the server to receive a submission.

To make it send, the quickest route is **Formspree** or **Web3Forms**: sign up,
get a form URL, then in `build.py` give the `<form>` an `action` and `method="POST"`
and remove the `e.preventDefault()` branch in `docs/assets/js/site.js`. Or move
the site to Netlify or Cloudflare Pages, which handle forms themselves.

## Domain

`docs/CNAME` contains `hiroki-filmuje.pl`. For that to work the domain's DNS must
point at GitHub, which is done at the registrar (seohost), not here:

| Type  | Host | Value |
|-------|------|-------|
| A     | @    | 185.199.108.153 |
| A     | @    | 185.199.109.153 |
| A     | @    | 185.199.110.153 |
| A     | @    | 185.199.111.153 |
| CNAME | www  | hiroki-sebata.github.io. |

Delete any existing A record for `@` pointing somewhere else first.

## Photo cropping on wide screens

Hero and full-width band photographs are cropped by the browser to fill the
space. A laptop window is far wider than it is tall, so a portrait frame loses
its top and bottom — and with the default centre anchor that cuts faces off.

`FOCUS` in `build.py` sets where each of those photographs is anchored:

```python
FOCUS = { "nm-39": "50% 20%" }   # horizontal, vertical — smaller = keep more of the top
```

Anything not listed uses `FOCUS_DEFAULT`. Phones are tall enough that there is
little cropping, which is why the same photographs look complete there.
