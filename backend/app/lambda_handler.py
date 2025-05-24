from app import create_app
import awsgi
import json

app = create_app()

def lambda_handler(event, context):
    """
    AWS Lambda handler function that processes API Gateway events.
    Handles both API Gateway v1.0 and v2.0 formats.
    """
    
    # Check if this is a v2.0 event
    if 'requestContext' in event and 'http' in event['requestContext']:
        # Convert v2.0 event to v1.0 format for awsgi
        v1_event = {
            'httpMethod': event['requestContext']['http']['method'],
            'path': event['requestContext']['http']['path'],
            'headers': event.get('headers', {}),
            'queryStringParameters': event.get('queryStringParameters', {}),
            'body': event.get('body', ''),
            'isBase64Encoded': event.get('isBase64Encoded', False)
        }
        return awsgi.response(app, v1_event, context)
    
    # If it's already v1.0 format, use it directly
    return awsgi.response(app, event, context) 