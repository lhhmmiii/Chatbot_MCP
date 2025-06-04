import os
import warnings
warnings.filterwarnings("ignore", category=ResourceWarning)

import mcp
from mcp.client.stdio import stdio_client

from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage

import asyncio

from config.prompt_template import file_agent_template
from config.llm import ollama_chat_model

# Import ChatHistoryService bạn đã có
from services.chat_history_service import ChatHistoryService  # giả sử file này tên chat_history_service.py

# Thiết lập server MCP để lấy file tools
server_params = mcp.StdioServerParameters(
    command="cmd",
    args=[
        "/c",
        "npx",
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "D:/Project/Chatbot_CNM/data",
    ],
)

async def run_agent(user_input: str, user_id: str = "1323"):
    # Khởi tạo service quản lý lịch sử chat
    chat_service = ChatHistoryService(user_id=user_id)

    # Load lịch sử chat trước (nếu có)
    chat_history = chat_service.get_chat_history()

    # Convert lịch sử hiện có sang list message
    # Nếu lịch sử rỗng, là []
    messages = chat_history if chat_history else []

    # Thêm message user mới
    messages.append(HumanMessage(content=user_input))
    chat_service.add_user_message(HumanMessage(content=user_input))

    async with stdio_client(server_params) as (read, write):
        async with mcp.ClientSession(read, write) as session:
            tools = await load_mcp_tools(session)

            prompt = PromptTemplate(template=file_agent_template, output_parser=StrOutputParser())

            agent = create_react_agent(
                model=ollama_chat_model,
                tools=tools,
                prompt=prompt,
            )

            response = await agent.ainvoke(
                {"messages": messages},
                config={"recursion_limit": 50}
            )

            ai_message_content = response["messages"][-1].content

            # Lưu phản hồi AI vào history
            chat_service.add_ai_message(AIMessage(content=ai_message_content))

            return ai_message_content


if __name__ == "__main__":
    user_question = "Lấy cho tôi file kế hoạch marketing"
    response = asyncio.run(run_agent(user_question))
    print(response)
    print("--------------------------------")
