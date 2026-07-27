#!/usr/bin/env python3
"""Generate Android launcher icons from source image."""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SRC = Path(r"F:\Project\e75a40c2-5c68-42b2-baaf-7fb86e3ae228.jpg")
RES = ROOT / "app" / "src" / "main" / "res"


def main() -> None:
    img = Image.open(SRC).convert("RGBA")
    w, h = img.size
    side = min(w, h)
    left = (w - side) // 2
    top = (h - side) // 2
    img = img.crop((left, top, left + side, top + side))

    mipmap_sizes = {
        "mipmap-mdpi": 48,
        "mipmap-hdpi": 72,
        "mipmap-xhdpi": 96,
        "mipmap-xxhdpi": 144,
        "mipmap-xxxhdpi": 192,
    }
    # Adaptive icon foreground (108dp base)
    adaptive_sizes = {
        "drawable-mdpi": 108,
        "drawable-hdpi": 162,
        "drawable-xhdpi": 216,
        "drawable-xxhdpi": 324,
        "drawable-xxxhdpi": 432,
    }

    for folder, size in mipmap_sizes.items():
        d = RES / folder
        d.mkdir(parents=True, exist_ok=True)
        out = img.resize((size, size), Image.Resampling.LANCZOS)
        out.save(d / "ic_launcher.png", "PNG")
        out.save(d / "ic_launcher_round.png", "PNG")
        print(f"mipmap {folder} {size}px")

    for folder, size in adaptive_sizes.items():
        d = RES / folder
        d.mkdir(parents=True, exist_ok=True)
        out = img.resize((size, size), Image.Resampling.LANCZOS)
        out.save(d / "ic_launcher_foreground.png", "PNG")
        print(f"adaptive {folder} {size}px")

    # default density fallback in drawable/
    base = RES / "drawable"
    base.mkdir(parents=True, exist_ok=True)
    img.resize((432, 432), Image.Resampling.LANCZOS).save(base / "ic_launcher_foreground.png", "PNG")

    # remove old vector if present
    old_vec = base / "ic_launcher_foreground.xml"
    if old_vec.exists():
        old_vec.unlink()
        print("removed old vector foreground")

    store = ROOT / "docs" / "store" / "icon_512.png"
    store.parent.mkdir(parents=True, exist_ok=True)
    img.resize((512, 512), Image.Resampling.LANCZOS).save(store, "PNG")

    brand = ROOT / "app" / "src" / "main" / "assets" / "branding"
    brand.mkdir(parents=True, exist_ok=True)
    img.resize((1024, 1024), Image.Resampling.LANCZOS).save(brand / "app_icon.png", "PNG")
    print("OK")


if __name__ == "__main__":
    main()
