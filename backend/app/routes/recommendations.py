from flask import Blueprint, request, jsonify
import logging

from app.services.recommendations import RecommendationsService, InsufficientWardrobeError
from app.services.interactions import InteractionsService
from app.services.trips import TripsService
from app.services.text_transformations import TextTransformationsService
from app.services.rate_limit import RateLimitError
from app.routes.auth import requires_auth

logger = logging.getLogger(__name__)

def init_recommendation_routes(app, recommendations_service: RecommendationsService, interactions_service: InteractionsService, trips_service: TripsService, text_transformations_service: TextTransformationsService):
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
        except RateLimitError as e:
            return jsonify({
                "error": str(e),
                "type": "rate_limit",
                "message": "You have exceeded your daily request limit. Please try again tomorrow."
            }), 429
        except Exception as e:
            logger.error(f"Error in outfit recommendation: {str(e)}", exc_info=True)
            return jsonify({"error": str(e)}), 500

    @app.route('/recommend/wear/trip/<trip_id>', methods=['POST'])
    @requires_auth
    def recommend_outfit_for_trip(trip_id):
        """
        Recommend an outfit based on a specific trip's context.
        """
        try:
            user_id = request.user['sub']
            
            # Get trip details
            trip = trips_service.get_trip(trip_id, user_id)
            if not trip:
                return jsonify({"error": "Trip not found"}), 404
            
            data = request.get_json()
            if not data or 'situation' not in data:
                return jsonify({"error": "Missing situation in request"}), 400

            situation = data['situation']

            # Get recommendation based on trip context
            recommendation = recommendations_service.get_trip_outfit_recommendation(
                trip=trip, situation=situation
            )
            
            # Save interaction
            interaction_id = interactions_service.save_recommendation_interaction(
                user_id=user_id,
                situation=situation,
                recommendation=recommendation,
                trip_id=trip_id
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
        except RateLimitError as e:
            return jsonify({
                "error": str(e),
                "type": "rate_limit",
                "message": "You have exceeded your daily request limit. Please try again tomorrow."
            }), 429
        except Exception as e:
            logger.error(f"Error in trip outfit recommendation: {str(e)}", exc_info=True)
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
        except RateLimitError as e:
            return jsonify({
                "error": str(e),
                "type": "rate_limit",
                "message": "You have exceeded your daily request limit. Please try again tomorrow."
            }), 429
        except Exception as e:
            logger.error(f"Error in purchase recommendation: {str(e)}", exc_info=True)
            return jsonify({"error": str(e)}), 500

    @app.route('/recommend/pack', methods=['POST'])
    @requires_auth
    def recommend_packing_list():
        """
        Recommend a packing list based on the user's wardrobe and trip description.
        """
        try:
            data = request.get_json()
            if not data or 'situation' not in data:
                return jsonify({"error": "Missing situation in request"}), 400

            situation = data['situation']
            user_id = request.user['sub']

            # Get recommendation
            packing_list = recommendations_service.get_packing_recommendation(user_id, situation)
            
            # Generate a clean title from the situation
            description = text_transformations_service.generate_trip_title(situation, user_id)
            
            # Save trip
            trip_id = trips_service.save_trip(
                user_id=user_id,
                description=description,
                packing_list=packing_list
            )

            # Save interaction
            interactions_service.save_trip_interaction(
                user_id=user_id,
                description=description,
                packing_list=packing_list
            )
            
            return jsonify({
                "trip_id": trip_id,
                "description": description,
                "packing_list": packing_list
            })
            
        except InsufficientWardrobeError as e:
            return jsonify({
                "error": str(e),
                "type": "insufficient_wardrobe",
                "message": "Please add more items to your wardrobe before requesting recommendations."
            }), 400
        except RateLimitError as e:
            return jsonify({
                "error": str(e),
                "type": "rate_limit",
                "message": "You have exceeded your daily request limit. Please try again tomorrow."
            }), 429
        except Exception as e:
            logger.error(f"Error in packing list recommendation: {str(e)}", exc_info=True)
            return jsonify({"error": str(e)}), 500
