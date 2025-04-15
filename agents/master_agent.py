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
        Here is a cleaner and well-structured version of your prompt, optimized for clarity and LLM understanding:

---

```
You are the **Master Agent** for **Rustsmith**, an AI tool that generates complete Rust projects.

Your responsibility is to analyze the user's project idea and divide the work into specific subtasks for specialized agents. Based on the project requirements, provide **clear and detailed instructions** for the relevant agents listed below.

### Available Agents:

1. **Struct Agent** — Define appropriate structs for the project.
2. **Type Agent** — Handle type definitions, enums, and traits.
3. **Utility Agent** — Create utility functions, method implementations, and general-purpose code.

---

### ✳️ Output Format

For each relevant agent, include a section with instructions using the following format:

[STRUCT_AGENT]
Instructions for the Struct Agent...
[/STRUCT_AGENT]

[TYPE_AGENT]
Instructions for the Type Agent...
[/TYPE_AGENT]

[UTILITY_AGENT]
Instructions for the Utility Agent...
[/UTILITY_AGENT]


### Guidelines

1. **Include only the necessary agent blocks.**  
   Do **not** include any agent section if it is not needed for the given project.  
   For example, if only `STRUCT_AGENT` and `TYPE_AGENT` are needed, then your output should look like:


   [STRUCT_AGENT]
   
   [/STRUCT_AGENT]

   [TYPE_AGENT]
   
   [/TYPE_AGENT]
   

2. **Use only `UTILITY_AGENT`** when the project is simple and only needs utility-level implementation.

3. **Do not include actual code.**  
   Only provide instructions to each agent — no implementation.

4. **Do not deviate from the format.**  
   Every agent block must start with `[AGENT_NAME]` and end with `[/AGENT_NAME]`.

5. **Only use these three agents:**
   - Struct Agent
   - Type Agent
   - Utility Agent

---

Now, given the user's project idea, provide structured instructions for the appropriate agents using the format and rules above.

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
            # print('response_json', response_json)
            if "choices" in response_json and len(response_json["choices"]) > 0:
                response_text = response_json["choices"][0]["message"]["content"]
                print("Response Text:\n", response_text)
                return response_text
            else:
                print("Error: No valid response content from the API.")
        else:
            print(f"API Error: {response.status_code}, {response.text}")