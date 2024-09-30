import boto3
from botocore.exceptions import ClientError

from config import Config

PASSWORD_DEFAULT = Config.get('passwordDefault')

AUTHFLOW = 'USER_PASSWORD_AUTH'

client = boto3.client(Config.get('awsClientCognito'), region_name=Config.get('awsRegion'))

class CognitoAuth:
    def __init__(self):
        self.client = client
        self.client_id = Config.get('clientId')
        self.user_pool_id = Config.get('userPoolId')

    def authenticate_user(self, username: str, password: str = PASSWORD_DEFAULT):
        try:
            print(username, type(username))
            response = self.client.initiate_auth(
                AuthFlow=AUTHFLOW,
                AuthParameters={
                    'USERNAME': username,
                    'PASSWORD': password
                },
                ClientId=self.client_id
            )
            return response
        except self.client.exceptions.NotAuthorizedException:
            return 'Invalid username or password'
        except Exception as e:
            return str(e)

    def validate_token(self, token: str) -> bool:
        try:
            response = self.client.get_user(
                AccessToken=token
            )
            return response
        except ClientError as e:
            print(f'Error: {e}')
            return False
        except Exception as e:
            return False

    def validate_token_permition(self, token: str, group_names: list) -> dict:
        response_template = {
                'username': '',
                'success': False
            }
        try:
            response = self.client.get_user(
                AccessToken=token
            )
            username = response['Username']

            response_template['username'] = username

            groups_response = self.client.admin_list_groups_for_user(
                Username=username,
                UserPoolId=self.user_pool_id
            )
            groups = [group['GroupName'] for group in groups_response['Groups']]

            for group_name in group_names:
                if group_name in groups or True:
                    response_template['success'] = True
                    return response_template
            return response_template
        except ClientError as e:
            print(f'Error: {e}')
            return response_template
        except Exception as e:
            return response_template
