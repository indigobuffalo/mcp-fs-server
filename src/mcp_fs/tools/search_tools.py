import logging
import os
import subprocess
from pathlib import Path
from typing import List
from easy_mcp.registration.tools import mcp_tool

from mcp_fs.utils.path_utils import validate_path, expand_path
from mcp_fs.config.constants.grep_ignore_dirs import GREP_IGNORE_DIRS


logger = logging.getLogger(__name__)


class SearchService:
    """Service for searching files and directories."""

    def __init__(self, allowed_dirs: List[Path]):
        self.allowed_dirs = allowed_dirs

    @mcp_tool
    def find_files_with_substring_in_path(
        self, search_path: Path, substring: str
    ) -> List[str]:
        """
        name: find_files_with_substring_in_path
        description: >
            Search for files in a directory and its subdirectories that contain a specific substring in their names.
        Arguments:
            search_path (Path): The path to the directory where the search will be performed.
            substring (str): The substring to search for in file names.
        Returns:
            List[str]: A list of file paths that match the search criteria.
        Example:
            >>> find_files_with_substring_in_path("/path/to/search", "example")
            ['/path/to/search/example_file.txt', '/path/to/search/subdir/example_file2.txt']
        """
        try:
            validated_search_path = validate_path(search_path, self.allowed_dirs)
            allowed_dirs = [expand_path(dir_path) for dir_path in self.allowed_dirs]

            matching_files = []
            for root, dirs, files in os.walk(validated_search_path):
                # Filter out ignored directories
                dirs[:] = [d for d in dirs if d not in GREP_IGNORE_DIRS]
                path_obj = Path(root)

                if not any(
                    str(path_obj).startswith(str(allowed_dir))
                    for allowed_dir in allowed_dirs
                ):
                    continue

                for file in files:
                    if substring.lower() in file.lower():
                        matching_files.append(os.path.join(root, file))

            return matching_files
        except ValueError as e:
            logger.error(f"Access denied for {search_path}: {e}")
            return []
        except Exception as e:
            logger.error(f"Error searching files in {search_path}: {e}")
            return []

    @mcp_tool
    def search_file_bodies_for_substring(
        self, search_path: Path, text: str
    ) -> List[str]:
        try:
            validated_search_path = validate_path(search_path, self.allowed_dirs)
            allowed_dirs = [expand_path(dir_path) for dir_path in self.allowed_dirs]
            excluded_dirs = [
                item
                for pattern in GREP_IGNORE_DIRS
                for item in ["--exclude-dir", pattern]
            ]

            result = subprocess.run(
                ["grep", "-irl", text, str(validated_search_path)] + excluded_dirs,
                capture_output=True,
                text=True,
            )

            matches_found, no_matches_found = 0, 1
            if result.returncode not in {
                matches_found,
                no_matches_found,
            }:
                raise RuntimeError(
                    f"grep failed with return code {result.returncode}: {result.stderr}"
                )

            matching_files = [line for line in result.stdout.splitlines()]

            # Filter out symbolic links that point outside allowed directories
            matching_files = [
                path
                for path in matching_files
                if any(
                    str(Path(path)).startswith(str(allowed_dir))
                    for allowed_dir in allowed_dirs
                )
            ]

            return matching_files

        except ValueError as e:
            logger.error(f"Access denied for {search_path}: {e}")
            return []
        except Exception as e:
            logger.error(f"Error searching file bodies in {search_path}: {e}")
            return []
