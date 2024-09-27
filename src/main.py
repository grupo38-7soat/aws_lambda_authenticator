import boto3

from services.UserManager import UserManager

client = boto3.client('cognito-idp', region_name='us-east-1')

USER_POOL_ID = ''

# Exemplo de uso das funções
if __name__ == '__main__':
    users_aux = UserManager(client, USER_POOL_ID)

    create_response = users_aux.create_user('28113359001', 'TempPassword123!', 'testuser@example.com', name='Test User')
    print('Create User Response:', create_response)

    update_response = users_aux.update_user('28113359001', 'email', 'newemail@example.com')
    print('Update User Response:', update_response)

    get_response = users_aux.get_user('28113359001')
    print('Get User Response:', get_response)

    delete_response = users_aux.delete_user('28113359001')
    print('Delete User Response:', delete_response)

    users = users_aux.list_all_users()
    for user in users:
        print(user)
