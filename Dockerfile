# ── Base image ────────────────────────────────────────────────────────────────
# Use the official CUDA + cuDNN runtime so onnxruntime-gpu works out of the box.
# Swap to python:3.11-slim if you only need CPU inference.
FROM nvidia/cuda:12.2.0-cudnn8-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# ── System deps ───────────────────────────────────────────────────────────────
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.11 python3.11-dev python3-pip \
    libglib2.0-0 libsm6 libxext6 libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

RUN ln -sf /usr/bin/python3.11 /usr/bin/python && \
    ln -sf /usr/bin/pip3      /usr/bin/pip

# ── Python deps ───────────────────────────────────────────────────────────────
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── Pre-download buffalo_l model so the first request isn't slow ──────────────
RUN python -c "\
from insightface.app import FaceAnalysis; \
fa = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider']); \
fa.prepare(ctx_id=-1, det_size=(640,640)); \
print('buffalo_l downloaded.')"

# ── App source ────────────────────────────────────────────────────────────────
COPY main.py face_service.py ./

# ── Runtime ───────────────────────────────────────────────────────────────────
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]