"""
Configuration for the Corezoid SDK.
"""

import os
from typing import Dict, Any, Optional


class Config:
    """
    Configuration for the Corezoid SDK.
    """
    
    # Default API URL
    DEFAULT_API_URL = "https://api.corezoid.com/api/2/json"
    
    # Default HTTP settings
    DEFAULT_TIMEOUT = 30
    DEFAULT_MAX_RETRIES = 3
    
    def __init__(self, 
                 api_login: Optional[str] = None, 
                 api_secret: Optional[str] = None,
                 api_url: Optional[str] = None,
                 timeout: Optional[int] = None,
                 max_retries: Optional[int] = None):
        """
        Initialize the configuration.
        
        Args:
            api_login: The API login (can also be set via COREZOID_API_LOGIN env var)
            api_secret: The API secret key (can also be set via COREZOID_API_SECRET env var)
            api_url: The API URL (can also be set via COREZOID_API_URL env var)
            timeout: The HTTP timeout in seconds (can also be set via COREZOID_TIMEOUT env var)
            max_retries: The maximum number of HTTP retries (can also be set via COREZOID_MAX_RETRIES env var)
        """
        # API credentials
        self.api_login = api_login or os.environ.get("COREZOID_API_LOGIN")
        self.api_secret = api_secret or os.environ.get("COREZOID_API_SECRET")
        
        # API URL
        self.api_url = api_url or os.environ.get("COREZOID_API_URL") or self.DEFAULT_API_URL
        
        # HTTP settings
        self.timeout = int(timeout or os.environ.get("COREZOID_TIMEOUT") or self.DEFAULT_TIMEOUT)
        self.max_retries = int(max_retries or os.environ.get("COREZOID_MAX_RETRIES") or self.DEFAULT_MAX_RETRIES)
    
    def validate(self) -> None:
        """
        Validate the configuration.
        
        Raises:
            ValueError: If the configuration is invalid
        """
        if not self.api_login:
            raise ValueError("API login is required")
        
        if not self.api_secret:
            raise ValueError("API secret is required")
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the configuration to a dictionary.
        
        Returns:
            The configuration as a dictionary
        """
        return {
            "api_login": self.api_login,
            "api_secret": self.api_secret,
            "api_url": self.api_url,
            "timeout": self.timeout,
            "max_retries": self.max_retries
        }
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'Config':
        """
        Create a configuration from a dictionary.
        
        Args:
            config_dict: The configuration dictionary
            
        Returns:
            The configuration
        """
        return cls(
            api_login=config_dict.get("api_login"),
            api_secret=config_dict.get("api_secret"),
            api_url=config_dict.get("api_url"),
            timeout=config_dict.get("timeout"),
            max_retries=config_dict.get("max_retries")
        )
    
    @classmethod
    def from_env(cls) -> 'Config':
        """
        Create a configuration from environment variables.
        
        Returns:
            The configuration
        """
        return cls()
