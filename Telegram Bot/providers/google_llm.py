import os
from google import genai  # Modern 2026 import
from .base import AIProvider

class GoogleProvider(AIProvider):
    def __init__(self):
        # The new client handles authentication via your GEMINI_API_KEY environment variable
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        
        # Using Gemini 3.1 Pro Preview, released Feb 19, 2026
        # Or use "gemini-3-flash-preview" for maximum speed
        self.model_id = "gemini-3.1-pro-preview" 

    def generate(self, prompt):
        # Modern SDK uses the 'models' namespace for generation
        response = self.client.models.generate_content(
            model=self.model_id,
            contents=prompt
        )
        return response.text