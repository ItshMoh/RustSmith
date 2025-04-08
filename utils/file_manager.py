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

def save_project1(smith_response: str, project_dir="output") -> str:
    """
    Save the generated Rust project to disk
    
    
    Returns:
        str: Path to the saved project
    """
    # Create a safe project name from the idea
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
    
    
    return project_dir

def extract_files_from_response1(response: str) -> Dict[str, str]:
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

def save_project(files: Dict[str, str], project_dir: str):
        for filepath, content in files.items():
            full_path = os.path.join(project_dir, filepath)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
        print(f"Files saved successfully in {project_dir}")

def extract_files_from_response(response: str) -> Dict[str, str]:
        files = {}
        current_file = None
        current_content = []
        extra_text = []
        inside_file = False
        inside_code_block = False
        
        lines = response.split('\n')
        
        for line in lines:
            if line.startswith('[FILE:'):
                if current_file and current_content:
                    files[current_file] = '\n'.join(current_content).strip()
                current_file = line[6:].strip().rstrip(']')
                current_content = []
                inside_file = True
                inside_code_block = False  
            elif line.startswith('[END FILE]'):
                if current_file and current_content:
                    files[current_file] = '\n'.join(current_content).strip()
                current_file = None
                inside_file = False
                inside_code_block = False
            elif inside_file:
                if line.strip().startswith('```'):
                    inside_code_block = not inside_code_block 
                    continue
                if inside_code_block:
                    current_content.append(line)
            else:
                extra_text.append(line)  
        
        if extra_text:
            files["src/README.md"] = '\n'.join(extra_text).strip()
        
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