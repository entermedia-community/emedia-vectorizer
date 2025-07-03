from flask import Blueprint, request

import image_utils
import buffalo

blueprint = Blueprint("routes", __name__)

@blueprint.route("/")
def home():
  return f"<h1>Welcome to eMedia Face Recognition API!</h1>"

@blueprint.route("/represent", methods=["POST"])
def represent():
  image_data = request.get_json()
  print(f"Received image data: {image_data['img'][:50]}...")  # Log the first 50 characters of the image data
  try:
    img = image_utils.load_image(image_data["img"])
    return buffalo.represent(img)
  except Exception as err:
    return {"exception": str(err)}, 400