# Steven
from json import dumps

from flask import Blueprint

THREAT = Blueprint('threat', __name__)

# Routes -----------------------------------------

@THREAT.route("/threat/search", methods=["GET"])
def get_packages_route():
    return dumps({
        "hi": "hello"
    })
