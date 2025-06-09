import asyncio
import logging
import os
import sys
from typing import List

from agents import set_default_openai_client, Agent, Runner
from agents.mcp import MCPServer, MCPServerStdio
from dotenv import load_dotenv
from openai import AsyncAzureOpenAI, AsyncOpenAI

from prompt import AGENT_INSTRUCTIONS, AGENT_NAME, DEFAULT_PROMPT

load_dotenv()


logger = logging.getLogger(__name__)
log_level = getattr(logging, os.getenv("LOG_LEVEL", "INFO").upper(), logging.INFO)
logging.basicConfig(
    level=log_level,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stderr,
)


def initialize_llm_client() -> None:
    logger.info("Initializing LLM client...")
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        logger.error(
            "Missing OpenAI API configuration. Please set OPENAI_API_KEY environment variable."
        )
        sys.exit(1)

    llm_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    set_default_openai_client(llm_client)
    logger.info("LLM client initialized successfully.")


async def run_agent(query: str, mcp_servers: List[MCPServer]) -> None:
    logger.info("Running agent...")
    agent = Agent(
        name=AGENT_NAME,
        instructions=AGENT_INSTRUCTIONS,
        mcp_servers=mcp_servers,
    )

    logger.info(f"Processing query: {query}")
    result = await Runner.run(starting_agent=agent, input=query)
    logger.info("=== Agent Result ===")
    logger.info(result.final_output)


async def main() -> None:
    logger.info("Starting main execution...")
    initialize_llm_client()

    allowed_dirs = ["/tmp"]
    allowed_tools = os.getenv("ALLOWED_TOOLS", "")
    allowed_resources = os.getenv("ALLOWED_RESOURCES", "")

    logger.info(f"Allowed directories: {allowed_dirs}")
    logger.info(f"Allowed tools: {allowed_tools}")
    logger.info(f"Allowed resources: {allowed_resources}")

    cmd_args = [
        "run",
        "python",
        "-m",
        "mcp_fs.launcher",
        "--allowed-dirs",
        *allowed_dirs,
    ]

    if allowed_tools:
        cmd_args.extend(["--allowed-tools", allowed_tools])
    if allowed_resources:
        cmd_args.extend(["--allowed-resources", allowed_resources])

    async with MCPServerStdio(
        name="FileSystemMCP",
        params={
            "command": "uv",
            "args": cmd_args,
        },
    ) as server:
        logger.info("MCP Server started successfully.")
        await run_agent(DEFAULT_PROMPT, [server])


if __name__ == "__main__":
    asyncio.run(main())
