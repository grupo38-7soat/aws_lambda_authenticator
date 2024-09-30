import json

from config import Config
from services.user_group_manager import UserGroupManager
from utils.check_document import validate_document
from utils.datetime_converter import datetime_converter

MESSAGE_ACTION = 'SUPPRESS'

class UserManager:
    def __init__(self, client):
        self.client = client
        self.user_pool_id = Config.get('userPoolId')

    @staticmethod
    def response_helper(response, message_sucess: str, message_error: str):
        if response:
            if response.get('ResponseMetadata').get('HTTPStatusCode') == 200:
                return {
                    'status_sucess': True,
                    'message': message_sucess,
                    'response': json.loads(json.dumps(response, default=datetime_converter))
                }
            else:
                return {
                    'status_sucess': False,
                    'message': message_error,
                    'response': json.loads(json.dumps(response, default=datetime_converter))
                }
        else:
            return {
                'status_sucess': False,
                'message': message_error,
                'response': None
            }

    def create_user(self, username, password, attributes: list[dict], group_name):
        try:
            check_document = validate_document(username)
            if check_document.get('status'):
                username = check_document.get('document')
                response = self.client.admin_create_user(
                    UserPoolId=self.user_pool_id,
                    Username=username,
                    UserAttributes=attributes,
                    TemporaryPassword=password,
                    MessageAction=MESSAGE_ACTION
                )

                self.client.admin_set_user_password(
                    UserPoolId=self.user_pool_id,
                    Username=username,
                    Password=password,
                    Permanent=True
                )

                user_group_manager = UserGroupManager(self.client)
                user_group_manager.add_user_to_group(username, group_name)

                return self.response_helper(response, 'Usuário criado com sucesso', 'Erro ao criar usuário')
            else:
                return self.response_helper(None, '', 'O CPF enviado é inválido')
        except self.client.exceptions.UsernameExistsException:
            return self.response_helper(None, '', 'Usuário já existe')
        except Exception as e:
            print(e)

    def get_user(self, username):
        try:
            response = self.client.admin_get_user(
                UserPoolId=self.user_pool_id,
                Username=username
            )
            return self.response_helper(response, 'Usuário Encontrado com Sucesso!', 'Erro ao buscar usuário')
        except self.client.exceptions.UserNotFoundException:
            return self.response_helper(None, '', 'Usuário não encontrado')
        except Exception as e:
            print(e)

    def update_user(self, username, attributes: list[dict]):
        try:
            response = self.client.admin_update_user_attributes(
                UserPoolId=self.user_pool_id,
                Username=username,
                UserAttributes=attributes
            )
            return self.response_helper(response, 'Usuário atualizado com sucesso', 'Erro ao atualizar usuário')
        except self.client.exceptions.UserNotFoundException:
            return self.response_helper(None, '', 'Usuário não encontrado')
        except Exception as e:
            print(e)
            return self.response_helper(None, '', 'Erro ao atualizar usuário')

    def delete_user(self, username):
        try:
            response = self.client.admin_delete_user(
                UserPoolId=self.user_pool_id,
                Username=username
            )
            return self.response_helper(response, 'Usuário deletado com sucesso', 'Erro ao deletar usuário')
        except self.client.exceptions.UserNotFoundException:
            return self.response_helper(None, '', 'Usuário não encontrado')
        except Exception as e:
            print(e)
            return self.response_helper(None, '', 'Erro ao deletar usuário')

    def list_all_users(self):
        try:
            response = self.client.list_users(
                UserPoolId=self.user_pool_id
            )
            return self.response_helper(response, 'Usuário encontrados!', 'Erro ao Carregar os usuários')
        except Exception as e:
            print(e)
            return self.response_helper(None, '', 'Erro ao Carregar os usuários')