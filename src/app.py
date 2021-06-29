import sys
from json import dumps

from flask import Flask
from flask_cors import CORS

from alt_pkgs import ALT_PKGS
from threat import THREAT

app = Flask(__name__)
CORS(app)
app.register_blueprint(ALT_PKGS)
app.register_blueprint(THREAT)

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

app.register_error_handler(Exception, default_handler)

@app.route("/")
def home():
    return "Hello there!"

if __name__ == "__main__":
    app.run(debug=True, port=(int(sys.argv[1]) if len(sys.argv) == 2 else 9447))
