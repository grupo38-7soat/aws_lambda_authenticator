import json

from config import Config
from utils.datetime_converter import datetime_converter

class GroupManager:
    def __init__(self, client):
        self.client = client
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

    def create_group(self, group_name, description):
        try:
            response = self.client.create_group(
                UserPoolId=self.user_pool_id,
                GroupName=group_name,
                Description=description
            )
            return self.response_helper(response, 'Group created successfully', 'Error creating group')
        except Exception as e:
            return self.response_helper(None, '', str(e))

    def get_group(self, group_name):
        try:
            response = self.client.get_group(
                UserPoolId=self.user_pool_id,
                GroupName=group_name
            )
            return self.response_helper(response, 'Group retrieved successfully', 'Error retrieving group')
        except Exception as e:
            return self.response_helper(None, '', str(e))

    def update_group(self, group_name, description):
        try:
            response = self.client.update_group(
                UserPoolId=self.user_pool_id,
                GroupName=group_name,
                Description=description
            )
            return self.response_helper(response, 'Group updated successfully', 'Error updating group')
        except Exception as e:
            return self.response_helper(None, '', str(e))

    def delete_group(self, group_name):
        try:
            response = self.client.delete_group(
                UserPoolId=self.user_pool_id,
                GroupName=group_name
            )
            return self.response_helper(response, 'Group deleted successfully', 'Error deleting group')
        except Exception as e:
            return self.response_helper(None, '', str(e))

    def list_all_groups(self):
        try:
            response = self.client.list_groups(
                UserPoolId=self.user_pool_id
            )
            return self.response_helper(response, 'Groups listed successfully', 'Error listing groups')
        except Exception as e:
            return self.response_helper(None, '', str(e))