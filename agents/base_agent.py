import google.generativeai as genai
import json
import logging
import os
from dotenv import load_dotenv

class CodeReviewAgent:
    def __init__(self, name, role_prompt):
        self.name = name
        self.role_prompt = role_prompt + """
        IMPORTANT: Response must be a valid JSON object with this exact structure:
        {
            "severity": "HIGH|MEDIUM|LOW",
            "issues": ["issue1", "issue2"],
            "recommendations": ["rec1", "rec2"]
        }
        """
        load_dotenv()
        try:
            genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        except Exception as e:
            logging.error(f"Failed to configure Gemini API: {str(e)}")
            raise
        
    def get_gemini_response(self, messages):
        try:
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content([m["content"] for m in messages])
            logging.info(f"Agent {self.name} raw response: {response.text}")
            return response.text.strip()
        except Exception as e:
            logging.error(f"Gemini API error in {self.name}: {str(e)}")
            return json.dumps({
                "severity": "ERROR",
                "issues": [f"API error: {str(e)}"],
                "recommendations": []
            })
        
    def build_messages(self, code, previous_reviews):
        messages = [
            {"role": "system", "content": self.role_prompt},
            {"role": "user", "content": f"Review this code:\n\n{code}"}
        ]
        if previous_reviews:
            messages.append({
                "role": "system", 
                "content": f"Previous review findings: {json.dumps(previous_reviews)}"
            })
        return messages
    
    def format_response(self, response):
        try:
            # Try to extract JSON if response contains other text
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            if start_idx >= 0 and end_idx > 0:
                json_str = response[start_idx:end_idx]
                result = json.loads(json_str)
                
                # Validate required fields
                required_fields = ['severity', 'issues', 'recommendations']
                if not all(field in result for field in required_fields):
                    raise ValueError("Missing required fields in response")
                    
                return result
            else:
                raise ValueError("No JSON object found in response")
                
        except Exception as e:
            logging.error(f"Failed to parse {self.name} response: {str(e)}\nResponse: {response}")
            return {
                "severity": "ERROR",
                "issues": [f"Failed to parse response: {str(e)}"],
                "recommendations": []
            }
            
    def review(self, code, previous_reviews=None):
        messages = self.build_messages(code, previous_reviews)
        response = self.get_gemini_response(messages)
        return self.format_response(response)