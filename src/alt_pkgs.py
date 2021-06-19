
from json import dumps

from flask import Blueprint

ALT_PKGS = Blueprint('alt-pkgs', __name__)

# Routes -----------------------------------------

@ALT_PKGS.route("/alt-pkgs/get", methods=["GET"])
def get_packages_route():
    return dumps({
        "hi": "hello"
    })
