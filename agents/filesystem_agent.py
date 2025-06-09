import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from config.llm import gemini
from config.prompt import filesystem_agent_prompt
from agents.base import BaseAgent
from schemas.agent_schema import ResponseFormat
from langgraph.checkpoint.memory import MemorySaver
import asyncio
from utils.get_agent_response import get_agent_response
from typing import Any, AsyncIterable, Dict
from langchain_core.messages import AIMessage

# Thiết lập server MCP để lấy file tools
client = MultiServerMCPClient({
    "document_search": {
        "command": "cmd",
        "args": [
            "/c",
            "npx",
            "-y",
            "@modelcontextprotocol/server-filesystem",
            "C:\\Users\\AIP-PC051\\Documents\\Chatbot_MCP\\data",
        ],
        "transport": "stdio",
    }
})

# MemorySaver
memory = MemorySaver()


class FilesystemAgent:
    def __init__(self, graph):
        self.graph = graph

    @classmethod
    async def create(cls):
        tools = await client.get_tools()
        graph = create_react_agent(
            model=gemini,
            tools=tools,
            prompt=filesystem_agent_prompt,
            name="Filesystem Agent",
            response_format=ResponseFormat,
            checkpointer=memory,
        )
        return cls(graph)
    
    async def run(self, query: str, session_id: str = "default"):
        config = {"recursion_limit": 50, "configurable": {"thread_id": session_id}}
        response = await self.graph.ainvoke(
            {"messages": [{"role": "user", "content": query}]},
            config=config
        )
        return get_agent_response(self.graph, response['messages'][-1], config)
        
    
    async def stream(
            self, query, sessionId, task_id
        ) -> AsyncIterable[Dict[str, Any]]:
            inputs = {'messages': [('user', query)]}
            config = {'configurable': {'thread_id': sessionId}, 'recursion_limit': 50}


            for item in self.graph.stream(inputs, config, stream_mode='values'):
                message = item['messages'][-1]
                if isinstance(message, AIMessage):
                    yield {
                        'response_type': 'text',
                        'is_task_complete': False,
                        'require_user_input': False,
                        'content': message.content,
                    }
            yield get_agent_response(self.graph, message, config)
    
    
async def main():
    agent = await FilesystemAgent.create()
    result = await agent.run("Tìm kiếm các file liên quan tới LLM trong thư mục cho phép", session_id="123")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())