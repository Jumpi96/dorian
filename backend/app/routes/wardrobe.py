from flask import jsonify, request
import uuid
from app.routes.auth import requires_auth

def init_wardrobe_routes(app, dynamodb):
    @app.route('/wardrobe/add', methods=['POST'])
    @requires_auth
    def add_wardrobe_item():
        user = request.user
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
    @requires_auth
    def get_wardrobe_items():
        user = request.user
        try:
            items = dynamodb.get_wardrobe_items(user['sub'])
            return jsonify({'items': items}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500 