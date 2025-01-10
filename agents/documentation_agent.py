from .base_agent import CodeReviewAgent

class DocumentationAgent(CodeReviewAgent):
    def __init__(self):
        prompt = """
        You are a documentation expert. Analyze code for:
        - Documentation completeness
        - Docstring quality
        - Comments clarity
        - API documentation
        
        Provide findings in JSON format:
        {
            "severity": "HIGH|MEDIUM|LOW",
            "issues": [],
            "recommendations": []
        }
        """
        super().__init__("DocumentationAgent", prompt)