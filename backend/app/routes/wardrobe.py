from flask import jsonify, request
import uuid
from app.routes.auth import get_user_from_token

def init_wardrobe_routes(app, dynamodb):
    @app.route('/wardrobe/add', methods=['POST'])
    def add_wardrobe_item():
        user = get_user_from_token()
        if not user:
            return jsonify({'error': 'Unauthorized'}), 401

        data = request.get_json()
        if not data or 'description' not in data:
            return jsonify({'error': 'Missing description'}), 400

        item_id = str(uuid.uuid4())
        try:
            dynamodb.add_wardrobe_item(
                user_id=user['sub'],
                item_id=item_id,
                description=data['description']
            )
            return jsonify({
                'itemId': item_id,
                'description': data['description']
            }), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/wardrobe', methods=['GET'])
    def get_wardrobe_items():
        user = get_user_from_token()
        if not user:
            return jsonify({'error': 'Unauthorized'}), 401

        try:
            items = dynamodb.get_wardrobe_items(user['sub'])
            return jsonify({'items': items}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500 