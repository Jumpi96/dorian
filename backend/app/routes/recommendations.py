from flask import Blueprint, request, jsonify
import logging

from app.services.recommendations import RecommendationsService, InsufficientWardrobeError
from app.services.interactions import InteractionsService
from app.routes.auth import requires_auth

logger = logging.getLogger(__name__)

def init_recommendation_routes(app, recommendations_service: RecommendationsService, interactions_service: InteractionsService):
    @app.route('/recommend/wear', methods=['POST'])
    @requires_auth
    def recommend_outfit():
        """
        Recommend an outfit based on the user's wardrobe and situation.
        """
        try:
            data = request.get_json()
            if not data or 'situation' not in data:
                return jsonify({"error": "Missing situation in request"}), 400

            situation = data['situation']
            user_id = request.user['sub']

            # Get recommendation
            recommendation = recommendations_service.get_outfit_recommendation(user_id, situation)
            
            # Save interaction
            interaction_id = interactions_service.save_recommendation_interaction(
                user_id=user_id,
                situation=situation,
                recommendation=recommendation
            )
            
            return jsonify({
                "outfit": recommendation,
                "interaction_id": interaction_id
            })
            
        except InsufficientWardrobeError as e:
            return jsonify({
                "error": str(e),
                "type": "insufficient_wardrobe",
                "message": "Please add more items to your wardrobe before requesting recommendations."
            }), 400
        except Exception as e:
            logger.error(f"Error in outfit recommendation: {str(e)}", exc_info=True)
            return jsonify({"error": str(e)}), 500

    @app.route('/recommend/buy', methods=['POST'])
    @requires_auth
    def recommend_items_to_buy():
        """
        Recommend a single item to buy based on the user's situation and current wardrobe.
        """
        try:
            data = request.get_json()
            if not data or 'situation' not in data:
                return jsonify({"error": "Missing situation in request"}), 400

            situation = data['situation']
            user_id = request.user['sub']

            # Get recommendation
            recommendation = recommendations_service.get_items_to_buy_recommendation(user_id, situation)
            
            # Save interaction
            interaction_id = interactions_service.save_purchase_recommendation_interaction(
                user_id=user_id,
                situation=situation,
                recommendation=recommendation
            )
            
            return jsonify({
                "item_to_buy": recommendation,
                "interaction_id": interaction_id
            })
            
        except InsufficientWardrobeError as e:
            return jsonify({
                "error": str(e),
                "type": "insufficient_wardrobe",
                "message": "Please add more items to your wardrobe before requesting recommendations."
            }), 400
        except Exception as e:
            logger.error(f"Error in purchase recommendation: {str(e)}", exc_info=True)
            return jsonify({"error": str(e)}), 500
