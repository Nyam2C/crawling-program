#!/usr/bin/env python3
"""
Main entry point for the Magnificent Seven Stock Analysis & Recommendation System
"""

import logging
from cli import StockAnalysisCLI


def setup_logging():
    """Configure logging for the application"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def main():
    """Main function"""
    setup_logging()
    
    cli = StockAnalysisCLI()
    cli.run()


if __name__ == "__main__":
    main()