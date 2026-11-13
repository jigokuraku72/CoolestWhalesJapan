# The Whale and the Blue Planet — Ukiyo-e

coolest-art-01 entry.

A giant whale swims through the galaxy in classic Japanese ukiyo-e
woodblock print style, its mouth open around a glowing blue planet.
Bold woodblock linework, deep indigo night palette with cream and
red accents, stylized waves and clouds. The image is resized to fit
within 1024x1024 without cropping, so the whole scene — whale, blue
planet, and stars — stays intact.

## Files

- `entry.png` — the artwork (1024x683, JPEG bytes, uncropped)
- `main.py` — copies `entry.png` to the output directory and verifies
  size, SHA-256, JPEG magic bytes, and dimensions
- `LICENSE` — MIT

## How it works

`main.py` reads the output directory from `MAKEFUN_OUTPUT_DIR` and
falls back to `/output` when it is not set (the grader's Docker
container does not set it). It verifies the source image before
copying and verifies the written file afterwards.
