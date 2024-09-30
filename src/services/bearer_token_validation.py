from flask_httpauth import HTTPTokenAuth
from services.user_auth import CognitoAuth
from config import Config

auth = HTTPTokenAuth(scheme='Bearer')

cognito_auth = CognitoAuth(Config.get('clientId'), Config.get('userPoolId'))

GROUP_NAME = ['admin']

@auth.verify_token
def verify_token(token):
    if token:
        response = cognito_auth.validate_token_permition(token, GROUP_NAME)
        if response['success']:
            return response['username']