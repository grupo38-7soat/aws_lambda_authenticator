import json
from utils.datetime_converter import datetime_converter
from botocore.exceptions import ClientError

class GroupManager:
    def __init__(self, client, user_pool_id):
        self.client = client
        self.user_pool_id = user_pool_id

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

    def create_group(self, group_name, description):
        try:
            response = self.client.create_group(
                UserPoolId=self.user_pool_id,
                GroupName=group_name,
                Description=description
            )
            return self.response_helper(response, 'Grupo criado com sucesso', 'Erro ao criar grupo')
        except Exception as e:
            return self.response_helper(None, '', str(e))

    def get_group(self, group_name):
        try:
            response = self.client.get_group(
                UserPoolId=self.user_pool_id,
                GroupName=group_name
            )
            return self.response_helper(response, 'Grupo recuperado com sucesso', 'Erro ao recuperar grupo')
        except Exception as e:
            return self.response_helper(None, '', str(e))

    def update_group(self, group_name, description):
        try:
            response = self.client.update_group(
                UserPoolId=self.user_pool_id,
                GroupName=group_name,
                Description=description
            )
            return self.response_helper(response, 'Grupo atualizado com sucesso', 'Erro ao atualizar grupo')
        except Exception as e:
            return self.response_helper(None, '', str(e))

    def delete_group(self, group_name):
        try:
            response = self.client.delete_group(
                UserPoolId=self.user_pool_id,
                GroupName=group_name
            )
            return self.response_helper(response, 'Grupo deletado com sucesso', 'Erro ao deletar grupo')
        except Exception as e:
            return self.response_helper(None, '', str(e))

    def list_all_groups(self):
        try:
            response = self.client.list_groups(
                UserPoolId=self.user_pool_id
            )
            return self.response_helper(response, 'Grupos listados com sucesso', 'Erro ao listar grupos')
        except Exception as e:
            return self.response_helper(None, '', str(e))
