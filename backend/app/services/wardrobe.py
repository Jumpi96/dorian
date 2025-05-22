import logging
from datetime import datetime, timezone
from app.clients.dynamodb import DynamoDBClient, DynamoDBError
from app.config import Config

logger = logging.getLogger(__name__)

WARDROBE_TABLE_NAME = f'{Config.ENV}-wardrobe-items'

class WardrobeService:
    def __init__(self, dynamodb_client: DynamoDBClient):
        self.dynamodb = dynamodb_client
        self.table_name = WARDROBE_TABLE_NAME

    def delete_wardrobe_item(self, user_id: str, item_id: str) -> bool:
        try:
            return self.dynamodb.delete_item(
                table_name=self.table_name,
                key={
                    'userId': user_id,
                    'itemId': item_id
                }
            )
        except DynamoDBError as e:
            logger.error(f"Error deleting wardrobe item: {str(e)}", exc_info=True)
            raise

    def add_wardrobe_item(self, user_id: str, item_id: str, description: str) -> bool:
        try:
            return self.dynamodb.put_item(
                table_name=self.table_name,
                item={
                    'userId': user_id,
                    'itemId': item_id,
                    'description': description,
                    'createdAt': datetime.now(timezone.utc).isoformat()
                }
            )
        except DynamoDBError as e:
            logger.error(f"Error adding wardrobe item: {str(e)}", exc_info=True)
            raise

    def get_wardrobe_items(self, user_id: str) -> list:
        try:
            response = self.dynamodb.query(
                table_name=self.table_name,
                key_condition_expression='userId = :uid',
                expression_attribute_values={
                    ':uid': user_id
                }
            )
            return response.get('Items', [])
        except DynamoDBError as e:
            logger.error(f"Error getting wardrobe items: {str(e)}", exc_info=True)
            raise 