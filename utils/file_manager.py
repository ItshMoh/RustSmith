"""
File and project management utilities for Rustsmith
"""
import os
import re
import json
import shutil
from datetime import datetime
from typing import Dict, Any
from config import OUTPUT_DIR

def save_project(smith_response: str, user_id: str, project_idea: str, version: int = 1) -> str:
    """
    Save the generated Rust project to disk
    
    Args:
        smith_response (str): The Smith agent's response with code
        user_id (str): User identifier
        project_idea (str): Original project idea
        version (int): Version number for the project
        
    Returns:
        str: Path to the saved project
    """
    # Create a safe project name from the idea
    project_name = re.sub(r'[^a-zA-Z0-9_]', '_', project_idea.lower())
    project_name = re.sub(r'_+', '_', project_name)
    project_name = project_name[:30]  # Limit length
    
    # Create timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create project directory
    project_dir = os.path.join(
        OUTPUT_DIR, 
        f"{user_id}_{project_name}_{timestamp}_v{version}"
    )
    
    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Remove directory if it already exists (unlikely due to timestamp)
    if os.path.exists(project_dir):
        shutil.rmtree(project_dir)
    
    # Create project directory
    os.makedirs(project_dir, exist_ok=True)
    
    # Parse files from smith_response
    files = extract_files_from_response(smith_response)
    
    # Write files
    for file_path, content in files.items():
        full_path = os.path.join(project_dir, file_path)
        
        # Create directories if needed
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        # Write the file
        with open(full_path, 'w') as f:
            f.write(content)
    
    # Create metadata file
    metadata = {
        "user_id": user_id,
        "project_idea": project_idea,
        "timestamp": timestamp,
        "version": version
    }
    
    with open(os.path.join(project_dir, "rustsmith_metadata.json"), 'w') as f:
        json.dump(metadata, f, indent=2)
    
    return project_dir

def extract_files_from_response(response: str) -> Dict[str, str]:
    """
    Extract file paths and contents from the Smith agent's response
    
    Args:
        response (str): The Smith agent's response
        
    Returns:
        dict: Dictionary mapping file paths to file contents
    """
    files = {}
    
    # Find all file blocks in the response
    file_blocks = re.finditer(
        r'File:\s*([^\n]+)\s*\n(.*?)(?=File:|$)',
        response,
        re.DOTALL
    )
    
    for block in file_blocks:
        file_path = block.group(1).strip()
        content = block.group(2).strip()
        
        # Remove markdown code block markers if present
        content = re.sub(r'^```(?:rust|toml)?|```$', '', content, flags=re.MULTILINE)
        
        files[file_path] = content.strip()
    
    # If no files were found, try alternative format with markdown code blocks
    if not files:
        file_blocks = re.finditer(
            r'```(?:rust|toml)?\s*(?:(?:File|Path|Filename):\s*([^\n]+))?\s*\n(.*?)```',
            response,
            re.DOTALL
        )
        
        for block in file_blocks:
            file_path = block.group(1)
            content = block.group(2)
            
            if not file_path:
                # If no explicit file path, try to infer from content
                if "fn main" in content:
                    file_path = "src/main.rs"
                elif "[package]" in content:
                    file_path = "Cargo.toml"
                else:
                    # Default to a lib.rs file if we can't determine
                    file_path = "src/lib.rs"
            
            files[file_path.strip()] = content.strip()
    
    # Ensure we have a Cargo.toml file
    if "Cargo.toml" not in files:
        files["Cargo.toml"] = generate_default_cargo_toml()
    
    # Ensure we have at least main.rs if no Rust files found
    if not any(f.endswith(".rs") for f in files):
        files["src/main.rs"] = generate_default_main_rs()
    
    return files

def generate_default_cargo_toml() -> str:
    """Generate a default Cargo.toml file"""
    return """[package]
name = "rustsmith_project"
version = "0.1.0"
edition = "2021"

[dependencies]
"""

def generate_default_main_rs() -> str:
    """Generate a default main.rs file"""
    return """fn main() {
    println!("Hello from Rustsmith!");
}
"""