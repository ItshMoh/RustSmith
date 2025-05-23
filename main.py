#!/usr/bin/env python3
"""
Rustsmith - A tool to generate Rust projects using AI agents
"""
import os
import sys
from database.mongodb import MongoDB
from agents.master_agent import MasterAgent
from agents.struct_agent import StructAgent
from agents.type_agent import TypeAgent
from agents.utility_agent import UtilityAgent
from agents.smith_agent import SmithAgent
from utils.parser import parse_master_response
from utils.compiler import compile_rust_project
from utils.file_manager import save_project
from config import MONGODB_URI, API_KEYS
from utils.file_manager import save_project, extract_files_from_response

def main():
    print("Welcome to Rustsmith - Generate Rust projects with AI")
    
    # Get user ID
    user_id = "123" # You can set anything you want.
    
    # Connect to MongoDB
    db = MongoDB(MONGODB_URI)
    
    # Get or create user context
    context = db.get_user_context(user_id)
    if not context:
        context = []
    
    # Get project idea from user
    project_idea = input("Enter your project idea (e.g., 'write a calculator in rust'): ")
    
    # Initialize agents
    master_agent = MasterAgent()
    struct_agent = StructAgent()
    type_agent = TypeAgent()
    utility_agent = UtilityAgent()
    smith_agent = SmithAgent()
    
    # Step 1: Master agent divides the task
    master_response = master_agent.process(project_idea, context)
    
    # Step 2: Parse master response to determine which agents to use
    agent_tasks = parse_master_response(master_response)
    
    # Step 3: Call each required agent
    agent_responses = {}
    
    if "struct" in agent_tasks:
        agent_responses["struct"] = struct_agent.process(
            project_idea, 
            agent_tasks["struct"], 
            context
        )
    
    if "type" in agent_tasks:
        agent_responses["type"] = type_agent.process(
            project_idea, 
            agent_tasks["type"], 
            context
        )
    
    if "utility" in agent_tasks:
        agent_responses["utility"] = utility_agent.process(
            project_idea, 
            agent_tasks["utility"], 
            context
        )
    
    # Step 4: Smith agent assembles the project
    smith_response = smith_agent.process(
        project_idea,
        master_response,
        agent_responses,
        context
    )
    print("Smith response:-----\n ", smith_response)
    # Step 5: Save the project
    # project_path = save_project(smith_response, user_id, project_idea)
    parsed_files = extract_files_from_response(smith_response)
    project_path = save_project(parsed_files,"output")
    # Step 6: Compile the project
    success, error = compile_rust_project('output/')
    print(f"Error ---- \n {error}")
    context.append({
            "question": project_idea,
            "answer": parsed_files,
            "error": error
        })
        
        # Save context to MongoDB
    db.update_user_context(user_id, context)
    print("the project is compiled --------------------------------------------- \n",success)
    # Step 7: If there are errors, update context and try again
    while (success !=True):
        
        # Try to fix errors
        fixed_response = smith_agent.process(
            project_idea,
            master_response,
            context
        )
        print("Smith response:-----\n ", fixed_response)
        parsed_files = extract_files_from_response(fixed_response)
        fixed_project_path = save_project(parsed_files,"output")
        
        # Compile again
        success, error = compile_rust_project('output/')
        print(f"Error ---- \n {error}")
        context.append({  
            "question": project_idea,
            "answer": smith_response,
            "error": error
        })
        
        # Save context to MongoDB
        db.update_user_context(user_id, context)
        if success:
            print(f"Project successfully generated and compiled at: {fixed_project_path}")
        else:
            print(f"Compilation failed. Attempting to fix errors...")
           

if __name__ == "__main__":
    main()