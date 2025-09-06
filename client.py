import asyncio
import os


from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.types import PromptReference, ResourceTemplateReference


server_params = StdioServerParameters(
    command="uv",
    args=["run", "mcp_server.py", "completion", "stdio"],
    env=None,
)


async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize our session
            await session.initialize()

            templates = await session.list_resource_templates()

            print("Available resource template")
            for template in templates.resourceTemplates:
                print(f" - {template.uriTemplate}")

            # List available prompts
            prompts = await session.list_prompts()
            print('prompts')
            for prompt in prompts.prompts:
                print(f"Prompt: {prompt.name}")

                # Complete resource template arguments
            # if templates.resourceTemplates:
            #     template = templates.resourceTemplates[0]
            #     print(
            #         f"\nCompleting arguments for resource template: {template.uriTemplate}"
            #     )

            # # Complete without context
            # result = await session.complete(
            #     ref=ResourceTemplateReference(
            #         type="ref/resource", uri=template.uriTemplate
            #     ),
            #     argument={"name": "owner", "value": "model"},
            # )
            # print(
            #     f"Completions for 'owner' starting with 'model': {result.completion.values}"
            # )

            # # Complete with context - repo suggestions based on owner
            # result = await session.complete(
            #     ref=ResourceTemplateReference(
            #         type="ref/resource", uri=template.uriTemplate
            #     ),
            #     argument={"name": "repo", "value": ""},
            #     context_arguments={"owner": "modelcontextprotocol"},
            # )
            # print(
            #     f"Completions for 'repo' with owner='modelcontextprotocol': {result.completion.values}"
            # )

            # Complete prompt arguments
            # if prompts.prompts:
            #     prompt_name = prompts.prompts[0].name
            #     print(f"\nCompleting arguments for prompt: {prompt_name}")

            #     result = await sessionx.complete(
            #         ref=PromptReference(type="ref/prompt", name=prompt_name),
            #         argument={"name": "style", "value": ""},
            #     )
            #     print(f"Completions for 'style' argument: {result.completion.values}")


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()
