"""Tests for tissue module."""

import numpy as np
import cv2

from crc_preproc.tissue import extract_s_channel, otsu_mask


def test_extract_s_channel():
    """Test S-channel extraction from RGB."""
    # Create a test RGB image
    rgb = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)

    S = extract_s_channel(rgb)

    assert S.shape == (100, 100)
    assert S.dtype == np.uint8
    assert S.min() >= 0
    assert S.max() <= 255


def test_otsu_mask():
    """Test Otsu thresholding."""
    # Create a synthetic S-channel image with distinct regions
    S = np.zeros((100, 100), dtype=np.uint8)
    # High saturation region
    S[20:40, 20:40] = 200
    # Low saturation region
    S[60:80, 60:80] = 30

    mask = otsu_mask(S)

    assert mask.shape == (100, 100)
    assert mask.dtype == np.uint8
    assert mask.min() == 0 or mask.min() == 255
    assert mask.max() == 0 or mask.max() == 255


def test_otsu_mask_with_opening_closing():
    """Test Otsu mask with morphological operations."""
    S = np.random.randint(0, 256, (50, 50), dtype=np.uint8)

    mask = otsu_mask(S, open_close=3)

    assert mask.shape == (50, 50)
    assert mask.dtype == np.uint8


def test_otsu_mask_with_min_frac():
    """Test Otsu mask with minimum fraction filtering."""
    # Create image with one large component
    S = np.zeros((100, 100), dtype=np.uint8)
    S[10:50, 10:50] = 255

    mask = otsu_mask(S, min_frac=0.05)

    assert mask.shape == (100, 100)
    assert mask.dtype == np.uint8
