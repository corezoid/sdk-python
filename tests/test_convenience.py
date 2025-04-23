"""
Tests for the convenience methods in the client module.
"""

import unittest
from unittest.mock import MagicMock, patch
from corezoid.client import CorezoidClient
from corezoid.batch import OperationBatch
from corezoid.exceptions import ValidationError


class TestConvenienceMethods(unittest.TestCase):
    """
    Tests for the convenience methods in the CorezoidClient class.
    """
    
    def setUp(self):
        """
        Set up the test case.
        """
        self.api_login = "test-login"
        self.api_secret = "test-secret"
        self.client = CorezoidClient(api_login=self.api_login, api_secret=self.api_secret)
    
    def test_create_task(self):
        """
        Test creating a task.
        """
        # Mock the send method
        self.client.send = MagicMock()
        
        # Create a task
        conv_id = "1234"
        data = {"key": "value"}
        ref = "test-ref"
        
        self.client.create_task(conv_id, data, ref)
        
        # Check that send was called with the correct operation
        self.client.send.assert_called_once()
        args, kwargs = self.client.send.call_args
        
        operations = args[0]
        self.assertEqual(len(operations), 1)
        self.assertEqual(operations[0]["type"], "create")
        self.assertEqual(operations[0]["conv_id"], conv_id)
        self.assertEqual(operations[0]["obj"], "task")
        self.assertEqual(operations[0]["ref"], ref)
        self.assertEqual(operations[0]["data"], data)
    
    def test_create_task_auto_ref(self):
        """
        Test creating a task with automatic reference generation.
        """
        # Mock the send method
        self.client.send = MagicMock()
        
        # Create a task
        conv_id = "1234"
        data = {"key": "value"}
        
        self.client.create_task(conv_id, data)
        
        # Check that send was called with the correct operation
        self.client.send.assert_called_once()
        args, kwargs = self.client.send.call_args
        
        operations = args[0]
        self.assertEqual(len(operations), 1)
        self.assertEqual(operations[0]["type"], "create")
        self.assertEqual(operations[0]["conv_id"], conv_id)
        self.assertEqual(operations[0]["obj"], "task")
        self.assertIsNotNone(operations[0]["ref"])
        self.assertEqual(operations[0]["data"], data)
    
    def test_modify_task(self):
        """
        Test modifying a task.
        """
        # Mock the send method
        self.client.send = MagicMock()
        
        # Modify a task
        conv_id = "1234"
        ref = "test-ref"
        data = {"key": "value"}
        
        self.client.modify_task(conv_id, ref, data)
        
        # Check that send was called with the correct operation
        self.client.send.assert_called_once()
        args, kwargs = self.client.send.call_args
        
        operations = args[0]
        self.assertEqual(len(operations), 1)
        self.assertEqual(operations[0]["type"], "modify")
        self.assertEqual(operations[0]["conv_id"], conv_id)
        self.assertEqual(operations[0]["obj"], "task")
        self.assertEqual(operations[0]["ref"], ref)
        self.assertEqual(operations[0]["data"], data)
    
    def test_get_task(self):
        """
        Test getting a task.
        """
        # Mock the send method
        self.client.send = MagicMock()
        
        # Get a task
        conv_id = "1234"
        ref = "test-ref"
        
        self.client.get_task(conv_id, ref)
        
        # Check that send was called with the correct operation
        self.client.send.assert_called_once()
        args, kwargs = self.client.send.call_args
        
        operations = args[0]
        self.assertEqual(len(operations), 1)
        self.assertEqual(operations[0]["type"], "get")
        self.assertEqual(operations[0]["conv_id"], conv_id)
        self.assertEqual(operations[0]["obj"], "task")
        self.assertEqual(operations[0]["ref"], ref)
    
    def test_create_batch(self):
        """
        Test creating a batch.
        """
        batch = self.client.create_batch(max_batch_size=10)
        
        self.assertIsInstance(batch, OperationBatch)
        self.assertEqual(batch.max_batch_size, 10)
    
    def test_send_batch(self):
        """
        Test sending a batch.
        """
        # Mock the send method
        self.client.send = MagicMock()
        
        # Create a batch
        batch = self.client.create_batch()
        
        # Add some operations
        operations = [
            {"type": "create", "conv_id": "1234", "obj": "task", "ref": "test-ref-1", "data": {}},
            {"type": "create", "conv_id": "1234", "obj": "task", "ref": "test-ref-2", "data": {}}
        ]
        
        for op in operations:
            batch.add(op)
        
        # Send the batch
        self.client.send_batch(batch)
        
        # Check that send was called with the correct operations
        self.client.send.assert_called_once_with(operations)
    
    def test_send_empty_batch(self):
        """
        Test sending an empty batch.
        """
        # Create an empty batch
        batch = self.client.create_batch()
        
        # Try to send the batch
        with self.assertRaises(ValidationError):
            self.client.send_batch(batch)


if __name__ == "__main__":
    unittest.main()
