#!/usr/bin/env python3
"""
Python Version Compatibility Checker
"""

import sys
import platform

def check_python_version():
    """Check if Python version is compatible"""
    required_version = (3, 9)
    current_version = sys.version_info[:2]
    
    if current_version < required_version:
        return False, f"Python {required_version[0]}.{required_version[1]}+ required, but you have {current_version[0]}.{current_version[1]}"
    
    return True, None

def get_system_info():
    """Get system information for debugging"""
    return {
        'python_version': platform.python_version(),
        'python_implementation': platform.python_implementation(),
        'system': platform.system(),
        'machine': platform.machine(),
        'platform': platform.platform()
    }

def show_compatibility_error():
    """Show detailed compatibility error information"""
    compatible, error = check_python_version()
    if not compatible:
        print("="*60)
        print("PYTHON VERSION COMPATIBILITY ERROR")
        print("="*60)
        print(f"Error: {error}")
        print()
        
        system_info = get_system_info()
        print("System Information:")
        for key, value in system_info.items():
            print(f"  {key.replace('_', ' ').title()}: {value}")
        
        print()
        print("Solutions:")
        print("1. Upgrade Python to version 3.9 or higher")
        print("2. Use a virtual environment with a compatible Python version")
        print("3. Check if you have multiple Python installations")
        
        return False
    
    return True

if __name__ == "__main__":
    compatible = show_compatibility_error()
    if not compatible:
        sys.exit(1)
    else:
        print("Python version is compatible!")