import pandas as pd
import os
import warnings
from pathlib import Path
from typing import Union, Optional


class SimpleDataLoader:
    """
    A class to load data from CSV and XLSX files.
    
    Can read from a single file or concatenate multiple files from a folder.
    Supports subfolder traversal and verbose output control.
    """
    
    def __init__(self, file_path: str, include_subfolders: bool = False, verbose: bool = True, 
                 column_consistency: str = 'error'):
        """
        Initialize the SimpleDataLoader.
        
        Args:
            file_path (str): Path to a file or folder
            include_subfolders (bool): Whether to include files from subfolders (default: False)
            verbose (bool): Whether to print detailed information (default: True)
            column_consistency (str): How to handle column consistency ('error', 'warning', 'ignore') (default: 'error')
        """
        self.file_path = Path(file_path)
        self.include_subfolders = include_subfolders
        self.verbose = verbose
        
        if column_consistency not in ['error', 'warning', 'ignore']:
            raise ValueError("column_consistency must be one of: 'error', 'warning', 'ignore'")
        self.column_consistency = column_consistency
        
    def load(self) -> pd.DataFrame:
        """
        Load data from the specified path.
        
        Returns:
            pd.DataFrame: Loaded data as a pandas DataFrame
        """
        if not self.file_path.exists():
            raise FileNotFoundError(f"Path does not exist: {self.file_path}")
        
        if self.file_path.is_file():
            return self._load_single_file()
        elif self.file_path.is_dir():
            return self._load_folder()
        else:
            raise ValueError(f"Path is neither a file nor a directory: {self.file_path}")
    
    def _load_single_file(self) -> pd.DataFrame:
        """Load data from a single file."""
        file_extension = self.file_path.suffix.lower()
        
        if file_extension == '.csv':
            df = pd.read_csv(self.file_path)
        elif file_extension in ['.xlsx', '.xls']:
            df = pd.read_excel(self.file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
        
        if self.verbose:
            print(f"{self.file_path.name} is imported with {len(df)} rows and {len(df.columns)} columns")
        
        return df
    
    def _load_folder(self) -> pd.DataFrame:
        """Load and concatenate data from all files in a folder."""
        dataframes = []
        file_count = 0
        
        # Get all files in the folder
        if self.include_subfolders:
            pattern = "**/*"
        else:
            pattern = "*"
        
        files = list(self.file_path.glob(pattern))
        
        # Filter for CSV and XLSX files
        supported_extensions = {'.csv', '.xlsx', '.xls'}
        data_files = [f for f in files if f.is_file() and f.suffix.lower() in supported_extensions]
        
        if not data_files:
            raise ValueError(f"No supported files (CSV, XLSX) found in {self.file_path}")
        
        if self.verbose:
            print(f"Found {len(data_files)} files to process")
        
        # Handle column consistency check
        if self.column_consistency == 'ignore':
            if self.verbose:
                print("Column consistency check is skipped")
            # Load files normally if consistency check is ignored
            for file_path in data_files:
                try:
                    df = self._load_single_file_from_path(file_path)
                    dataframes.append(df)
                    file_count += 1
                except Exception as e:
                    if self.verbose:
                        print(f"Error loading {file_path.name}: {str(e)}")
                    continue
            
            if not dataframes:
                raise ValueError("No files could be successfully loaded")
        else:
            # First pass: load all files to check consistency
            temp_dataframes = []
            for file_path in data_files:
                try:
                    df = self._load_single_file_from_path(file_path)
                    temp_dataframes.append((df, file_path.name))
                except Exception as e:
                    if self.verbose:
                        print(f"Error loading {file_path.name}: {str(e)}")
                    continue
            
            if not temp_dataframes:
                raise ValueError("No files could be successfully loaded")
            
            # Check column consistency
            self._check_column_consistency(temp_dataframes)
            
            # If we get here and mode is 'error', consistency check passed
            dataframes = [df for df, _ in temp_dataframes]
            file_count = len(dataframes)
        
        # Concatenate all dataframes
        combined_df = pd.concat(dataframes, ignore_index=True)
        
        if self.verbose:
            print(f"\nSummary:")
            print(f"Successfully loaded {file_count} files")
            print(f"Combined dataset has {len(combined_df)} rows and {len(combined_df.columns)} columns")
        
        return combined_df
    
    def _check_column_consistency(self, temp_dataframes):
        """Check if all dataframes have consistent columns."""
        if len(temp_dataframes) < 2:
            return  # No need to check consistency for single file
        
        # Get column information from first file
        first_df, first_filename = temp_dataframes[0]
        first_columns = list(first_df.columns)
        first_column_count = len(first_columns)
        
        # Check consistency with other files
        inconsistent_files = []
        
        for df, filename in temp_dataframes[1:]:
            current_columns = list(df.columns)
            current_column_count = len(current_columns)
            
            # Check column count
            if current_column_count != first_column_count:
                inconsistent_files.append({
                    'file': filename,
                    'issue': f"Column count mismatch: {current_column_count} vs {first_column_count}",
                    'columns': current_columns
                })
                continue
            
            # Check column names
            if current_columns != first_columns:
                inconsistent_files.append({
                    'file': filename,
                    'issue': f"Column names mismatch",
                    'columns': current_columns,
                    'expected': first_columns
                })
        
        # Handle inconsistencies based on mode
        if inconsistent_files:
            error_message = f"Column consistency issues found:\n"
            error_message += f"Reference file: {first_filename} (columns: {first_columns})\n\n"
            
            for issue in inconsistent_files:
                error_message += f"File: {issue['file']}\n"
                error_message += f"Issue: {issue['issue']}\n"
                if 'expected' in issue:
                    error_message += f"Expected columns: {issue['expected']}\n"
                error_message += f"Actual columns: {issue['columns']}\n\n"
            
            if self.column_consistency == 'error':
                raise ValueError(error_message.strip())
            elif self.column_consistency == 'warning':
                warnings.warn(error_message.strip())
                if self.verbose:
                    print("WARNING: Column consistency issues detected but continuing...")
    
    def _load_single_file_from_path(self, file_path: Path) -> pd.DataFrame:
        """Load data from a single file path (used internally)."""
        file_extension = file_path.suffix.lower()
        
        if file_extension == '.csv':
            df = pd.read_csv(file_path)
        elif file_extension in ['.xlsx', '.xls']:
            df = pd.read_excel(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
        
        if self.verbose:
            print(f"{file_path.name} is imported with {len(df)} rows and {len(df.columns)} columns")
        
        return df


# Convenience function for direct usage
def load_data(file_path: str, include_subfolders: bool = False, verbose: bool = True, 
              column_consistency: str = 'error') -> pd.DataFrame:
    """
    Convenience function to load data directly.
    
    Args:
        file_path (str): Path to a file or folder
        include_subfolders (bool): Whether to include files from subfolders (default: False)
        verbose (bool): Whether to print detailed information (default: True)
        column_consistency (str): How to handle column consistency ('error', 'warning', 'ignore') (default: 'error')
    
    Returns:
        pd.DataFrame: Loaded data as a pandas DataFrame
    """
    loader = SimpleDataLoader(file_path, include_subfolders, verbose, column_consistency)
    return loader.load()
