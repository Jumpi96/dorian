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

    @app.route('/interactions/<interaction_id>/feedback', methods=['PATCH'])
    @requires_auth
    def update_interaction_feedback(interaction_id):
        """
        Update an interaction with user feedback.
        
        Args:
            interaction_id (str): The ID of the interaction to update
            
        Request body:
            {
                "feedback": 1  # 1 for positive, 0 for negative
            }
        """
        try:
            user_id = request.user['sub']
            data = request.get_json()
            
            if not data or 'feedback' not in data:
                return jsonify({
                    "error": "Missing feedback",
                    "type": "validation_error",
                    "message": "Feedback value is required"
                }), 400
                
            feedback = data['feedback']
            if feedback not in [0, 1]:
                return jsonify({
                    "error": "Invalid feedback value",
                    "type": "validation_error",
                    "message": "Feedback must be either 0 or 1"
                }), 400
            
            # Update the interaction with feedback
            interactions_service.update_interaction_feedback(user_id, interaction_id, feedback)
            
            return jsonify({
                "message": "Feedback updated successfully"
            })
            
        except Exception as e:
            logger.error(f"Error updating interaction feedback: {str(e)}", exc_info=True)
            return jsonify({"error": str(e)}), 500
