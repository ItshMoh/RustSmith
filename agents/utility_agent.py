"""
Utility Agent for Rustsmith
Creates utility functions, implementations, and other general-purpose code
"""
import openai
from typing import List, Dict, Any
from config import DEFAULT_MODEL, DEFAULT_TEMPERATURE, MAX_TOKENS
import os
import json
import requests
from dotenv import load_dotenv
load_dotenv()
class UtilityAgent:
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
        Generate utility functions and implementations based on the project requirements
        
        Args:
            project_idea (str): The user's project idea
            task_description (str): Specific task description from the Master Agent
            context (list): List of past interactions
            
        Returns:
            str: Response with utility functions and implementations
        """
        system_message = """
        You are the **Utility Agent** for **Rustsmith**, a tool that generates Rust projects.

Your task is to create **utility functions**, **struct implementations**, and other **general-purpose code** required for the project.

---

## Guidelines

1. Implement methods for structs where applicable (`impl` blocks).
2. Create reusable utility functions with proper **error handling**.
3. Follow **Rust naming conventions** and best practices.
4. Include a `main` function if appropriate for the project type.
5. Use inline documentation comments (`///`) or inline comments (`//`) as needed.
6. The output must be a valid Rust code block — **no explanations or text outside** the code block.

---

## Output Format

- Output must be inside a **Rust code block** using triple backticks and `rust`.
- All comments should be **inside** the code block.
- Do **not** include anything outside the code block.

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
    "model": "qwen2.5-coder:7b",
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