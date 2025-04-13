import boto3
from botocore.exceptions import ClientError
from app.config import Config
from datetime import datetime

class DynamoDBService:
    def __init__(self):
        self.dynamodb = boto3.resource(
            'dynamodb',
            aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
            region_name=Config.AWS_REGION
        )
        self.users_table = self.dynamodb.Table('dev-users')

    def get_user(self, user_id):
        try:
            response = self.users_table.get_item(Key={'userId': user_id})
            return response.get('Item')
        except ClientError as e:
            print(f"Error getting user: {e}")
            return None

    def create_user(self, user_id, email):
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