import logging
from datetime import datetime, timezone
from app.clients.dynamodb import DynamoDBClient, DynamoDBError

logger = logging.getLogger(__name__)

RATE_LIMIT_TABLE = 'dev-rate-limits'
MAX_REQUESTS_PER_DAY = 10

class RateLimitError(Exception):
    """Exception raised when rate limit is exceeded"""
    pass

class RateLimitService:
    def __init__(self, dynamodb_client: DynamoDBClient):
        self.dynamodb = dynamodb_client
        self.table_name = RATE_LIMIT_TABLE

    def _get_today_key(self, user_id: str) -> str:
        """Generate a unique key for today's rate limit record"""
        today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
        return f"{user_id}:{today}"

    def check_and_increment(self, user_id: str) -> bool:
        """
        Check if user has exceeded rate limit and increment if not.
        
        Args:
            user_id (str): The user's ID
            
        Returns:
            bool: True if request is allowed, False if rate limit exceeded
            
        Raises:
            RateLimitError: If rate limit is exceeded
        """
        try:
            today_key = self._get_today_key(user_id)
            
            # Try to get existing record
            response = self.dynamodb.get_item(
                table_name=self.table_name,
                key={'id': today_key}
            )
            
            if 'Item' not in response:
                # First request of the day
                self.dynamodb.put_item(
                    table_name=self.table_name,
                    item={
                        'id': today_key,
                        'userId': user_id,
                        'count': 1,
                        'createdAt': str(datetime.now(timezone.utc))
                    }
                )
                return True
            
            current_count = response['Item']['count']
            
            if current_count >= MAX_REQUESTS_PER_DAY:
                raise RateLimitError("Daily rate limit exceeded")
            
            # Increment count
            self.dynamodb.update_item(
                table_name=self.table_name,
                key={'id': today_key},
                update_expression='SET #count = #count + :inc',
                expression_attribute_names={'#count': 'count'},
                expression_attribute_values={':inc': 1}
            )
            
            return True
            
        except RateLimitError:
            raise
        except DynamoDBError as e:
            logger.error(f"Error in rate limit check: {str(e)}", exc_info=True)
            # In case of DynamoDB errors, we'll allow the request to proceed
            # This is a fail-open approach to avoid blocking legitimate requests
            return True 