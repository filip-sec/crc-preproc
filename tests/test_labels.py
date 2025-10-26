"""Tests for labels module."""

import pandas as pd
from pathlib import Path
from tempfile import NamedTemporaryFile

from crc_preproc.labels import build_labels


def test_build_labels_empty():
    """Test build_labels with non-existent file."""
    result = build_labels(Path("/nonexistent/file.csv"))
    assert result == {}


def test_build_labels_none():
    """Test build_labels with None."""
    result = build_labels(None)
    assert result == {}


def test_build_labels_valid_csv():
    """Test build_labels with valid CSV."""
    # Create a test CSV
    with NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write("filename,label\n")
        f.write("CRC_0000.svs,0\n")
        f.write("CRC_0001.svs,1\n")
        csv_path = f.name

    try:
        result = build_labels(Path(csv_path))

        assert "CRC_0000" in result
        assert "CRC_0001" in result
        assert result["CRC_0000"] == 0
        assert result["CRC_0001"] == 1
    finally:
        Path(csv_path).unlink()


def test_build_labels_different_column_names():
    """Test build_labels with different column names."""
    with NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write("slide_name,slide_label\n")
        f.write("CRC_0000.svs,2\n")
        f.write("CRC_0001.tiff,1\n")
        csv_path = f.name

    try:
        result = build_labels(Path(csv_path))

        assert "CRC_0000" in result
        assert "CRC_0001" in result
        assert result["CRC_0000"] == 2
        assert result["CRC_0001"] == 1
    finally:
        Path(csv_path).unlink()


def test_build_labels_no_matching_columns():
    """Test build_labels with CSV missing required columns."""
    with NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write("id,name\n")
        f.write("1,test\n")
        csv_path = f.name

    try:
        result = build_labels(Path(csv_path))
        assert result == {}
    finally:
        Path(csv_path).unlink()
