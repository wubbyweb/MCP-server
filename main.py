import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.types import CreateMessageRequestParams, CreateMessageResult, TextContent

async def handle_sampling_message(message: CreateMessageRequestParams) -> CreateMessageResult:
    return CreateMessageResult(
        role="assistant",
        content=TextContent(
            type="text",
            text="Hello from the sampling callback!",
        ),
        model="gpt-3.5-turbo",
        stopReason="endTurn",
    )

async def main():
    # Configure server parameters for local connection
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "mcp.server", "--port", "8080"]
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write, sampling_callback=handle_sampling_message) as session:
            # Initialize the connection
            await session.initialize()

            # List available tools
            tools = await session.list_tools()
            print(f"Available tools: {tools}")

            # Call a tool (assuming 'get_forecast' is available)
            try:
                forecast = await session.call_tool("get_forecast", arguments={"latitude": 40.7128, "longitude": -74.0060})
                print(f"Forecast: {forecast}")
            except Exception as e:
                print(f"Error calling tool: {e}")

            # Read a resource (if available)
            try:
                content, mime_type = await session.read_resource("weather://new-york")
                print(f"Weather resource content: {content}")
                print(f"MIME type: {mime_type}")
            except Exception as e:
                print(f"Error reading resource: {e}")

if __name__ == "__main__":
    asyncio.run(main())
