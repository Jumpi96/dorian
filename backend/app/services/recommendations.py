import logging
from app.services.llm import LLMService
from app.services.wardrobe import WardrobeService
from app.services.rate_limit import RateLimitError

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
            RateLimitError: If the user has exceeded their daily rate limit
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
            
            return self._generate_outfit_recommendation(wardrobe_items, situation, user_id)
            
        except InsufficientWardrobeError:
            raise
        except RateLimitError:
            logger.error("Rate limit exceeded while getting outfit recommendation", exc_info=True)
            raise
        except Exception as e:
            logger.error(f"Error getting outfit recommendation: {str(e)}", exc_info=True)
            raise

    def get_trip_outfit_recommendation(self, trip: dict, situation: str) -> dict:
        """
        Get an outfit recommendation based on a trip's packing list and situation.
        
        Args:
            trip (dict): The trip object containing description and packing list
            situation (str): The situation the user described
            
        Returns:
            dict: The outfit recommendation
            
        Raises:
            RateLimitError: If the user has exceeded their daily rate limit
            Exception: If there's an error getting the recommendation
        """
        try:
            # Transform packing list dictionary into a list of items
            packing_list = []
            for _, items in trip['packingList'].items():
                if isinstance(items, list):
                    packing_list.extend(items)
                else:
                    packing_list.append(items)

            # Create wardrobe items from the packing list
            wardrobe_items = [{"description": item} for item in packing_list]
            
            return self._generate_outfit_recommendation(wardrobe_items, situation, trip['userId'])
            
        except RateLimitError:
            logger.error("Rate limit exceeded while getting trip outfit recommendation", exc_info=True)
            raise
        except Exception as e:
            logger.error(f"Error getting trip outfit recommendation: {str(e)}", exc_info=True)
            raise

    def _generate_outfit_recommendation(self, wardrobe_items: list, situation: str, user_id: str) -> dict:
        """
        Internal method to generate outfit recommendations.
        
        Args:
            wardrobe_items (list): List of wardrobe items
            situation (str): The situation description
            user_id (str): The user's ID
            
        Returns:
            dict: The outfit recommendation
            
        Raises:
            RateLimitError: If the user has exceeded their daily rate limit
            Exception: If there's an error generating the recommendation
        """
        try:
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
        except RateLimitError:
            logger.error("Rate limit exceeded while generating outfit recommendation", exc_info=True)
            raise
        except Exception as e:
            logger.error(f"Error generating outfit recommendation: {str(e)}", exc_info=True)
            raise

    def get_items_to_buy_recommendation(self, user_id: str, situation: str) -> dict:
        """
        Get a recommendation for a single item to buy based on the user's wardrobe and situation.
        
        Args:
            user_id (str): The user's ID
            situation (str): The situation the user described
            
        Returns:
            dict: The item to buy recommendation with format:
                {
                    "item": "description of the item to buy",
                    "explanation": "detailed explanation of why this item would be beneficial"
                }
        
        Raises:
            InsufficientWardrobeError: If user has fewer than MIN_WARDROBE_ITEMS items
            RateLimitError: If the user has exceeded their daily rate limit
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

Recommend ONE item they should buy to improve their wardrobe for this situation. Format the response as a JSON object with the following structure:
{{
    "item": "detailed description of the item to buy",
    "explanation": "detailed explanation of why this item would be beneficial for the situation, including how it complements their existing wardrobe"
}}"""

            # Get recommendation from LLM
            return self.llm_service.get_completion(prompt, user_id)
            
        except InsufficientWardrobeError:
            raise
        except RateLimitError:
            logger.error("Rate limit exceeded while getting items to buy recommendation", exc_info=True)
            raise
        except Exception as e:
            logger.error(f"Error getting items to buy recommendation: {str(e)}", exc_info=True)
            raise 

    def get_packing_recommendation(self, user_id: str, situation: str) -> dict:
        """
        Get a packing list recommendation based on the user's wardrobe and trip situation.
        
        Args:
            user_id (str): The user's ID
            situation (str): The trip situation
            
        Returns:
            dict: The packing list recommendation with format:
                {
                    "tops": ["item1", "item2", ...],
                    "bottoms": ["item1", "item2", ...],
                    "shoes": ["item1", "item2", ...],
                    "outerwear": ["item1", "item2", ...],
                    "accessories": ["item1", "item2", ...]
                }
            
        Raises:
            InsufficientWardrobeError: If user has fewer than MIN_WARDROBE_ITEMS items
            RateLimitError: If the user has exceeded their daily rate limit
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

The user is planning this trip: {situation}

Recommend a packing list using only items from their wardrobe. Format the response as a JSON object with the following structure:
{{
    "tops": ["list of tops"],
    "bottoms": ["list of bottoms"],
    "shoes": ["list of shoes"],
    "outerwear": ["list of outerwear"],
    "accessories": ["list of accessories"]
}}

Each list should contain 2-3 items that would be appropriate for the trip."""

            # Get recommendation from LLM
            return self.llm_service.get_completion(prompt, user_id)
            
        except InsufficientWardrobeError:
            raise
        except RateLimitError:
            logger.error("Rate limit exceeded while getting packing recommendation", exc_info=True)
            raise
        except Exception as e:
            logger.error(f"Error getting packing recommendation: {str(e)}", exc_info=True)
            raise 