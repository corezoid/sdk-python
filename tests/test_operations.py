"""
Tests for the operations module.
"""

import unittest
from corezoid.operations import RequestOperation, ResponseOperation


class TestRequestOperation(unittest.TestCase):
    """
    Tests for the RequestOperation class.
    """
    
    def test_create(self):
        """
        Test creating a task.
        """
        conv_id = "1234"
        ref = "test-ref"
        data = {"key": "value"}
        
        operation = RequestOperation.create(conv_id, ref, data)
        
        self.assertEqual(operation["type"], "create")
        self.assertEqual(operation["conv_id"], conv_id)
        self.assertEqual(operation["obj"], "task")
        self.assertEqual(operation["ref"], ref)
        self.assertEqual(operation["data"], data)
    
    def test_modify_ref(self):
        """
        Test modifying a task by reference.
        """
        conv_id = "1234"
        ref = "test-ref"
        data = {"key": "value"}
        
        operation = RequestOperation.modify_ref(conv_id, ref, data)
        
        self.assertEqual(operation["type"], "modify")
        self.assertEqual(operation["conv_id"], conv_id)
        self.assertEqual(operation["obj"], "task")
        self.assertEqual(operation["ref"], ref)
        self.assertEqual(operation["data"], data)
    
    def test_modify_id(self):
        """
        Test modifying a task by ID.
        """
        conv_id = "1234"
        obj_id = "5678"
        data = {"key": "value"}
        
        operation = RequestOperation.modify_id(conv_id, obj_id, data)
        
        self.assertEqual(operation["type"], "modify")
        self.assertEqual(operation["conv_id"], conv_id)
        self.assertEqual(operation["obj"], "task")
        self.assertEqual(operation["obj_id"], obj_id)
        self.assertEqual(operation["data"], data)
    
    def test_get(self):
        """
        Test getting a task by reference.
        """
        conv_id = "1234"
        ref = "test-ref"
        
        operation = RequestOperation.get(conv_id, ref)
        
        self.assertEqual(operation["type"], "get")
        self.assertEqual(operation["conv_id"], conv_id)
        self.assertEqual(operation["obj"], "task")
        self.assertEqual(operation["ref"], ref)
    
    def test_get_by_id(self):
        """
        Test getting a task by ID.
        """
        conv_id = "1234"
        obj_id = "5678"
        
        operation = RequestOperation.get_by_id(conv_id, obj_id)
        
        self.assertEqual(operation["type"], "get")
        self.assertEqual(operation["conv_id"], conv_id)
        self.assertEqual(operation["obj"], "task")
        self.assertEqual(operation["obj_id"], obj_id)


class TestResponseOperation(unittest.TestCase):
    """
    Tests for the ResponseOperation class.
    """
    
    def test_ok(self):
        """
        Test creating a success response.
        """
        conv_id = "1234"
        ref = "test-ref"
        data = {"key": "value"}
        
        operation = ResponseOperation.ok(conv_id, ref, data)
        
        self.assertEqual(operation["obj"], "task")
        self.assertEqual(operation["proc"], "ok")
        self.assertEqual(operation["conv_id"], conv_id)
        self.assertEqual(operation["ref"], ref)
        self.assertEqual(operation["data"], data)
    
    def test_ok_without_data(self):
        """
        Test creating a success response without data.
        """
        conv_id = "1234"
        ref = "test-ref"
        
        operation = ResponseOperation.ok(conv_id, ref)
        
        self.assertEqual(operation["obj"], "task")
        self.assertEqual(operation["proc"], "ok")
        self.assertEqual(operation["conv_id"], conv_id)
        self.assertEqual(operation["ref"], ref)
        self.assertNotIn("data", operation)
    
    def test_error(self):
        """
        Test creating an error response.
        """
        conv_id = "1234"
        ref = "test-ref"
        error_message = "Test error"
        error_code = "TEST_ERROR"
        
        operation = ResponseOperation.error(conv_id, ref, error_message, error_code)
        
        self.assertEqual(operation["obj"], "task")
        self.assertEqual(operation["proc"], "error")
        self.assertEqual(operation["conv_id"], conv_id)
        self.assertEqual(operation["ref"], ref)
        self.assertEqual(operation["error_message"], error_message)
        self.assertEqual(operation["error_code"], error_code)
    
    def test_error_without_code(self):
        """
        Test creating an error response without an error code.
        """
        conv_id = "1234"
        ref = "test-ref"
        error_message = "Test error"
        
        operation = ResponseOperation.error(conv_id, ref, error_message)
        
        self.assertEqual(operation["obj"], "task")
        self.assertEqual(operation["proc"], "error")
        self.assertEqual(operation["conv_id"], conv_id)
        self.assertEqual(operation["ref"], ref)
        self.assertEqual(operation["error_message"], error_message)
        self.assertNotIn("error_code", operation)


if __name__ == "__main__":
    unittest.main()
