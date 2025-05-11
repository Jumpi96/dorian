import logging
from app.services.llm import LLMService
from app.services.wardrobe import WardrobeService

logger = logging.getLogger(__name__)

class InsufficientWardrobeError(Exception):
    """Exception raised when user has insufficient items in their wardrobe for recommendations"""
    pass 

MIN_WARDROBE_ITEMS = 3

class RecommendationsService:
    def __init__(self, llm_service: LLMService, wardrobe_service: WardrobeService):
        self.llm_service = llm_service
        self.wardrobe_service = wardrobe_service

    def get_outfit_recommendation(self, user_id: str, situation: str) -> dict:
        """
        Get an outfit recommendation based on the user's wardrobe and situation.
        
        Args:
            user_id (str): The user's ID
            situation (str): The situation the user described
            
        Returns:
            dict: The outfit recommendation
            
        Raises:
            InsufficientWardrobeError: If user has fewer than MIN_WARDROBE_ITEMS items
            Exception: If there's an error getting the recommendation
        """
        try:
            # Get user's wardrobe items
            wardrobe_items = self.wardrobe_service.get_wardrobe_items(user_id)
            
            # Check if user has enough items
            if len(wardrobe_items) < MIN_WARDROBE_ITEMS:
                raise InsufficientWardrobeError(
                    f"Need at least {MIN_WARDROBE_ITEMS} items in wardrobe for recommendations. "
                    f"Current items: {len(wardrobe_items)}"
                )
            
            # Construct the prompt
            wardrobe_description = "\n".join([item["description"] for item in wardrobe_items])
            prompt = f"""Given the following wardrobe items:
{wardrobe_description}

The user is in this situation: {situation}

Recommend an outfit using only items from their wardrobe. Format the response as a JSON object with the following structure:
{{
    "top": "description of top",
    "bottom": "description of bottom",
    "shoes": "description of shoes",
    "outerwear": "description of outerwear (optional)",
    "accessories": "description of accessories (optional)"
}}"""

            # Get recommendation from LLM
            return self.llm_service.get_completion(prompt, user_id)
            
        except InsufficientWardrobeError:
            raise
        except Exception as e:
            logger.error(f"Error getting outfit recommendation: {str(e)}", exc_info=True)
            raise 