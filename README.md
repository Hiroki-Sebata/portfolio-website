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

`docs/assets/js/films.js`. Each entry becomes one row on the Work page — poster
on one side, your writing on the other, alternating sides down the page. Clicking
the poster opens the film in a window over the site.

```js
{
  type: "youtube",            // or "drive"
  id: "XPw7D7KUssw",          // YouTube: after v= or youtu.be/
                              // Drive:   the id between /d/ and /view
  poster: "mj",               // a file in docs/assets/img/film/  (without .jpg)
  couple: "Monika & Julien",
  titleEn: "A Celebration of Love", titlePl: "A Celebration of Love",
  textEn: "...", textPl: "...",
}
```

A poster should be 16:9 and about 1280px wide. For a Drive video you can usually
grab one with
`https://drive.google.com/thumbnail?id=THE_ID&sz=w1600`; otherwise crop a frame
from that wedding's photographs.

**Drive videos must be shared as "Anyone with the link"**, or the player shows
nothing.

All six films are currently Drive files.

If you ever use YouTube again, note that an embedded YouTube video shows
*"error 153"* when the page sends no referrer — which is what happens if you open
an `.html` file straight from Finder. That is not a broken setting. Test over a
real address instead:

```bash
cd docs && python3 -m http.server 8000     # then open http://localhost:8000
```

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

The form posts to **Web3Forms**, which emails the enquiry to `sebasuta@gmail.com`.
No server of our own is involved, which is what makes it work on GitHub Pages.

The access key lives in `build.py` as `WEB3FORMS_KEY` and is written into both
contact pages. Web3Forms keys are *meant* to be public — the key sits in the page
source of every site that uses one. Spam is held back by a hidden `botcheck`
field. If the key is ever abused, generate a new one at web3forms.com and change
that one line.

The page submits with `fetch`, so the visitor stays put and sees a message in
place. If the request fails for any reason, the form shows what they wrote,
formatted for copying, along with the email address — nothing typed is lost.
With JavaScript switched off, the plain `action="https://api.web3forms.com/submit"`
still works; the visitor just lands on Web3Forms' own confirmation page.

Note: Web3Forms refuses submissions sent from a server (curl and the like) on the
free plan. Test it from a browser.

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
