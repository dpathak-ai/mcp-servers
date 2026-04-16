from dotenv import load_dotenv
import asyncio
from agents import Agent, Runner, agent, result
from agents.mcp import MCPServerStdio

# Load local env vars (API keys, endpoints, etc.) for the Agents/MCP runtime.
load_dotenv(override=True)

# Launch the MCP server as a subprocess via `uv run`.
# This keeps the server in the same virtualenv context as the repo.
params = {"command": "uv", "args": ["run", "mcp_hello.py"]}

async def getTools():
    # `client_session_timeout_seconds` bounds how long the client waits on MCP responses.
    async with MCPServerStdio(
        params=params, client_session_timeout_seconds=30
    ) as hello_server:
        mcp_tools = await hello_server.list_tools()
        print(mcp_tools)


async def run_agent():
     # Keep instructions short and specific—this agent is meant to use the MCP tools
     # exposed by `hello_server` to produce a greeting-style response.
     instruction = """ You are a Greeting Assistance and you greet user using 'hello_server' """
     async with MCPServerStdio(params=params, client_session_timeout_seconds=30) as hello_server:
        agent = Agent(
            name="Hello Agent",
            instructions=instruction,
            model="gpt-4.1-mini",
            mcp_servers=[hello_server],
    )
        # Runner manages the full tool-calling loop until the agent produces a final answer.
        result = await Runner.run(agent,"Hi I'm Deepak! How are you!")
        print(result.final_output)

if __name__ == "__main__":
    # Top-level entrypoint: run the async agent flow from a sync context.
    asyncio.run(run_agent())
