import boto3
from flask import request
from loguru import logger
from flask_restx import Namespace, Resource, fields

from config import Config
from services.user_group_manager import UserGroupManager

user_groups_ns = Namespace(name='user-groups', description='Gerenciamento de usuarios dentro dos grupos')

client = boto3.client(Config.get('awsClientCognito'), region_name=Config.get('awsRegion'))
user_group_manager = UserGroupManager(client, Config.get('userPoolId'))

add_user_to_group_model = user_groups_ns.model('AddUserToGroup', {
    'username': fields.String(required=True, description='Username'),
    'group_name': fields.String(required=True, description='Group name')
})

response_model = user_groups_ns.model('Response', {
    'status_sucess': fields.Boolean,
    'response': fields.Raw,
    'message': fields.String
})


@user_groups_ns.route('/add_user_to_group')
class AddUserToGroupResource(Resource):
    @user_groups_ns.expect(add_user_to_group_model)
    @user_groups_ns.marshal_with(response_model)
    def post(self):
        logger.info(f'endpoint add_user_to_group was called with data {user_groups_ns.payload}')

        data = user_groups_ns.payload
        response = user_group_manager.add_user_to_group(data['username'], data['group_name'])
        return response


@user_groups_ns.route('/remove_user_from_group')
class RemoveUserFromGroupResource(Resource):
    @user_groups_ns.expect(add_user_to_group_model)
    @user_groups_ns.marshal_with(response_model)
    def post(self):
        logger.info(f'endpoint remove_user_from_group was called with data {user_groups_ns.payload}')

        data = user_groups_ns.payload
        response = user_group_manager.remove_user_from_group(data['username'], data['group_name'])
        return response


@user_groups_ns.route('/list_users_in_group')
class ListUsersInGroupResource(Resource):
    @user_groups_ns.marshal_with(response_model)
    @user_groups_ns.param('group_name', 'The name of the group', _in='query')
    def get(self):
        group_name = request.args.get('group_name')
        logger.info(f'endpoint list_users_in_group was called with group_name {group_name}')

        response = user_group_manager.list_users_in_group(group_name)
        return response
