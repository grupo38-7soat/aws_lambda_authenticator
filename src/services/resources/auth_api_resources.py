from flask_restx import Namespace, Resource

from config import Config
from flask import request
from src.services.user_auth import CognitoAuth

auth_ns = Namespace('auth', description='Authentication operations')

cognito = CognitoAuth(client_id=Config.get('clientId'), user_pool_id=Config.get('awsUserPoolId'))

@auth_ns.route('/login')
class LoginResource(Resource):
    @auth_ns.param('username', 'The username of the user', _in='formData')
    def post(self):
        data = request.form
        username = data.get('username')

        response = cognito.authenticate_user(username)
        return response

@auth_ns.route('/validate_token')
class ValidateTokenResource(Resource):
    @auth_ns.param('token', 'The token to validate', _in='formData')
    def post(self):
        data = request.form
        token = data.get('token')
        print(token)
        is_valid = cognito.validate_token(token)
        return {'is_valid': is_valid}