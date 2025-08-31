from mcp.server.fastmcp import FastMCP


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


# Set up a server with necessary tool and resourc
if __name__ == "__main__":
    import asyncio

    asyncio.run(mcp.run(transport="sse"))
