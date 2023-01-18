from flask import Flask
from flask_cors import CORS

from config import config

# Routes
from routes import instagrapi

app = Flask(__name__)

CORS(app, resources={"*": {"origins": "http://localhost:9300"}})


def page_not_found(error):
    return "<h1>Not found page</h1>", 404


if __name__ == '__main__':
    app.config.from_object(config['development'])

    # Blueprints
    app.register_blueprint(instagrapi.main, url_prefix='/api')

    # Error handlers
    app.register_error_handler(404, page_not_found)
    app.run()
