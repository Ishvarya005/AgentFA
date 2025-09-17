#!/usr/bin/env python3

# Debug memory system execution
import sys
import traceback

try:
    print("Starting memory module execution...")
    
    # Read the memory.py file
    with open('core/services/memory.py', 'r') as f:
        content = f.read()
    
    print("File read successfully")
    
    # Execute line by line to find the issue
    lines = content.split('\n')
    namespace = {}
    
    for i, line in enumerate(lines, 1):
        try:
            if line.strip() and not line.strip().startswith('#'):
                exec(line, namespace)
        except Exception as e:
            print(f"Error at line {i}: {line}")
            print(f"Error: {e}")
            traceback.print_exc()
            break
    
    # Check what's in the namespace
    classes = [name for name in namespace if isinstance(namespace.get(name), type)]
    print(f"Classes found: {classes}")
    
except Exception as e:
    print(f"Error: {e}")
    traceback.print_exc()