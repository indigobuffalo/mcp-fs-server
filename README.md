# mcp-fs-server
File System MCP Server

## Requirements

This project uses [uv](https://github.com/astral-sh/uv) for virtual environment and package management. You can install `uv` using Homebrew:

```sh
brew install uv
```

## Setting up the virtual environment

To set up the virtual environment with all development dependencies and extras, run:

```sh
uv sync --dev --all-extras
```

## Example Directory

The `example/` directory contains scripts that demonstrate how to interact with the MCP File System Agent. See `example/README.md` for details on running the examples using both standard input/output and SSE transports.

## Project Structure

The main source code is located in the `src/mcp_fs/` directory. The structure is as follows:

- `main.py` / `src/mcp_fs/launcher.py`: Entry points for starting the server.
- `src/mcp_fs/server.py`: Defines the main `FileSystemMCP` server class and registers tools/resources.
- `src/mcp_fs/tools/`: Contains tool classes for file, directory, and search operations. Add new tools here.
- `src/mcp_fs/resources/`: Contains resource definitions. Add new resources here.
- `src/mcp_fs/config/`: Configuration constants (e.g., ignored directories for search).
- `src/mcp_fs/utils/`: Utility functions (e.g., path validation).

### Contributor Guide

- To add new file or directory operations, implement them as methods in a class in `src/mcp_fs/tools/` and decorate with `@mcp_tool`.
- To add new resources, define them in `src/mcp_fs/resources/` and decorate with `@mcp_resource`.
- Update the server registration in `src/mcp_fs/server.py` if you add new tool or resource modules.
- Use the `example/` directory to add or update usage examples.
