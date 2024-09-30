import json

from config import Config
from utils.datetime_converter import datetime_converter

class UserGroupManager:
    def __init__(self, client):
        self.client = client
        self.user_pool_id = Config.get('userPoolId')

    @staticmethod
    def response_helper(response, message_sucess: str, message_error: str):
        if response:
            if response.get('ResponseMetadata').get('HTTPStatusCode') == 200:
                return {
                    'status_sucesso': True,
                    'mensagem': message_sucess,
                    'response': json.loads(json.dumps(response, default=datetime_converter))
                }
            else:
                return {
                    'status_sucesso': False,
                    'mensagem': message_error,
                    'response': json.loads(json.dumps(response, default=datetime_converter))
                }
        else:
            return {
                'status_sucesso': False,
                'mensagem': message_error,
                'response': None
            }

    def add_user_to_group(self, username, group_name):
        try:
            response = self.client.admin_add_user_to_group(
                UserPoolId=self.user_pool_id,
                Username=username,
                GroupName=group_name
            )
            return self.response_helper(response, 'Usuário adicionado ao grupo com sucesso',
                                        'Erro ao adicionar usuário ao grupo')
        except Exception as e:
            return self.response_helper(None, '', str(e))


    def remove_user_from_group(self, username, group_name):
        try:
            response = self.client.admin_remove_user_from_group(
                UserPoolId=self.user_pool_id,
                Username=username,
                GroupName=group_name
            )
            return self.response_helper(response, 'Usuário removido do grupo com sucesso',
                                        'Erro ao remover usuário do grupo')
        except Exception as e:
            return self.response_helper(None, '', str(e))


    def list_users_in_group(self, group_name):
        try:
            response = self.client.list_users_in_group(
                UserPoolId=self.user_pool_id,
                GroupName=group_name
            )
            return self.response_helper(response, 'Usuários listados com sucesso', 'Erro ao listar usuários no grupo')
        except Exception as e:
            return self.response_helper(None, '', str(e))