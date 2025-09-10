import asyncio
import os


from mcp import ClientSession, StdioServerParameters,
from mcp.client.stdio import stdio_client
from mcp.types import PromptReference, ResourceTemplateReference


class MCPCLient:
    def __init__(self, name, transport, config):
        self.name = name
        self.transport = transport
        self.config = config
        self.client

    async def initialize_connnection(self, server_script_path):

        if self.transport == 'stdio':
            self.server_params = StdioServerParameters(
                command="python", args=[server_script_path]
            )
        # elif 'http' in self.transport:
        #     self.server_params = 
        
        # Next step: set up connection and store it

    async def chat_loop(self):
        pass
    async def clean_up(self):
        pass
