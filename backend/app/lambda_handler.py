from app import create_app
import awsgi
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = create_app()

def lambda_handler(event, context):
    logger.info(f"Received event: {json.dumps(event)}")
    return awsgi.response(app, event, context) 