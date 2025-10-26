"""Tests for io_utils module."""

from pathlib import Path
from PIL import Image

from crc_preproc.io_utils import alpha_to_white, slide_key


def test_slide_key():
    """Test slide key extraction."""
    # Test .svs extension
    assert slide_key("slide.svs") == "slide"
    assert slide_key("data/slide.svs") == "slide"
    assert slide_key("path/to/CRC_0000.svs") == "CRC_0000"

    # Test different extensions
    assert slide_key("slide.tiff") == "slide"
    assert slide_key("slide.TIF") == "slide"
    assert slide_key("slide.scn") == "slide"

    # Test without extension
    assert slide_key("slide") == "slide"

    # Test with path
    assert slide_key(Path("path/to/CRC_0001.svs")) == "CRC_0001"


def test_slide_key_case_insensitive():
    """Test case insensitive matching."""
    assert slide_key("SLIDE.SVS") == "SLIDE"
    assert slide_key("Slide.TifF") == "Slide"


def test_alpha_to_white_rgb():
    """Test alpha_to_white with RGB image."""
    img = Image.new("RGB", (10, 10), color=(255, 0, 0))
    result = alpha_to_white(img)

    assert result.mode == "RGB"
    assert result.size == (10, 10)


def test_alpha_to_white_rgba():
    """Test alpha_to_white with RGBA image."""
    img = Image.new("RGBA", (10, 10), color=(0, 255, 0, 128))
    result = alpha_to_white(img)

    assert result.mode == "RGB"
    assert result.size == (10, 10)
    # The result should be composited to white background
    assert result.mode != "RGBA"
