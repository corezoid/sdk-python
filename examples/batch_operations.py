"""
Example of using batch operations in Corezoid.
"""

import time
import sys
import os

# Add the parent directory to the path so we can import the corezoid package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from corezoid.client import CorezoidClient
from corezoid.batch import OperationBatch
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
        # Create a batch
        batch = client.create_batch(max_batch_size=10)
        
        # Add operations to the batch
        for i in range(3):
            # Create task data
            task_data = {
                "customer_id": f"customer-{i}",
                "amount": 100.50 + i,
                "currency": "USD",
                "timestamp": int(time.time())
            }
            
            # Add a create operation to the batch
            ref = batch.add_create(conveyor_id, task_data)
            print(f"Added task with reference: {ref}")
        
        # Send the batch
        print(f"Sending batch with {batch.size()} operations...")
        response = client.send_batch(batch)
        
        # Check if the request was successful
        if response.is_success():
            print("Batch sent successfully")
            
            # Get the results for each operation
            for op_result in response.get_operation_results():
                ref = op_result.get('ref')
                proc = op_result.get('proc')
                print(f"Operation with reference {ref}: {proc}")
        else:
            print(f"Failed to send batch: {response.get_error()}")
        
        # Create another batch for modification
        batch.clear()
        
        # Add modification operations
        for op_result in response.get_operation_results():
            ref = op_result.get('ref')
            if ref:
                # Create update data
                update_data = {
                    "status": "processed",
                    "processed_at": int(time.time())
                }
                
                # Add a modify operation to the batch
                batch.add_modify_ref(conveyor_id, ref, update_data)
                print(f"Added modification for task with reference: {ref}")
        
        # Send the batch if not empty
        if not batch.is_empty():
            print(f"Sending batch with {batch.size()} operations...")
            response = client.send_batch(batch)
            
            # Check if the request was successful
            if response.is_success():
                print("Batch sent successfully")
                
                # Get the results for each operation
                for op_result in response.get_operation_results():
                    ref = op_result.get('ref')
                    proc = op_result.get('proc')
                    print(f"Operation with reference {ref}: {proc}")
            else:
                print(f"Failed to send batch: {response.get_error()}")
    
    except CorezoidError as e:
        print(f"Error: {e}")
    
    finally:
        # Close the client
        client.close()


if __name__ == "__main__":
    main()
