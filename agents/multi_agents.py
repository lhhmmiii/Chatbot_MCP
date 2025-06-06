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

        Các Agent hiện có trong hệ thống bao gồm:

        - **Filesystem Agent**: Tìm kiếm và truy xuất các tài liệu phù hợp dựa trên truy vấn người dùng.
        - **Text Extraction Agent**: Trích xuất nội dung văn bản từ các tệp PDF, DOCX hoặc PPTX được dẫn ra từ bước tìm kiếm trước.
        - **File Classification Agent**: Phân loại tài liệu dựa trên nội dung đã trích xuất, chia vào các nhóm như hợp đồng, hóa đơn, báo cáo, v.v.
        - **Metadata Agent**: Trích xuất metadata từ tài liệu như tên tác giả, ngày tạo, từ khóa, v.v., và tổng hợp thành một file Excel. Agent này chỉ được sử dụng sau khi tài liệu đã được phân loại.

        Hãy đọc kỹ đầu vào và lựa chọn Agent (hoặc tổ hợp Agent) phù hợp để xử lý hiệu quả.  
        Tránh sử dụng các Agent không cần thiết nhằm tối ưu hiệu suất và tài nguyên hệ thống.
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