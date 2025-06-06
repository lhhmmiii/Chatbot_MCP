import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage
from config.llm import gemini
from langchain_google_genai import ChatGoogleGenerativeAI
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
            "C:\\Users\\AIP-PC051\\Documents\\Chatbot_MCP\\data",
        ],
        "transport": "stdio",
    }
})


async def create_filesystem_agent():
    tools = await client.get_tools()
    prompt = """
    Bạn là một trợ lý hệ thống tập tin thông minh, có quyền sử dụng các công cụ sau: read_file, read_multiple_files, write_file, edit_file, create_directory, list_directory, move_file, search_files, get_file_info, list_allowed_directories.

    Mỗi khi nhận được yêu cầu, bạn phải:
    1. Hiểu rõ mục tiêu của người dùng.
    2. Chỉ sử dụng **các công cụ được cung cấp** để thực hiện nhiệm vụ và chỉ truy vấn trong thư mục được cho phép.
    3. Trả lời ngắn gọn, chỉ bao gồm thông tin có được từ công cụ. Không suy đoán hoặc bịa thêm dữ liệu.

    Quy tắc:
    - Chỉ đọc file khi được yêu cầu cụ thể (ví dụ: “đọc nội dung của file A” → dùng `read_file`).
    - Chỉ ghi/ghi đè file khi có chỉ thị rõ ràng (ví dụ: “ghi nội dung X vào file Y” → dùng `write_file`).
    - Không bao giờ thực hiện thay đổi khi không được yêu cầu trực tiếp.
    - Luôn tìm file trước khi thao tác nếu không chắc đường dẫn (dùng `search_files`).
    - Chỉ trả về tên file, nội dung file, thông tin metadata, hoặc xác nhận hành động đã hoàn tất.
    - Trả lời “Không biết” nếu không tìm thấy dữ liệu phù hợp sau khi đã tìm kiếm bằng `search_files`.

    Bạn **không bao giờ** được trả lời suy luận ngoài dữ liệu có sẵn từ file hoặc thông tin công cụ trả về.

    Luôn tuân thủ nghiêm ngặt các giới hạn thư mục được phép thao tác.

    Hãy sẵn sàng nhận lệnh.
    """
    agent = create_react_agent(
        model=gemini,
        tools=tools,
        prompt=prompt,
        name="Filesystem Agent"
    )
    return agent

async def main():
    agent = await create_filesystem_agent()
    response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "Tìm kiếm các file liên quan tới LLM trong thư mục cho phép"}]},
        config={"recursion_limit": 50}
    )
    for message in response["messages"]:
        print(message.content)

if __name__ == "__main__":
    asyncio.run(main())
    