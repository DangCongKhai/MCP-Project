from mcp.server.fastmcp import FastMCP


mcp = FastMCP(name = "mcp_server")



@mcp.tool(description="Get weather tool")
def get_weather(location: str):
    return 20


# Define resource
@mcp.resource(uri="file://{name}.txt")
def get_hello_file(name: str):
    """Get a person name"""
    return f"Hello, {name}"


@mcp.prompt()
def find_weather():
    prompt = "Give me the weather condition in a specified place in the most specific way"

# Set up a server with necessary tool and resourc