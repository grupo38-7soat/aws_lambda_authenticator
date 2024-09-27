from utils.check_document import validate_document


class UserManager:
    def __init__(self, client, user_pool_id):
        self.client = client
        self.user_pool_id = user_pool_id

    @staticmethod
    def response_helper(response):
        if response.get('ResponseMetadata').get('HTTPStatusCode') == 200:
            return True
        else:
            return False

    def create_user(self, username, password, email, name):
        try:
            if validate_document(username):
                response = self.client.admin_create_user(
                    UserPoolId=self.user_pool_id,
                    Username=username,
                    UserAttributes=[
                        {
                            'Name': 'email',
                            'Value': email
                        },
                        {
                            'Name': 'name',
                            'Value': name
                        },
                    ],
                    TemporaryPassword=password,
                    MessageAction='SUPPRESS'
                )

                self.client.admin_set_user_password(
                    UserPoolId=self.user_pool_id,
                    Username=username,
                    Password=password,
                    Permanent=True
                )
                if self.response_helper(response):
                    return 'Usuário criado com sucesso'
                else:
                    return 'Erro ao criar usuário'
            else:
                return 'CPF inválido'
        except Exception as e:
            print(e)

    def get_user(self, username):
        response = self.client.admin_get_user(
            UserPoolId=self.user_pool_id,
            Username=username
        )
        return response

    def update_user(self, username, attr_name, value):
        response = self.client.admin_update_user_attributes(
            UserPoolId=self.user_pool_id,
            Username=username,
            UserAttributes=[
                {
                    'Name': f'{attr_name}',
                    'Value': value
                },
            ]
        )
        if self.response_helper(response):
            return 'Usuário atualizado com sucesso'
        else:
            return 'Erro ao atualizar usuário'

    def delete_user(self, username):
        response = self.client.admin_delete_user(
            UserPoolId=self.user_pool_id,
            Username=username
        )
        if self.response_helper(response):
            return 'Usuário deletado com sucesso'
        else:
            return 'Erro ao deletar usuário'

    def list_all_users(self):
        response = self.client.list_users(
            UserPoolId=self.user_pool_id
        )
        return response['Users']
