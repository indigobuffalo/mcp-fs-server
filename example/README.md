# Example Directory

This directory contains example scripts demonstrating how to interact with the MCP File System Agent.

## Prerequisites

- Use the `uv` virtual environment located at the project root for Python dependency management.
- Source that environnment with:
  ```sh
  source .venv/bin/activate 
  ```

## Usage

### 1. Start the Server

Before running the SSE example, start the server with the SSE transport type:

```sh
python main.py --allowed-dirs /tmp --transport sse
```

### 2. Run Examples

- `sse_example.py`: Demonstrates using Server-Sent Events (SSE) to communicate with the server. **Requires the server to be running with SSE transport.**

```sh
python example/sse_example.py
``` 

- `stdio_example.py`: Demonstrates using standard input/output for communication.

```sh
python example/stdio_example.py
```
