# Jocelyn
from json import dumps

from flask import Blueprint

NOTIF = Blueprint('notif', __name__)

# Routes -----------------------------------------

@NOTIF.route("/notif/get", methods=["GET"])
def get_packages_route():
    return dumps({
        "hi": "hello"
    })
