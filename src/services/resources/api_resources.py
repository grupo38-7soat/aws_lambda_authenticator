import boto3
from flask import request
from loguru import logger
from flask_restx import Namespace, Resource, fields

from config import Config
from services.user_manager import UserManager

users_ns = Namespace(name='users', description='Gerenciamento de usuarios')

# Initialize Cognito client and UserManager
client = boto3.client(Config.get('awsClientCognito'), region_name=Config.get('awsRegion'))
user_manager = UserManager(client, Config.get('userPoolId'))

create_and_update_user_model = users_ns.model('User', {
    'username': fields.String(required=True, description='Username'),
    'attributes': fields.List(fields.Nested(users_ns.model('Attribute', {
        'Name': fields.String(required=True, description='Attribute name'),
        'Value': fields.String(required=True, description='Attribute value')
    })), required=True, description='List of attributes')
})

response_model = users_ns.model('Response', {
    'status_sucess': fields.Boolean,
    'response': fields.Raw,
    'message': fields.String
})

@users_ns.route('/create_user')
class CreateUserResource(Resource):
    @users_ns.expect(create_and_update_user_model)
    @users_ns.marshal_with(response_model)
    def post(self):
        logger.info(f'endpoint get_user was called with data {users_ns.payload}')

        data = users_ns.payload
        response = user_manager.create_user(data['username'], Config.get('passwordDefault'), data['attributes'])
        return response

@users_ns.route('/get_user')
class GetUserResource(Resource):
    @users_ns.marshal_with(response_model)
    @users_ns.param('username', 'The username of the user', _in='query')
    def get(self):
        username = request.args.get('username')
        logger.info(f'endpoint get_user was called with username {username}')

        response = user_manager.get_user(username)
        return response

@users_ns.route('/update_user')
class UpdateUserResource(Resource):
    @users_ns.expect(create_and_update_user_model)
    @users_ns.marshal_with(response_model)
    def put(self):
        logger.info(f'endpoint update_user was called with data {users_ns.payload}')

        data = users_ns.payload
        response = user_manager.update_user(data['username'], data['attributes'])
        return response

@users_ns.route('/delete_user')
class DeleteUserResource(Resource):
    @users_ns.marshal_with(response_model)
    @users_ns.param('username', 'The username of the user', _in='query')
    def delete(self):
        username = request.args.get('username')
        logger.info(f'endpoint delete_user was called with username {username}')

        response = user_manager.delete_user(username)
        return response

@users_ns.route('/list_all_users')
class ListAllUsersResource(Resource):
    @users_ns.marshal_with(response_model)
    def get(self):
        logger.info('endpoint list_all_users was called')

        response = user_manager.list_all_users()
        return response