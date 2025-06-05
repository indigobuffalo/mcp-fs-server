import logging
from pathlib import Path
from typing import List

from easy_mcp.registration.tools import mcp_tool

from mcp_fs.utils.path_utils import validate_path

logger = logging.getLogger(__name__)


class FileService:
    def __init__(self, allowed_dirs: List[Path]):
        self.allowed_dirs = allowed_dirs

    @mcp_tool
    def file_exists(self, file_path: str) -> bool:
        """
        name: file_exists
        description: >
            Check if a file exists at the specified path.

        Arguments:
            file_path (Path): The path to the file to check.

        Returns:
            bool: True if the file exists, False otherwise.

        Example:
            >>> file_exists("/path/to/file.txt")
            True
        """
        try:
            path_obj = validate_path(file_path, self.allowed_dirs)
            exists = path_obj.exists() and path_obj.is_file()
            logger.debug(f"File exists check for {file_path}: {exists}")
            return exists
        except ValueError as e:
            logger.error(f"Access denied for {file_path}: {e}")
            return False
        except Exception as e:
            logger.error(f"Error checking file existence for {file_path}: {e}")
            return False

    @mcp_tool
    def read_file(self, file_path: str) -> str:
        """
        name: read_file
        description: >
            Read the contents of a file at the specified path.

        Arguments:
            file_path (Path): The path to the file to read.

        Returns:
            str: The contents of the file.

        Raises:
            ValueError: If the file path is not allowed.
            FileNotFoundError: If the file does not exist.

        Example:
            >>> read_file("/path/to/file.txt")
            "File contents here."
        """
        try:
            path_obj = validate_path(file_path, self.allowed_dirs)
            logger.debug(f"Attempting to read file: {file_path}")
            with path_obj.open("r", encoding="utf-8") as file:
                content = file.read()
            return content
        except FileNotFoundError as e:
            logger.error(f"File not found: {file_path}.")
            raise
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {e}")
            raise

    @mcp_tool
    def write_file(self, file_path: str, content: str) -> str:
        """
        name: write_file
        description: >
            Write content to a file at the specified path.

        Arguments:
            file_path (Path): The path to the file to write.
            content (str): The content to write to the file.

        Returns:
            A dictionary with information about the operation:
            - success (bool): True if the write was successful.
            - path (str): Resolved path of the file written to.
            - message (str): A message indicating the result of the operation.
            - bytes_written (int): Number of bytes written to the file.

        Example:
            >>> write_file("/path/to/file.txt", "New content")
            {
                "success": True,
                "path": "/path/to/file.txt",
                "message": "File written successfully.",
                "bytes_written": 123
            }
        """
        try:
            path_obj = validate_path(file_path, self.allowed_dirs)
            logger.debug(f"Attempting to write to file: {file_path}")
            with path_obj.open("w", encoding="utf-8") as file:
                file.write(content)
            return {
                "success": True,
                "path": str(path_obj),
                "message": "File written successfully.",
                "bytes_written": len(content.encode("utf-8")),
            }
        except FileNotFoundError as e:
            logger.error(f"File not found for writing: {file_path}.")
            raise
        except Exception as e:
            logger.error(f"Error writing to file {file_path}: {e}")
            raise

    @mcp_tool
    def append_to_file(self, file_path: str, content: str) -> dict:
        """
        name: append_to_file
        description: >
            Append content to a file at the specified path.

        Arguments:
            file_path (Path): The path to the file to append to.
            content (str): The content to append to the file.

        Returns:
            A dictionary with information about the operation:
            - success (bool): True if the append was successful.
            - path (str): Resolved path of the file appended to.
            - message (str): A message indicating the result of the operation.
            - bytes_appended (int): Number of bytes appended to the file.

        Example:
            >>> append_to_file("/path/to/file.txt", "Additional content")
            {
                "success": True,
                "path": "/path/to/file.txt",
                "message": "Content appended successfully.",
                "bytes_appended": 45
            }
        """
        try:
            path_obj = validate_path(file_path, self.allowed_dirs)
            logger.debug(f"Attempting to append to file: {file_path}")

            if not path_obj.exists():
                logger.warning(f"File {file_path} does not exist. Creating a new file.")
                path_obj.parent.mkdir(parents=True, exist_ok=True)

            with path_obj.open("a", encoding="utf-8") as file:
                bytes_written = file.write(content)
            return {
                "success": True,
                "path": str(path_obj),
                "message": "Content appended successfully.",
                "bytes_appended": bytes_written,
            }
        except Exception as e:
            logger.error(f"Error appending to file {file_path}: {e}")
            raise
