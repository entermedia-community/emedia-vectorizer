from flask import Blueprint, request
import logging

import image_utils
import buffalo
import strans

logging.basicConfig(
  level=logging.INFO,
  format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

blueprint = Blueprint("routes", __name__)

@blueprint.route("/")
def home():
  return f"<h1>Welcome to eMedia Vectorization API!</h1>"

@blueprint.route("/text", methods=["POST"])
def text_represent():
  json_data = request.get_json()
  data = json_data.get("data", {})

  if(len(data) == 0):
    return {"error": "No data provided"}, 400

  for d in data:
    if not d['id'] or not d['text']:
      return {"error": "Each item must have 'id' and 'text'"}, 400
    else:
      print(f"Processing {d['id']}:{d['text'][:50]}...")

  try:
    return strans.represent(data)
  except Exception as err:
    logger.error(f"Error occurred while representing text: {err}")
    return {"exception": str(err)}, 400

@blueprint.route("/represent", methods=["POST"])
@blueprint.route("/face", methods=["POST"])
def face_represent():
  image_data = request.get_json()
  img = image_data.get("img", None)

  if img is None:
    return {"error": "No 'img' field provided"}, 400

  print(f"Received image data: {img[:50]}...")

  try:
    loaded_img = image_utils.load_image(img)
    return buffalo.represent(loaded_img)
  except Exception as err:
    logger.error(f"Error occurred while processing image: {err}")
    return {"exception": str(err)}, 400
