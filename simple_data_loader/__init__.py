"""
Simple Data Loader Package

A Python package for loading data from CSV and XLSX files.
Supports single file loading and folder concatenation with column consistency checking.
"""

from .simple_data_loader import SimpleDataLoader, load_data

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

__all__ = ["SimpleDataLoader", "load_data"]
