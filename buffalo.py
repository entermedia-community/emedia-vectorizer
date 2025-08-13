from typing import Any

import numpy as np

from insightface.app import FaceAnalysis

def parsenp(obj):
  if isinstance(obj, np.ndarray):
    return obj.tolist()
  if isinstance(obj, np.float32):
    return float(obj)
  if isinstance(obj, np.int64):
    return int(obj)
  return obj

app = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'], silent=True)
app.prepare(ctx_id=-1)

def represent(img: np.ndarray) -> Any:
  # img = cv2.imread(image_path)
  faces = app.get(img)

  resp_objs = []

  for face in faces:
    embedding = parsenp(face['embedding'])
    bbox = parsenp(face['bbox'])
    facial_area = {
      "x": bbox[0],
      "y": bbox[1],
      "w": bbox[2] - bbox[0],
      "h": bbox[3] - bbox[1],
    }
    age = parsenp(face['age']),
    gender = parsenp(face['gender'])
    # landmark_2d = parsenp(face['landmark_2d_106'])
    # landmark_3d = parsenp(face['landmark_3d_68'])
    # right_eye = parsenp(face['right_eye']),
    # left_eye = parsenp(face['left_eye']),
    # nose = parsenp(face['nose']),
    # mouth_left = parsenp(face['mouth_left']),
    # mouth_right = parsenp(face['mouth_right']),
    face_confidence = parsenp(face['det_score'])
    data = {
      "facial_area": facial_area,
      "age": age,
      "gender": gender,
      # "right_eye": right_eye,
      # "left_eye": left_eye,
      # "nose": nose,
      # "mouth_left": mouth_left,
      # "mouth_right": mouth_right,
      # "landmark_2d": landmark_2d,
      # "landmark_3d": landmark_3d,
      "face_confidence": face_confidence,
      "embedding": embedding,
    }
    resp_objs.append(data)
    
  return resp_objs
