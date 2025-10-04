"""
Pytest test suite for DataLoader class.

This module contains comprehensive tests for the DataLoader functionality:
- Single file loading
- Folder loading with consistent files
- Folder loading with inconsistent files
- Column consistency validation
- Convenience function testing
"""

import pytest
import pandas as pd
import os
import tempfile
import shutil
from pathlib import Path
from data_loader import DataLoader, load_data


@pytest.fixture(scope="module")
def test_data_dir():
    """Create temporary directory with test data."""
    # Create temporary directory
    temp_dir = tempfile.mkdtemp()
    
    # Create test data structure
    single_file_dir = os.path.join(temp_dir, "single_file")
    consistent_dir = os.path.join(temp_dir, "consistent_folder")
    inconsistent_dir = os.path.join(temp_dir, "inconsistent_folder")
    
    os.makedirs(single_file_dir, exist_ok=True)
    os.makedirs(consistent_dir, exist_ok=True)
    os.makedirs(inconsistent_dir, exist_ok=True)
    
    # Create single file test data
    employees_data = pd.DataFrame({
        'id': range(1, 11),
        'name': ['Alice Johnson', 'Bob Smith', 'Charlie Brown', 'Diana Prince', 'Eve Wilson',
                'Frank Miller', 'Grace Lee', 'Henry Davis', 'Ivy Chen', 'Jack Wilson'],
        'age': [25, 30, 35, 28, 32, 29, 27, 31, 26, 33],
        'department': ['Engineering', 'Marketing', 'Sales', 'Engineering', 'HR',
                      'Engineering', 'Marketing', 'Sales', 'HR', 'Engineering'],
        'salary': [75000, 65000, 70000, 80000, 60000, 72000, 68000, 75000, 62000, 78000],
        'city': ['New York', 'Los Angeles', 'Chicago', 'Boston', 'Seattle',
                'Austin', 'Denver', 'Miami', 'Portland', 'San Francisco']
    })
    employees_data.to_csv(os.path.join(single_file_dir, "employees.csv"), index=False)
    
    # Create consistent folder test data
    for quarter, start_id in [('Q1', 101), ('Q2', 201), ('Q3', 301)]:
        sales_data = pd.DataFrame({
            'product_id': range(start_id, start_id + 10),
            'product_name': [f'Product {i}' for i in range(start_id, start_id + 10)],
            'category': ['Electronics', 'Accessories'] * 5,
            'price': [99.99 + i for i in range(10)],
            'quantity_sold': [50 + i for i in range(10)],
            'quarter': [quarter] * 10
        })
        sales_data.to_csv(os.path.join(consistent_dir, f"{quarter.lower()}_sales.csv"), index=False)
    
    # Create inconsistent folder test data
    # File 1: Complete customer data
    customers1 = pd.DataFrame({
        'customer_id': range(1001, 1011),
        'first_name': ['John', 'Jane', 'Mike', 'Sarah', 'David', 'Lisa', 'Tom', 'Amy', 'Chris', 'Emma'],
        'last_name': ['Doe', 'Smith', 'Johnson', 'Brown', 'Wilson', 'Davis', 'Miller', 'Garcia', 'Martinez', 'Anderson'],
        'email': [f'customer{i}@email.com' for i in range(1001, 1011)],
        'phone': [f'555-{i:04d}' for i in range(1001, 1011)],
        'city': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix',
                'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose'],
        'state': ['NY', 'CA', 'IL', 'TX', 'AZ', 'PA', 'TX', 'CA', 'TX', 'CA'],
        'registration_date': ['2023-01-15', '2023-01-20', '2023-02-01', '2023-02-10', '2023-02-15',
                             '2023-03-01', '2023-03-05', '2023-03-10', '2023-03-15', '2023-03-20']
    })
    customers1.to_csv(os.path.join(inconsistent_dir, "customers_q1.csv"), index=False)
    
    # File 2: Complete customer data (different quarter)
    customers2 = pd.DataFrame({
        'customer_id': range(2001, 2011),
        'first_name': ['Alex', 'Maria', 'James', 'Jennifer', 'Robert', 'Linda', 'William', 'Elizabeth', 'Richard', 'Patricia'],
        'last_name': ['Taylor', 'Thomas', 'Jackson', 'White', 'Harris', 'Martin', 'Thompson', 'Garcia', 'Martinez', 'Robinson'],
        'email': [f'customer{i}@email.com' for i in range(2001, 2011)],
        'phone': [f'555-{i:04d}' for i in range(2001, 2011)],
        'city': ['Austin', 'Jacksonville', 'Fort Worth', 'Columbus', 'Charlotte',
                'San Francisco', 'Indianapolis', 'Seattle', 'Denver', 'Washington'],
        'state': ['TX', 'FL', 'TX', 'OH', 'NC', 'CA', 'IN', 'WA', 'CO', 'DC'],
        'registration_date': ['2023-04-01', '2023-04-05', '2023-04-10', '2023-04-15', '2023-04-20',
                             '2023-05-01', '2023-05-05', '2023-05-10', '2023-05-15', '2023-05-20']
    })
    customers2.to_csv(os.path.join(inconsistent_dir, "customers_q2.csv"), index=False)
    
    # File 3: Incomplete customer data (missing columns: phone, state, registration_date)
    customers3 = pd.DataFrame({
        'customer_id': range(3001, 3011),
        'first_name': ['Michael', 'Barbara', 'Christopher', 'Susan', 'Joseph', 'Jessica', 'Daniel', 'Sarah', 'Matthew', 'Karen'],
        'last_name': ['Clark', 'Rodriguez', 'Lewis', 'Lee', 'Walker', 'Hall', 'Allen', 'Young', 'Hernandez', 'King'],
        'email': [f'customer{i}@email.com' for i in range(3001, 3011)],
        'city': ['Boston', 'El Paso', 'Nashville', 'Detroit', 'Oklahoma City',
                'Portland', 'Las Vegas', 'Louisville', 'Baltimore', 'Milwaukee']
        # Missing: phone, state, registration_date columns
    })
    customers3.to_csv(os.path.join(inconsistent_dir, "customers_q3.csv"), index=False)
    
    yield temp_dir
    
    # Cleanup
    shutil.rmtree(temp_dir)


