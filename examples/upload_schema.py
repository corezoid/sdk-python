"""
Example of uploading a process schema to Corezoid.
"""

import sys
import os
import json

# Add the parent directory to the path so we can import the corezoid package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from corezoid.client import CorezoidClient
from corezoid.exceptions import CorezoidError
from corezoid.config import Config
from corezoid.logging import get_logger
import logging


def main():
    # Enable debug logging
    logger = get_logger(level=logging.DEBUG)

    # Replace these with your actual credentials
    api_login = "your_api_login"  # Or set COREZOID_API_LOGIN env var
    api_secret = "your_api_secret"  # Or set COREZOID_API_SECRET env var
    folder_id = "your_folder_id"

    # Create configuration
    config = Config(api_login=api_login, api_secret=api_secret)

    # Initialize the client
    client = CorezoidClient(config=config)

    # Example schema (replace with your actual schema)
    schema = json.dumps([
        {
            "title": "Example Process",
            "description": "A simple example process",
            "nodes": [
                {
                    "id": "start",
                    "type": "start",
                    "title": "Start"
                },
                {
                    "id": "end",
                    "type": "end",
                    "title": "End"
                }
            ],
            "edges": [
                {
                    "source": "start",
                    "target": "end"
                }
            ]
        }
    ])

    try:
        # Upload the schema
        response = client.upload_schema(folder_id, schema)

        # Check if the request was successful
        if response.is_success():
            print("Schema uploaded successfully")
            print(f"Response: {response}")
        else:
            print(f"Failed to upload schema: {response.get_error()}")

    except CorezoidError as e:
        print(f"Error: {e}")

    finally:
        # Close the client
        client.close()


if __name__ == "__main__":
    main()
