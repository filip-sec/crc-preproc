"""Tile WSI based on tissue mask."""

from tqdm import tqdm

from .io_utils import alpha_to_white


def tile_wsi(
    slide, mask_thumb, tw_th, W0_H0, out_dir, slide_id, tile_px=512, strict=True
):
    """Extract tiles from WSI, filtering by tissue mask."""
    tw, th, W0, H0 = *tw_th, *W0_H0
    sx, sy = tw / W0, th / H0
    out_dir.mkdir(parents=True, exist_ok=True)

    rows, saved = [], 0

    for y in tqdm(range(0, H0, tile_px), desc=slide_id, leave=False):
        for x in range(0, W0, tile_px):
            if x + tile_px > W0 or y + tile_px > H0:
                continue

            # Map level-0 tile to thumbnail ROI
            tx0, ty0, tx1, ty1 = (
                max(0, min(tw, int(x * sx))),
                max(0, min(th, int(y * sy))),
                max(0, min(tw, int((x + tile_px) * sx))),
                max(0, min(th, int((y + tile_px) * sy))),
            )

            roi = mask_thumb[ty0:ty1, tx0:tx1]

            # Tissue check
            if roi.size and (
                roi.min() == 255 if strict else (roi == 255).mean() >= 0.95
            ):
                try:
                    out_path = out_dir / f"{slide_id}_x{x}_y{y}.png"
                    alpha_to_white(
                        slide.read_region((x, y), 0, (tile_px, tile_px))
                    ).save(out_path, optimize=True)
                    # Store relative path from tiles_dir (slide_id/)
                    rel_path = out_path.relative_to(out_dir)
                    rows.append(
                        {
                            "slide_id": slide_id,
                            "x": x,
                            "y": y,
                            "tile_px": tile_px,
                            "file": str(rel_path),
                        }
                    )
                    saved += 1
                except Exception:
                    pass

    return rows, saved
