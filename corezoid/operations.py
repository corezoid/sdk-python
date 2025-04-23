"""
Operation builders for the Corezoid SDK.
"""

from typing import Dict, Any, List, Optional, Union


class RequestOperation:
    """
    Builder for Corezoid API request operations.
    """
    
    @staticmethod
    def create(conv_id: Union[str, int], ref: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new task in a conveyor.
        
        Args:
            conv_id: The conveyor ID
            ref: A unique reference for the task
            data: The task data
            
        Returns:
            The operation dictionary
        """
        return {
            "type": "create",
            "conv_id": str(conv_id),
            "obj": "task",
            "ref": ref,
            "data": data
        }
    
    @staticmethod
    def modify_ref(conv_id: Union[str, int], ref: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Modify a task by reference.
        
        Args:
            conv_id: The conveyor ID
            ref: The task reference
            data: The updated task data
            
        Returns:
            The operation dictionary
        """
        return {
            "type": "modify",
            "conv_id": str(conv_id),
            "obj": "task",
            "ref": ref,
            "data": data
        }
    
    @staticmethod
    def modify_id(conv_id: Union[str, int], obj_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Modify a task by ID.
        
        Args:
            conv_id: The conveyor ID
            obj_id: The task ID
            data: The updated task data
            
        Returns:
            The operation dictionary
        """
        return {
            "type": "modify",
            "conv_id": str(conv_id),
            "obj": "task",
            "obj_id": obj_id,
            "data": data
        }
    
    @staticmethod
    def get(conv_id: Union[str, int], ref: str) -> Dict[str, Any]:
        """
        Get a task by reference.
        
        Args:
            conv_id: The conveyor ID
            ref: The task reference
            
        Returns:
            The operation dictionary
        """
        return {
            "type": "get",
            "conv_id": str(conv_id),
            "obj": "task",
            "ref": ref
        }
    
    @staticmethod
    def get_by_id(conv_id: Union[str, int], obj_id: str) -> Dict[str, Any]:
        """
        Get a task by ID.
        
        Args:
            conv_id: The conveyor ID
            obj_id: The task ID
            
        Returns:
            The operation dictionary
        """
        return {
            "type": "get",
            "conv_id": str(conv_id),
            "obj": "task",
            "obj_id": obj_id
        }


class ResponseOperation:
    """
    Builder for Corezoid API response operations.
    """
    
    @staticmethod
    def ok(conv_id: Union[str, int], ref: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Create a success response operation.
        
        Args:
            conv_id: The conveyor ID
            ref: The task reference
            data: Optional response data
            
        Returns:
            The operation dictionary
        """
        operation = {
            "obj": "task",
            "proc": "ok",
            "conv_id": str(conv_id),
            "ref": ref
        }
        
        if data:
            operation["data"] = data
            
        return operation
    
    @staticmethod
    def error(conv_id: Union[str, int], ref: str, error_message: str, 
              error_code: Optional[str] = None) -> Dict[str, Any]:
        """
        Create an error response operation.
        
        Args:
            conv_id: The conveyor ID
            ref: The task reference
            error_message: The error message
            error_code: Optional error code
            
        Returns:
            The operation dictionary
        """
        operation = {
            "obj": "task",
            "proc": "error",
            "conv_id": str(conv_id),
            "ref": ref,
            "error_message": error_message
        }
        
        if error_code:
            operation["error_code"] = error_code
            
        return operation
