# Gunakan image yang ringan
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install dependencies sistem (Poppler untuk pdf2image dan libgl untuk OpenCV)
RUN apt-get update && apt-get install -y --no-install-recommends \
    poppler-utils \
    libgl1 \
    libglib2.0-0 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements dan install dependencies
# Gunakan --no-cache-dir untuk menghemat ruang
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy semua source code
COPY . .

# Pre-download model EasyOCR agar tidak memakan RAM saat runtime pertama kali
# Ini akan mendownload model bahasa Indonesia dan Inggris saat proses build
RUN python -c "import easyocr; reader = easyocr.Reader(['id', 'en'], gpu=False)"

# Expose port FastAPI
EXPOSE 8000

# Jalankan aplikasi menggunakan uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]