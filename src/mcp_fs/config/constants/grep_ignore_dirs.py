from typing import List


GREP_IGNORE_DIRS: List[str] = [
    # VCS directories
    ".git",
    ".svn",
    ".hg",
    ".bzr",
    # Dependency Management
    "node_modules",
    "vendor",
    "bower_components",
    "packages",
    # Build Directories
    "build",
    "dist",
    "out",
    "target",
    "coverage",
    "logs",
    "bin",
    "*.log",
    # IDE and Editor Directories
    ".idea",
    ".vscode",
    ".vscode-test",
    ".vscode-*",
    ".settings",
    # OS and Hidden Directories
    ".DS_Store",
    ".Trash",
    ".cache",
    ".local",
    "*.tmp",
    "*.swp",
    "*.swo",
    "*.bak",
    # Python Specific
    "__pycache__",
    "*.pyc",
    "*.pyo",
    ".pytest_cache",
    ".mypy_cache",
    ".tox",
    ".coverage",
    ".eggs",
    ".ipynb_checkpoints",
    # Java Specific
    "target",
    "out",
    "*.class",
    "*.jar",
    "*.war",
    "*.ear",
    # Ruby Specific
    ".bundle",
    "log",
    "tmp",
    "vendor",
    # Go Specific
    "vendor",
]
