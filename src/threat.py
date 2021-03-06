# Steven
from json import dumps

import flask
from flask import Blueprint
from package_detail_retrieval import package_detail_retrieval 
from vuln_search import package_list_data, root_format

THREAT = Blueprint('threat', __name__)

# Routes -----------------------------------------

@THREAT.route("/threat/search", methods=["GET", "POST"])
async def get_packages_route():
    json_data = flask.request.json
    package_manager_type, package_list, level, severity, date = json_data["package_manager_type"], json_data["package_list"], json_data['level'], json_data['severity'], json_data['date']
    package_dic = package_detail_retrieval(package_manager_type, package_list)

    output = await package_list_data(package_dic, severity, date)
    return root_format(package_list, package_dic, output, 0, level)



