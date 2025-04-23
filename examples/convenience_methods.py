"""
Example of using convenience methods in Corezoid.
"""

import time
import sys
import os

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
    conveyor_id = "your_conveyor_id"
    
    # Create configuration
    config = Config(api_login=api_login, api_secret=api_secret)
    
    # Initialize the client
    client = CorezoidClient(config=config)
    
    try:
        # Create task data
        task_data = {
            "customer_id": "12345",
            "amount": 100.50,
            "currency": "USD",
            "timestamp": int(time.time())
        }
        
        # Create a task using the convenience method
        print("Creating a task...")
        response = client.create_task(conveyor_id, task_data)
        
        # Check if the request was successful
        if response.is_success():
            # Get the reference from the response
            op_result = response.get_operation_results()[0]
            ref = op_result.get('ref')
            
            print(f"Task created successfully with reference: {ref}")
            
            # Modify the task
            print(f"Modifying task with reference: {ref}")
            update_data = {
                "status": "processed",
                "processed_at": int(time.time())
            }
            
            response = client.modify_task(conveyor_id, ref, update_data)
            
            # Check if the modification was successful
            if response.is_success():
                print("Task modified successfully")
                
                # Get the task
                print(f"Getting task with reference: {ref}")
                response = client.get_task(conveyor_id, ref)
                
                # Check if the get was successful
                if response.is_success():
                    print("Task retrieved successfully")
                    print(f"Task data: {response.get_operation_results()[0]}")
                else:
                    print(f"Failed to get task: {response.get_error()}")
            else:
                print(f"Failed to modify task: {response.get_error()}")
        else:
            print(f"Failed to create task: {response.get_error()}")
    
    except CorezoidError as e:
        print(f"Error: {e}")
    
    finally:
        # Close the client
        client.close()


if __name__ == "__main__":
    main()
