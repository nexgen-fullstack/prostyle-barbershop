"""Обробка фото: raw -> оптимізовані WebP для сайту."""
from PIL import Image, ImageOps, ImageFilter
from pathlib import Path

RAW = Path("img/raw")
OUT = Path("site/assets/img")
OUT.mkdir(parents=True, exist_ok=True)

def save(src, name, max_w, crop=None, q=80):
    im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    if crop:  # (ratio_w, ratio_h, focus_y)
        rw, rh, fy = crop
        w, h = im.size
        tr = rw / rh
        if w / h > tr:
            nw = int(h * tr); x = (w - nw) // 2; im = im.crop((x, 0, x + nw, h))
        else:
            nh = int(w / tr); y = int((h - nh) * fy); im = im.crop((0, y, w, y + nh))
    if im.width > max_w:
        im = im.resize((max_w, int(im.height * max_w / im.width)), Image.LANCZOS)
    im.save(OUT / f"{name}.webp", "WEBP", quality=q, method=6)
    if name in ("og-image",):
        im.save(OUT / f"{name}.jpg", "JPEG", quality=85, optimize=True)
    print(name, im.size, (OUT / f"{name}.webp").stat().st_size // 1024, "KB")

save(RAW/"gm/g1.jpg", "hero-team", 1100)
save(RAW/"gm/g1.jpg", "hero-team-sm", 640)
save(RAW/"gm/g2.jpg", "storefront", 900, crop=(4, 5, 0.35))
save(RAW/"gm/g3.jpg", "logo-wall", 900, crop=(4, 5, 0.45))
save(RAW/"gm/g4.jpg", "barber-at-work", 900, crop=(4, 5, 0.3))
save(RAW/"gm/g5.jpg", "window", 900, crop=(4, 5, 0.4))
save(RAW/"work8.jpg", "interior", 1400, crop=(16, 10, 0.5))
save(RAW/"shop-sign.jpg", "sign-night", 1024)
save(RAW/"logo.jpg", "logo-3d", 600)
for n in ("alvaro", "elias", "junior", "matheus"):
    save(RAW/f"{n}.jpg", f"team-{n}", 544, q=82)
save(RAW/"work8.jpg", "og-image", 1200, crop=(1200, 630, 0.5), q=82)

# favicon / apple-touch з центру лого (монограма)
logo = Image.open(RAW/"logo.jpg").convert("RGB")
w, h = logo.size
mono = logo.crop((int(w*0.21), int(h*0.0), int(w*0.79), int(h*0.58)))
for s, n in ((180, "apple-touch-icon.png"), (32, "favicon-32.png"), (512, "icon-512.png")):
    mono.resize((s, s), Image.LANCZOS).save(Path("site") / n)
print("icons ok")
