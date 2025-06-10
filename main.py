import argparse
import logging
import os
import sys

from dotenv import load_dotenv

from mcp_fs.launcher import start, directory_path_type


load_dotenv()


log_level = getattr(logging, os.getenv("LOG_LEVEL", "INFO").upper(), logging.INFO)
logging.basicConfig(
    level=log_level,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stderr,
)


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments for the File System MCP server."""
    parser = argparse.ArgumentParser(
        description="Provide a File System MCP server with directory and file operations."
    )
    parser.add_argument(
        "--transport",
        type=str.lower,
        help="The transport type for the MCP server (e.g., STDIO, HTTP)",
        default="stdio",
        choices=["sse", "stdio"],
    )
    parser.add_argument(
        "--host",
        type=str,
        help="The host address for the MCP server. Use to override FASTMCP_HOST environment variable.",
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
        metavar="DIR",
    )
    parser.add_argument(
        "--allowed-tools",
        type=str,
        help="Comma-separated list of allowed tools for the MCP server.",
        default=os.getenv("ALLOWED_TOOLS", ""),
    )
    parser.add_argument(
        "--allowed-resources",
        type=str,
        help="Comma-separated list of allowed resources for the MCP server.",
        default=os.getenv("ALLOWED_RESOURCES", ""),
    )
    return parser.parse_args()


def main():
    """Main function to run the File System MCP server."""
    args = parse_arguments()
    allowed_dirs = args.allowed_dirs
    logging.info(f"Allowed directories: {allowed_dirs}")

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


if __name__ == "__main__":
    main()
