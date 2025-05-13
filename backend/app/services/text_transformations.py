import logging
from app.services.llm import LLMService

logger = logging.getLogger(__name__)

class TextTransformationsService:
    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service

    def generate_trip_title(self, situation: str, user_id: str) -> str:
        """
        Generate a clean, concise title from a trip situation description.
        
        Args:
            situation (str): The trip situation description
            user_id (str): The user's ID
            
        Returns:
            str: A clean, concise title for the trip
            
        Raises:
            Exception: If there's an error generating the title
        """
        try:
            prompt = f"""Given this trip situation:
{situation}

Generate a clean, concise title (max 5 words) that summarizes this trip. 
The title should be professional and easy to understand.
Return the response as a JSON object with a single field 'title' containing the title text."""

            # Get title from LLM
            response = self.llm_service.get_completion(prompt, user_id)
            
            # Extract title from JSON response
            title = response.get('title', '').strip().strip('"\'')
            
            return title
            
        except Exception as e:
            logger.error(f"Error generating trip title: {str(e)}", exc_info=True)
            raise 