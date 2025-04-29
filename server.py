# server.py
from mcp.server.fastmcp import FastMCP
from typing import List, Dict, Any, Optional
import json
import logging
import sys
import os
from datetime import datetime
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("file_operations.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)

# Create an MCP server
mcp = FastMCP("asur_file_generator")

# Default output directory
DEFAULT_OUTPUT_DIR = os.path.join(os.getcwd(), "output")

# Ensure output directory exists
os.makedirs(DEFAULT_OUTPUT_DIR, exist_ok=True)

# File Operations Tools


@mcp.tool()
def set_output_directory(directory: str) -> str:
    """Set the default output directory for file operations"""
    try:
        # Create directory if it doesn't exist
        os.makedirs(directory, exist_ok=True)

        # Update the default output directory
        global DEFAULT_OUTPUT_DIR
        DEFAULT_OUTPUT_DIR = os.path.abspath(directory)

        logger.info(f"Output directory set to: {DEFAULT_OUTPUT_DIR}")
        return f"Output directory set to: {DEFAULT_OUTPUT_DIR}"
    except Exception as e:
        logger.error(f"Error setting output directory: {str(e)}")
        raise


@mcp.tool()
def get_output_directory() -> str:
    """Get the current output directory"""
    return DEFAULT_OUTPUT_DIR


@mcp.tool()
def list_files(directory: str = None) -> List[str]:
    """List all files in a directory"""
    try:
        # Use default output directory if none specified
        if directory is None:
            directory = DEFAULT_OUTPUT_DIR

        files = [
            f
            for f in os.listdir(directory)
            if os.path.isfile(os.path.join(directory, f))
        ]
        logger.info(f"Successfully retrieved {len(files)} files from {directory}")
        return files
    except Exception as e:
        logger.error(f"Error listing files: {str(e)}")
        raise


@mcp.tool()
def create_file(file_path: str, content: str = "", use_output_dir: bool = True) -> str:
    """Create a new file with specified content"""
    try:
        # Use output directory if specified
        if use_output_dir:
            file_path = os.path.join(DEFAULT_OUTPUT_DIR, file_path)

        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Write content to file
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        logger.info(f"Successfully created file: {file_path}")
        return f"File created successfully at {file_path}"
    except Exception as e:
        logger.error(f"Error creating file: {str(e)}")
        raise


@mcp.tool()
def read_file(file_path: str, use_output_dir: bool = True) -> str:
    """Read content from a file"""
    try:
        # Use output directory if specified
        if use_output_dir:
            file_path = os.path.join(DEFAULT_OUTPUT_DIR, file_path)

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        logger.info(f"Successfully read file: {file_path}")
        return content
    except Exception as e:
        logger.error(f"Error reading file: {str(e)}")
        raise


@mcp.tool()
def append_to_file(file_path: str, content: str, use_output_dir: bool = True) -> str:
    """Append content to a file"""
    try:
        # Use output directory if specified
        if use_output_dir:
            file_path = os.path.join(DEFAULT_OUTPUT_DIR, file_path)

        with open(file_path, "a", encoding="utf-8") as f:
            f.write("\n" + content)

        logger.info(f"Successfully appended to file: {file_path}")
        return f"Content appended successfully to {file_path}"
    except Exception as e:
        logger.error(f"Error appending to file: {str(e)}")
        raise


@mcp.tool()
def modify_file(
    file_path: str, search_text: str, replace_text: str, use_output_dir: bool = True
) -> str:
    """Replace text in a file"""
    try:
        # Use output directory if specified
        if use_output_dir:
            file_path = os.path.join(DEFAULT_OUTPUT_DIR, file_path)

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Perform the replacement
        new_content = content.replace(search_text, replace_text)

        # Write back to file
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)

        logger.info(f"Successfully modified file: {file_path}")
        return f"File modified successfully at {file_path}"
    except Exception as e:
        logger.error(f"Error modifying file: {str(e)}")
        raise


