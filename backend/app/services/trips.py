import logging
from datetime import datetime, UTC
from app.clients.dynamodb import DynamoDBClient, DynamoDBError

logger = logging.getLogger(__name__)

TRIPS_TABLE = 'dev-trips'

class TripsService:
    def __init__(self, dynamodb_client: DynamoDBClient):
        self.dynamodb = dynamodb_client
        self.table_name = TRIPS_TABLE

    def save_trip(self, user_id: str, description: str, packing_list: dict) -> str:
        """
        Save a trip to DynamoDB.
        
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
                    "tripId": trip_id,
                    "userId": user_id,
                    "description": description,
                    "packingList": packing_list,
                    "createdAt": timestamp
                }
            )
            
            return trip_id
        except DynamoDBError as e:
            logger.error(f"Error saving trip: {str(e)}", exc_info=True)
            raise 