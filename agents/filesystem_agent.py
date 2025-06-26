import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage
from config.llm import ollama_chat_model, gemini
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
            "D:\\Project\\Chatbot_CNM\\data",
        ],
        "transport": "stdio",
    }
})


async def create_filesystem_agent():
    tools = await client.get_tools()
    file_system_agent_prompt = """
### 🧠 Vai trò:
Bạn là một trợ lý hệ thống tệp thông minh, được cung cấp các công cụ sau:
`read_file`, `read_multiple_files`, `write_file`, `edit_file`, `create_directory`, `list_directory`, `move_file`, `search_files`, `get_file_info`, `list_allowed_directories`.

---

### 🎯 Mục tiêu:
Xử lý yêu cầu của người dùng bằng cách sử dụng **duy nhất các công cụ được cung cấp**, và chỉ truy cập trong **các thư mục được phép**.

---

### 🛠️ Hành vi bắt buộc:
1. **Hiểu rõ mục tiêu của người dùng.**
2. **Chỉ dùng công cụ nếu được yêu cầu rõ ràng.**
3. **Tuyệt đối không suy diễn, không dự đoán nội dung.**
4. Chỉ phản hồi với: tên tệp, nội dung tệp, thông tin metadata, hoặc xác nhận hành động đã thực hiện.

---

### ⚠️ Quy tắc nghiêm ngặt:
- Chỉ dùng `read_file` khi được yêu cầu cụ thể: *"Đọc nội dung tệp A"*.
- Chỉ dùng `write_file` nếu có hướng dẫn rõ: *"Ghi nội dung X vào tệp Y"*.
- Không thay đổi bất kỳ tệp nào nếu không được chỉ định rõ ràng.
- Nếu không chắc đường dẫn, **bắt buộc phải dùng `search_files` trước**.
- Nếu không tìm thấy dữ liệu phù hợp sau khi tìm kiếm, phản hồi: `"Unknown"`.
- **Không được suy đoán** hoặc tạo ra nội dung không có thật từ tệp.

---

Bạn đã sẵn sàng tiếp nhận lệnh.
"""

    agent = create_react_agent(
        model=gemini,
        tools=tools,
        prompt=file_system_agent_prompt,
        name="Filesystem Agent"
    )
    return agent

async def main():
    agent = await create_filesystem_agent()
    response = await agent.ainvoke(
        {"messages": [
            {
                "role": "user", 
                "content": "Tìm kiếm file liên quan đến LLM trong thư mục được phép"
            }
        ]
        },
        config={"recursion_limit": 50}
    )
    for message in response["messages"]:
        print(message.content)

if __name__ == "__main__":
    asyncio.run(main())
    