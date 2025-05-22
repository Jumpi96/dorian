from app import create_app
import awsgi

app = create_app()

def lambda_handler(event, context):
    return awsgi.response(app, event, context) 