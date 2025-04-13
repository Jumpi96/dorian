import boto3
from botocore.exceptions import ClientError
from app.config import Config
from datetime import datetime

class DynamoDBService:
    def __init__(self, testing=False):
        if not testing:
            self.dynamodb = boto3.resource(
                'dynamodb',
                aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
                region_name=Config.AWS_REGION
            )
            self.users_table = self.dynamodb.Table('dev-users')
        else:
            # In test mode, we don't connect to DynamoDB
            self.testing = True

    def get_user(self, user_id):
        if hasattr(self, 'testing'):
            return None  # In test mode, always return None to simulate new user
            
        try:
            response = self.users_table.get_item(Key={'userId': user_id})
            return response.get('Item')
        except ClientError as e:
            print(f"Error getting user: {e}")
            return None

    def create_user(self, user_id, email):
        if hasattr(self, 'testing'):
            return True  # In test mode, always return success
            
        try:
            self.users_table.put_item(
                Item={
                    'userId': user_id,
                    'email': email,
                    'createdAt': str(datetime.utcnow())
                }
            )
            return True
        except ClientError as e:
            print(f"Error creating user: {e}")
            return False 