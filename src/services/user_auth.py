from botocore.exceptions import ClientError

from config import Config

AUTHFLOW = 'USER_PASSWORD_AUTH'


class CognitoAuth:
    def __init__(self, client, client_id, user_pool_id):
        self.client = client
        self.client_id = client_id
        self.user_pool_id = user_pool_id

    def authenticate_user(self, username: str, password: str = Config.get('passwordDefault')) :
        try:
            response = self.client.initiate_auth(
                AuthFlow=AUTHFLOW,
                AuthParameters={
                    'USERNAME': username,
                    'PASSWORD': password
                },
                ClientId=self.client_id
            )
            return response.get('AuthenticationResult').get('AccessToken', '')
        except self.client.exceptions.NotAuthorizedException:
            return 'Invalid username or password'
        except Exception as e:
            return str(e)

    def validate_token(self, token: str) -> bool:
        try:
            response = self.client.get_user(
                AccessToken=token
            )
            return True
        except ClientError as e:
            print(f'Error: {e}')
            return False
        except Exception as e:
            return False
