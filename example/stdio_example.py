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
    stream=sys.stederr,
)


def initialize_llm_client() -> None:
    logger.info("Initializing LLM client...")
    api_key = os.getenv("OPENAI_API_KEY")
    api_version = os.getenv("OPENAI_API_VERSION")
    endpoint = os.getenv("OPENAI_API_ENDPOINT")
    deployment = os.getenv("OPENAI_API_DEPLOYMENT")

    if not all([api_key, api_version, endpoint, deployment]):
        logger.error(
            "Missing OpenAI API configuration. Please set OPENAI_API_KEY, OPENAI_API_VERSION, OPENAI_API_ENDPOINT, and OPENAI_API_DEPLOYMENT environment variables."
        )
        sys.exit(1)

    # TODO: CONTINUE FROM HERE
    # llm_client = AsyncAzureOpenAI(
    # api_key=api_key,
    # api_version=api_version,
    # azure_endpoint=endpoint,
    # azure_deployment_name=deployment,
    # )
