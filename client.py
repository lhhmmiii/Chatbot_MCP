import os
import warnings
warnings.filterwarnings("ignore", category=ResourceWarning)
import mcp
from mcp.client.stdio import stdio_client
from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import asyncio
from config.prompt_template import file_agent_template
from config.llm import ollama_chat_model

## Connect to the server
server_params = mcp.StdioServerParameters(
    command="cmd",  # Executable
    args = [
        "/c",
        "npx",
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "D:/Project/Chatbot_CNM/data",
      ],
)



async def run_agent():
    # Connect to the server using stdio client
    async with stdio_client(server_params) as (read, write):
        async with mcp.ClientSession(read, write) as session:
            # List available tools
            tools = await load_mcp_tools(session)
            # Create and run the agent
            prompt = PromptTemplate(template = file_agent_template, output_parser = StrOutputParser())
            agent = create_react_agent(model = ollama_chat_model, tools = tools, prompt = prompt)
            agent_response = await agent.ainvoke(
                {"messages": "Search for the files related to 'abandon'"},
                config={"recursion_limit": 50}
            )
            return agent_response["messages"][-1].content


# if __name__ == "__main__":
#     response = asyncio.run(run_agent())
#     print(response)
#     print("--------------------------------")
