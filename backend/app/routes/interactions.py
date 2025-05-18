from flask import Blueprint, request, jsonify
import logging

from app.services.interactions import InteractionsService
from app.routes.auth import requires_auth

logger = logging.getLogger(__name__)

def init_interaction_routes(app, interactions_service: InteractionsService):
    @app.route('/interactions', methods=['GET'])
    @requires_auth
    def get_user_interactions():
        """
        Get all interactions for the authenticated user.
        """
        try:
            user_id = request.user['sub']
            
            # Get the user's interactions
            interactions = interactions_service.get_user_interactions(user_id)
            
            if not interactions:
                return jsonify({
                    "error": "No interactions found",
                    "type": "not_found",
                    "message": "You don't have any interactions yet."
                }), 404
            
            return jsonify(interactions)
            
        except Exception as e:
            logger.error(f"Error getting user interactions: {str(e)}", exc_info=True)
            return jsonify({"error": str(e)}), 500
