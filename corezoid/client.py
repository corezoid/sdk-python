"""
Main client for the Corezoid SDK.
"""

import json
import logging
from typing import Dict, Any, List, Optional, Union

from .http import HTTPClient
from .utils import generate_signature, current_timestamp, to_json, from_json
from .exceptions import APIError, ValidationError
from .logging import logger
from .config import Config
from .batch import OperationBatch


class CorezoidResponse:
    """
    Response from the Corezoid API.
    """

    def __init__(self, response_data: Dict[str, Any]):
        """
        Initialize the response.

        Args:
            response_data: The raw response data from the API
        """
        self.data = response_data
        self.request_proc = response_data.get('request_proc')
        self.ops = response_data.get('ops', [])

    def is_success(self) -> bool:
        """
        Check if the request was successful.

        Returns:
            True if the request was successful, False otherwise
        """
        return self.request_proc == 'ok'

    def get_error(self) -> Optional[str]:
        """
        Get the error message if the request failed.

        Returns:
            The error message, or None if the request was successful
        """
        if self.is_success():
            return None

        return self.data.get('error_message')

    def get_operation_results(self) -> List[Dict[str, Any]]:
        """
        Get the results of all operations.

        Returns:
            A list of operation results
        """
        return self.ops

    def get_operation_result(self, ref: str) -> Optional[Dict[str, Any]]:
        """
        Get the result of a specific operation by reference.

        Args:
            ref: The operation reference

        Returns:
            The operation result, or None if not found
        """
        for op in self.ops:
            if op.get('ref') == ref:
                return op
        return None

    def __str__(self) -> str:
        """
        Get a string representation of the response.

        Returns:
            A string representation of the response
        """
        return json.dumps(self.data, indent=2)


class CorezoidClient:
    """
    Client for interacting with the Corezoid API.
    """

    def __init__(self, api_login: Optional[str] = None, api_secret: Optional[str] = None,
                 api_url: Optional[str] = None, config: Optional[Config] = None):
        """
        Initialize the client.

        Args:
            api_login: The API login (can also be set via COREZOID_API_LOGIN env var)
            api_secret: The API secret key (can also be set via COREZOID_API_SECRET env var)
            api_url: Optional custom API URL (can also be set via COREZOID_API_URL env var)
            config: Optional configuration object (overrides other parameters if provided)
        """
        # Initialize configuration
        if config is not None:
            self.config = config
        else:
            self.config = Config(api_login=api_login, api_secret=api_secret, api_url=api_url)

        # Validate configuration
        self.config.validate()

        # Initialize HTTP client
        self.http_client = HTTPClient(timeout=self.config.timeout, max_retries=self.config.max_retries)

        logger.debug(f"Initialized CorezoidClient with API URL: {self.config.api_url}")

    def send(self, operations: List[Dict[str, Any]]) -> CorezoidResponse:
        """
        Send operations to the Corezoid API.

        Args:
            operations: A list of operations to send

        Returns:
            The API response

        Raises:
            ValidationError: If the operations are invalid
            APIError: If the API returns an error
        """
        if not operations:
            raise ValidationError("No operations provided")

        logger.debug(f"Sending {len(operations)} operations to Corezoid API")

        timestamp = current_timestamp()
        content = self._prepare_content(operations)
        signature = generate_signature(self.config.api_secret, timestamp, content)

        headers = {
            'Content-Type': 'application/json',
            'X-API-Login': self.config.api_login,
            'X-API-Signature': signature,
            'X-API-Timestamp': timestamp
        }

        logger.debug(f"Request to {self.config.api_url} with content: {content}")

        try:
            response_data = self.http_client.post(self.config.api_url, from_json(content), headers)
            logger.debug(f"Response from Corezoid API: {json.dumps(response_data)}")

            response = CorezoidResponse(response_data)

            if not response.is_success():
                logger.warning(f"Corezoid API returned error: {response.get_error()}")
            else:
                logger.debug("Corezoid API request successful")

            return response
        except Exception as e:
            logger.error(f"Error sending request to Corezoid API: {str(e)}")
            raise

    def upload_schema(self, folder_id: Union[str, int], schema: str, async_mode: bool = False) -> CorezoidResponse:
        """
        Upload a process schema to Corezoid.

        Args:
            folder_id: The folder ID to upload to
            schema: The process schema as a JSON string
            async_mode: Whether to use async mode

        Returns:
            The API response
        """
        operation = {
            "type": "create",
            "obj": "obj_scheme",
            "folder_id": str(folder_id),
            "scheme": schema,
            "async": "true" if async_mode else "false"
        }

        return self.send([operation])

    def create_task(self, conv_id: Union[str, int], data: Dict[str, Any],
                   ref: Optional[str] = None) -> CorezoidResponse:
        """
        Create a new task in a conveyor.

        Args:
            conv_id: The conveyor ID
            data: The task data
            ref: Optional reference (generated if not provided)

        Returns:
            The API response
        """
        from .operations import RequestOperation
        import time
        import uuid

        # Generate a reference if not provided
        if ref is None:
            ref = f"task-{int(time.time())}-{uuid.uuid4().hex[:8]}"

        # Create the operation
        operation = RequestOperation.create(conv_id, ref, data)

        # Send the request
        response = self.send([operation])

        return response

    def modify_task(self, conv_id: Union[str, int], ref: str,
                    data: Dict[str, Any]) -> CorezoidResponse:
        """
        Modify an existing task by reference.

        Args:
            conv_id: The conveyor ID
            ref: The task reference
            data: The updated task data

        Returns:
            The API response
        """
        from .operations import RequestOperation

        # Create the operation
        operation = RequestOperation.modify_ref(conv_id, ref, data)

        # Send the request
        response = self.send([operation])

        return response

    def get_task(self, conv_id: Union[str, int], ref: str) -> CorezoidResponse:
        """
        Get a task by reference.

        Args:
            conv_id: The conveyor ID
            ref: The task reference

        Returns:
            The API response
        """
        from .operations import RequestOperation

        # Create the operation
        operation = RequestOperation.get(conv_id, ref)

        # Send the request
        response = self.send([operation])

        return response

    def create_batch(self, max_batch_size: int = 100) -> OperationBatch:
        """
        Create a new operation batch.

        Args:
            max_batch_size: Maximum number of operations in the batch

        Returns:
            The operation batch
        """
        return OperationBatch(max_batch_size=max_batch_size)

    def send_batch(self, batch: OperationBatch) -> CorezoidResponse:
        """
        Send a batch of operations to Corezoid.

        Args:
            batch: The operation batch

        Returns:
            The API response
        """
        if batch.is_empty():
            raise ValidationError("Batch is empty")

        return self.send(batch.get_operations())

    def _prepare_content(self, operations: List[Dict[str, Any]]) -> str:
        """
        Prepare the request content.

        Args:
            operations: A list of operations

        Returns:
            The request content as a JSON string
        """
        request = {
            "ops": operations
        }

        return to_json(request)

    def close(self):
        """
        Close the HTTP client.
        """
        self.http_client.close()
