"""
HTTP client for the Corezoid SDK.
"""

import json
import requests
import logging
from typing import Dict, Any, Optional, Union

from .exceptions import ConnectionError, APIError
from .utils import to_json
from .logging import logger


class HTTPClient:
    """
    HTTP client for making requests to the Corezoid API.
    """

    def __init__(self, timeout: int = 30, max_retries: int = 3):
        """
        Initialize the HTTP client.

        Args:
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries for failed requests
        """
        self.timeout = timeout
        self.session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(max_retries=max_retries)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)

    def post(self, url: str, data: Dict[str, Any], headers: Dict[str, str]) -> Dict[str, Any]:
        """
        Make a POST request to the Corezoid API.

        Args:
            url: The URL to request
            data: The request data
            headers: The request headers

        Returns:
            The response data

        Raises:
            ConnectionError: If the request fails
            APIError: If the API returns an error
        """
        logger.debug(f"Making POST request to {url}")

        try:
            json_data = to_json(data)
            logger.debug(f"Request data: {json_data}")

            response = self.session.post(
                url,
                data=json_data,
                headers=headers,
                timeout=self.timeout
            )

            logger.debug(f"Response status code: {response.status_code}")

            response.raise_for_status()

            try:
                response_json = response.json()
                logger.debug(f"Response data: {json.dumps(response_json)}")
                return response_json
            except json.JSONDecodeError:
                logger.error(f"Invalid JSON response: {response.text}")
                raise APIError("Invalid JSON response from Corezoid API", response=response.text)

        except requests.exceptions.RequestException as e:
            logger.error(f"Request exception: {str(e)}")
            raise ConnectionError(f"Failed to connect to Corezoid API: {str(e)}")

    def close(self):
        """
        Close the HTTP session.
        """
        self.session.close()
