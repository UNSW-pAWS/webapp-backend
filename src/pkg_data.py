
from json import dumps

from flask import Blueprint

PKG_DATA = Blueprint('pkg', __name__)

# Routes -----------------------------------------

@PKG_DATA.route("/pkg/info", methods=["GET"])
def get_packages_route():
    return dumps({
        "hi": "hello"
    })
