import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage
from config.llm import ollama_chat_model
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph_swarm import create_handoff_tool
import asyncio

# Thiết lập server MCP để lấy file tools
client = MultiServerMCPClient({
    "document_search": {
        "command": "cmd",
        "args": [
            "/c",
            "npx",
            "-y",
            "@modelcontextprotocol/server-filesystem",
            "D:/Project/Chatbot_CNM/data",
        ],
        "transport": "stdio",
    }
})

async def get_search_files_tool():
    tools = await client.get_tools()
    return [tool for tool in tools if tool.name == "search_files"]

gemini = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key="AIzaSyD87mLar9TxgjIUa_wQdRSvC16aQ97pRhs"
)

async def create_document_search_agent():
    
    tools = await get_search_files_tool()
    prompt = (
        "Bạn là một trợ lý thông minh, chỉ sử dụng công cụ tìm kiếm files để hoàn thành nhiệm vụ. "
        "Khi được hỏi, hãy trả về tên file tìm được liên quan đến yêu cầu. "
        "Nếu không tìm thấy file nào phù hợp, hãy trả lời chính xác: 'Không biết'. "
        "Không được trả lời thêm thông tin gì khác ngoài tên file hoặc câu 'Không biết'."
    )
    # Handoff
    transfer_to_text_extraction_agent = create_handoff_tool(
        agent_name="Text Extraction Agent",
        description="Transfer to Text Extraction Agent"
    )
    tools.append(transfer_to_text_extraction_agent)
    agent = create_react_agent(
        model=ollama_chat_model,
        tools=tools,
        prompt=prompt,
        name="Document Search Agent"
    )
    return agent

if __name__ == "__main__":
    agent = asyncio.run(create_document_search_agent())
    response = agent.invoke(
        {"messages": "Tìm kiếm file có liên quan tới LLM"},
        config = {"recursion_limit": 50}
    )
    for message in response["messages"]:
        print(message.content)
    