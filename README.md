# codebase-to-txt-for-llms

This Python script, `codebase2txt.py`, generates a tree-like representation of your project's directory structure, excluding files and directories specified in your `.gitignore` file, the `.git` folder, and the script file itself. It reads the contents of all `.py` Python files, `Dockerfile`, and Docker Compose files (`docker-compose.yml`, `docker-compose.yaml`), writing both the directory structure and file contents into a text file. The output is formatted using clear ASCII delimiters, making it suitable for processing by Large Language Models (LLMs).

## Features

- **Exclude Specified Files**: Automatically excludes files and directories listed in your `.gitignore`, the `.git` folder, and the script file itself.
- **Directory Tree Visualization**: Generates a visual tree-like representation of your project's directory structure.
- **File Content Extraction**: Reads and includes the contents of all Python files (`.py`), `Dockerfile`, and Docker Compose files.
- **LLM-Friendly Output**: Formats the output with clear ASCII delimiters for easy parsing by language models.

## Repository

- **GitHub URL**: [https://github.com/Shivank1006/codebase-to-txt-for-llms](https://github.com/Shivank1006/codebase-to-txt-for-llms)

## Requirements

- **Python**: 3.6 or higher
- **Python Packages**:
  - `pathspec` (Install via `pip install pathspec`)

## Installation

1. **Clone or Download the Repository**

   ```bash
   git clone https://github.com/Shivank1006/codebase-to-txt-for-llms.git
   cd codebase-to-txt-for-llms
   ```

2. **Install Dependencies**

   Install the required Python package using pip:

   ```bash
   pip install pathspec
   ```

## Usage

1. **Place the Script**

   Copy the `codebase2txt.py` script into the root directory of the project you want to analyze.

2. **Run the Script**

   Execute the script using Python:

   ```bash
   python codebase2txt.py
   ```

3. **View the Output**

   The script generates a file named `project_structure_and_contents.txt` in your project's root directory. Open this file to view the directory structure and the contents of the included files.

## Output Format

The output file contains:

- **Project File Structure**: A tree-like visualization of your project's directories and files.
- **File Contents**: The contents of each included file, marked with clear delimiters.

### Example

```
Project File Structure:
├── README.md
├── app
│   ├── __init__.py
│   ├── main.py
│   └── utils
│       └── helper.py
└── Dockerfile


File Contents:


===== Start of app/__init__.py =====
# __init__.py content
===== End of app/__init__.py =====


===== Start of app/main.py =====
# main.py content
===== End of app/main.py =====


===== Start of app/utils/helper.py =====
# helper.py content
===== End of app/utils/helper.py =====


===== Start of Dockerfile =====
# Dockerfile content
===== End of Dockerfile =====
```

## Customization

### Include Additional File Types

To include other file types, modify the `should_include_file` function in the script:

```python
def should_include_file(filename: str) -> bool:
    include_extensions = ['.py', '.yml', '.yaml', '.txt']  # Add desired extensions
    include_filenames = ['Dockerfile', 'docker-compose.yml', 'docker-compose.yaml', 'Makefile']
    name, ext = os.path.splitext(filename)
    return ext in include_extensions or filename in include_filenames
```

### Exclude Specific Files or Directories

To exclude additional files or directories, update the `exclude_files` list or modify the exclusion logic in the `print_directory_tree` function:

```python
# Exclude additional files or directories
exclude_files = [script_filename, 'node_modules', '.venv']
```

## Important Considerations

- **Sensitive Information**: Review the `project_structure_and_contents.txt` file before sharing it to ensure no sensitive information (e.g., API keys, passwords) is included.
- **Licensing and Compliance**: Ensure that sharing code content complies with your project's licensing terms and any confidentiality agreements.

## License

This project is licensed under the [MIT License](LICENSE).

## Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the Repository**

   Create a fork of the project on GitHub.

2. **Create a Feature Branch**

   ```bash
   git checkout -b feature/YourFeature
   ```

3. **Commit Your Changes**

   ```bash
   git commit -am 'Add new feature'
   ```

4. **Push to the Branch**

   ```bash
   git push origin feature/YourFeature
   ```

5. **Create a Pull Request**

   Open a pull request on GitHub with a descriptive title and detailed explanation.

## Contact

For questions or suggestions, please open an issue on the [GitHub repository](https://github.com/Shivank1006/codebase-to-txt-for-llms).

---
