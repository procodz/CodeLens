from typing import List, Optional
from .security_agent import SecurityAgent
from .style_agent import StyleAgent
from .performance_agent import PerformanceAgent
from .documentation_agent import DocumentationAgent

class AgentFactory:
    def create_agents(self):
        return [
            SecurityAgent(),
            StyleAgent(),
            PerformanceAgent(),
            DocumentationAgent()
        ]