@mcp.tool()
def delete_file(file_path: str, use_output_dir: bool = True) -> str:
    """Delete a file"""
    try:
        # Use output directory if specified
        if use_output_dir:
            file_path = os.path.join(DEFAULT_OUTPUT_DIR, file_path)

        os.remove(file_path)
        logger.info(f"Successfully deleted file: {file_path}")
        return f"File deleted successfully: {file_path}"
    except Exception as e:
        logger.error(f"Error deleting file: {str(e)}")
        raise


@mcp.tool()
def generate_text(topic: str, format: str = "markdown", length: str = "medium") -> str:
    """Generate text content based on topic and format"""
    try:
        # Define length parameters
        length_params = {"short": 100, "medium": 500, "long": 1000}

        # Generate content based on format
        if format.lower() == "markdown":
            content = f"""# {topic}
                        ## Introduction
                        This is a generated document about {topic}.

                        ## Main Content
                        Here is some detailed information about {topic}.

                        ## Conclusion
                        This concludes our discussion about {topic}.
                        """
        elif format.lower() == "text":
            content = f"""Topic: {topic}
                            Introduction:
                            This document provides information about {topic}.

                            Main Content:
                            Detailed discussion about {topic}.

                            Conclusion:
                            Summary of {topic}.
                            """
        else:
            content = f"Content about {topic}"

        logger.info(f"Successfully generated {format} content about {topic}")
        return content
    except Exception as e:
        logger.error(f"Error generating text: {str(e)}")
        raise


@mcp.tool()
def create_document(
    topic: str, output_file: str, format: str = "markdown", use_output_dir: bool = True
) -> str:
    """Create a new document with generated content"""
    try:
        # Generate content
        content = generate_text(topic, format)

        # Create file with generated content
        create_file(output_file, content, use_output_dir)

        logger.info(f"Successfully created document: {output_file}")
        return f"Document created successfully at {output_file}"
    except Exception as e:
        logger.error(f"Error creating document: {str(e)}")
        raise


@mcp.tool()
def modify_document(
    file_path: str, modifications: str, use_output_dir: bool = True
) -> str:
    """Apply multiple modifications to a document"""
    try:
        # Use output directory if specified
        if use_output_dir:
            file_path = os.path.join(DEFAULT_OUTPUT_DIR, file_path)

        # Parse modifications
        mods = json.loads(modifications)

        # Read current content
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Apply each modification
        for mod in mods:
            if "search" in mod and "replace" in mod:
                content = content.replace(mod["search"], mod["replace"])
            elif "append" in mod:
                content += "\n" + mod["append"]
            elif "prepend" in mod:
                content = mod["prepend"] + "\n" + content

        # Write back to file
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        logger.info(f"Successfully modified document: {file_path}")
        return f"Document modified successfully at {file_path}"
    except Exception as e:
        logger.error(f"Error modifying document: {str(e)}")
        raise


@mcp.tool()
def create_folder(folder_name: str, use_output_dir: bool = True) -> str:
    """Create a new folder"""
    try:
        # Use output directory if specified
        if use_output_dir:
            folder_path = os.path.join(DEFAULT_OUTPUT_DIR, folder_name)
        else:
            folder_path = folder_name

        # Create folder
        os.makedirs(folder_path, exist_ok=True)

        logger.info(f"Successfully created folder: {folder_path}")
        return f"Folder created successfully at {folder_path}"
    except Exception as e:
        logger.error(f"Error creating folder: {str(e)}")
        raise


@mcp.tool()
def list_folders(directory: str = None) -> List[str]:
    """List all folders in a directory"""
    try:
        # Use default output directory if none specified
        if directory is None:
            directory = DEFAULT_OUTPUT_DIR

        folders = [
            f
            for f in os.listdir(directory)
            if os.path.isdir(os.path.join(directory, f))
        ]
        logger.info(f"Successfully retrieved {len(folders)} folders from {directory}")
        return folders
    except Exception as e:
        logger.error(f"Error listing folders: {str(e)}")
        raise


# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello Hi, {name}!"
