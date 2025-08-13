from flask import Blueprint, request

import image_utils
import buffalo
import strans

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
    ## TODO
    return strans.represent(data)
  except Exception as err:
    return {"exception": str(err)}, 400

@blueprint.route("/represent", methods=["POST"])
@blueprint.route("/face", methods=["POST"])
def represent():
  image_data = request.get_json()
  print(f"Received image data: {image_data['img'][:50]}...")  # Log the first 50 characters of the image data
  try:
    img = image_utils.load_image(image_data["img"])
    return buffalo.represent(img)
  except Exception as err:
    return {"exception": str(err)}, 400
