"""Tissue detection via thumbnail and Otsu masking."""

import numpy as np
import cv2


def make_thumbnail(slide, downsample=32):
    """Generate RGB thumbnail from WSI."""
    W0, H0 = slide.dimensions
    thumb_np = np.array(
        slide.get_thumbnail(
            (max(1, W0 // downsample), max(1, H0 // downsample))
        ).convert("RGB")
    )
    thumb_size = (max(1, W0 // downsample), max(1, H0 // downsample))
    slide_size = (W0, H0)
    return thumb_np, thumb_size, slide_size


def extract_s_channel(thumb_rgb):
    """Extract HSV saturation channel from RGB thumbnail."""
    return cv2.cvtColor(thumb_rgb, cv2.COLOR_RGB2HSV)[:, :, 1]


def otsu_mask(S, open_close=5, min_frac=1e-3):
    """Create binary tissue mask using Otsu thresholding."""
    _, mask = cv2.threshold(S, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    if open_close > 0:
        k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (open_close, open_close))
        mask = cv2.morphologyEx(
            cv2.morphologyEx(mask, cv2.MORPH_OPEN, k), cv2.MORPH_CLOSE, k
        )

    if min_frac > 0:
        H, W = mask.shape
        n, lab, stats, _ = cv2.connectedComponentsWithStats(mask, connectivity=8)
        keep = stats[1:, cv2.CC_STAT_AREA] >= int(min_frac * H * W)
        mask = np.concatenate([[False], keep])[lab].astype(np.uint8) * 255

    return mask
