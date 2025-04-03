"""
Parser utilities for Rustsmith
"""
import re
from typing import Dict, Any

def parse_master_response(response: str) -> Dict[str, str]:
    """
    Parse the master agent's response to extract tasks for each agent
    
    Args:
        response (str): The master agent's response
        
    RThis project structure organizes the code into distinct modules, following Rust best practices. The `main.rs` file handles the user interface, while `calculator.rs` contains all the logic for the calculator operations and state management. The `lib.rs` file serves as the root module that exports the `calculator` module.eturns:
        dict: Dictionary with keys for each agent and their tasks
    """
    agent_tasks = {}
    
    # Extract tasks for Struct Agent
    struct_match = re.search(r'\[STRUCT_AGENT\](.*?)\[/STRUCT_AGENT\]', 
                            response, re.DOTALL)
    if struct_match:
        agent_tasks["struct"] = struct_match.group(1).strip()
    
    # Extract tasks for Type Agent
    type_match = re.search(r'\[TYPE_AGENT\](.*?)\[/TYPE_AGENT\]', 
                          response, re.DOTALL)
    if type_match:
        agent_tasks["type"] = type_match.group(1).strip()
    
    # Extract tasks for Utility Agent
    utility_match = re.search(r'\[UTILITY_AGENT\](.*?)\[/UTILITY_AGENT\]', 
                             response, re.DOTALL)
    if utility_match:
        agent_tasks["utility"] = utility_match.group(1).strip()
    
    return agent_tasks