import threading
from typing import List, Dict, Any

import cv2
import numpy as np
import insightface
from insightface.app import FaceAnalysis


class FaceService:
    """Singleton wrapper around InsightFace buffalo_l FaceAnalysis."""

    _lock = threading.Lock()

    def __init__(self, det_size: tuple = (640, 640), ctx_id: int = 0):
        """
        Initialize the InsightFace model.

        Args:
            det_size: Detection input size (width, height). Default 640x640.
            ctx_id:   GPU context id. Use 0 for GPU, -1 for CPU.
        """
        self.app = FaceAnalysis(
            name="buffalo_l",
            providers=["CUDAExecutionProvider", "CPUExecutionProvider"],
        )
        self.app.prepare(ctx_id=ctx_id, det_size=det_size)

    def analyze(self, img_bgr: np.ndarray) -> List[Dict[str, Any]]:
        """
        Run face detection + recognition on a BGR image.

        Returns a list of dicts matching the API response schema.
        """
        with self._lock:
            faces = self.app.get(img_bgr)

        results = []
        for face in faces:
            # Bounding box: [x1, y1, x2, y2]
            bbox = face.bbox.astype(int)
            x1, y1, x2, y2 = bbox[0], bbox[1], bbox[2], bbox[3]

            # Gender: insightface returns "M" / "F" or 1 / 0 depending on version
            gender_raw = face.gender
            if isinstance(gender_raw, str):
                gender = 1 if gender_raw == "M" else 0
            else:
                # Numeric: 1 = Male, 0 = Female
                gender = int(gender_raw)

            # Age
            age = int(round(float(face.age))) if face.age is not None else -1

            # Embedding (512-d for buffalo_l)
            embedding = face.normed_embedding.tolist() if face.normed_embedding is not None else []

            # Detection confidence score
            det_score = float(face.det_score) if face.det_score is not None else 0.0

            results.append(
                {
                    "age": age,
                    "embedding": embedding,
                    "face_confidence": round(det_score, 6),
                    "facial_area": {
                        "h": int(y2 - y1),
                        "w": int(x2 - x1),
                        "x": int(x1),
                        "y": int(y1),
                    },
                    "gender": gender,
                }
            )

        # Sort by x-position (left-to-right) for deterministic ordering
        results.sort(key=lambda r: r["facial_area"]["x"])
        return results