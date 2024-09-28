import sys
import awsgi
from flask import Flask
from loguru import logger

from services.expose_api_service import ApiService

app = Flask(__name__)

logger.remove(0)
logger.add(sys.stdout)
logger.info('start aplication')

def lambda_handler(event, context):
    return awsgi.response(app, event, context)

if __name__ == '__main__':
    ApiService().run()
