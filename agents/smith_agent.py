"""
Smith Agent for Rustsmith
Assembles the final Rust project based on output from other agents
"""
import openai
from typing import List, Dict, Any
from config import DEFAULT_MODEL, DEFAULT_TEMPERATURE, MAX_TOKENS
import os
import json
import requests
from dotenv import load_dotenv
load_dotenv()
class SmithAgent:
    def __init__(self):
        self.base_url = "https://anura-testnet.lilypad.tech/api/v1/chat/completions"
        self.model = "qwen/qwen-2.5-coder-32b-instruct:free"
        self.api_key = os.getenv('ROUTER_API_KEY')
    
    def _prepare_headers(self) -> Dict[str, str]:
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
    
    def process(
        self, 
        project_idea: str, 
        master_workflow: str, 
        agent_responses: Dict[str, str], 
        context: List[Dict[str, Any]]
    ) -> str:
        endpoint = f"{self.base_url}"
        """
        Assemble the final Rust project using outputs from specialized agents
        
        Args:
            project_idea (str): The user's project idea
            master_workflow (str): The Master Agent's workflow description
            agent_responses (dict): Dictionary of responses from specialized agents
            context (list): List of past interactions including errors
            
        Returns:
            str: Final assembled project with file paths and content
        """
        system_message = """
        You are the Smith Agent for Rustsmith, a tool that generates Rust projects.
        Your task is to assemble a complete Rust project using the outputs from specialized agents.
        
        Follow these guidelines:

        Always generate these files:
        1. Cargo.toml with proper metadata and dependencies
        2. src/main.rs or src/lib.rs as appropriate
        3. Any needed module files under src/
        4. Fix any issues or inconsistencies between the agents' outputs
        Format your response strictly as follows:
    
    [FILE: Cargo.toml]
    ```
    <content>
    ```
    [END FILE]
    
    [FILE: src/main.rs]
    ```
    <content>
    ```
    [END FILE]
    
    [FILE: src/<module_name>.rs]
    ```
    <content>
    ```
    [END FILE]
    
    you will always produce the 
    After every file content block, you must write [END FILE]. you have to strictly follow the above response format for files.
    
        """
        
        # Check if there are any errors in the context to fix
        error_context = ""
        for item in context:
            if isinstance(item, dict) and item.get("error"):
                error_context += f"Previous error:\n{item.get('error')}\n\n"
        
        # Format agent responses
        agent_responses_str = ""
        for agent_name, response in agent_responses.items():
            agent_responses_str += f"{agent_name.upper()} AGENT OUTPUT:\n{response}\n\n"
        
        user_message = f"""
        Project idea: {project_idea}
        
        Master workflow:
        {master_workflow}
        
        Agent responses:
        {agent_responses_str}
        
        {error_context}
        
       
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