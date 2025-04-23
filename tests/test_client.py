"""
Tests for the client module.
"""

import unittest
import json
from unittest.mock import patch, MagicMock

from corezoid.client import CorezoidClient, CorezoidResponse
from corezoid.exceptions import ValidationError


class TestCorezoidResponse(unittest.TestCase):
    """
    Tests for the CorezoidResponse class.
    """

    def test_is_success(self):
        """
        Test checking if a response is successful.
        """
        success_response = CorezoidResponse({"request_proc": "ok"})
        error_response = CorezoidResponse({"request_proc": "error"})

        self.assertTrue(success_response.is_success())
        self.assertFalse(error_response.is_success())

    def test_get_error(self):
        """
        Test getting an error message from a response.
        """
        success_response = CorezoidResponse({"request_proc": "ok"})
        error_response = CorezoidResponse({
            "request_proc": "error",
            "error_message": "Test error"
        })

        self.assertIsNone(success_response.get_error())
        self.assertEqual(error_response.get_error(), "Test error")

    def test_get_operation_results(self):
        """
        Test getting operation results from a response.
        """
        ops = [{"ref": "test-ref", "proc": "ok"}]
        response = CorezoidResponse({"request_proc": "ok", "ops": ops})

        self.assertEqual(response.get_operation_results(), ops)

    def test_get_operation_result(self):
        """
        Test getting a specific operation result from a response.
        """
        ops = [
            {"ref": "test-ref-1", "proc": "ok"},
            {"ref": "test-ref-2", "proc": "error"}
        ]
        response = CorezoidResponse({"request_proc": "ok", "ops": ops})

        self.assertEqual(response.get_operation_result("test-ref-1"), ops[0])
        self.assertEqual(response.get_operation_result("test-ref-2"), ops[1])
        self.assertIsNone(response.get_operation_result("non-existent"))


class TestCorezoidClient(unittest.TestCase):
    """
    Tests for the CorezoidClient class.
    """

    def setUp(self):
        """
        Set up the test case.
        """
        self.api_login = "test-login"
        self.api_secret = "test-secret"
        self.client = CorezoidClient(api_login=self.api_login, api_secret=self.api_secret)

    def test_init(self):
        """
        Test initializing the client.
        """
        self.assertEqual(self.client.config.api_login, self.api_login)
        self.assertEqual(self.client.config.api_secret, self.api_secret)
        self.assertEqual(self.client.config.api_url, "https://api.corezoid.com/api/2/json")

        custom_url = "https://custom.api.url"
        custom_client = CorezoidClient(api_login=self.api_login, api_secret=self.api_secret, api_url=custom_url)
        self.assertEqual(custom_client.config.api_url, custom_url)

    @patch('corezoid.client.HTTPClient')
    def test_send_empty_operations(self, mock_http_client):
        """
        Test sending empty operations.
        """
        with self.assertRaises(ValidationError):
            self.client.send([])

    def test_send(self):
        """
        Test sending operations.
        """
        # Mock the client's methods
        self.client._prepare_content = MagicMock(return_value='{"ops":[{"type":"create"}]}')
        self.client.http_client = MagicMock()
        self.client.http_client.post = MagicMock(return_value={"request_proc": "ok", "ops": []})

        # Create operations
        operations = [{"type": "create", "conv_id": "1234", "obj": "task", "ref": "test-ref", "data": {}}]

        # Send the operations
        response = self.client.send(operations)

        # Check that the HTTP client was called
        self.client.http_client.post.assert_called_once()

        # Check the response
        self.assertIsInstance(response, CorezoidResponse)
        self.assertTrue(response.is_success())

    @patch('corezoid.client.HTTPClient')
    def test_upload_schema(self, mock_http_client):
        """
        Test uploading a schema.
        """
        # Mock the HTTP client
        mock_http = MagicMock()
        mock_http_client.return_value = mock_http
        mock_http.post.return_value = {"request_proc": "ok", "ops": []}

        # Create a schema
        folder_id = "1234"
        schema = json.dumps({"key": "value"})

        # Mock the send method
        self.client.send = MagicMock()
        self.client.send.return_value = CorezoidResponse({"request_proc": "ok", "ops": []})

        # Upload the schema
        response = self.client.upload_schema(folder_id, schema)

        # Check that the send method was called correctly
        self.client.send.assert_called_once()
        args, kwargs = self.client.send.call_args

        # Check the operations
        operations = args[0]
        self.assertEqual(len(operations), 1)
        self.assertEqual(operations[0]["type"], "create")
        self.assertEqual(operations[0]["obj"], "obj_scheme")
        self.assertEqual(operations[0]["folder_id"], folder_id)
        self.assertEqual(operations[0]["scheme"], schema)
        self.assertEqual(operations[0]["async"], "false")

        # Check the response
        self.assertIsInstance(response, CorezoidResponse)
        self.assertTrue(response.is_success())


if __name__ == "__main__":
    unittest.main()
