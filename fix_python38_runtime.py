#!/usr/bin/env python3
"""
Runtime fix for Python 3.8 - Replace problematic type hint syntax
"""

import os
import re
import sys

def fix_type_hints_in_file(filepath):
    """Remove or fix problematic type hints in a file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Replace Dict[str, Type] with just dict
        content = re.sub(r': Dict\[[^\]]+\]', ': dict', content)
        content = re.sub(r': List\[[^\]]+\]', ': list', content)
        content = re.sub(r': Optional\[[^\]]+\]', '', content)
        content = re.sub(r'-> Dict\[[^\]]+\]', '-> dict', content)
        content = re.sub(r'-> List\[[^\]]+\]', '-> list', content)
        content = re.sub(r'-> Optional\[[^\]]+\]', '', content)
        
        # Fix variable annotations
        content = re.sub(r'(\w+): Dict\[[^\]]+\] = ', r'\1 = ', content)
        content = re.sub(r'(\w+): List\[[^\]]+\] = ', r'\1 = ', content)
        content = re.sub(r'(\w+): Optional\[[^\]]+\] = ', r'\1 = ', content)
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed type hints in: {filepath}")
            return True
        else:
            print(f"No changes needed: {filepath}")
            return False
            
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def main():
    """Fix all Python files"""
    files_with_issues = [
        "src/gui/components/ui_core/keyboard_manager.py",
        "src/gui/components/ui_core/action_manager.py",
        "src/trading/models.py",
        "src/trading/trading_engine.py",
        "src/trading/scoreboard_manager.py",
        "src/data/yfinance_data_source.py",
        "src/gui/components/trading/mock_trading_tab.py"
    ]
    
    fixed_count = 0
    for filepath in files_with_issues:
        if os.path.exists(filepath):
            if fix_type_hints_in_file(filepath):
                fixed_count += 1
        else:
            print(f"File not found: {filepath}")
    
    print(f"\nProcessed {len(files_with_issues)} files, fixed {fixed_count}")

if __name__ == "__main__":
    main()