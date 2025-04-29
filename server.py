# server.py
from mcp.server.fastmcp import FastMCP
from pymongo import MongoClient
from typing import List, Dict, Any, Optional
import json

# Create an MCP server
mcp = FastMCP("asur_mongo_db")

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['mcp_demo_db']

# Add an addition tool
#@mcp.tool()
#def add(a: int, b: int) -> int:
#    """Add two numbers"""
#    return a + b

# MongoDB Tools

@mcp.tool()
def list_databases() -> List[str]:
    """List all available MongoDB databases"""
    return client.list_database_names()

@mcp.tool()
def list_collections(database_name: str) -> List[str]:
    """List all collections in a database"""
    db = client[database_name]
    return db.list_collection_names()

@mcp.tool()
def insert_document(database_name: str, collection_name: str, document: str) -> str:
    """Insert a document into a collection"""
    db = client[database_name]
    collection = db[collection_name]
    doc = json.loads(document)
    result = collection.insert_one(doc)
    return f"Document inserted with ID: {result.inserted_id}"

@mcp.tool()
def find_documents(database_name: str, collection_name: str, query: str = "{}", limit: int = 10) -> List[Dict[str, Any]]:
    """Find documents in a collection based on a query"""
    db = client[database_name]
    collection = db[collection_name]
    query_dict = json.loads(query)
    cursor = collection.find(query_dict).limit(limit)
    return list(cursor)

@mcp.tool()
def update_document(database_name: str, collection_name: str, query: str, update: str) -> str:
    """Update documents in a collection based on a query"""
    db = client[database_name]
    collection = db[collection_name]
    query_dict = json.loads(query)
    update_dict = json.loads(update)
    result = collection.update_many(query_dict, {"$set": update_dict})
    return f"Modified {result.modified_count} document(s)"

@mcp.tool()
def delete_documents(database_name: str, collection_name: str, query: str) -> str:
    """Delete documents from a collection based on a query"""
    db = client[database_name]
    collection = db[collection_name]
    query_dict = json.loads(query)
    result = collection.delete_many(query_dict)
    return f"Deleted {result.deleted_count} document(s)"

@mcp.tool()
def count_documents(database_name: str, collection_name: str, query: str = "{}") -> int:
    """Count documents in a collection based on a query"""
    db = client[database_name]
    collection = db[collection_name]
    query_dict = json.loads(query)
    return collection.count_documents(query_dict)

# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello Hi, {name}!"