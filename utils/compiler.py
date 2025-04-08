"""
Interface with the Rust compiler
"""
import os
import subprocess
from typing import Tuple

def compile_rust_project(project_path: str) -> Tuple[bool, str]:
    """
    Compile a Rust project using cargo
    
    Args:
        project_path (str): Path to the Rust project
        
    Returns:
        tuple: (success, error_message)
    """
    try:
        result = subprocess.run(
            ['cargo', 'build'],
            cwd=project_path,
            capture_output=True,
            text=True
        )
        success = result.returncode == 0
        output = result.stdout if success else result.stderr
        return success, output
    except Exception as e:
        return False, str(e)