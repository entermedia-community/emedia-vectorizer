import base64
import io
from typing import List

import cv2
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from face_service import FaceService

app = FastAPI(
    title="InsightFace Buffalo_L API",
    description="Face recognition API using InsightFace buffalo_l model",
    version="1.0.0",
)

face_service = FaceService()


class ImageRequest(BaseModel):
    image: str  # base64-encoded image


class FacialArea(BaseModel):
    h: int
    w: int
    x: int
    y: int


class FaceResult(BaseModel):
    age: int
    embedding: List[float]
    face_confidence: float
    facial_area: FacialArea
    gender: int  # 0 = Female, 1 = Male


@app.get("/health")
def health():
    return {"status": "ok", "model": "buffalo_l"}


@app.post("/analyze", response_model=List[FaceResult])
def analyze(req: ImageRequest):
    # Decode base64 image
    try:
        image_data = req.image
        # Strip data URI prefix if present (e.g. "data:image/jpeg;base64,...")
        if "," in image_data:
            image_data = image_data.split(",", 1)[1]

        raw = base64.b64decode(image_data)
        img_array = np.frombuffer(raw, dtype=np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

        if img is None:
            raise ValueError("Could not decode image")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image: {e}")

    # Run face analysis
    results = face_service.analyze(img)
    return results