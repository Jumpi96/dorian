import os
import json
import logging
from openai import OpenAI
from app.config import Config

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)

    def get_completion(self, prompt: str, model: str = "gpt-3.5-turbo") -> dict:
        """
        Get a completion from the OpenAI API.
        
        Args:
            prompt (str): The prompt to send to the model
            model (str): The model to use (default: gpt-3.5-turbo)
            
        Returns:
            dict: The parsed JSON response from the API
            
        Raises:
            Exception: If there's an error calling the API or parsing the response
        """
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                response_format={ "type": "json_object" }
            )
            
            try:
                return json.loads(response.choices[0].message.content)
            except json.JSONDecodeError as e:
                logger.error(f"Error parsing JSON response: {str(e)}", exc_info=True)
                raise Exception(f"Failed to parse JSON response: {str(e)}")
            
        except Exception as e:
            logger.error(f"Error calling OpenAI API: {str(e)}", exc_info=True)
            raise Exception(f"Failed to get completion from OpenAI: {str(e)}") 