# commission/gateways.py

import json
from groq import Groq
from django.conf import settings

class GroqGateway:
    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)

    def extract_meeting_summary_info(self, content):
        prompt = f"""
        Extract the following information from the meeting summary:
        - Client Name
        - Product Name
        - Product Category (e.g., INSURANCE, INVESTMENT)
        - Product Type (e.g., Term, Whole Life, etc.)
        - Amount

        Meeting Summary:
        {content}

        Please provide the extracted information in JSON format.
        """

        response = self.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )

        # Extract the content from the response
        json_str = response.choices[0].message.content.strip()
        
        # Try to parse the entire response as JSON first
        try:
            extracted_info = json.loads(json_str)
        except json.JSONDecodeError:
            # If that fails, try to extract JSON from markdown code blocks
            try:
                json_str = json_str.split('```')[1]  # This works for both ```json and ``` without a language specifier
                extracted_info = json.loads(json_str)
            except (IndexError, json.JSONDecodeError):
                # If JSON parsing fails, return a default structure
                extracted_info = {
                    "client_name": "Unknown",
                    "product_name": "Unknown",
                    "product_category": "Unknown",
                    "product_type": "Unknown",
                    "amount": 0
                }

        return extracted_info