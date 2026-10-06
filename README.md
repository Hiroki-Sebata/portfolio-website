# Hiroki Filmuje — website

Static site. No build step for viewing: the `.html` files in this repo are the site.
Polish lives in `/pl/`, English at the root.

```
index.html  work.html  about.html  offer.html  contact.html     ← English
pl/index.html  pl/work.html  pl/about.html  pl/offer.html  pl/contact.html   ← Polish
assets/css/site.css     all styling
assets/js/site.js       menu, hero, gallery, lightbox, tabs, form
assets/js/films.js      >>> YOUR YOUTUBE LINKS GO HERE <<<
assets/img/lg/          photographs, long edge 1600px (lightbox + hero)
assets/img/md/          photographs, long edge 900px (grids + strips)
build.py                regenerates all ten HTML pages from one copy file
```

## Adding your films

Open `assets/js/films.js` and add one line per film. You only need the video ID —
the part of the YouTube URL after `v=` or after `youtu.be/`:

```js
window.HF_FILMS = [
  { id: "dQw4w9WgXcQ", couple: "Barbara & Michał", place: "Highlight", len: "4:12" },
];
```

Both the Polish and the English pages read this one file. Films load only when a
visitor presses play, so the page stays fast, and the embed uses
`youtube-nocookie.com`.

## Changing text

All copy for both languages sits in the `COPY` dictionary in `build.py`. Edit it,
then run:

```bash
python3 build.py
```

That rewrites all ten HTML pages. Editing an `.html` file directly also works, but
the next `build.py` run will overwrite it.

## Changing photographs

Drop new files into `assets/img/lg/` and `assets/img/md/`, then edit the
`GALLERY_BY_COUPLE`, `HERO` and `STRIP` lists in `build.py`. The gallery order is
generated round-robin so two photographs from the same wedding never sit next to
each other.

Images were resized and had all EXIF metadata (including GPS location) stripped
before being added here.

## The contact form

The form validates what a visitor types and lays it out ready to copy — it does
**not** send email. GitHub Pages serves files only; it cannot run code, so there
is nothing on the server to receive a submission.

To make it actually send, pick one:

- **Formspree** (formspree.io) — free tier, no server. Create a form, then in
  `contact.html` and `pl/contact.html` set
  `<form action="https://formspree.io/f/YOUR_ID" method="POST">` and delete the
  `e.preventDefault()` branch in `assets/js/site.js`.
- **Web3Forms** (web3forms.com) — same idea, email-key based.
- Move the site to a host that runs code (Netlify, Vercel, Cloudflare Pages) and
  use its built-in form handling.

Until then the email address and phone number on the contact page are the route in,
and both have a copy button.

## Custom domain

Add a file named `CNAME` at the repo root containing just the domain, then point
the domain's DNS at GitHub Pages. Settings → Pages in the repo has the current
instructions.
