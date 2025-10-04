# Simple Data Loader

A Python package for loading data from CSV and XLSX files, with support for single files or concatenating multiple files from folders.

## Features

- **Single File Loading**: Read CSV or XLSX files individually
- **Folder Loading**: Automatically concatenate all CSV/XLSX files in a folder
- **Subfolder Support**: Option to include files from subfolders
- **Verbose Output**: Control the level of detail in console output
- **Error Handling**: Graceful handling of file errors and unsupported formats
- **Flexible Usage**: Both class-based and function-based interfaces

## Installation

### Install from PyPI (when published)
```bash
pip install simple-data-loader
```

### Install from wheel file
```bash
pip install simple_data_loader-1.0.2-py3-none-any.whl
```

### Install from source
```bash
git clone https://github.com/shenzj1994/simple-data-loader.git
cd simple-data-loader
pip install -e .
```

### Install dependencies only
```bash
pip install pandas openpyxl xlrd
```

## Dependencies

- **pandas** (>=1.3.0): For data manipulation and DataFrame operations
- **openpyxl** (>=3.0.0): For reading Excel (.xlsx) files
- **xlrd** (>=2.0.0): For reading legacy Excel (.xls) files

## Quick Start

### Basic Usage

```python
from simple_data_loader import SimpleDataLoader

# Load a single file
loader = SimpleDataLoader("data.csv")
df = loader.load()

# Load all files from a folder
loader = SimpleDataLoader("data_folder")
df = loader.load()
```

### Using the Convenience Function

```python
from simple_data_loader import load_data

# Direct loading
df = load_data("data.csv")
df = load_data("data_folder")
```

## Detailed Usage

### Class Initialization

```python
SimpleDataLoader(file_path, include_subfolders=False, verbose=True, column_consistency='error')
```

**Parameters:**
- `file_path` (str): Path to a file or folder
- `include_subfolders` (bool): Whether to include files from subfolders (default: False)
- `verbose` (bool): Whether to print detailed information (default: True)
- `column_consistency` (str): How to handle column consistency ('error', 'warning', 'ignore') (default: 'error')

### Examples

#### 1. Single File Loading

```python
from simple_data_loader import SimpleDataLoader

# Load a CSV file
loader = SimpleDataLoader("sales_data.csv")
df = loader.load()

# Load an Excel file
loader = SimpleDataLoader("financial_report.xlsx")
df = loader.load()
```

**Output:**
```
sales_data.csv is imported with 1000 rows and 5 columns
```

#### 2. Folder Loading (No Subfolders)

```python
loader = SimpleDataLoader("data_folder", include_subfolders=False)
df = loader.load()
```

**Output:**
```
Found 3 files to process
data_1.csv is imported with 500 rows and 4 columns
data_2.csv is imported with 300 rows and 4 columns
data_3.xlsx is imported with 200 rows and 4 columns

Summary:
Successfully loaded 3 files
Combined dataset has 1000 rows and 4 columns
```

#### 3. Folder Loading (With Subfolders)

```python
loader = SimpleDataLoader("data_folder", include_subfolders=True)
df = loader.load()
```

This will recursively search through all subfolders and load all CSV/XLSX files.

#### 4. Quiet Mode

```python
loader = SimpleDataLoader("data.csv", verbose=False)
df = loader.load()
```

No console output will be displayed.

#### 5. Column Consistency Control

```python
# Error mode (default) - stops if columns don't match
loader = SimpleDataLoader("data_folder", column_consistency='error')
df = loader.load()

# Warning mode - shows warning but continues
loader = SimpleDataLoader("data_folder", column_consistency='warning')
df = loader.load()

# Ignore mode - skips consistency check entirely
loader = SimpleDataLoader("data_folder", column_consistency='ignore')
df = loader.load()
```

**Column Consistency Modes:**
- `'error'` (default): Raises an error if files have different column counts or names
- `'warning'`: Shows a warning but continues processing
- `'ignore'`: Skips consistency check entirely

#### 6. Convenience Function

```python
from simple_data_loader import load_data

# All parameters are optional
df = load_data("data.csv")  # Uses defaults
df = load_data("data_folder", include_subfolders=True, verbose=False, column_consistency='warning')
```

## Supported File Formats

- **CSV files**: `.csv`
- **Excel files**: `.xlsx`, `.xls`

## Error Handling

The SimpleDataLoader handles various error scenarios:

- **File not found**: Raises `FileNotFoundError`
- **Unsupported format**: Raises `ValueError` with format information
- **Invalid path**: Raises `ValueError` if path is neither file nor directory
- **Column consistency errors**: Raises `ValueError` when `column_consistency='error'` and files have mismatched columns
- **Individual file errors**: Continues processing other files and reports errors in verbose mode

## Example Project Structure

```
project/
├── simple_data_loader/
│   ├── __init__.py
│   └── simple_data_loader.py
├── tests/
│   └── test_data_loader_pytest.py
├── requirements.txt
├── example_usage.py
├── README.md
├── data/
│   ├── sales_2023.csv
│   ├── sales_2024.csv
│   └── reports/
│       ├── monthly_report.xlsx
│       └── quarterly_summary.csv
└── single_file.csv
```

## Running Examples

To see the SimpleDataLoader in action, run the example script:

```bash
python example_usage.py
```

This will create sample data files and demonstrate various usage patterns.

## Testing

Run the comprehensive test suite:

```bash
# Run all tests
python -m pytest

# Run tests with verbose output
python -m pytest -v

# Run specific test class
python -m pytest tests/test_data_loader_pytest.py::TestSingleFileLoading -v
```

The test suite includes 20 tests covering:
- Single file loading
- Folder loading with consistent files
- Column consistency validation
- Error handling
- Data integrity checks

## API Reference

### SimpleDataLoader Class

#### Methods

- `load()`: Load data from the specified path
  - Returns: `pandas.DataFrame`

#### Internal Methods

- `_load_single_file()`: Load data from a single file
- `_load_folder()`: Load and concatenate data from folder
- `_load_single_file_from_path()`: Internal method for loading individual files

### Convenience Function

- `load_data(file_path, include_subfolders=False, verbose=True, column_consistency='error')`: Direct data loading function

## Performance Notes

- Large files are loaded into memory entirely
- For very large datasets, consider processing files individually
- Concatenation happens in memory, so ensure sufficient RAM for large folder operations

## License

This project is open source and available under the MIT License.
