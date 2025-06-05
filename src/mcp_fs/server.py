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
from mcp_fs.resources.sample_resource import get_user_file


logger = logging.getLogger(__name__)


class FileSystemMCP(BaseMCPServer):
    """
    File System MCP Server.

    This server provides tools for file and directory operations, including searching files,
    reading files, and listing directories.
    """

    # TODO: CONTINUE FROM HERE
