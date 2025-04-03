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
        # Save current directory
        current_dir = os.getcwd()
        
        try:
            # Change to the project directory
            os.chdir(project_path)

        
            build_result = subprocess.run(
                ["cargo", "build"],
                capture_output=True,
                text=True
            )
            
            if build_result.returncode != 0:
                return False, build_result.stderr
            
            return True, ""
        finally:
            # Restore original directory
            os.chdir(current_dir)
    except FileNotFoundError:
        return False, "Rust/Cargo not found on the system. Please install Rust."
    except Exception as e:
        return False, str(e)