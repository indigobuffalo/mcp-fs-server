"""
Server module.
"""

import logging
from typing import List, Optional
from pathlib import Path
from venv import logger

from easy_mcp.server import BaseMCPServer
from easy_mcp.model import TransportType

from mcp_fs.tools.directory_tools import DirectoryService
from mcp_fs.tools.file_tools import FileService
from mcp_fs.tools.search_tools import SearchService
from mcp_fs.resources import sample_resource 


logger = logging.getLogger(__name__)


class FileSystemMCP(BaseMCPServer):
    """
    File System MCP Server.

    This server provides tools for file and directory operations, including searching files,
    reading files, and listing directories.
    """

    def __init__(
        self,
        allowed_dirs: List[str | Path],
        name: Optional[str] = "FileSystemMCP",
        transport: TransportType = TransportType.STDIO,
        host: Optional[str] = None,
        port: Optional[int] = None,
        allowed_tools: Optional[List[str]] = None,
        allowed_resources: Optional[List[str]] = None,
    ):
        super().__init__(
            name=name,
            transport=transport,
            host=host,
            port=port,
            allowed_tools=allowed_tools,
            allowed_resources=allowed_resources,
        )

        self.allowed_dirs = [
            Path(dir_path) if isinstance(dir_path, str) else dir_path
            for dir_path in allowed_dirs
        ]

        logger.info(f"FileSystemMCP initialized with allowed directories: {self.allowed_dirs}")

        directory_service = DirectoryService(self.allowed_dirs)
        file_service = FileService(self.allowed_dirs)
        search_service = SearchService(self.allowed_dirs)

        self._register_tools(
            class_instances=[directory_service, file_service, search_service]
        )
        self._register_resources(modules=[sample_resource])