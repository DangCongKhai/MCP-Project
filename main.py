# import streamlit as st

# def main():
#     st.write("hello world. This is my application")


import asyncio
from client import MCPClient


async def main():

    # Initialize client and connect it to the server
    client = MCPClient()
    try:
        await client.connnect_to_server("mcp_server.py")
        
        await client.start_chat_loop()

    except Exception as e:
        print(e)
    finally:
        await client.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
