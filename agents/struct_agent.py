"""
Struct Agent for Rustsmith
Handles the creation of Rust structs based on project requirements
"""
import openai
from typing import List, Dict, Any
from config import DEFAULT_MODEL, DEFAULT_TEMPERATURE, MAX_TOKENS
import os
import json
import requests
from dotenv import load_dotenv
load_dotenv()
class StructAgent:
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
        Generate appropriate struct definitions based on the project requirements
        
        Args:
            project_idea (str): The user's project idea
            task_description (str): Specific task description from the Master Agent
            context (list): List of past interactions
            
        Returns:
            str: Response with struct definitions and implementations
        """
        system_message = """
       You are the **Struct Agent** for **Rustsmith**, a tool that generates Rust projects.

Your task is to create **appropriate struct definitions** for a Rust project based on the provided instructions.

---

## Guidelines

1. Define structs with appropriate **fields** and **data types**.
2. Add relevant `#[derive(...)]` attributes such as `Debug`, `Clone`, `Serialize`, etc., where appropriate.
3. Follow **Rust naming conventions** and best practices.
4. Include **documentation comments** (`///`) for each struct and its fields.
5. Focus **only** on struct definitions — do **not** include implementations, methods, or logic.

---

## Output Format

- Output must be **only a Rust code block** using triple backticks and the `rust` language identifier.
- All comments (struct-level and field-level) must be **inside** the Rust code block.
- Do **not** include any explanation or text outside the code block.

---
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
        
        """
        
        
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]
        payload = json.dumps({
    "model": "phi4:14b",
    "messages": messages
    
})
        
        response = requests.post(endpoint, headers=self._prepare_headers(), data=payload)
        if response.status_code == 200:
            response_json = response.json()
            # print('response_json', response_json)
            if "choices" in response_json and len(response_json["choices"]) > 0:
                response_text = response_json["choices"][0]["message"]["content"]
                print("Response Text:\n", response_text)
                return response_text
            else:
                print("Error: No valid response content from the API.")
        else:
            print(f"API Error: {response.status_code}, {response.text}")