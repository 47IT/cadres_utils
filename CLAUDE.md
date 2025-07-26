# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Dependency Management
- `uv lock --upgrade && uv sync` - Update dependencies using uv (defined in Makefile)
- `uv sync` - Install dependencies
- `uv run python test_main.py` - Run the test file

### Package Management
- Uses `pyproject.toml` for project configuration
- Python 3.13+ required
- Main dependencies: aiohttp, openpyxl, pandas, setuptools

## Project Architecture

### Package Structure
The `cadres_utils` package provides utility functions organized into specialized modules:

- **api/**: Web API utilities with aiohttp-based HTTP client
  - `wapi_invoker.py`: Main API client with authentication and error handling
  - `exception.py`: Custom exceptions for API operations
  - `default_request.py`: Request formatting utilities

- **common_data/**: Configuration and shared data structures
  - `config.py`: Application configuration

- **date_utils.py**: Date manipulation and formatting utilities
  - Functions for date conversion, API string formatting, and date range generation

- **field_utils.py**: Field value processing and formatting
  - Handles different data types (datetime, int64, float) with custom formatting

- **excel/**: Excel file processing utilities
  - `excel_data_source.py`: Excel data source handling
  - `excel_utils.py`: Excel manipulation utilities
  - `reader.py`: Excel file reading functionality

- **file/**: File processing utilities
  - `utils.py`: General file operations

- **logger/**: Logging configuration
  - `initializer.py`: Logger setup and configuration

- **list_utils.py**: List manipulation utilities
- **doc_utils.py**: Document processing utilities

### Key Patterns
- Uses async/await for API operations with aiohttp
- Pandas DataFrames for data manipulation
- Custom exception hierarchy for API errors
- Consistent date formatting patterns (VIEW_DATE_FORMAT: '%d.%m.%Y', SERVER_DATE_FORMAT: '%Y-%m-%d')
- Logger initialization pattern using `init_logger()`

### Testing
- `test_main.py` contains example usage and testing patterns
- Uses pandas for data processing and datetime manipulation
- Demonstrates error handling for OutOfBoundsDatetime exceptions