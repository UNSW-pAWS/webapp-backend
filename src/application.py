from json import dumps

from flask import Flask
from flask_cors import CORS

from alt_pkgs import ALT_PKGS
from threat import THREAT

application = Flask(__name__)
CORS(application)
application.register_blueprint(ALT_PKGS)
application.register_blueprint(THREAT)

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
