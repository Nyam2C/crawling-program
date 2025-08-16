#!/usr/bin/env python3
"""
Fix Python 3.8 compatibility by adding __future__ imports
"""

import os
import re

def fix_file(filepath):
    """Add __future__ import annotations to a Python file if needed"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if file needs fixing (has typing imports but no __future__ import)
        has_typing = re.search(r'from typing import|: Dict|: List|: Optional|-> Dict|-> List|-> Optional', content)
        has_future = '__future__' in content and 'annotations' in content
        
        if has_typing and not has_future:
            lines = content.split('\n')
            
            # Find the position to insert __future__ import
            insert_pos = 0
            for i, line in enumerate(lines):
                if line.startswith('#!') or line.startswith('"""') or line.startswith("'''"):
                    continue
                if line.strip() == '':
                    continue
                if line.startswith('"""') and '"""' in line[3:]:
                    continue
                if line.startswith("'''") and "'''" in line[3:]:
                    continue
                # Check for multi-line docstrings
                if i > 0 and ('"""' in lines[i-1] or "'''" in lines[i-1]):
                    if '"""' in line or "'''" in line:
                        continue
                insert_pos = i
                break
            
            # Insert the __future__ import
            lines.insert(insert_pos, 'from __future__ import annotations')
            if insert_pos > 0 and lines[insert_pos-1].strip() != '':
                lines.insert(insert_pos, '')
            
            # Write back the modified content
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write('\n'.join(lines))
            
            print(f"Fixed: {filepath}")
            return True
        else:
            print(f"Skipped: {filepath} (no changes needed)")
            return False
            
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def main():
    """Fix all Python files in src directory"""
    files_to_fix = [
        "src/analysis/advanced_financial_analyzer.py",
        "src/analysis/financial_analyzer.py", 
        "src/analysis/investment_personality_analyzer.py",
        "src/analysis/recommendation_engine.py",
        "src/data/stock_crawler.py",
        "src/data/yfinance_data_source.py",
        "src/gui/components/panels/trading_order_panel.py",
        "src/gui/components/panels/trading_portfolio_panel.py",
        "src/gui/components/panels/trading_watchlist_panel.py",
        "src/gui/components/tabs/investment_analysis_tab.py",
        "src/gui/components/tabs/scoreboard_tab.py",
        "src/gui/components/trading/mock_trading_tab.py",
        "src/trading/data_manager.py",
        "src/trading/scoreboard_manager.py",
        "src/trading/scoreboard_models.py",
        "src/trading/trading_engine.py",
        "src/utils/stock_validator.py"
    ]
    
    fixed_count = 0
    for filepath in files_to_fix:
        if os.path.exists(filepath):
            if fix_file(filepath):
                fixed_count += 1
        else:
            print(f"File not found: {filepath}")
    
    print(f"\nFixed {fixed_count} files total")

if __name__ == "__main__":
    main()