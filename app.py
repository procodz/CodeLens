from flask import Flask, request, jsonify
from flask_cors import CORS
from agents.agent_factory import AgentFactory
from utils.code_parser import parse_code
from utils.result_formatter import format_review_results
import logging
import os
from dotenv import load_dotenv, find_dotenv
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_environment():
    """Initialize environment variables"""
    try:
        # Find and load .env file
        env_path = find_dotenv()
        if not env_path:
            logger.warning(".env file not found")
        load_dotenv(env_path)
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    except Exception as e:
        logger.error(f"Error loading environment variables: {str(e)}")
        raise

@app.route('/review', methods=['POST'])
def review_code():
    try:
        init_environment()
        code_input = request.json.get('code')
        if not code_input:
            return jsonify({"error": "No code provided"}), 400
            
        logger.info(f"Received code review request")
        parsed_code = parse_code(code_input)
        
        factory = AgentFactory()
        agents = factory.create_agents()
        
        review_results = {}
        for agent in agents:
            try:
                results = agent.review(parsed_code, review_results)
                review_results[agent.name] = results
                logger.info(f"{agent.name} review complete")
            except Exception as e:
                logger.error(f"Error in {agent.name}: {str(e)}")
                review_results[agent.name] = {
                    "severity": "ERROR",
                    "issues": [f"Agent error: {str(e)}"],
                    "recommendations": []
                }
        
        formatted_results = format_review_results(review_results)
        return jsonify({"results": formatted_results})
    except Exception as e:
        logger.error(f"Review error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)