class TestSingleFileLoading:
    """Test cases for single file loading."""
    
    def test_load_single_csv_file(self, test_data_dir):
        """Test loading a single CSV file."""
        file_path = os.path.join(test_data_dir, "single_file", "employees.csv")
        loader = DataLoader(file_path, verbose=False)
        df = loader.load()
        
        # Assertions
        assert isinstance(df, pd.DataFrame)
        assert df.shape == (10, 6)
        assert list(df.columns) == ['id', 'name', 'age', 'department', 'salary', 'city']
        assert df['id'].tolist() == list(range(1, 11))
    
    def test_load_single_file_with_verbose(self, test_data_dir, capsys):
        """Test single file loading with verbose output."""
        file_path = os.path.join(test_data_dir, "single_file", "employees.csv")
        loader = DataLoader(file_path, verbose=True)
        df = loader.load()
        
        captured = capsys.readouterr()
        assert "employees.csv is imported with 10 rows and 6 columns" in captured.out
        assert df.shape == (10, 6)


class TestConsistentFolderLoading:
    """Test cases for folder loading with consistent files."""
    
    def test_load_consistent_folder(self, test_data_dir):
        """Test loading a folder with consistent files."""
        folder_path = os.path.join(test_data_dir, "consistent_folder")
        loader = DataLoader(folder_path, verbose=False)
        df = loader.load()
        
        # Assertions
        assert isinstance(df, pd.DataFrame)
        assert df.shape == (30, 6)  # 3 files * 10 rows each
        assert list(df.columns) == ['product_id', 'product_name', 'category', 'price', 'quantity_sold', 'quarter']
        assert df['quarter'].value_counts().to_dict() == {'Q1': 10, 'Q2': 10, 'Q3': 10}
    
    def test_load_consistent_folder_with_verbose(self, test_data_dir, capsys):
        """Test consistent folder loading with verbose output."""
        folder_path = os.path.join(test_data_dir, "consistent_folder")
        loader = DataLoader(folder_path, verbose=True)
        df = loader.load()
        
        captured = capsys.readouterr()
        assert "Found 3 files to process" in captured.out
        assert "Successfully loaded 3 files" in captured.out
        assert "Combined dataset has 30 rows and 6 columns" in captured.out
        assert df.shape == (30, 6)
    
    def test_load_consistent_folder_with_subfolders(self, test_data_dir):
        """Test loading consistent folder with subfolder option."""
        folder_path = os.path.join(test_data_dir, "consistent_folder")
        loader = DataLoader(folder_path, include_subfolders=True, verbose=False)
        df = loader.load()
        
        # Should work the same since no subfolders exist
        assert df.shape == (30, 6)


