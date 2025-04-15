

# 🦀 Rustsmith

**Rustsmith** is an AI-powered tool that generates Rust projects using a system of specialized agents. It streamlines Rust development by breaking down project creation into modular tasks and automatically handling compilation and error correction.
---

## Overview

Rustsmith takes a project idea from the user and divides the development work among AI agents, each focused on a specific task: It uses small language models which are less than 10b parameters. Our multi agent architecture enhances the Rust coding ability of these small agents which were earlier possible by Large language models.


### Master Agent
- Analyzes the project idea
- Breaks it down into manageable subtasks for `Struct Agent`, `Type Agent`, and `Utility Agent`
- Currently I am using `llama3.1:8b` through Anura Inferece API.

### Struct Agent
- Creates appropriate `struct` definitions
- Handles all stuffs related to `struct`.
- Currently I am using `phi4:14b` through Anura Inference API.

### Type Agent
- Defines types, `enums`, and `traits`
- Currently I am using `deepseek-r1:7b` through Anura Inference API.

### Utility Agent
- Implements functions, methods, and utility code
- Currently I am using `qwen2.5-coder:7b` through Anura Inference API.

### Smith Agent
- Assembles all the Sub-Agents responses to make the project
- Fixes compilation errors sent by the rust compiler.
- Currently I am using `llama3.1:8b` through Anura Inference API.

The system compiles the generated Rust code and automatically attempts to resolve any compilation issues.

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/ItshMoh/RustSmith.git
cd RustSmith
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Install Rust and Cargo

Visit [rust-lang.org/tools/install](https://www.rust-lang.org/tools/install) for platform-specific instructions.

### 4. Set Up Environment Variables

```bash
cp .env.example .env
# Edit .env with your API keys and MongoDB connection details
```

### 5. Ensure MongoDB is Running

Refer to the [MongoDB installation guide](https://www.mongodb.com/docs/manual/installation/) if needed.

Setup the MongoDB and make a database name `rustsmith` and a collection name `user_contexts`. 

`NOTE` You can name the database and collection you want but you have to change it where the above were placed in the code.

---

## Usage

Run the main script:

```bash
# Setup the user_id in the main.py file
python main.py
```

Follow the prompts:

- Enter your **project idea** (e.g., `"write a command-line todo app in rust"`)

Rustsmith will:
- Generate the project structure and code
- Compile the Rust project using Cargo
- Fix any compilation errors
- Save the completed project in the `output/` directory

---

## ⚙ How It Works

1. You input a project idea.
2. The **Master Agent** divides the work into subtasks.
3. 3 Specialized agents generate corresponding code.
4. The **Smith Agent** assembles the full project.
5. The project is compiled using Cargo.
6. Compilation errors (if any) are automatically fixed.
7. Context and results are stored in **MongoDB**.

---

## Project Directory Structure

```
Rustsmith/
│
├── main.py                     # Entry point
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
│
├── agents/                     # AI agent implementations
│   ├── master_agent.py
│   ├── struct_agent.py
│   ├── type_agent.py
│   ├── utility_agent.py
│   └── smith_agent.py
│
├── database/                   # Database operations
│   └── mongodb.py
│
├── utils/                      # Utility functions
│   ├── parser.py
│   ├── compiler.py
│   └── file_manager.py
│
└── output/                     # Generated projects
```

---

## 🧾 Example Output

After running Rustsmith with a calculator project idea, you'll find a directory like:

```
output/
├── Cargo.toml                  # Project configuration
├── src/
│   ├── lib.rs                  # Library code with structs and types
  └── main.rs                 # Main executable with 
```

---

## Requirements

- Python 3.8+
- Rust and Cargo
- MongoDB
- Anura API Key get it from Here (https://anura.lilypad.tech/)

---

## Extending Rustsmith

We will be extending Rustsmith by:
- Adding new agents for other Rust development aspects
- Supporting different LLM providers
- Enhancing error correction mechanisms
- Publishing it is a library.

---

## 📄 License

This project is licensed under the **MIT License**.

---
