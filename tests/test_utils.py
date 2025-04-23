"""
Tests for the utils module.
"""

import unittest
import json
from corezoid.utils import (
    generate_signature, verify_signature, to_json, from_json,
    validate_required_params, clean_dict
)


class TestUtils(unittest.TestCase):
    """
    Tests for utility functions.
    """
    
    def test_generate_signature(self):
        """
        Test generating a signature.
        """
        api_secret = "test-secret"
        timestamp = "1234567890"
        content = '{"key":"value"}'
        
        signature = generate_signature(api_secret, timestamp, content)
        
        self.assertIsInstance(signature, str)
        self.assertEqual(len(signature), 64)  # SHA-256 hex digest is 64 characters
    
    def test_verify_signature(self):
        """
        Test verifying a signature.
        """
        api_secret = "test-secret"
        timestamp = "1234567890"
        content = '{"key":"value"}'
        
        signature = generate_signature(api_secret, timestamp, content)
        
        self.assertTrue(verify_signature(signature, api_secret, timestamp, content))
        self.assertFalse(verify_signature("invalid-signature", api_secret, timestamp, content))
    
    def test_to_json(self):
        """
        Test converting a dictionary to a JSON string.
        """
        data = {"key": "value", "nested": {"inner": "value"}}
        
        json_str = to_json(data)
        
        self.assertIsInstance(json_str, str)
        self.assertEqual(json_str, '{"key":"value","nested":{"inner":"value"}}')
    
    def test_from_json(self):
        """
        Test converting a JSON string to a dictionary.
        """
        json_str = '{"key":"value","nested":{"inner":"value"}}'
        
        data = from_json(json_str)
        
        self.assertIsInstance(data, dict)
        self.assertEqual(data, {"key": "value", "nested": {"inner": "value"}})
    
    def test_validate_required_params(self):
        """
        Test validating required parameters.
        """
        params = {"key1": "value1", "key2": "value2"}
        
        # Should not raise an exception
        validate_required_params(params, ["key1", "key2"])
        
        # Should raise a ValueError
        with self.assertRaises(ValueError):
            validate_required_params(params, ["key1", "key3"])
    
    def test_clean_dict(self):
        """
        Test cleaning a dictionary.
        """
        data = {"key1": "value1", "key2": None, "key3": "value3"}
        
        cleaned = clean_dict(data)
        
        self.assertEqual(cleaned, {"key1": "value1", "key3": "value3"})


if __name__ == "__main__":
    unittest.main()
