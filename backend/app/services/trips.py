import logging
from datetime import datetime, UTC
from app.clients.dynamodb import DynamoDBClient, DynamoDBError

logger = logging.getLogger(__name__)

TRIPS_TABLE = 'dev-trips'

class TripNotFoundError(Exception):
    """Exception raised when a trip is not found"""
    pass

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

    def get_user_trip(self, user_id: str) -> dict:
        """
        Get the user's most recent trip.
        
        Args:
            user_id (str): The user's ID
            
        Returns:
            dict: The trip data or None if no trip found
            
        Raises:
            DynamoDBError: If there's an error querying DynamoDB
        """
        try:
            # Query trips by userId, sorted by createdAt in descending order
            response = self.dynamodb.query(
                table_name=self.table_name,
                key_condition_expression='userId = :uid',
                expression_attribute_values={':uid': user_id},
                scan_index_forward=False,  # Sort in descending order
                limit=1  # Get only the most recent trip
            )
            
            if not response.get('Items'):
                return None
                
            return response['Items'][0]
            
        except DynamoDBError as e:
            logger.error(f"Error getting user trip: {str(e)}", exc_info=True)
            raise

    def delete_trip(self, user_id: str, trip_id: str) -> None:
        """
        Delete a specific trip.
        
        Args:
            user_id (str): The user's ID
            trip_id (str): The ID of the trip to delete
            
        Raises:
            TripNotFoundError: If the trip is not found
            DynamoDBError: If there's an error deleting from DynamoDB
        """
        try:
            # First verify the trip exists and belongs to the user
            response = self.dynamodb.get_item(
                table_name=self.table_name,
                key={
                    'userId': user_id,
                    'tripId': trip_id
                }
            )
            
            if 'Item' not in response:
                raise TripNotFoundError(f"Trip {trip_id} not found")
            
            # Delete the trip
            self.dynamodb.delete_item(
                table_name=self.table_name,
                key={
                    'userId': user_id,
                    'tripId': trip_id
                }
            )
            
        except TripNotFoundError:
            raise
        except DynamoDBError as e:
            logger.error(f"Error deleting trip: {str(e)}", exc_info=True)
            raise 