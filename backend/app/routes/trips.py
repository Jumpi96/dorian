from flask import Blueprint, request, jsonify
import logging

from app.services.trips import TripsService
from app.routes.auth import requires_auth

logger = logging.getLogger(__name__)

def init_trip_routes(app, trips_service: TripsService):
    @app.route('/trips', methods=['GET'])
    @requires_auth
    def get_user_trip():
        """
        Get the user's most recent trip.
        """
        try:
            user_id = request.user['sub']
            
            # Get the user's trip
            trip = trips_service.get_user_trip(user_id)
            
            if not trip:
                return jsonify({
                    "error": "No trip found",
                    "type": "not_found",
                    "message": "You don't have any trips yet."
                }), 404
            
            return jsonify(trip)
            
        except Exception as e:
            logger.error(f"Error getting user trip: {str(e)}", exc_info=True)
            return jsonify({"error": str(e)}), 500

    @app.route('/trips/<trip_id>', methods=['DELETE'])
    @requires_auth
    def delete_trip(trip_id: str):
        """
        Delete a specific trip.
        
        Args:
            trip_id (str): The ID of the trip to delete
        """
        try:
            user_id = request.user['sub']
            
            # Delete the trip
            trips_service.delete_trip(user_id, trip_id)
            
            return jsonify({
                "message": "Trip deleted successfully"
            })
            
        except Exception as e:
            logger.error(f"Error deleting trip: {str(e)}", exc_info=True)
            return jsonify({"error": str(e)}), 500 