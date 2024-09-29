import awsgi
from flask_restx import Api
from flask import Flask

from services.resources.user_api_resources import users_ns

app = Flask(__name__)

api = Api(app)

api.add_namespace(users_ns)

def api_using_aws_lambda(event, context):
    return awsgi.response(app, event, context)