import logging
from pathlib import Path
from typing import List

from easy_mcp.registration.tools import mcp_tool

from mcp_fs.utils.path_utils import validate_path


logger = logging.getLogger(__name__)


class DirectoryService:
    def __init__(self, allowed_dirs: List[Path]):
        self.allowed_dirs = allowed_dirs

    @mcp_tool
    def list_directory(self, dir_path: Path) -> List[str]:
        """
        name: list_directory
        description: >
            List the contents of a directory.

        Arguments:
            dir_path (Path): The path to the directory to list.

        Returns:
            List[str]: A list of file and directory names in the specified directory.

        Example:
            >>> list_directory("/path/to/directory")
            ['file1.txt', 'file2.txt', 'subdir']
        """
        if isinstance(dir_path, str):
            dir_path = Path(dir_path)

        validated_path = validate_path(dir_path, self.allowed_dirs)

        if not validated_path.exists() or not validated_path.is_dir():
            raise ValueError(f"Path {validated_path} is not a valid directory.")

        return [str(item.name) for item in validated_path.iterdir()]

    @mcp_tool
    def create_directory(self, dir_path: Path) -> str:
        """
        name: create_directory
        description: >
            Create a new directory at the specified path.
            This will create any necessary parent directories as well.

        Arguments:
            dir_path (Path): The path to the directory to create.

        Returns:
            str: The path of the created directory.

        Example:
            >>> create_directory("/path/to/new_directory")
            '/path/to/new_directory'
        """
        if isinstance(dir_path, str):
            dir_path = Path(dir_path)

        validated_path = validate_path(dir_path, self.allowed_dirs)

        if validated_path.exists() and validated_path.is_dir():
            logger.info
            return f"Directory {validated_path} already exists."

        validated_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"Directory {validated_path} created successfully.")
        return str(validated_path)
