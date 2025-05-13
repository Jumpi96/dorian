import boto3
from botocore.exceptions import ClientError
from app.config import Config
import logging

logger = logging.getLogger(__name__)

class DynamoDBError(Exception):
    """Base exception for DynamoDB related errors"""
    pass

class DynamoDBClient:
    def __init__(self):
        self.client = boto3.resource(
            'dynamodb',
            aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
            region_name=Config.AWS_REGION
        )
    
    def get_table(self, table_name: str):
        """Get a DynamoDB table by name"""
        return self.client.Table(table_name)
    
    def put_item(self, table_name: str, item: dict) -> bool:
        """Put an item in a DynamoDB table"""
        try:
            table = self.get_table(table_name)
            table.put_item(Item=item)
            return True
        except (ClientError, Exception) as e:
            logger.error(f"Error putting item in {table_name}: {str(e)}", exc_info=True)
            raise DynamoDBError(f"Failed to put item in {table_name}: {str(e)}")
    
    def get_item(self, table_name: str, key: dict) -> dict:
        """Get an item from a DynamoDB table"""
        try:
            table = self.get_table(table_name)
            response = table.get_item(Key=key)
            return response
        except (ClientError, Exception) as e:
            logger.error(f"Error getting item from {table_name}: {str(e)}", exc_info=True)
            raise DynamoDBError(f"Failed to get item from {table_name}: {str(e)}")
    
    def update_item(self, table_name: str, key: dict, update_expression: str, 
                   expression_attribute_names: dict, expression_attribute_values: dict) -> bool:
        """Update an item in a DynamoDB table"""
        try:
            table = self.get_table(table_name)
            table.update_item(
                Key=key,
                UpdateExpression=update_expression,
                ExpressionAttributeNames=expression_attribute_names,
                ExpressionAttributeValues=expression_attribute_values
            )
            return True
        except (ClientError, Exception) as e:
            logger.error(f"Error updating item in {table_name}: {str(e)}", exc_info=True)
            raise DynamoDBError(f"Failed to update item in {table_name}: {str(e)}")
    
    def delete_item(self, table_name: str, key: dict) -> bool:
        """Delete an item from a DynamoDB table"""
        try:
            table = self.get_table(table_name)
            table.delete_item(Key=key)
            return True
        except (ClientError, Exception) as e:
            logger.error(f"Error deleting item from {table_name}: {str(e)}", exc_info=True)
            raise DynamoDBError(f"Failed to delete item from {table_name}: {str(e)}")
    
    def query(self, table_name: str, key_condition_expression: str, 
             expression_attribute_values: dict, scan_index_forward: bool = True,
             limit: int = None) -> dict:
        """
        Query items from a DynamoDB table
        
        Args:
            table_name (str): Name of the table to query
            key_condition_expression (str): The condition expression for the query
            expression_attribute_values (dict): Values for the condition expression
            scan_index_forward (bool): Whether to scan forward or backward (default: True)
            limit (int): Maximum number of items to return (default: None)
            
        Returns:
            dict: The query response containing Items and other metadata
        """
        try:
            table = self.get_table(table_name)
            query_params = {
                'KeyConditionExpression': key_condition_expression,
                'ExpressionAttributeValues': expression_attribute_values,
                'ScanIndexForward': scan_index_forward
            }
            
            if limit is not None:
                query_params['Limit'] = limit
                
            response = table.query(**query_params)
            return response
        except (ClientError, Exception) as e:
            logger.error(f"Error querying items from {table_name}: {str(e)}", exc_info=True)
            raise DynamoDBError(f"Failed to query items from {table_name}: {str(e)}") 