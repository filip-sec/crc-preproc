"""Quality control montage generation."""

import math
import random
from pathlib import Path

import numpy as np
from PIL import Image


def save_qc(tile_dir, out_png, n=64, size=128):
    """Generate QC montage from random sample of tiles."""
    if not (paths := list(tile_dir.glob("*.png"))):
        return

    random.shuffle((paths := paths[:n]))

    cols = int(math.sqrt(n))
    rows = int(np.ceil(n / cols))
    canvas = Image.new("RGB", (cols * size, rows * size), (255, 255, 255))

    for i, (r, c) in enumerate(
        [(r, c) for r in range(rows) for c in range(cols)][: len(paths)]
    ):
        try:
            canvas.paste(
                Image.open(paths[i])
                .convert("RGB")
                .resize((size, size), Image.BILINEAR),
                (c * size, r * size),
            )
        except Exception as e:
            print(f"Failed to process {paths[i]}: {e}")

    canvas.save(out_png, optimize=False)
