import boto3
from botocore.exceptions import ClientError
from app.config import Config
from datetime import datetime, UTC
import logging

logger = logging.getLogger(__name__)

WARDROBE_TABLE_NAME = 'dev-wardrobe-items'

class DynamoDBError(Exception):
    """Base exception for DynamoDB related errors"""
    pass

class DynamoDBService:
    def __init__(self):
        self.dynamodb = boto3.resource(
            'dynamodb',
            aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
            region_name=Config.AWS_REGION
        )
        self.wardrobe_table = self.dynamodb.Table(WARDROBE_TABLE_NAME)

    def delete_wardrobe_item(self, user_id, item_id):
        try:
            self.wardrobe_table.delete_item(
                Key={
                    'userId': user_id,
                    'itemId': item_id
                }
            )
            return True
        except ClientError as e:
            logger.error(f"Error deleting wardrobe item: {str(e)}", exc_info=True)
            raise DynamoDBError(f"Failed to delete wardrobe item: {str(e)}")

    def add_wardrobe_item(self, user_id, item_id, description):
        try:
            self.wardrobe_table.put_item(
                Item={
                    'userId': user_id,
                    'itemId': item_id,
                    'description': description,
                    'createdAt': datetime.now(UTC).isoformat()
                }
            )
            return True
        except ClientError as e:
            logger.error(f"Error adding wardrobe item: {str(e)}", exc_info=True)
            raise DynamoDBError(f"Failed to add wardrobe item: {str(e)}")

    def get_wardrobe_items(self, user_id):
        try:
            response = self.wardrobe_table.query(
                KeyConditionExpression='userId = :uid',
                ExpressionAttributeValues={
                    ':uid': user_id
                }
            )
            return response.get('Items', [])
        except ClientError as e:
            logger.error(f"Error getting wardrobe items: {str(e)}", exc_info=True)
            raise DynamoDBError(f"Failed to retrieve wardrobe items: {str(e)}")
