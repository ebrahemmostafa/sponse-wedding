# Wedding invitation

A single-page wedding invitation that mixes two templates: the silver envelope and photobooth from one, and the theatre curtain, scratch-to-reveal date, menu frame and dress code from the other.

**Flow:** tap the envelope to open it → the curtains open on the names → the silver photobooth prints a photo strip → scratch the silver disc to reveal the date (with countdown and add-to-calendar) → venue → programme → dress code → RSVP over WhatsApp.

## Edit the content

All text, the date, venue, programme and the WhatsApp number for RSVPs are in [`config.js`](config.js).

- **Photos for the photobooth strip:** put up to 3 images in `assets/photos/` and list them in `photos` in `config.js`. They print in black and white.
- **Initials on the envelope:** the envelope image and opening video are rendered with your initials:

  ```bash
  python tools/personalize_envelope.py --initials "Y&M"
  python tools/personalize_envelope.py --initials "Y&M" --photo assets/photos/us.jpg   # your photo in the oval instead of the cupid
  ```

  Needs Python with `opencv-python`, `numpy`, `pillow`, and `ffmpeg` on the PATH.
- **Share card + link preview:** after editing `config.js`, rebuild the image you send on WhatsApp (`assets/images/share-card.png`) and the link preview (`assets/images/og-card.jpg`):

  ```bash
  python tools/make_card.py
  ```

## Run locally

```bash
python -m http.server 8000
```

Then open http://localhost:8000.

## Publish

It is a static site, so it can be hosted anywhere. On GitHub Pages: repo **Settings → Pages → Deploy from branch → `main` / root**.
