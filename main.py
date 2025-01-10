import logging
import os
import sys
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
import google.generativeai as genai

from agents.agent_factory import AgentFactory
from utils.code_parser import parse_code
from utils.result_formatter import format_review_results

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
        sys.exit(1)

def main():
    try:
        # Initialize environment
        init_environment()
        
        # Get code input
        code_input = input("Paste your code for review: ")
        parsed_code = parse_code(code_input)
        
        # Initialize review pipeline
        factory = AgentFactory()
        agents = factory.create_agents()
        
        review_results = {}
        for agent in agents:
            try:
                results = agent.review(parsed_code, review_results)
                review_results[agent.name] = results
            except Exception as e:
                logger.error(f"Error in {agent.name}: {str(e)}")
                review_results[agent.name] = {
                    "severity": "ERROR",
                    "issues": [f"Agent error: {str(e)}"],
                    "recommendations": []
                }
    
        print(format_review_results(review_results))
    except Exception as e:
        logger.error(f"Main error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()