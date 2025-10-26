# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-12-18

### Added
- Initial release of CRC WSI preprocessing pipeline
- Command-line interface for batch processing
- Automatic tissue detection using HSV color space
- Tile extraction with configurable thresholds
- Quality control montage generation
- Docker support for containerized deployment
- Thumbnail generation (RGB, S-channel, mask, overlay)
- CSV indexing for tiles and slides
- Multi-worker support for parallel tiling

### Features
- Process whole slide images (.svs, .tiff)
- Configurable tile size and downsample factors
- Strict and relaxed tissue filtering modes
- Skip existing slides for incremental processing
- Label support via CSV files

[1.0.0]: https://github.com/filip-sec/crc-preproc/releases/tag/v1.0.0
