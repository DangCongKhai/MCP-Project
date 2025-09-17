import asyncio
from typing import Optional

from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import logging

load_dotenv()
GEMINI_API_KEY = os.environ.get("")

logger = logging.getLogger(__name__)


class MCPClient:
    def __init__(self):
        # Initialize session and client objects
        self.session: Optional[ClientSession] = None
        self.model = genai.Client(api_key=GEMINI_API_KEY)
        self.exit_stack = AsyncExitStack()

    async def connnect_to_server(self, server_script_path: str):
        """Connect to MCP server

        Args:
            server_script_path (str): Path to your server
        """

        is_python = server_script_path.endswith(".py")
        is_js = server_script_path.endswith(".js")

        if not is_python and not is_js:
            raise ValueError("Server script must be a .py and .js file")

        command = "python" if is_python else "node"

        server_params = StdioServerParameters(
            command=command, args=[server_script_path]
        )

        stdio_transport = await self.exit_stack.enter_async_context(
            stdio_client(server_params)
        )
        self.stdio, self.write = stdio_transport

        self.session = await self.exit_stack.enter_async_context(
            ClientSession(self.stdio, self.write)
        )
        await self.session.initialize()

        # List available tools
        response = await self.session.list_tools()
        logger.info("Response for tools: ", response)
        tools = response.tools
        logger.info("\nConnected to server with tools:", [tool.name for tool in tools])

    async def process_query(self, query: str) -> str:
        """Process a query

        Args:
            query (str): Query of user

        Returns:
            str: Response from the model
        """

        # messages = [{"role": "user", "content": query}]

        mcp_tools = await self.session.list_tools()
        print("MCP tools: ", mcp_tools.tools)

        available_tools = [
            types.Tool(
                function_declarations=[
                    {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": {
                            k: v
                            for k, v in tool.inputSchema.items()
                            if k not in ["additionalProperties", "$schema"]
                        },
                    }
                ]
            )
            for tool in mcp_tools.tools
        ]

        response = self.model.models.generate_content(
            model="gemini-2.5-flash",
            contents=query,
            config=types.GenerateContentConfig(temperature=0, tools=available_tools),
        )
        print("Model response:")
        print(response)

    async def start_chat_loop(self):
        print("\nMCP Client Started!")
        print("Type your queries or 'quit' to exit.")
        while True:
            try:
                query = input("Please enter your query: ")

                if query.lower() == "exit" or query.lower() == "quit":
                    print("Good bye")
                    break
                await self.process_query(query)
            except Exception as e:
                print(f"\nError: {str(e)}")

    async def cleanup(self):
        await self.exit_stack.aclose()
