# CRC WSI Preprocessing Pipeline

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-success.svg)](https://github.com/filip-sec/crc-preproc)

Whole Slide Image preprocessing pipeline for CRC (Colorectal Cancer) analysis.

## Features

- 🧬 Automatic tissue detection and masking
- 🖼️ Multi-resolution thumbnail generation
- ✂️ Intelligent tiling with configurable thresholds
- 📊 Quality control montages
- 🐳 Docker support for reproducible processing
- ⚡ Parallel processing for efficient batch operations

## Project Structure

```
project/
├─ data/
│  ├─ wsi/                 # Whole Slide Images (.svs, .tiff)
│  ├─ images/              # All generated images
│  │  ├─ thumbs/           # Thumbnails, S-channel, masks, overlays
│  │  └─ tiles/            # Per-slide tile folders (PNG/TIFF)
│  └─ labels/              # Labels and generated indexes
│     ├─ labels.csv        # Slide-level labels (0/1/2)
│     ├─ tiles_index.csv   # Auto-generated
│     └─ slides_index.csv  # Auto-generated
└─ crc_preproc/            # Python package
   ├─ io_utils.py          # I/O utilities
   ├─ tissue.py            # Tissue detection
   ├─ tiler.py             # Tiling logic
   ├─ labels.py            # Label loading
   ├─ qc.py                # Quality control
   ├─ runner.py            # Process single slide
   └─ cli.py               # Command-line interface
```

## Usage

```bash
# Process all slides
python -m crc_preproc.cli \
  --wsi_dir data/wsi \
  --pattern "*.svs" \
  --labels_csv data/labels/labels.csv \
  --out_dir .

# Options:
#   --downsample 32        # Thumbnail downsample factor
#   --tile_px 512          # Tile size in pixels
#   --relax                 # Use 95% tissue threshold (default: 100%)
#   --skip_existing         # Skip already processed slides
#   --num_workers 4        # Number of parallel workers for tiling

# Process single slide (testing)
python -m crc_preproc.cli \
  --wsi_dir data/wsi \
  --pattern "CRC_0001.svs" \
  --labels_csv data/labels/labels.csv \
  --out_dir .
```

## Output

- **Tiles**: `data/images/tiles/{slide_id}/`
- **Thumbnails**: `data/images/thumbs/`
- **CSV Index**: `data/labels/{slide_id}_tiles.csv`
- **QC Montage**: `data/images/tiles/{slide_id}_QC.png`

## Installation

### Local Installation

```bash
pip install -e .
```

### Docker (Recommended)

```bash
# Build image
docker build -t crc-preproc .

# Run with your data mounted
docker run -v $(pwd)/data:/app/data crc-preproc \
  python -m crc_preproc.cli \
  --wsi_dir /app/data/wsi \
  --pattern "*.svs" \
  --labels_csv /app/data/labels/labels.csv \
  --out_dir /app
```
