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
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.model = "qwen/qwen-2.5-coder-32b-instruct:free"
        self.api_key = os.getenv('ROUTER_API_KEY')
    
    def _prepare_headers(self) -> Dict[str, str]:
        return {
            
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
        1. Organize code into appropriate files (lib.rs, main.rs, modules)
        2. Create a proper Cargo.toml file with necessary dependencies
        3. Ensure the project follows Rust best practices
        4. Fix any issues or inconsistencies between the agents' outputs
        5. Format your response clearly indicating file paths and content
        6. Don't output any Project description outside of the rust markdown code block. If any required do that in the comments format in the file. It is a very critical step.
        7. Don't write anything outside the rust markdown code block, no matter what. In the code block there can be some comments
        For each file, format your response as:
        
        ```
        File: path/to/file
        file content here...
        ```
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
        
        Assemble a complete Rust project that implements the requirements.
        Organize the code into appropriate files with correct paths.
        For each file, provide the file path and content.
        Ensure the project structure follows Rust best practices.
        Don't output any Project description outside of the rust markdown code block.
        You have to just output the rust code markdown block. Nothing else
        """
        
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]
        payload = json.dumps({
    "model": "qwen/qwen-2.5-coder-32b-instruct:free",
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