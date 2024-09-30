from flask import request
from flask_restx import Namespace, Resource, fields

from config import Config
from src.services.user_auth import CognitoAuth

auth_ns = Namespace('auth', description='Authentication operations')

cognito = CognitoAuth()

PASSWORD_DEFAULT = Config.get('passwordDefault')

auth_model = auth_ns.model('LoginModel', {
        'username': fields.String(required=True, description='The username of the user'),
        'password': fields.String(required=False, description='The password of the user')
    })

@auth_ns.route('/login')
class LoginResource(Resource):
    @auth_ns.expect(auth_model)
    def post(self):
        data = request.json
        username = data.get('username')
        password = data.get('password', PASSWORD_DEFAULT)

        response = cognito.authenticate_user(username, password)
        return response

@auth_ns.route('/validate_token')
class ValidateTokenResource(Resource):
    @auth_ns.param('token', 'The token to validate', _in='formData')
    def post(self):
        data = request.form
        token = data.get('token')
        return cognito.validate_token(token)