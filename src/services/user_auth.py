import json
import boto3
from botocore.exceptions import ClientError

from config import Config
from utils.datetime_converter import datetime_converter

PASSWORD_DEFAULT = Config.get('passwordDefault')

AUTHFLOW = 'USER_PASSWORD_AUTH'

client = boto3.client(Config.get('awsClientCognito'), region_name=Config.get('awsRegion'))


class CognitoAuth:
    def __init__(self):
        self.client = client
        self.client_id = Config.get('clientId')
        self.user_pool_id = Config.get('userPoolId')

    @staticmethod
    def response_helper(response, message_success: str, message_error: str):
        if response:
            if response.get('ResponseMetadata').get('HTTPStatusCode') == 200:
                return {
                    'status_success': True,
                    'message': message_success,
                    'response': json.loads(json.dumps(response, default=datetime_converter))
                }
            else:
                return {
                    'status_success': False,
                    'message': message_error,
                    'response': json.loads(json.dumps(response, default=datetime_converter))
                }
        else:
            return {
                'status_success': False,
                'message': message_error,
                'response': None
            }

    def authenticate_user(self, username: str, password: str):
        try:
            response = self.client.initiate_auth(
                AuthFlow=AUTHFLOW,
                AuthParameters={
                    'USERNAME': username,
                    'PASSWORD': password
                },
                ClientId=self.client_id
            )
            return self.response_helper(response, 'User authenticated successfully', 'Authentication failed')
        except self.client.exceptions.NotAuthorizedException:
            return self.response_helper(None, '', 'Invalid username or password')
        except Exception as e:
            return self.response_helper(None, '', str(e))

    def validate_token(self, token: str) -> dict:
        if not token.startswith('Bearer '):
            return self.response_helper(None, '', 'Token must start with "Bearer "')

        token = token[len('Bearer '):]

        try:
            response = self.client.get_user(
                AccessToken=token
            )
            return self.response_helper(response, 'Token is valid', 'Token validation failed')
        except ClientError as e:
            return self.response_helper(None, '', f'Error: {e}')
        except Exception as e:
            return self.response_helper(None, '', str(e))

    def validate_token_permission(self, token: str, group_names: list) -> dict:
        try:
            response = self.client.get_user(
                AccessToken=token
            )
            username = response['Username']

            groups_response = self.client.admin_list_groups_for_user(
                Username=username,
                UserPoolId=self.user_pool_id
            )
            groups = [group['GroupName'] for group in groups_response['Groups']]

            for group_name in group_names:
                if group_name in groups:
                    return self.response_helper(response, f'User {username} has required permissions',
                                                'Permission validation failed')
            return self.response_helper(response, '', f'User {username} does not have required permissions')

        except ClientError as e:
            return self.response_helper('', '', f'Error: {e}')
        except Exception as e:
            return self.response_helper('', '', str(e))