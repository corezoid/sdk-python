#!/usr/bin/env python
"""
Run all examples for the Corezoid SDK.
"""

import os
import sys
import importlib.util


def run_example(file_path):
    """
    Run an example script.
    
    Args:
        file_path: The path to the example script
    """
    print(f"\nRunning example: {os.path.basename(file_path)}")
    print("=" * 80)
    
    # Import the module
    spec = importlib.util.spec_from_file_location("example", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    # Run the main function
    if hasattr(module, "main"):
        module.main()
    
    print("=" * 80)


def main():
    """
    Run all examples.
    """
    examples_dir = os.path.join(os.path.dirname(__file__), "examples")
    
    # Get all Python files in the examples directory
    example_files = [
        os.path.join(examples_dir, f)
        for f in os.listdir(examples_dir)
        if f.endswith(".py") and not f.startswith("__")
    ]
    
    # Run each example
    for example_file in example_files:
        run_example(example_file)


if __name__ == "__main__":
    main()
