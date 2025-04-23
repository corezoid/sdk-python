"""
Tests for the batch module.
"""

import unittest
from corezoid.batch import OperationBatch


class TestOperationBatch(unittest.TestCase):
    """
    Tests for the OperationBatch class.
    """
    
    def setUp(self):
        """
        Set up the test case.
        """
        self.batch = OperationBatch(max_batch_size=3)
    
    def test_add(self):
        """
        Test adding an operation to the batch.
        """
        operation = {"type": "create", "conv_id": "1234", "obj": "task", "ref": "test-ref", "data": {}}
        self.batch.add(operation)
        
        self.assertEqual(len(self.batch.operations), 1)
        self.assertEqual(self.batch.operations[0], operation)
    
    def test_add_full_batch(self):
        """
        Test adding an operation to a full batch.
        """
        # Fill the batch
        for i in range(3):
            self.batch.add({"type": "create", "conv_id": "1234", "obj": "task", "ref": f"test-ref-{i}", "data": {}})
        
        # Try to add another operation
        with self.assertRaises(ValueError):
            self.batch.add({"type": "create", "conv_id": "1234", "obj": "task", "ref": "test-ref-4", "data": {}})
    
    def test_add_create(self):
        """
        Test adding a create operation to the batch.
        """
        conv_id = "1234"
        data = {"key": "value"}
        ref = "test-ref"
        
        result_ref = self.batch.add_create(conv_id, data, ref)
        
        self.assertEqual(result_ref, ref)
        self.assertEqual(len(self.batch.operations), 1)
        self.assertEqual(self.batch.operations[0]["type"], "create")
        self.assertEqual(self.batch.operations[0]["conv_id"], conv_id)
        self.assertEqual(self.batch.operations[0]["obj"], "task")
        self.assertEqual(self.batch.operations[0]["ref"], ref)
        self.assertEqual(self.batch.operations[0]["data"], data)
    
    def test_add_create_auto_ref(self):
        """
        Test adding a create operation with automatic reference generation.
        """
        conv_id = "1234"
        data = {"key": "value"}
        
        ref = self.batch.add_create(conv_id, data)
        
        self.assertIsNotNone(ref)
        self.assertTrue(ref.startswith("task-"))
        self.assertEqual(len(self.batch.operations), 1)
        self.assertEqual(self.batch.operations[0]["type"], "create")
        self.assertEqual(self.batch.operations[0]["conv_id"], conv_id)
        self.assertEqual(self.batch.operations[0]["obj"], "task")
        self.assertEqual(self.batch.operations[0]["ref"], ref)
        self.assertEqual(self.batch.operations[0]["data"], data)
    
    def test_add_modify_ref(self):
        """
        Test adding a modify operation by reference to the batch.
        """
        conv_id = "1234"
        ref = "test-ref"
        data = {"key": "value"}
        
        self.batch.add_modify_ref(conv_id, ref, data)
        
        self.assertEqual(len(self.batch.operations), 1)
        self.assertEqual(self.batch.operations[0]["type"], "modify")
        self.assertEqual(self.batch.operations[0]["conv_id"], conv_id)
        self.assertEqual(self.batch.operations[0]["obj"], "task")
        self.assertEqual(self.batch.operations[0]["ref"], ref)
        self.assertEqual(self.batch.operations[0]["data"], data)
    
    def test_add_modify_id(self):
        """
        Test adding a modify operation by ID to the batch.
        """
        conv_id = "1234"
        obj_id = "5678"
        data = {"key": "value"}
        
        self.batch.add_modify_id(conv_id, obj_id, data)
        
        self.assertEqual(len(self.batch.operations), 1)
        self.assertEqual(self.batch.operations[0]["type"], "modify")
        self.assertEqual(self.batch.operations[0]["conv_id"], conv_id)
        self.assertEqual(self.batch.operations[0]["obj"], "task")
        self.assertEqual(self.batch.operations[0]["obj_id"], obj_id)
        self.assertEqual(self.batch.operations[0]["data"], data)
    
    def test_add_get(self):
        """
        Test adding a get operation by reference to the batch.
        """
        conv_id = "1234"
        ref = "test-ref"
        
        self.batch.add_get(conv_id, ref)
        
        self.assertEqual(len(self.batch.operations), 1)
        self.assertEqual(self.batch.operations[0]["type"], "get")
        self.assertEqual(self.batch.operations[0]["conv_id"], conv_id)
        self.assertEqual(self.batch.operations[0]["obj"], "task")
        self.assertEqual(self.batch.operations[0]["ref"], ref)
    
    def test_add_get_by_id(self):
        """
        Test adding a get operation by ID to the batch.
        """
        conv_id = "1234"
        obj_id = "5678"
        
        self.batch.add_get_by_id(conv_id, obj_id)
        
        self.assertEqual(len(self.batch.operations), 1)
        self.assertEqual(self.batch.operations[0]["type"], "get")
        self.assertEqual(self.batch.operations[0]["conv_id"], conv_id)
        self.assertEqual(self.batch.operations[0]["obj"], "task")
        self.assertEqual(self.batch.operations[0]["obj_id"], obj_id)
    
    def test_clear(self):
        """
        Test clearing the batch.
        """
        # Add some operations
        for i in range(3):
            self.batch.add({"type": "create", "conv_id": "1234", "obj": "task", "ref": f"test-ref-{i}", "data": {}})
        
        # Clear the batch
        self.batch.clear()
        
        self.assertEqual(len(self.batch.operations), 0)
    
    def test_is_empty(self):
        """
        Test checking if the batch is empty.
        """
        self.assertTrue(self.batch.is_empty())
        
        # Add an operation
        self.batch.add({"type": "create", "conv_id": "1234", "obj": "task", "ref": "test-ref", "data": {}})
        
        self.assertFalse(self.batch.is_empty())
    
    def test_is_full(self):
        """
        Test checking if the batch is full.
        """
        self.assertFalse(self.batch.is_full())
        
        # Fill the batch
        for i in range(3):
            self.batch.add({"type": "create", "conv_id": "1234", "obj": "task", "ref": f"test-ref-{i}", "data": {}})
        
        self.assertTrue(self.batch.is_full())
    
    def test_size(self):
        """
        Test getting the number of operations in the batch.
        """
        self.assertEqual(self.batch.size(), 0)
        
        # Add some operations
        for i in range(2):
            self.batch.add({"type": "create", "conv_id": "1234", "obj": "task", "ref": f"test-ref-{i}", "data": {}})
        
        self.assertEqual(self.batch.size(), 2)
    
    def test_get_operations(self):
        """
        Test getting all operations in the batch.
        """
        operations = [
            {"type": "create", "conv_id": "1234", "obj": "task", "ref": "test-ref-1", "data": {}},
            {"type": "create", "conv_id": "1234", "obj": "task", "ref": "test-ref-2", "data": {}}
        ]
        
        # Add the operations
        for op in operations:
            self.batch.add(op)
        
        # Get the operations
        result = self.batch.get_operations()
        
        self.assertEqual(result, operations)


if __name__ == "__main__":
    unittest.main()
