
# 🦀 Rustsmith

**Rustsmith** is an AI-powered tool that generates Rust projects using a system of specialized agents. It streamlines Rust development by breaking down project creation into modular tasks and automatically handling compilation and error correction.

---

## Overview

Rustsmith takes a project idea from the user and divides the development work among AI agents, each focused on a specific task:

### Master Agent
- Analyzes the project idea
- Breaks it down into manageable subtasks

### Struct Agent
- Creates appropriate `struct` definitions

### Type Agent
- Defines types, `enums`, and `traits`

### Utility Agent
- Implements functions, methods, and utility code

### Smith Agent
- Assembles the final project
- Fixes compilation errors

The system compiles the generated Rust code and automatically attempts to resolve any compilation issues.

---

## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/rustsmith.git
cd rustsmith
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

---

## 🧪 Usage

Run the main script:

```bash
python main.py
```

Follow the prompts:
- Enter your **user ID** (for tracking context)
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
3. Specialized agents generate corresponding code.
4. The **Smith Agent** assembles the full project.
5. The project is compiled using Cargo.
6. Compilation errors (if any) are automatically fixed.
7. Context and results are stored in **MongoDB**.

---

## Project Directory Structure

```
rustsmith/
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

## Example Output

After running Rustsmith with a calculator project idea, you'll find a directory like:

```
output/your_user_id_calculator_20250413_123456_v1/
├── Cargo.toml                  # Project configuration
├── src/
│   ├── lib.rs                  # Library code with structs and types
│   └── main.rs                 # Main executable with user interface
└── rustsmith_metadata.json     # Project metadata
```

---

## 📋 Requirements

- Python 3.8+
- Rust and Cargo
- MongoDB
- OpenAI API key or other LLM provider

---

## Extending Rustsmith

You can extend Rustsmith by:
- Adding new agents for other Rust development aspects
- Supporting different LLM providers
- Enhancing error correction mechanisms
- Creating a web-based interface

---

## 📄 License

This project is licensed under the **MIT License**.

---

Let me know if you'd like to add badges (build status, license, etc.), a demo GIF, or usage examples!