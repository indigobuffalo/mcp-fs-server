"""
Filesystem MCP Server Launcher

This modules provides a programmatic way to launch the MCP server
"""

import argparse
import logging
from pathlib import Path
from typing import List, Optional

from easy_mcp.model import TransportType

from mcp_fs.server import FileSystemMCP


logger = logging.getLogger(__name__)

# TODO: CONTINUE FROM HERE
