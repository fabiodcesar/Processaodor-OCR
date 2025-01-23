FROM nvidia/cuda:11.7.1-cudnn8-runtime-ubuntu22.04

WORKDIR /app

COPY . /app

# Install Python, pip, and system libraries
RUN apt-get update && apt-get install -y \
    python3 python3-pip \
    libgl1 libglib2.0-0 && \
    pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu117 && \
    pip3 install easyocr

CMD ["python3", "ocr-extractor.py"]
