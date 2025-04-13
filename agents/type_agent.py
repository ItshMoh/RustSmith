"""
Type Agent for Rustsmith
Handles type definitions, enums, and traits for Rust projects
"""
import openai
from typing import List, Dict, Any
from config import DEFAULT_MODEL, DEFAULT_TEMPERATURE, MAX_TOKENS
import os
import requests
import json
from dotenv import load_dotenv
load_dotenv()
class TypeAgent:
    def __init__(self):
        self.base_url = "https://anura-testnet.lilypad.tech/api/v1/chat/completions"
        self.api_key = os.getenv('ROUTER_API_KEY')
    
    
    def _prepare_headers(self) -> Dict[str, str]:
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
    
    def process(self, project_idea: str, task_description: str, context: List[Dict[str, Any]]) -> str:
        endpoint = f"{self.base_url}"
        """
        Generate type definitions, enums, and traits based on the project requirements
        
        Args:
            project_idea (str): The user's project idea
            task_description (str): Specific task description from the Master Agent
            context (list): List of past interactions
            
        Returns:
            str: Response with type definitions, enums, and traits
        """
        system_message = """
        You are the Type Agent for Rustsmith, a tool that generates Rust projects.
        Your task is to create appropriate type definitions, enums, and traits for a Rust project.
        
        Follow these guidelines:
        1. Create well-documented enums, type aliases, and traits
        2. Include derive attributes where appropriate (Debug, Clone, PartialEq, etc.)
        3. Implement Display and Error traits for error types
        4. Use Rust naming conventions and best practices
        5. Provide clear documentation comments for each type definition
        """
        
        # Format the context for the prompt
        context_str = ""
        if context:
            context_str = "Previous context:\n"
            for item in context:
                if isinstance(item, dict):
                    question = item.get("question", "")
                    answer = item.get("answer", "")
                    error = item.get("error", "")
                    context_str += f"Question: {question}\n"
                    context_str += f"Answer: {answer}\n"
                    if error:
                        context_str += f"Error: {error}\n"
                    context_str += "---\n"
        
        user_message = f"""
        Project idea: {project_idea}
        
        Task description from Master Agent:
        {task_description}
        
        {context_str}
        
        Generate Rust type definitions, enums, and traits that fulfill these requirements.
        Include omments, appropriate variants/methods, and any necessary
        derive attributes or implementations.
        There should be nothing outside the rust code markdown block. The comments will be inside the markdown block, nothing should be outside the markdown block.
        """
        
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]
        payload = json.dumps({
    "model": "deepseek-r1:7b",
    "messages": messages
    
})
        
        response = requests.post(endpoint, headers=self._prepare_headers(), data=payload)
        if response.status_code == 200:
            response_json = response.json()
            print('response_json', response_json)
            if "choices" in response_json and len(response_json["choices"]) > 0:
                response_text = response_json["choices"][0]["message"]["content"]
                print("Response Text:\n", response_text)
                return response_text
            else:
                print("Error: No valid response content from the API.")
        else:
            print(f"API Error: {response.status_code}, {response.text}")