"""
Batch operations for the Corezoid SDK.
"""

from typing import Dict, Any, List, Optional, Union, Callable
import time
import uuid

from .operations import RequestOperation
from .logging import logger


class OperationBatch:
    """
    A batch of operations to be sent to Corezoid in a single request.
    """
    
    def __init__(self, max_batch_size: int = 100):
        """
        Initialize the batch.
        
        Args:
            max_batch_size: Maximum number of operations in a batch
        """
        self.operations = []
        self.max_batch_size = max_batch_size
    
    def add(self, operation: Dict[str, Any]) -> None:
        """
        Add an operation to the batch.
        
        Args:
            operation: The operation to add
            
        Raises:
            ValueError: If the batch is full
        """
        if len(self.operations) >= self.max_batch_size:
            raise ValueError(f"Batch is full (max size: {self.max_batch_size})")
        
        self.operations.append(operation)
        logger.debug(f"Added operation to batch. Batch size: {len(self.operations)}")
    
    def add_create(self, conv_id: Union[str, int], data: Dict[str, Any], 
                   ref: Optional[str] = None) -> str:
        """
        Add a create operation to the batch.
        
        Args:
            conv_id: The conveyor ID
            data: The task data
            ref: Optional reference (generated if not provided)
            
        Returns:
            The reference used for the operation
        """
        # Generate a reference if not provided
        if ref is None:
            ref = f"task-{int(time.time())}-{uuid.uuid4().hex[:8]}"
        
        # Create the operation
        operation = RequestOperation.create(conv_id, ref, data)
        
        # Add to batch
        self.add(operation)
        
        return ref
    
    def add_modify_ref(self, conv_id: Union[str, int], ref: str, 
                       data: Dict[str, Any]) -> None:
        """
        Add a modify operation by reference to the batch.
        
        Args:
            conv_id: The conveyor ID
            ref: The task reference
            data: The updated task data
        """
        operation = RequestOperation.modify_ref(conv_id, ref, data)
        self.add(operation)
    
    def add_modify_id(self, conv_id: Union[str, int], obj_id: str, 
                      data: Dict[str, Any]) -> None:
        """
        Add a modify operation by ID to the batch.
        
        Args:
            conv_id: The conveyor ID
            obj_id: The task ID
            data: The updated task data
        """
        operation = RequestOperation.modify_id(conv_id, obj_id, data)
        self.add(operation)
    
    def add_get(self, conv_id: Union[str, int], ref: str) -> None:
        """
        Add a get operation by reference to the batch.
        
        Args:
            conv_id: The conveyor ID
            ref: The task reference
        """
        operation = RequestOperation.get(conv_id, ref)
        self.add(operation)
    
    def add_get_by_id(self, conv_id: Union[str, int], obj_id: str) -> None:
        """
        Add a get operation by ID to the batch.
        
        Args:
            conv_id: The conveyor ID
            obj_id: The task ID
        """
        operation = RequestOperation.get_by_id(conv_id, obj_id)
        self.add(operation)
    
    def clear(self) -> None:
        """
        Clear the batch.
        """
        self.operations = []
        logger.debug("Batch cleared")
    
    def is_empty(self) -> bool:
        """
        Check if the batch is empty.
        
        Returns:
            True if the batch is empty, False otherwise
        """
        return len(self.operations) == 0
    
    def is_full(self) -> bool:
        """
        Check if the batch is full.
        
        Returns:
            True if the batch is full, False otherwise
        """
        return len(self.operations) >= self.max_batch_size
    
    def size(self) -> int:
        """
        Get the number of operations in the batch.
        
        Returns:
            The number of operations
        """
        return len(self.operations)
    
    def get_operations(self) -> List[Dict[str, Any]]:
        """
        Get all operations in the batch.
        
        Returns:
            The list of operations
        """
        return self.operations
