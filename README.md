# MCP File Generator Server

A server that provides tools for generating and modifying text files through MCP (Model Control Protocol).

## Installation

1. Make sure you have Python 3.7+ installed on your system.

2. Create a virtual environment (recommended):
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the server:
```bash
python server.py
```

2. The server will start and listen for connections. You can use it with any MCP-compatible client.

## Available Tools

### File Operations
- `list_files(directory: str = ".")`: List all files in a directory
- `create_file(file_path: str, content: str = "")`: Create a new file with content
- `read_file(file_path: str)`: Read content from a file
- `append_to_file(file_path: str, content: str)`: Append content to a file
- `modify_file(file_path: str, search_text: str, replace_text: str)`: Replace text in a file
- `delete_file(file_path: str)`: Delete a file

### Text Generation
- `generate_text(topic: str, format: str = "markdown", length: str = "medium")`: Generate text content
- `create_document(topic: str, output_file: str, format: str = "markdown")`: Create a new document
- `modify_document(file_path: str, modifications: str)`: Apply multiple modifications

## Example Usage

```python
# Create a markdown document
create_document("Artificial Intelligence", "ai_intro.md", "markdown")

# Modify a document
modifications = [
    {"search": "AI", "replace": "Artificial Intelligence"},
    {"append": "\n## New Section\nAdditional content."}
]
modify_document("ai_intro.md", json.dumps(modifications))

# List files
list_files()
```

## Logging

The server logs all operations to:
- Console output
- `file_operations.log` file

## Requirements

- Python 3.7+
- mcp-server>=1.6.0
- python-dotenv>=0.19.0
