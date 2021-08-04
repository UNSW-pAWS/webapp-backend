from json import dumps

from flask import Flask
from flask_cors import CORS

from threat import THREAT
from config import CONFIG

application = Flask(__name__)
CORS(application)
application.register_blueprint(THREAT)
application.register_blueprint(CONFIG)

def default_handler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

application.register_error_handler(Exception, default_handler)

@application.route("/")
def home():
    return "Hello there!"

if __name__ == "__main__":
    application.run()
