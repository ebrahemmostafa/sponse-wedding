"""Render the shareable invitation card from config.js.

  python tools/make_card.py

Writes assets/images/share-card.png (1080x1350, to send as an image)
and assets/images/og-card.jpg (1200x630, the WhatsApp/link preview).
"""
import json, os, subprocess
from datetime import datetime, timedelta, timezone
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
IMG = os.path.join(ROOT, "assets", "images")
F = os.path.join(HERE, "fonts")

S = 2  # supersample
W, H = 1080 * S, 1350 * S
IVORY = (247, 241, 230)
GARNET = (122, 23, 18)
INK = (74, 20, 27)
SILVER_TXT = (128, 120, 108)


def config():
    js = "global.window={};require(process.argv[1]);console.log(JSON.stringify(window.INVITE))"
    out = subprocess.check_output(["node", "-e", js, os.path.join(ROOT, "config.js")])
    return json.loads(out)


def font(name, size, wght=None):
    f = ImageFont.truetype(os.path.join(F, name), size)
    if wght:
        try:
            f.set_variation_by_axes([wght])
        except Exception:
            pass
    return f


def velvet(w, h):
    tile = Image.open(os.path.join(IMG, "velvet.webp")).convert("RGB")
    tile = tile.resize((tile.width * S, tile.height * S), Image.LANCZOS)
    bg = Image.new("RGB", (w, h))
    for y in range(0, h, tile.height):
        for x in range(0, w, tile.width):
            bg.paste(tile, (x, y))
    a = np.asarray(bg).astype(np.float32)
    yy, xx = np.mgrid[0:h, 0:w]
    r = np.sqrt(((xx - w / 2) / w) ** 2 + ((yy - h * .45) / h) ** 2)
    a *= np.clip(1.15 - 1.1 * r, .45, 1.1)[..., None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def paper(w, h):
    rng = np.random.default_rng(7)
    n = rng.normal(0, 1, (h // 2, w // 2)).astype(np.float32)
    n = np.asarray(Image.fromarray(((n * 18) + 128).clip(0, 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)).astype(np.float32) - 128
    base = np.ones((h, w, 3), np.float32) * np.array(IVORY, np.float32)
    base += n[..., None] * np.array([.10, .09, .08])
    return base


def curtains(card, w, h):
    """Open curtains fitted to the card height, each half anchored to its edge, multiplied onto ivory."""
    cur = Image.open(os.path.join(IMG, "curtain-open.jpg")).convert("RGB")
    s = h / cur.height
    cw = int(cur.width * s)
    cur = cur.resize((cw, h), Image.LANCZOS)
    c = np.asarray(cur).astype(np.float32) / 255
    half = cw // 2
    layer = np.ones((h, w, 3), np.float32)
    layer[:, :half] = c[:, :half]
    layer[:, w - (cw - half):] = c[:, half:]
    return card * layer


def silver_cupid(size):
    cup = Image.open(os.path.join(IMG, "cupid.png")).convert("RGBA").resize((size, size), Image.LANCZOS)
    a = np.asarray(cup)[..., 3].astype(np.float32) / 255
    g = np.linspace(0, 1, size)[:, None]
    col = (np.array([176, 168, 156]) * (1 - g) + np.array([96, 88, 79]) * g)[..., None, :].repeat(size, 1)
    blur = np.asarray(Image.fromarray((a * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.4))).astype(np.float32) / 255
    hi = np.clip(np.roll(blur, (-2, -2), (0, 1)) - blur, 0, 1)
    col = col + hi[..., None] * 90
    rgba = np.dstack([np.clip(col, 0, 255), a * 255]).astype(np.uint8)
    return Image.fromarray(rgba, "RGBA")


def centered(d, cx, y, text, f, fill, spacing=0):
    if spacing:
        widths = [d.textlength(ch, font=f) for ch in text]
        total = sum(widths) + spacing * (len(text) - 1)
        x = cx - total / 2
        for ch, w_ in zip(text, widths):
            d.text((x, y), ch, font=f, fill=fill)
            x += w_ + spacing
        return
    w_ = d.textlength(text, font=f)
    d.text((cx - w_ / 2, y), text, font=f, fill=fill)


def main():
    c = config()
    when = datetime.fromisoformat(c["date"])
    one, two = c["couple"]["one"], c["couple"]["two"]

    img = velvet(W, H)
    # card
    m = 84 * S
    cw, ch = W - 2 * m, H - 2 * m
    card = curtains(paper(cw, ch), cw, ch)
    card_img = Image.fromarray(np.clip(card, 0, 255).astype(np.uint8))
    shadow = Image.new("L", (W, H), 0)
    ImageDraw.Draw(shadow).rectangle((m, m + 14 * S, m + cw, m + ch + 14 * S), fill=170)
    shadow = shadow.filter(ImageFilter.GaussianBlur(28 * S))
    img = Image.composite(Image.new("RGB", (W, H), (12, 2, 4)), img, shadow)
    img.paste(card_img, (m, m))
    d = ImageDraw.Draw(img)
    d.rectangle((m, m, m + cw - 1, m + ch - 1), outline=(189, 182, 170), width=2 * S)

    cx = W / 2
    y0 = m
    # cupid seal
    cup = silver_cupid(190 * S)
    img.paste(cup, (int(cx - cup.width / 2 + 8 * S), y0 + 92 * S), cup)

    serif_i = font("CormorantGaramond-Italic[wght].ttf", 34 * S, 400)
    serif = font("CormorantGaramond[wght].ttf", 34 * S, 400)
    serif_m = font("CormorantGaramond[wght].ttf", 36 * S, 500)
    sc = font("CormorantSC-Medium.ttf", 27 * S)
    script = font("GreatVibes-Regular.ttf", 138 * S)
    amp = font("GreatVibes-Regular.ttf", 64 * S)

    centered(d, cx, y0 + 314 * S, c["hero"]["above"], serif_i, INK)
    centered(d, cx, y0 + 364 * S, one, script, GARNET)
    centered(d, cx, y0 + 498 * S, "&", amp, SILVER_TXT)
    centered(d, cx, y0 + 544 * S, two, script, GARNET)
    centered(d, cx, y0 + 738 * S, c["hero"]["below"], serif, INK)

    # hairline with a centre knot
    ky = y0 + 822 * S
    d.line((cx - 70 * S, ky, cx - 12 * S, ky), fill=(189, 182, 170), width=S)
    d.line((cx + 12 * S, ky, cx + 70 * S, ky), fill=(189, 182, 170), width=S)
    d.ellipse((cx - 4 * S, ky - 4 * S, cx + 4 * S, ky + 4 * S), fill=SILVER_TXT)

    date_line = f"{when.strftime('%A')} {when.day} {when.strftime('%B')} {when.year}"
    time_line = when.strftime("%I:%M %p").lstrip("0")
    centered(d, cx, y0 + 852 * S, date_line, sc, GARNET, spacing=3 * S)
    centered(d, cx, y0 + 894 * S, time_line, sc, SILVER_TXT, spacing=3 * S)
    centered(d, cx, y0 + 958 * S, c["venue"]["name"], serif_m, INK)
    city = c["venue"]["address"].split(",")[-1].strip()
    centered(d, cx, y0 + 1006 * S, city, serif_i, (109, 86, 80))

    out = img.resize((W // S, H // S), Image.LANCZOS)
    out.save(os.path.join(IMG, "share-card.png"), optimize=True)

    # link preview: card on velvet, 1200x630
    og = velvet(1200 * S, 630 * S).resize((1200, 630), Image.LANCZOS)
    small = out.crop((84, 84, 1080 - 84, 1350 - 84))
    small = small.resize((int(small.width * 590 / small.height), 590), Image.LANCZOS)
    og.paste(small, ((1200 - small.width) // 2, 20))
    og.save(os.path.join(IMG, "og-card.jpg"), quality=88)
    print("wrote share-card.png and og-card.jpg")


if __name__ == "__main__":
    main()