class TestInconsistentFolderLoading:
    """Test cases for folder loading with inconsistent files."""
    
    def test_inconsistent_folder_error_mode(self, test_data_dir):
        """Test inconsistent folder loading with error mode."""
        folder_path = os.path.join(test_data_dir, "inconsistent_folder")
        loader = DataLoader(folder_path, column_consistency='error', verbose=False)
        
        with pytest.raises(ValueError, match="Column consistency issues found"):
            loader.load()
    
    def test_inconsistent_folder_warning_mode(self, test_data_dir):
        """Test inconsistent folder loading with warning mode."""
        folder_path = os.path.join(test_data_dir, "inconsistent_folder")
        loader = DataLoader(folder_path, column_consistency='warning', verbose=False)
        
        # Should not raise an error, but should show warning
        with pytest.warns(UserWarning, match="Column consistency issues found"):
            df = loader.load()
        
        assert isinstance(df, pd.DataFrame)
        assert df.shape == (30, 8)  # 3 files * 10 rows, 8 columns (from first file)
    
    def test_inconsistent_folder_ignore_mode(self, test_data_dir):
        """Test inconsistent folder loading with ignore mode."""
        folder_path = os.path.join(test_data_dir, "inconsistent_folder")
        loader = DataLoader(folder_path, column_consistency='ignore', verbose=False)
        
        df = loader.load()
        
        assert isinstance(df, pd.DataFrame)
        assert df.shape == (30, 8)  # 3 files * 10 rows, 8 columns (from first file)
    
    def test_inconsistent_folder_warning_mode_with_verbose(self, test_data_dir, capsys):
        """Test warning mode with verbose output."""
        folder_path = os.path.join(test_data_dir, "inconsistent_folder")
        loader = DataLoader(folder_path, column_consistency='warning', verbose=True)
        
        with pytest.warns(UserWarning):
            df = loader.load()
        
        captured = capsys.readouterr()
        assert "WARNING: Column consistency issues detected but continuing..." in captured.out
        assert df.shape == (30, 8)
    
    def test_inconsistent_folder_ignore_mode_with_verbose(self, test_data_dir, capsys):
        """Test ignore mode with verbose output."""
        folder_path = os.path.join(test_data_dir, "inconsistent_folder")
        loader = DataLoader(folder_path, column_consistency='ignore', verbose=True)
        
        df = loader.load()
        
        captured = capsys.readouterr()
        assert "Column consistency check is skipped" in captured.out
        assert df.shape == (30, 8)


class TestConvenienceFunction:
    """Test cases for the convenience function."""
    
    def test_load_data_single_file(self, test_data_dir):
        """Test convenience function with single file."""
        file_path = os.path.join(test_data_dir, "single_file", "employees.csv")
        df = load_data(file_path, verbose=False)
        
        assert isinstance(df, pd.DataFrame)
        assert df.shape == (10, 6)
        assert list(df.columns) == ['id', 'name', 'age', 'department', 'salary', 'city']
    
    def test_load_data_consistent_folder(self, test_data_dir):
        """Test convenience function with consistent folder."""
        folder_path = os.path.join(test_data_dir, "consistent_folder")
        df = load_data(folder_path, verbose=False)
        
        assert isinstance(df, pd.DataFrame)
        assert df.shape == (30, 6)
    
    def test_load_data_with_all_parameters(self, test_data_dir):
        """Test convenience function with all parameters."""
        folder_path = os.path.join(test_data_dir, "consistent_folder")
        df = load_data(folder_path, include_subfolders=True, verbose=False, column_consistency='error')
        
        assert isinstance(df, pd.DataFrame)
        assert df.shape == (30, 6)


class TestErrorHandling:
    """Test cases for error handling."""
    
    def test_file_not_found(self):
        """Test handling of non-existent file."""
        loader = DataLoader("non_existent_file.csv", verbose=False)
        
        with pytest.raises(FileNotFoundError):
            loader.load()
    
    def test_invalid_path_type(self):
        """Test handling of invalid path type."""
        loader = DataLoader("test_path", verbose=False)
        
        # This should work if test_path doesn't exist as file or directory
        with pytest.raises(FileNotFoundError):
            loader.load()
    
    def test_invalid_column_consistency_value(self):
        """Test handling of invalid column_consistency parameter."""
        with pytest.raises(ValueError, match="column_consistency must be one of"):
            DataLoader("test.csv", column_consistency='invalid')
    
    def test_empty_folder(self, test_data_dir):
        """Test handling of empty folder."""
        empty_folder = os.path.join(test_data_dir, "empty_folder")
        os.makedirs(empty_folder, exist_ok=True)
        
        loader = DataLoader(empty_folder, verbose=False)
        
        with pytest.raises(ValueError, match="No supported files"):
            loader.load()


class TestDataIntegrity:
    """Test cases for data integrity and edge cases."""
    
    def test_data_types_preserved(self, test_data_dir):
        """Test that data types are preserved correctly."""
        file_path = os.path.join(test_data_dir, "single_file", "employees.csv")
        loader = DataLoader(file_path, verbose=False)
        df = loader.load()
        
        # Check data types
        assert df['id'].dtype in ['int64', 'int32']
        assert df['age'].dtype in ['int64', 'int32']
        assert df['salary'].dtype in ['int64', 'int32']
        assert df['name'].dtype == 'object'
        assert df['department'].dtype == 'object'
        assert df['city'].dtype == 'object'
    
    def test_index_reset_after_concatenation(self, test_data_dir):
        """Test that index is reset after concatenation."""
        folder_path = os.path.join(test_data_dir, "consistent_folder")
        loader = DataLoader(folder_path, verbose=False)
        df = loader.load()
        
        # Index should be reset to 0, 1, 2, ..., 29
        assert list(df.index) == list(range(30))
    
    def test_no_duplicate_columns_after_concatenation(self, test_data_dir):
        """Test that no duplicate columns exist after concatenation."""
        folder_path = os.path.join(test_data_dir, "consistent_folder")
        loader = DataLoader(folder_path, verbose=False)
        df = loader.load()
        
        # Should have exactly 6 unique columns
        assert len(df.columns) == 6
        assert len(set(df.columns)) == 6
