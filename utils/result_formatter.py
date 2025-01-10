from typing import Dict, Any

def format_review_results(results: Dict[str, Any]) -> str:
    """
    Format code review results into a readable markdown string.
    
    Args:
        results: Dictionary containing review results from each agent
        
    Returns:
        str: Formatted markdown string containing review results
    """
    formatted_output = "## Code Review Results\n\n"
    
    for agent_name, findings in results.items():
        # Agent section header
        formatted_output += f"### {agent_name}\n"
        
        # Severity section
        severity = findings.get('severity', 'UNKNOWN')
        formatted_output += f"Severity: {severity}\n\n"
        
        # Issues section
        formatted_output += "Issues:\n"
        issues = findings.get('issues', [])
        if issues:
            for issue in issues:
                if isinstance(issue, dict):
                    # Extract description from dictionary
                    description = issue.get('description', '')
                    formatted_output += f"- {description}\n"
                else:
                    # Handle plain string issues
                    formatted_output += f"- {issue}\n"
        else:
            formatted_output += "- No issues found\n"
            
        # Recommendations section
        formatted_output += "\nRecommendations:\n"
        recommendations = findings.get('recommendations', [])
        if recommendations:
            for rec in recommendations:
                if isinstance(rec, dict):
                    # Extract description from dictionary
                    description = rec.get('description', '')
                    formatted_output += f"- {description}\n"
                else:
                    # Handle plain string recommendations
                    formatted_output += f"- {rec}\n"
        else:
            formatted_output += "- No recommendations provided\n"
        
        # Complexity metrics section (if available)
        if 'complexity_metrics' in findings:
            formatted_output += "\nComplexity Metrics:\n"
            metrics = findings['complexity_metrics']
            for metric, value in metrics.items():
                formatted_output += f"- {metric}: {value}\n"
        
        formatted_output += "\n"
        
    return formatted_output