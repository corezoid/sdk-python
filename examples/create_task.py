"""
Example of creating a new task in Corezoid.
"""

import time
import sys
import os

# Add the parent directory to the path so we can import the corezoid package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from corezoid.client import CorezoidClient
from corezoid.operations import RequestOperation
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

    # Alternatively, you can initialize the client directly:
    # client = CorezoidClient(api_login=api_login, api_secret=api_secret)

    # Or use environment variables:
    # client = CorezoidClient()

    # Create task data
    task_data = {
        "customer_id": "12345",
        "amount": 100.50,
        "currency": "USD",
        "timestamp": int(time.time())
    }

    # Create a unique reference for the task
    reference = f"order-{int(time.time())}"

    try:
        # Create the operation
        operation = RequestOperation.create(conveyor_id, reference, task_data)

        # Send the request
        response = client.send([operation])

        # Check if the request was successful
        if response.is_success():
            print(f"Task created successfully with reference: {reference}")
            print(f"Response: {response}")
        else:
            print(f"Failed to create task: {response.get_error()}")

    except CorezoidError as e:
        print(f"Error: {e}")

    finally:
        # Close the client
        client.close()


if __name__ == "__main__":
    main()
