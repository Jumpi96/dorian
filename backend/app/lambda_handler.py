from app import create_app
from awsgi import response

app = create_app()

def handler(event, context):
    return response(app, event, context) 