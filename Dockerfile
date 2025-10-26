FROM python:3.10-slim

# Install system dependencies for OpenSlide and OpenCV
RUN apt-get update && apt-get install -y \
    libopenslide0 \
    libopenslide-dev \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY crc_preproc/ ./crc_preproc/
COPY setup.py .
RUN pip install -e .

# Default command
CMD ["python", "-m", "crc_preproc.cli", "--help"]
