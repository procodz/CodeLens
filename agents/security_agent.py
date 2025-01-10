from .base_agent import CodeReviewAgent
import logging
import json
import google.generativeai as genai

class SecurityAgent(CodeReviewAgent):
    def __init__(self):
        prompt = """
        You are a code review expert focusing on security best practices. Analyze code for potential security issues:
        - Input validation issues
        - Data handling concerns
        - Authentication checks
        - Access control
        - Error handling
        
        Return findings in JSON format:
        {
            "severity": "HIGH|MEDIUM|LOW",
            "issues": [
                {
                    "type": "issue_type",
                    "description": "description of potential concern"
                }
            ],
            "recommendations": [
                {
                    "type": "improvement_type",
                    "description": "suggested improvement"
                }
            ]
        }
        """
        super().__init__("SecurityAgent", prompt)

    def get_gemini_response(self, messages):
        try:
            model = genai.GenerativeModel('gemini-pro')
            # Convert messages to plain text format
            prompt_text = "\n".join([m["content"] for m in messages])
            
            generation_config = {
                "temperature": 0.3,  # Lower temperature for more focused responses
                "top_p": 0.8,
                "top_k": 40,
                "max_output_tokens": 1024,
            }
            
            safety_settings = {
                "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_NONE",
                "HARM_CATEGORY_HATE_SPEECH": "BLOCK_NONE",
                "HARM_CATEGORY_HARASSMENT": "BLOCK_NONE",
                "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_NONE"
            }
            
            response = model.generate_content(
                prompt_text,
                generation_config=generation_config,
                safety_settings=safety_settings
            )
            
            if hasattr(response, 'text'):
                return response.text.strip()
            
            # Handle blocked content
            return json.dumps({
                "severity": "ERROR",
                "issues": ["Response blocked by safety settings"],
                "recommendations": []
            })
                
        except Exception as e:
            logging.error(f"Gemini API error: {str(e)}")
            return json.dumps({
                "severity": "ERROR",
                "issues": [f"API error: {str(e)}"],
                "recommendations": []
            })