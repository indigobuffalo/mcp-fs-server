import argparse
import asyncio
import logging
import os
import sys
from typing import List

from agents import set_default_openai_client, Agent, Runner
from agents.mcp import MCPServer, MCPServerSse
from dotenv import load_dotenv
from openai import AsyncOpenAI

from prompt import AGENT_INSTRUCTIONS, AGENT_NAME, DEFAULT_PROMPT, LLM_MODEL

load_dotenv()

logger = logging.getLogger(__name__)
log_level = getattr(logging, os.getenv("LOG_LEVEL", "INFO").upper(), logging.INFO)
logging.basicConfig(
    level=log_level,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stderr,
)


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments for the SSE example."""
    parser = argparse.ArgumentParser(description="Run the SSE example with MCP server.")
    parser.add_argument(
        "--host",
        type=str,
        help="The host address for the MCP server. Use to override FASTMCP_HOST environment variable.",
        required=False,
        default="localhost",
    )
    parser.add_argument(
        "--port",
        type=int,
        help="The port for the MCP server. Use to override FASTMCP_PORT environment variable.",
        required=False,
        default=8000,
    )
    return parser.parse_args()


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
        model=LLM_MODEL,
    )

    logger.info(f"Processing query: {query}")
    result = await Runner.run(starting_agent=agent, input=query)
    logger.info("=== Agent Result ===")
    logger.info(result.final_output)


async def main(host: str, port: str) -> None:
    logger.info("Starting main execution...")
    initialize_llm_client()

    async with MCPServerSse(
        name="sse_example",
        params={
            "url": f"http://{host}:{port}/sse",
        },
    ) as server:
        logger.info("MCP server initialized successfully.")
        await run_agent(DEFAULT_PROMPT, [server])


if __name__ == "__main__":
    args = parse_arguments()
    host = args.host
    port = args.port

    logger.info(f"Starting SSE example with host: {host}, port: {port}")

    asyncio.run(main(host, port))
