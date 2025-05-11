from flask import jsonify, request, current_app
import uuid
import logging
from app.routes.auth import requires_auth
from app.services.wardrobe import WardrobeService

logger = logging.getLogger(__name__)

def init_wardrobe_routes(app, wardrobe_service: WardrobeService):
    @app.route('/wardrobe', methods=['POST'])
    @requires_auth
    def add_wardrobe_item():
        user = request.user
        data = request.get_json()
        if not data or 'description' not in data:
            return jsonify({'error': 'Missing description'}), 400

        item_id = str(uuid.uuid4())
        try:
            wardrobe_service.add_wardrobe_item(
                user_id=user['sub'],
                item_id=item_id,
                description=data['description']
            )
            return jsonify({
                'itemId': item_id,
                'description': data['description']
            }), 201
        except Exception as e:
            logger.error(f"Error adding wardrobe item: {str(e)}", exc_info=True)
            if current_app.debug:
                return jsonify({'error': str(e)}), 500
            return jsonify({'error': 'An error occurred while adding the item'}), 500

    @app.route('/wardrobe', methods=['GET'])
    @requires_auth
    def get_wardrobe_items():
        user = request.user
        try:
            items = wardrobe_service.get_wardrobe_items(user['sub'])
            return jsonify({'items': items}), 200
        except Exception as e:
            logger.error(f"Error getting wardrobe items: {str(e)}", exc_info=True)
            if current_app.debug:
                return jsonify({'error': str(e)}), 500
            return jsonify({'error': 'An error occurred while retrieving items'}), 500

    @app.route('/wardrobe/<item_id>', methods=['DELETE'])
    @requires_auth
    def delete_wardrobe_item(item_id):
        user = request.user
        try:
            success = wardrobe_service.delete_wardrobe_item(user['sub'], item_id)
            if success:
                return jsonify({'message': 'Item deleted successfully'}), 200
            return jsonify({'error': 'Failed to delete item'}), 500
        except Exception as e:
            logger.error(f"Error deleting wardrobe item: {str(e)}", exc_info=True)
            if current_app.debug:
                return jsonify({'error': str(e)}), 500
            return jsonify({'error': 'An error occurred while deleting the item'}), 500 
