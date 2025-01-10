from .base_agent import CodeReviewAgent
import ast
import logging
from typing import Dict, Any

class PerformanceAgent(CodeReviewAgent):
    def __init__(self):
        prompt = """
        You are a performance optimization expert. Analyze code for:
        - Time complexity (Big O notation)
        - Space complexity analysis
        - Resource usage and memory management
        - Performance bottlenecks
        - Optimization opportunities
        - Algorithmic efficiency
        - Caching and memoization needs
        
        Focus on concrete metrics and provide specific recommendations.
        
        Provide findings in JSON format:
        {
            "severity": "HIGH|MEDIUM|LOW",
            "issues": ["List detailed performance issues found"],
            "recommendations": ["List specific optimization suggestions"],
            "complexity": {
                "time": "Big O notation",
                "space": "Big O notation"
            }
        }
        """
        super().__init__("PerformanceAgent", prompt)
        
    def analyze_complexity(self, code: str) -> Dict[str, Any]:
        """Analyze code complexity using AST"""
        try:
            tree = ast.parse(code)
            # Basic complexity analysis
            loops = len([node for node in ast.walk(tree) if isinstance(node, (ast.For, ast.While))])
            nested = len([node for node in ast.walk(tree) if isinstance(node, ast.ListComp)])
            return {
                "loops": loops,
                "nested_operations": nested
            }
        except Exception as e:
            logging.error(f"Complexity analysis failed: {str(e)}")
            return {}
            
    def review(self, code: str, previous_reviews: Dict = None) -> Dict[str, Any]:
        """Override review to include complexity analysis"""
        try:
            complexity = self.analyze_complexity(code)
            messages = self.build_messages(code, previous_reviews)
            messages.append({
                "role": "system",
                "content": f"Code complexity metrics: {complexity}"
            })
            response = self.get_gemini_response(messages)
            results = self.format_response(response)
            results["complexity_metrics"] = complexity
            return results
        except Exception as e:
            logging.error(f"Performance review failed: {str(e)}")
            return {
                "severity": "ERROR",
                "issues": [f"Performance analysis error: {str(e)}"],
                "recommendations": [],
                "complexity_metrics": {}
            }