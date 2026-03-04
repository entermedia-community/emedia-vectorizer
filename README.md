# InsightFace buffalo_l — FastAPI

REST API for face detection, age/gender estimation, and 512-d embedding extraction using **InsightFace buffalo_l**.

---

## Endpoints

| Method | Path       | Description                     |
| ------ | ---------- | ------------------------------- |
| GET    | `/health`  | Liveness check                  |
| POST   | `/analyze` | Analyse faces in a base64 image |
| GET    | `/docs`    | Swagger UI (auto-generated)     |

### `POST /analyze`

**Request body**

```json
{ "image": "<base64-encoded image, with or without data-URI prefix>" }
```

**Response** — array of detected faces, sorted left-to-right:

```json
[
  {
    "age": 28,
    "embedding": [ 0.012, -0.034, ... ],   // 512 floats
    "face_confidence": 0.9983,
    "facial_area": { "h": 210, "w": 180, "x": 94, "y": 56 },
    "gender": 1                              // 0 = Female, 1 = Male
  }
]
```

---

## Quick start (Docker — recommended)

### GPU

```bash
docker compose up --build
```

### CPU only

Edit `docker-compose.yml` — remove the `deploy` block, then:

```bash
docker compose up --build
```

---

## Quick start (local)

```bash
# 1. Install deps
pip install -r requirements.txt   # GPU: onnxruntime-gpu  |  CPU: onnxruntime

# 2. Run
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The buffalo_l model weights (~500 MB) are downloaded automatically on first run
and cached in `~/.insightface/models/buffalo_l/`.

---

## Test

```bash
# Smoke-test with a real image
python test_api.py /path/to/photo.jpg

# Or with curl
curl -s -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d "{\"image\": \"$(base64 -w0 photo.jpg)\"}" | python -m json.tool
```

---

## Notes

- **Embedding** is the L2-normalised 512-d ArcFace vector from `buffalo_l`.  
  Cosine similarity between two embeddings is just their dot product (both are unit vectors).
- `ctx_id=0` → GPU; `ctx_id=-1` → CPU. Edit `face_service.py` to change.
- For multi-GPU or multi-worker setups, replace the threading lock with a process-level model pool.
