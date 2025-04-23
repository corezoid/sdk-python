# Corezoid Python SDK

A modern Python client library for interacting with the [Corezoid Process Engine](https://corezoid.com/) platform.

## Overview

The Corezoid SDK for Python provides a simplified interface for creating, modifying, and managing tasks within Corezoid processes (also called conveyors). This SDK handles complex aspects like secure communication, message signing, HTTP connection management, and request/response formatting.

## Requirements

- Python 3.7 or higher
- `requests` library
- `pycryptodome` library

## Installation

### Using pip

```bash
pip install corezoid-sdk
```

### From source

```bash
git clone https://github.com/corezoid/sdk-python.git
cd sdk-python
pip install -e .
```

## Usage Examples

### Creating a New Task

```python
from corezoid.client import CorezoidClient
from corezoid.operations import RequestOperation
import time

# Initialize client
client = CorezoidClient(api_login="your_api_login", api_secret="your_api_secret")

# Create task data
task_data = {
    "customer_id": "12345",
    "amount": 100.50,
    "currency": "USD"
}

# Create operation
conveyor_id = "1234"  # Your conveyor ID
reference = f"order-{int(time.time())}"  # Unique reference
operation = RequestOperation.create(conveyor_id, reference, task_data)

# Send request
response = client.send([operation])
print(f"Response: {response}")

# Check operation status
if response.is_success():
    print(f"Task created successfully with reference: {reference}")
else:
    print(f"Failed to create task: {response.get_error()}")
```

### Modifying an Existing Task

```python
# Modify task by reference
update_data = {
    "status": "processed",
    "processed_at": int(time.time())
}

operation = RequestOperation.modify_ref(conveyor_id, reference, update_data)
response = client.send([operation])

if response.is_success():
    print(f"Task modified successfully with reference: {reference}")
else:
    print(f"Failed to modify task: {response.get_error()}")
```

## API Documentation

### Core Classes

#### CorezoidClient

The main client class for interacting with the Corezoid API.

```python
client = CorezoidClient(api_login, api_secret, api_url=None)
```

Parameters:
- `api_login`: Your Corezoid API login
- `api_secret`: Your Corezoid API secret key
- `api_url`: Optional custom API URL (defaults to Corezoid cloud API)

Methods:
- `send(operations)`: Send operations to Corezoid
- `upload_schema(folder_id, schema)`: Upload a process schema

#### RequestOperation

Provides builders for different types of operations that can be performed on Corezoid tasks.

```python
# Create a new task
RequestOperation.create(conv_id, ref, data)

# Modify a task by ID
RequestOperation.modify_id(conv_id, task_id, data)

# Modify a task by reference
RequestOperation.modify_ref(conv_id, ref, data)
```

#### CorezoidResponse

Represents a response from the Corezoid API.

Methods:
- `is_success()`: Check if the operation was successful
- `get_error()`: Get error message if operation failed
- `get_result()`: Get operation result

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Additional Resources

- [Corezoid API Documentation](https://doc.corezoid.com/en/api/upload_modify.html)
- [Corezoid Website](https://corezoid.com/)