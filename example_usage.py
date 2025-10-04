"""
Example usage of the DataLoader class.

This script demonstrates how to use the DataLoader to load data from
single files or folders containing CSV and XLSX files.
"""

from simple_data_loader import SimpleDataLoader, load_data
import pandas as pd


def example_single_file():
    """Example: Load data from a single file."""
    print("=== Example: Single File Loading ===")
    
    # Example with verbose output (default)
    loader = SimpleDataLoader("example_data.csv", verbose=True)
    df = loader.load()
    print(f"Loaded data shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print()


def example_folder():
    """Example: Load data from a folder."""
    print("=== Example: Folder Loading ===")
    
    # Load all files from a folder (no subfolders)
    loader = SimpleDataLoader("data_folder", include_subfolders=False, verbose=True)
    df = loader.load()
    print(f"Combined data shape: {df.shape}")
    print()


def example_with_subfolders():
    """Example: Load data from a folder including subfolders."""
    print("=== Example: Folder Loading with Subfolders ===")
    
    # Load all files from a folder including subfolders
    loader = SimpleDataLoader("data_folder", include_subfolders=True, verbose=True)
    df = loader.load()
    print(f"Combined data shape: {df.shape}")
    print()


def example_quiet_mode():
    """Example: Load data with minimal output."""
    print("=== Example: Quiet Mode ===")
    
    # Load data with minimal output
    loader = SimpleDataLoader("example_data.csv", verbose=False)
    df = loader.load()
    print(f"Loaded data shape: {df.shape} (no verbose output)")
    print()


def example_column_consistency():
    """Example: Column consistency checking."""
    print("=== Example: Column Consistency Checking ===")
    
    # Create files with different column structures
    import os
    os.makedirs("inconsistent_data", exist_ok=True)
    
    # File 1: 4 columns
    df1 = pd.DataFrame({
        'id': [1, 2, 3],
        'name': ['Alice', 'Bob', 'Charlie'],
        'age': [25, 30, 35],
        'city': ['NYC', 'LA', 'Chicago']
    })
    df1.to_csv("inconsistent_data/file1.csv", index=False)
    
    # File 2: 3 columns (different count)
    df2 = pd.DataFrame({
        'id': [4, 5, 6],
        'name': ['Diana', 'Eve', 'Frank'],
        'age': [28, 32, 29]
    })
    df2.to_csv("inconsistent_data/file2.csv", index=False)
    
    # File 3: 4 columns but different names
    df3 = pd.DataFrame({
        'id': [7, 8, 9],
        'full_name': ['Grace', 'Henry', 'Ivy'],  # Different column name
        'age': [31, 27, 33],
        'location': ['Boston', 'Seattle', 'Miami']  # Different column name
    })
    df3.to_csv("inconsistent_data/file3.csv", index=False)
    
    print("Created inconsistent data files for testing")
    
    # Test error mode
    try:
        loader = SimpleDataLoader("inconsistent_data", column_consistency='error')
        df = loader.load()
    except ValueError as e:
        print(f"Error mode caught inconsistency: {str(e)[:100]}...")
    
    # Test warning mode
    print("\nTesting warning mode:")
    loader = SimpleDataLoader("inconsistent_data", column_consistency='warning')
    df = loader.load()
    print(f"Warning mode loaded data shape: {df.shape}")
    
    # Test ignore mode
    print("\nTesting ignore mode:")
    loader = SimpleDataLoader("inconsistent_data", column_consistency='ignore')
    df = loader.load()
    print(f"Ignore mode loaded data shape: {df.shape}")
    print()


def example_convenience_function():
    """Example: Using the convenience function."""
    print("=== Example: Convenience Function ===")
    
    # Using the convenience function
    df = load_data("example_data.csv", verbose=True)
    print(f"Loaded data shape: {df.shape}")
    print()


def create_sample_data():
    """Create some sample data files for demonstration."""
    import os
    
    # Create sample CSV file
    sample_data = pd.DataFrame({
        'id': [1, 2, 3, 4, 5],
        'name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'],
        'age': [25, 30, 35, 28, 32],
        'city': ['New York', 'London', 'Tokyo', 'Paris', 'Sydney']
    })
    
    sample_data.to_csv("example_data.csv", index=False)
    print("Created example_data.csv")
    
    # Create a sample folder with multiple files
    os.makedirs("data_folder", exist_ok=True)
    
    # Create multiple CSV files
    for i in range(3):
        df = sample_data.copy()
        df['id'] = df['id'] + (i * 5)  # Make IDs unique
        df.to_csv(f"data_folder/data_{i+1}.csv", index=False)
    
    # Create an Excel file
    sample_data.to_excel("data_folder/data_excel.xlsx", index=False)
    
    print("Created data_folder with sample files")
    print()


if __name__ == "__main__":
    # Create sample data for demonstration
    create_sample_data()
    
    # Run examples
    try:
        example_single_file()
        example_folder()
        example_with_subfolders()
        example_quiet_mode()
        example_column_consistency()
        example_convenience_function()
        
    except FileNotFoundError as e:
        print(f"File not found: {e}")
        print("Make sure to run this script from the directory containing the data files.")
    except Exception as e:
        print(f"Error: {e}")
