"""
Master Agent for Rustsmith
Divides the project task among specialized agents
"""

from typing import List, Dict, Any
from config import DEFAULT_MODEL, DEFAULT_TEMPERATURE, MAX_TOKENS
import os
import json
import requests
from dotenv import load_dotenv
load_dotenv()
class MasterAgent:
    def __init__(self):
        self.base_url = "https://anura-testnet.lilypad.tech/api/v1/chat/completions"
        self.api_key = os.getenv('ROUTER_API_KEY')
    def _prepare_headers(self) -> Dict[str, str]:
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
    
    def process(self, project_idea: str, context: List[Dict[str, Any]]) -> str:
        endpoint = f"{self.base_url}"
        """
        Process the project idea and divide it into subtasks
        
        Args:
            project_idea (str): The user's project idea
            context (list): List of past interactions
            
        Returns:
            str: Response with task division for each agent
        """
        system_message = """
        You are the Master Agent for Rustsmith, a tool that generates Rust projects. 
        Your task is to divide a Rust project into specific subtasks for specialized agents:
        
        Struct Agent: Define appropriate structs for the project
        Type Agent: Handle type definitions, enums, and traits
        Utility Agent: Create utility functions, implementations, and other general-purpose code
        
        For each agent, provide detailed instructions on what they should implement.

        Format your response with clear sections for each agent:
        
        [STRUCT_AGENT]
        Instructions for the Struct Agent...
        [/STRUCT_AGENT]
        
        [TYPE_AGENT]
        Instructions for the Type Agent...
        [/TYPE_AGENT]
        
        [UTILITY_AGENT]
        Instructions for the Utility Agent...
        [/UTILITY_AGENT]


        Some Guidlines to follow:
        1. If an agent isn't needed for this project, Don't write any insturctions for that agent and does not include any file format for that agent. It means you don't write even the given format for that agent as given above. write the above format for agent only which are needed for the project.
        For example you will need to have instructions for the TYPE_AGENT and STRUCT_AGENT but not the UTILITY_AGENT then the response should contain something like this:
        
        [STRUCT_AGENT]
        Instructions for the Struct Agent...
        [/STRUCT_AGENT]

        [TYPE_AGENT]
        Instructions for the Type Agent...
        [/TYPE_AGENT]
        
        2. In case the project only requires some easy implementation and work use only Utility Agent.
        3. You must follow the Agent Response format. It is the most important thing. After the instruction of each agent you have to end the response with the given format. 
        4. You only have these Agents: Struct Agent, Type Agent, Utility Agent.
        5. Only give the insturctions for each Agent don't give the code.
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
        

        """
        
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]
        payload = json.dumps({
    "model": "llama3.1:8b",
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