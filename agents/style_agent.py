from .base_agent import CodeReviewAgent
import logging
import json
import google.generativeai as genai

class StyleAgent(CodeReviewAgent):
    def __init__(self):
        prompt = """
        You are a Python code style expert. Analyze code for PEP 8 compliance and best practices.
        Provide all responses in English only.

        Check for:
        - PEP 8 style guide compliance
        - Naming conventions (snake_case for functions/variables, PascalCase for classes)
        - Proper indentation (4 spaces)
        - Line length limits (79 characters)
        - Import organization
        - Whitespace usage
        - Comment and docstring style
        
        Provide findings in JSON format:
        {
            "severity": "HIGH|MEDIUM|LOW",
            "issues": [
                {
                    "type": "style_violation",
                    "description": "Description of the style issue in English"
                }
            ],
            "recommendations": [
                {
                    "type": "style_fix",
                    "description": "Description of the recommended fix in English"
                }
            ]
        }

        IMPORTANT: All responses must be in English language only.
        """
        super().__init__("StyleAgent", prompt)

    def get_gemini_response(self, messages):
        """Override to ensure English responses"""
        try:
            model = genai.GenerativeModel('gemini-pro')
            generation_config = {
                "temperature": 0.3,
                "top_p": 0.8,
                "top_k": 40,
                "max_output_tokens": 1024,
            }
            
            response = model.generate_content(
                [m["content"] for m in messages],
                generation_config=generation_config
            )
            
            if hasattr(response, 'text'):
                return response.text.strip()
            
            return json.dumps({
                "severity": "ERROR",
                "issues": ["Failed to generate style review"],
                "recommendations": []
            })
                
        except Exception as e:
            logging.error(f"Style review error: {str(e)}")
            return json.dumps({
                "severity": "ERROR",
                "issues": [f"Style review error: {str(e)}"],
                "recommendations": []
            })

    def review(self, code, previous_reviews=None):
        """Review code for style issues"""
        try:
            messages = self.build_messages(code, previous_reviews)
            response = self.get_gemini_response(messages)
            return self.format_response(response)
        except Exception as e:
            logging.error(f"Style review failed: {str(e)}")
            return {
                "severity": "ERROR",
                "issues": [f"Style review failed: {str(e)}"],
                "recommendations": []
            }