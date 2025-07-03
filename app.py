from flask import Flask
from flask_cors import CORS

from routes import blueprint

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(blueprint)
    return app
