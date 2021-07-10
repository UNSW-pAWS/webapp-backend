# Aniket
from json import dumps
import requests

from flask import Blueprint, request
# import boto3

CONFIG = Blueprint('config', __name__)

def getConfig(service, resource):
  url     = "https://d2stg8d246z9di.cloudfront.net/latest/gzip/CloudFormationResourceSpecification.json"
  ret_key = f'AWS::{service.upper()}::{resource}' if (resource != 'blank') else f'AWS::{service.upper()}'
  data    = requests.get(url).json()
  configs = data['PropertyTypes']
  ret     = {}
  for key in configs:
    if ret_key.upper() in key.upper():
      ret[key] = configs[key]
  return(ret)

# def getConfigFromAPI(resource):
#   ret_key       = f'AWS::{resource.upper()}'
#   client        = boto3.client('config')
#   select_fields = "resourceId, resourceType, configuration.instanceType"
#   # query         = f"SELECT {select_fields} WHERE resourceType LIKE '{ret_key}%'"
#   query         = f"SELECT {select_fields} WHERE resourceType LIKE='AWS::EC2::Instance'"
#   res           = client.select_resource_config(Expression=query, Limit=100)
#   return res

# Routes -----------------------------------------

@CONFIG.route("/config/get", methods=["GET"])
def get_config():
    service  = request.args.get('service')
    resource  = request.args.get('resource')
    data      = getConfig(service, resource)
    return dumps(data)

# @CONFIG.route("/config/api/get", methods=["GET"])
# def get_api_config():
#     resource  = request.args.get('resource')
#     data      = getConfigFromAPI(resource)
#     return dumps(data)
