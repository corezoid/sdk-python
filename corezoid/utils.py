"""
Utility functions for the Corezoid SDK.
"""

import hashlib
import hmac
import json
import time
from typing import Dict, Any, Union


def generate_signature(api_secret: str, timestamp: str, content: str) -> str:
    """
    Generate a signature for Corezoid API requests.
    
    Args:
        api_secret: The API secret key
        timestamp: The current timestamp
        content: The request content
        
    Returns:
        The generated signature
    """
    message = f"{timestamp}{content}"
    signature = hmac.new(
        api_secret.encode('utf-8'),
        message.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    return signature


def verify_signature(signature: str, api_secret: str, timestamp: str, content: str) -> bool:
    """
    Verify a signature from Corezoid API responses.
    
    Args:
        signature: The signature to verify
        api_secret: The API secret key
        timestamp: The timestamp from the response
        content: The response content
        
    Returns:
        True if the signature is valid, False otherwise
    """
    expected_signature = generate_signature(api_secret, timestamp, content)
    return hmac.compare_digest(signature, expected_signature)


def current_timestamp() -> str:
    """
    Get the current timestamp in the format required by Corezoid API.
    
    Returns:
        The current timestamp as a string
    """
    return str(int(time.time()))


def to_json(data: Dict[str, Any]) -> str:
    """
    Convert a dictionary to a JSON string.
    
    Args:
        data: The dictionary to convert
        
    Returns:
        The JSON string
    """
    return json.dumps(data, separators=(',', ':'))


def from_json(data: str) -> Dict[str, Any]:
    """
    Convert a JSON string to a dictionary.
    
    Args:
        data: The JSON string to convert
        
    Returns:
        The dictionary
    """
    return json.loads(data)


def validate_required_params(params: Dict[str, Any], required: list) -> None:
    """
    Validate that all required parameters are present.
    
    Args:
        params: The parameters to validate
        required: The list of required parameter names
        
    Raises:
        ValueError: If a required parameter is missing
    """
    missing = [param for param in required if param not in params or params[param] is None]
    if missing:
        raise ValueError(f"Missing required parameters: {', '.join(missing)}")


def clean_dict(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Remove None values from a dictionary.
    
    Args:
        data: The dictionary to clean
        
    Returns:
        The cleaned dictionary
    """
    return {k: v for k, v in data.items() if v is not None}
