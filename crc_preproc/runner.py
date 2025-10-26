"""Process single WSI."""

import numpy as np
import openslide
import pandas as pd
from PIL import Image

from .io_utils import slide_key
from .qc import save_qc
from .tiler import tile_wsi
from .tissue import extract_s_channel, make_thumbnail, otsu_mask


def process_one(
    wsi_path,
    out_root,
    labels_map,
    downsample=32,
    tile_px=512,
    strict=True,
    skip=False,
):
    """Process a single WSI: thumbnail, mask, tile, save CSV."""
    slide_id = slide_key(wsi_path)

    # New structure: data/images/{thumbs,tiles}, data/labels/
    img_root = out_root / "data" / "images"
    labels_dir = out_root / "data" / "labels"

    thumb_dir = img_root / "thumbs"
    tiles_dir = img_root / "tiles"
    csv_path = labels_dir / f"{slide_id}_tiles.csv"

    # Skip if already processed
    if skip and csv_path.exists():
        df = pd.read_csv(csv_path)
        if df.empty or "label" not in df.columns or df["label"].isna().all():
            pass  # Labels missing, regenerate
        else:
            return slide_id, len(df), labels_map.get(slide_id)

    # Open slide
    slide = openslide.OpenSlide(str(wsi_path))
    thumb_rgb, (tw, th), (W0, H0) = make_thumbnail(slide, downsample)
    S = extract_s_channel(thumb_rgb)
    mask = otsu_mask(S)

    # Save thumbnails
    thumb_dir.mkdir(parents=True, exist_ok=True)
    for name, arr in [("thumb_rgb", thumb_rgb), ("thumb_S", S), ("thumb_mask", mask)]:
        Image.fromarray(arr).save(thumb_dir / f"{slide_id}_{name}.png", optimize=False)

    # Save overlay
    ov = thumb_rgb.copy()
    ov[mask == 255] = (0.5 * ov[mask == 255] + 0.5 * np.array([0, 255, 0])).astype(
        np.uint8
    )
    Image.fromarray(ov).save(
        thumb_dir / f"{slide_id}_thumb_overlay.png", optimize=False
    )

    # Tile WSI
    rows, saved = tile_wsi(
        slide,
        mask,
        (tw, th),
        (W0, H0),
        tiles_dir / slide_id,
        slide_id,
        tile_px,
        strict,
    )
    slide.close()

    # Save CSV
    df = pd.DataFrame(rows)
    df["label"] = labels_map.get(slide_id, "")
    df.to_csv(csv_path, index=False)

    # QC montage
    if saved > 0:
        save_qc(
            tiles_dir / slide_id,
            tiles_dir / f"{slide_id}_QC.png",
        )

    return slide_id, saved, labels_map.get(slide_id)
