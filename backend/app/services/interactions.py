import logging
from datetime import datetime, UTC
from app.clients.dynamodb import DynamoDBClient, DynamoDBError
from app.config import Config

logger = logging.getLogger(__name__)

INTERACTIONS_TABLE = f'{Config.ENV}-interactions'

class InteractionsService:
    def __init__(self, dynamodb_client: DynamoDBClient):
        self.dynamodb = dynamodb_client
        self.table_name = INTERACTIONS_TABLE

    def save_recommendation_interaction(self, user_id: str, situation: str, recommendation: dict, trip_id: str = None) -> str:
        """
        Save an outfit recommendation interaction to DynamoDB.
        
        Args:
            user_id (str): The user's ID
            situation (str): The situation the user described
            recommendation (dict): The outfit recommendation
            
        Returns:
            str: The interaction ID
            
        Raises:
            DynamoDBError: If there's an error saving to DynamoDB
        """
        try:
            timestamp = datetime.now(UTC).isoformat()
            interaction_id = f"rec_{timestamp}"
            self.dynamodb.put_item(
                table_name=self.table_name,
                item={
                    "interactionId": interaction_id,
                    "userId": user_id,
                    "type": "outfit_recommendation",
                    "situation": situation,
                    "recommendation": recommendation,
                    "tripId": trip_id,
                    "createdAt": timestamp
                }
            )
            
            return interaction_id
        except DynamoDBError as e:
            logger.error(f"Error saving recommendation interaction: {str(e)}", exc_info=True)
            raise

    def save_purchase_recommendation_interaction(self, user_id: str, situation: str, recommendation: dict) -> str:
        """
        Save a purchase recommendation interaction to DynamoDB.
        
        Args:
            user_id (str): The user's ID
            situation (str): The situation the user described
            recommendation (dict): The item to buy recommendation
            
        Returns:
            str: The interaction ID
            
        Raises:
            DynamoDBError: If there's an error saving to DynamoDB
        """
        try:
            timestamp = datetime.now(UTC).isoformat()
            interaction_id = f"buy_{timestamp}"
            self.dynamodb.put_item(
                table_name=self.table_name,
                item={
                    "interactionId": interaction_id,
                    "userId": user_id,
                    "type": "purchase_recommendation",
                    "situation": situation,
                    "recommendation": recommendation,
                    "createdAt": timestamp
                }
            )
            return interaction_id
        except DynamoDBError as e:
            logger.error(f"Error saving purchase recommendation interaction: {str(e)}", exc_info=True)
            raise

    def save_trip_interaction(self, user_id: str, description: str, packing_list: dict) -> str:
        """
        Save a trip interaction to DynamoDB.
        
        Args:
            user_id (str): The user's ID
            description (str): The trip description
            packing_list (dict): The complete packing list recommendation
            
        Returns:
            str: The trip ID
            
        Raises:
            DynamoDBError: If there's an error saving to DynamoDB
        """
        try:
            timestamp = datetime.now(UTC).isoformat()
            trip_id = f"trip_{timestamp}"
            
            self.dynamodb.put_item(
                table_name=self.table_name,
                item={
                    "interactionId": trip_id,
                    "userId": user_id,
                    "type": "trip",
                    "description": description,
                    "recommendation": {
                        "packingList": packing_list
                    },
                    "createdAt": timestamp
                }
            )
            
            return trip_id
        except DynamoDBError as e:
            logger.error(f"Error saving trip interaction: {str(e)}", exc_info=True)
            raise

    def get_user_interactions(self, user_id: str) -> list:
        """
        Get all interactions for a user from DynamoDB, sorted by creation date in descending order.
        
        Args:
            user_id (str): The user's ID
            
        Returns:
            list: List of user interactions
            
        Raises:
            DynamoDBError: If there's an error querying DynamoDB
        """
        try:
            response = self.dynamodb.query(
                table_name=self.table_name,
                key_condition_expression="userId = :user_id",
                expression_attribute_values={":user_id": user_id},
                scan_index_forward=False  # This will sort in descending order
            )
            
            return response.get('Items', [])
        except DynamoDBError as e:
            logger.error(f"Error getting user interactions: {str(e)}", exc_info=True)
            raise

    def delete_interaction(self, user_id: str, interaction_id: str) -> None:
        """
        Delete a specific interaction from DynamoDB.
        
        Args:
            user_id (str): The user's ID
            interaction_id (str): The interaction ID to delete
            
        Raises:
            DynamoDBError: If there's an error deleting from DynamoDB
        """
        try:
            self.dynamodb.delete_item(
                table_name=self.table_name,
                key={
                    "userId": user_id,
                    "interactionId": interaction_id
                }
            )
        except DynamoDBError as e:
            logger.error(f"Error deleting interaction: {str(e)}", exc_info=True)
            raise 