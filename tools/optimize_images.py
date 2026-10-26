#!/usr/bin/env python3
"""Make smaller WebP copies of the blog images. Needs Pillow (pip install pillow).

    python3 tools/optimize_images.py

For every PNG or JPG in assets/blog/<slug>/ it writes <name>-<width>.webp at a few widths
(never wider than the original). tools/build_blog.py picks these up and serves them with
srcset, so phones download a small file and the original stays as the fallback.
Run it after adding images, then run the build.
"""
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
WIDTHS = (320, 640, 960, 1280, 1920)

for path in sorted((ROOT / "assets" / "blog").glob("*/*")):
    if path.suffix.lower() not in (".png", ".jpg", ".jpeg"):
        continue
    with Image.open(path) as im:
        im.load()
        targets = [w for w in WIDTHS if w < im.width] + [im.width]
        for w in targets:
            out = path.with_name(f"{path.stem}-{w}.webp")
            h = round(im.height * w / im.width)
            im.resize((w, h), Image.LANCZOS).save(out, "WEBP", quality=80, method=6)
            print(f"{out.relative_to(ROOT)}  {out.stat().st_size // 1024} KiB")
