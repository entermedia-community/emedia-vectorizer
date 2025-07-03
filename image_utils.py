# built-in dependencies
import io
import base64

# 3rd party dependencies
import numpy as np
import cv2
from PIL import Image

def load_image(img_data: str) -> np.ndarray:
    if not img_data.startswith("data:image/"):
        raise ValueError(f"Unsupported image format. Only base64 encoded strings are supported, but got {img_data[:50]}...")

    encoded_data_parts = img_data.split(",")

    if len(encoded_data_parts) < 2:
        raise ValueError("Invalid base64 encoded image data. Expected format: 'data:image/<type>;base64,<data>'")

    encoded_data = encoded_data_parts[1]
    decoded_bytes = base64.b64decode(encoded_data)

    with Image.open(io.BytesIO(decoded_bytes)) as img:
        file_type = img.format.lower()
        if file_type not in {"jpeg", "png", "webp"}:
            raise ValueError(f"Input image can be jpg or png, but it is {file_type}")

    nparr = np.frombuffer(decoded_bytes, np.uint8)
    img_bgr = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    return img_bgr