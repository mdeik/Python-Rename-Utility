# Python-Rename-Utility

A Python script for renaming files within directories based on user-specified rules.

## Introduction

The `rename_utility.py` script allows you to rename one or more files within a directory by applying various replacement, removal, and addition operations. The utility also supports recursive subdirectory scanning, logging, and dry run modes.

## Features

*   **Replacement**: Replace specific strings in file names with user-specified replacements.
*   **Removal**: Remove sections from file names using start and end indices or negative values for counting from the end of the string.
*   **Addition**: Insert text at specified positions (positive or negative) in file names.
*   **File Extension Consideration**: Optionally include the file extension when applying renaming rules.
*   **Subdirectory Support**: Recursively scan subdirectories and rename files within them if specified.
*   **Logging**: Log renaming actions to a file for auditing purposes.
*   **Dry Run Mode**: Perform a simulation of the renaming process without making any actual changes.

## Usage

To use this utility, simply run `rename_utility.py` from the command line or import it in your Python scripts. The script will guide you through the interactive configuration and execution process.

### Command-Line Usage

```bash
python rename_utility.py [options] directory
```

### Importing in Python Scripts

```python
import rename_utility

# Configure renaming rules and execute the utility
rename_utility.rename(
    directory='/path/to/directory',
    replace=[('old_string', 'new_string')],
    remove=[(5, 10)],
    add=[(-3, 'prefix_')],
    # Other options...
)
```

## Options

The `rename` function accepts the following keyword arguments:

*   `directory`: Path to the directory containing files to be renamed.
*   `replace`: List of tuples with strings to be replaced and their replacements.
*   `remove`: List of tuples specifying sections to remove from file names (start, end) or negative indices for counting from the end.
*   `add`: List of tuples specifying positions (positive or negative) and text to add to file names.
*   `replace_first`: Flag to replace only the first occurrence of each string in `replace`.
*   `check_func`: Function to filter files to be renamed.
*   `extension`: File extension(s) to consider for renaming.
*   `include_extension`: Flag to include the file extension when applying renaming rules.
*   `overwrite`: Flag to overwrite existing files with new names.
*   `inc_subdirs`: Flag to recursively scan subdirectories.
*   `show_output`: Flag to print renaming actions to the console.
*   `log`: Flag to log renaming actions to a file.
*   `log_path`: Path to the log file.
*   `test`: Flag to perform a dry run without making any changes.
