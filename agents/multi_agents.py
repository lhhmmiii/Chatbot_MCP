import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from langgraph_supervisor import create_supervisor
from agents.filesystem_agent import create_filesystem_agent
from text_extraction_agent import create_text_extraction_agent
from file_classification_agent import create_file_classification_agent
from metadata_agent import create_metadata_agent
from config.llm import ollama_chat_model
from utils.pretty_print_message import pretty_print_messages
from PIL import Image
import io
import asyncio


async def create_supervisor_agent():
    filesystem_agent = await create_filesystem_agent()
    text_extraction_agent = create_text_extraction_agent()
    file_classification_agent = create_file_classification_agent()
    metadata_agent = create_metadata_agent()
    supervisor = create_supervisor(
        agents=[filesystem_agent, text_extraction_agent, file_classification_agent, metadata_agent],
        model=ollama_chat_model,
        prompt = """
        Bạn đóng vai trò là người điều phối trong một hệ thống gồm nhiều Agent chuyên trách xử lý tài liệu.  
        Nhiệm vụ của bạn là tiếp nhận và phân tích yêu cầu đầu vào (có thể là truy vấn, tệp tin hoặc mô tả nhiệm vụ), sau đó phân công chính xác các Agent phù hợp để thực hiện tác vụ đó.

        Khi tiếp nhận đầu vào, bạn cần thực hiện theo quy trình sau (trừ khi được yêu cầu cụ thể khác):

        1. Nếu đầu vào là truy vấn tìm tài liệu: dùng Filesystem Agent để truy xuất danh sách file phù hợp.
        2. Nếu đã có danh sách file: sử dụng Text Extraction Agent để trích xuất nội dung văn bản.
        3. Sau khi có nội dung: sử dụng File Classification Agent để phân loại tài liệu.
        4. Nếu tài liệu đã được phân loại: sử dụng Metadata Agent để trích xuất thông tin và tổng hợp metadata.

        Lưu ý:
        - Không gọi Metadata Agent nếu chưa phân loại tài liệu.
        - Chỉ gọi Text Extraction nếu đã có file.
        - Chỉ gọi File Classification nếu đã có nội dung.
        """,
        supervisor_name="SupervisorAgent"
    ).compile()
    return supervisor


async def create_graph():
    supervisor = await create_supervisor_agent()
    png_bytes = supervisor.get_graph().draw_mermaid_png()  # giả sử trả về bytes PNG

    # Lưu bytes PNG ra file
    with open("graph.png", "wb") as f:
        f.write(png_bytes)

    # Mở và hiển thị ảnh bằng PIL
    img = Image.open(io.BytesIO(png_bytes))
    img.show()

async def main():
    supervisor = await create_supervisor_agent()
    async for chunk in supervisor.astream(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "Tìm kiếm các file liên quan tới LLM trong thư mục cho phép và xuất metadata vào file excel."
                }
            ]
        }
    ):
        pretty_print_messages(chunk)

if __name__ == "__main__":
    asyncio.run(main())