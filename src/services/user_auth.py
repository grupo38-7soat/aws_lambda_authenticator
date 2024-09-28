import boto3
from botocore.exceptions import ClientError

AUTHFLOW = 'USER_PASSWORD_AUTH'


class CognitoAuth:
    def __init__(self, client, client_id, user_pool_id):
        self.client = client
        self.client_id = client_id
        self.user_pool_id = user_pool_id

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

# Exemplo de uso
# if __name__ == '__main__':
#     client = boto3.client('cognito-idp', region_name='us-east-1')
#
#     client_id = '7lan6gn1giu1cea0lrifmopb6n'
#     user_pool_id = 'us-east-1_C9dme06v7'
#     username = '281133590011'
#     password = 'TempPassword123!'
#
#     auth = CognitoAuth(client, client_id, user_pool_id)
#     tokens = auth.authenticate_user(username, password)
#     print('Tokens:', tokens)
#
#     print(auth.validate_token(tokens, user_pool_id))
