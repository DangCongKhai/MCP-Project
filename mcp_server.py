from mcp.server.fastmcp import FastMCP

import sys
import logging
import asyncio
from dotenv import load_dotenv
import os
import httpx
from typing_extensions import Dict
load_dotenv()

OPEN_WEATHER_API_KEY = os.environ.get("OPEN_WEATHER_API_KEY")
BASE_OPEN_WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
mcp = FastMCP(name="mcp_server")

@mcp.tool(description="Get weather tool")
async def get_weather(location: str) -> Dict[str, any]:
    """Get the weather condition at a given location

    Args:
        location (str): Location in the user query
    """
    
    url = BASE_OPEN_WEATHER_URL + f"?q={location}"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
            
            if response.status_code == 200:
                # Get response
                result = response.json()
                weather_info = result['weather']
                return {
                    "weather_condition" : weather_info['main'],
                    "description" : weather_info['description']
                }
            else:
                return {}
        except httpx.HTTPStatusError as exc:
            print(f"Error response {exc.response.status_code} while making request")
            return {}
        except Exception as e:
            print(F"An exception occurs while getting weather at given location")
            return {}
            
            
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    mcp.run(transport='sse')