import boto3

from services.user_manager import UserManager

client = boto3.client('cognito-idp', region_name='us-east-1')

USER_POOL_ID = ''
CLIENT_ID = ''
PASSWORD_DEFAULT = 'Dx6f2vxHb^Qig^%EmmMjZ8'

# Exemplo de uso das funções
if __name__ == '__main__':
    users_aux = UserManager(client, USER_POOL_ID)

    attr = [{'Name': 'name', 'Value': '1'}, {'Name': 'email', 'Value': 'hello@example.com'}]

    create_response = users_aux.create_user('612.533.434-11', PASSWORD_DEFAULT, attr)
    print('Create User Response:', create_response)

    # update_response = users_aux.update_user('123', attr)
    # print('Update User Response:', update_response)
    #
    get_response = users_aux.get_user('123')
    print('Get User Response:', get_response)

    delete_response = users_aux.delete_user('1')
    print('Delete User Response:', delete_response)

    users = users_aux.list_all_users()
    print(users)
