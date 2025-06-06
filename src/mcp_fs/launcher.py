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


def directory_path_type(path_str: str) -> Path:
    try:
        path = Path(path_str).expanduser()
        return path
    except Exception as e:
        raise argparse.ArgumentTypeError(f"Invalid directory path: {path_str}. Error: {e}")


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Launch the File System MCP Server")
    parser.add_argument(
        "--transport",
        type=TransportType,
        help="The transport type for the MCP server (e.g., STDIO, HTTP)",
        default=TransportType.STDIO,
        choices=[t for t in TransportType],
    )
    parser.add_argument(
        "--host",
        type=str,
        help="The host address for the MCP server.  Use to override FASTMCP_HOST environment variable.",
        required=False,
    )
    parser.add_argument(
        "--port",
        type=int,
        help="The port for the MCP server. Use to override FASTMCP_PORT environment variable.",
        required=False,
    )
    parser.add_argument(
        "--allowed-dirs",
        type=directory_path_type,
        nargs="+",
        required=True,
        help="List of allowed directories for the MCP server to access.",
    )
    parser.add_argument(
        "--allowed-tools",
        type=str,
        help="Comma-separated list of allowed tools for the MCP server.",
        default=""
    )
    parser.add_argument(
        "--allowed-resources",
        type=str,
        help="Comma-separated list of allowed resources for the MCP server.",
        default=""
    )
    return parser.parse_args()

def start(
    allowed_dirs: List[Path],
    transport: TransportType = TransportType.STDIO,
    host: Optional[str] = None,
    port: Optional[int] = None,
    allowed_tools: Optional[List[str]] = None,
    allowed_resources: Optional[List[str]] = None,
):
    """
    Start the File System MCP Server with the specified parameters.
    """
    logger.info("Starting File System MCP Server...")
    logger.info(f"Allowed directories: {allowed_dirs}")
    
    mcp_server = FileSystemMCP(
    allowed_dirs=allowed_dirs,
    transport=TransportType(transport.lower()),
    host=host,
    port=port,
    allowed_tools=allowed_tools,
    allowed_resources=allowed_resources,
    )

    mcp_server.start()


# Enable module to be run directly with `python -m mcp_fs.launcher`
# or `python src/mcp_fs/launcher.py`
if __name__ == "__main__":
    args = parse_arguments()
    
    allowed_dirs = [Path(dir_path) for dir_path in args.allowed_dirs]
    
    allowed_tools = (
        [t.strip() for t in args.allowed_tools.split(",")] 
        if args.allowed_tools 
        else None
    )
    
    allowed_resources = (
        [r.strip() for r in args.allowed_resources.split(",")] 
        if args.allowed_resources 
        else None
    )

    start(
        allowed_dirs=allowed_dirs,
        transport=args.transport,
        host=args.host,
        port=args.port,
        allowed_tools=allowed_tools,
        allowed_resources=allowed_resources,
    )