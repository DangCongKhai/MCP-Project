from mcp.server.fastmcp import FastMCP

import sys
import logging

mcp = FastMCP(name="mcp_server")


@mcp.tool(description="Get weather tool")
def get_weather(location: str):
    logging.info("Get weather")
    return 20


# Define resource
@mcp.resource(uri="file://{name}.txt")
def get_info(name: str):
    """Get a person info"""
    logging.info("Get person info")
    return f"Hello, {name}. Here is your resource"


@mcp.prompt()
def find_weather():
    logging.info("Return user prompt")
    prompt = (
        "Give me the weather condition in a specified place in the most specific way"
    )
    return prompt


# # Set up a server with necessary tool and resourc
# if __name__ == "__main__":

#     print("Start server in stdio mode")
#     mcp.run(transport='stdio')
#     print(f"Server is still running")
#     # import asyncio

#     # asyncio.run(mcp.run(transport="sse"))
logging.basicConfig(
    stream=sys.stdout,  # IMPORTANT — use stderr, not stdout
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

# Here are my additional questions that I really want to know more about
# 1. How much should I understand about a particular thing in programing?
# 2. Should we only 
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Starting MCP stdio server (logs → stderr)...")
    mcp.run(transport="stdio")
    # logger.info("Server is still running")
    print('Server is still running', file=sys.stderr)
