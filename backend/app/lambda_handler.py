from app import create_app
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.utilities.data_classes import APIGatewayProxyEvent
from aws_lambda_powertools.utilities.parser import parse, BaseModel
from aws_lambda_powertools.utilities.parser.models import APIGatewayProxyEventModel

app = create_app()

def handler(event: dict, context: LambdaContext) -> dict:
    # Convert Lambda event to WSGI environment
    environ = {
        'REQUEST_METHOD': event.get('httpMethod', 'GET'),
        'SCRIPT_NAME': '',
        'PATH_INFO': event.get('path', ''),
        'QUERY_STRING': event.get('queryStringParameters', ''),
        'SERVER_NAME': event.get('headers', {}).get('Host', ''),
        'SERVER_PORT': '443',
        'SERVER_PROTOCOL': 'HTTP/1.1',
        'wsgi.version': (1, 0),
        'wsgi.url_scheme': 'https',
        'wsgi.input': event.get('body', ''),
        'wsgi.errors': None,
        'wsgi.multithread': False,
        'wsgi.multiprocess': False,
        'wsgi.run_once': False,
    }

    # Add headers
    for key, value in event.get('headers', {}).items():
        environ[f'HTTP_{key.upper().replace("-", "_")}'] = value

    # Create response
    response = app(environ, lambda status, headers, exc_info=None: None)

    # Convert WSGI response to Lambda response
    status_code = int(response.status.split()[0])
    headers = dict(response.headers)
    body = b''.join(response.response).decode('utf-8')

    return {
        'statusCode': status_code,
        'headers': headers,
        'body': body
    } 