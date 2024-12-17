#!/usr/bin/env python3
"""
codebase2txt.py

This script generates a tree-like representation of your project directory,
excluding files and directories specified in your .gitignore file, the .git folder,
and the script file itself. It also reads the contents of all .py files,
Dockerfiles, and docker-compose files, and writes the directory structure
and file contents to a text file, using ASCII delimiters for clarity.

Usage:
    python generate_structure.py

Dependencies:
    - pathspec (install via `pip install pathspec`)

Outputs:
    - project_structure_and_contents.txt
"""

import os
import sys
from typing import Dict, List
import pathspec

def load_gitignore_spec(gitignore_path: str) -> pathspec.PathSpec:
    """
    Loads the .gitignore file and returns a PathSpec object for matching paths.

    Args:
        gitignore_path: The path to the .gitignore file.

    Returns:
        A PathSpec object containing the ignore patterns.
    """
    with open(gitignore_path, 'r') as gitignore_file:
        gitignore_content = gitignore_file.read()
    spec = pathspec.PathSpec.from_lines('gitwildmatch', gitignore_content.splitlines())
    return spec

def should_include_file(filename: str) -> bool:
    """
    Determines if the file should be included based on its extension or name.

    Args:
        filename: The name of the file.

    Returns:
        True if the file should be included; False otherwise.
    """
    include_extensions = ['.py', '.yml', '.yaml']  # File extensions to include
    include_filenames = ['Dockerfile', 'docker-compose.yml', 'docker-compose.yaml']
    name, ext = os.path.splitext(filename)
    return ext in include_extensions or filename in include_filenames or filename == 'Dockerfile'

def read_file_content(file_path: str) -> str:
    """
    Reads the content of a file.

    Args:
        file_path: The path to the file.

    Returns:
        A string containing the file's content.
    """
    try:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
            content = file.read()
    except Exception as e:
        content = f"<Could not read file due to error: {e}>"
    return content

def print_directory_tree(
    root_path: str,
    spec: pathspec.PathSpec,
    output_lines: List[str],
    prefix: str = '',
    exclude_files: List[str] = None,
    file_contents: Dict[str, str] = None
):
    """
    Recursively builds the directory tree and collects content from specified files.

    Args:
        root_path: The current directory path.
        spec: The PathSpec object for matching ignored paths.
        output_lines: A list to collect lines of the directory tree.
        prefix: The prefix for tree formatting.
        exclude_files: List of filenames to exclude from the tree.
        file_contents: Dictionary to collect file contents.
    """
    if exclude_files is None:
        exclude_files = []
    if file_contents is None:
        file_contents = {}

    items = sorted(os.listdir(root_path))
    # Exclude ignored items, .git directory, and specified exclude files
    items = [
        item for item in items
        if not spec.match_file(os.path.relpath(os.path.join(root_path, item), start=base_dir))
        and item != '.git'
        and item not in exclude_files
    ]
    for index, item in enumerate(items):
        item_path = os.path.join(root_path, item)
        relative_path = os.path.relpath(item_path, start=base_dir)
        is_last = index == (len(items) - 1)
        connector = '└── ' if is_last else '├── '
        output_lines.append(prefix + connector + item)
        if os.path.isdir(item_path):
            extension = '    ' if is_last else '│   '
            # Recursive call for subdirectories
            print_directory_tree(
                item_path,
                spec,
                output_lines,
                prefix + extension,
                exclude_files,
                file_contents
            )
        else:
            # Collect content of specified file types
            if should_include_file(item):
                file_contents[relative_path] = read_file_content(item_path)

def main():
    """Main function to execute the script."""
    try:
        import pathspec
    except ImportError:
        print("This script requires the 'pathspec' module. Install it by running 'pip install pathspec'.")
        sys.exit(1)

    global base_dir
    base_dir = os.getcwd()
    gitignore_path = os.path.join(base_dir, '.gitignore')

    # Get the script filename to exclude it from the output
    script_filename = os.path.basename(__file__)

    # List of files to exclude (script file itself)
    exclude_files = [script_filename]

    if os.path.isfile(gitignore_path):
        spec = load_gitignore_spec(gitignore_path)
    else:
        # If no .gitignore file, create an empty spec
        spec = pathspec.PathSpec.from_lines('gitwildmatch', [])

    # List to hold the lines of the directory tree
    output_lines = []
    # Dictionary to hold file contents
    file_contents = {}

    # Generate the directory tree and collect file contents
    print_directory_tree(
        base_dir,
        spec,
        output_lines,
        exclude_files=exclude_files,
        file_contents=file_contents
    )

    # Write the output to a text file
    output_filepath = os.path.join(base_dir, 'project_structure_and_contents.txt')
    with open(output_filepath, 'w', encoding='utf-8') as output_file:
        # Write the project file structure
        output_file.write("Project File Structure:\n")
        for line in output_lines:
            output_file.write(line + '\n')

        # Write the contents of the files
        output_file.write("\n\n")
        output_file.write("File Contents:\n")
        for relative_path, content in file_contents.items():
            output_file.write("\n\n")
            output_file.write(f"===== Start of {relative_path} =====\n")
            # Write the content with clear delimiters
            output_file.write(content)
            output_file.write(f"\n===== End of {relative_path} =====\n")

    print(f"Project structure and file contents have been written to '{output_filepath}'")

if __name__ == '__main__':
    main()
