import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from langgraph_supervisor import create_supervisor, create_handoff_tool
from agents.filesystem_agent import create_filesystem_agent
from text_extraction_agent import create_text_extraction_agent
from file_classification_agent import create_file_classification_agent
from metadata_agent import create_metadata_agent
from config.llm import gemini
from utils.pretty_print_message import pretty_print_messages
from langgraph.prebuilt.chat_agent_executor import StructuredResponseSchema
from PIL import Image
import io
import asyncio

tfs = [
  create_handoff_tool(agent_name="Filesystem Agent"),
  create_handoff_tool(agent_name="Text Extraction Agent"),
  create_handoff_tool(agent_name="File Classification Agent"),
  create_handoff_tool(agent_name="Metadata Agent")
]


async def create_supervisor_agent():
    filesystem_agent = await create_filesystem_agent()
    text_extraction_agent = create_text_extraction_agent()
    file_classification_agent = create_file_classification_agent()
    metadata_agent = create_metadata_agent()
    supervisor = create_supervisor(
        agents=[filesystem_agent, text_extraction_agent, file_classification_agent, metadata_agent],
        model=gemini,
        tools=tfs,
        prompt = """
### Vai trò:
Bạn là SupervisorAgent - Agent điều phối trung tâm trong hệ thống đa tác nhân xử lý tài liệu.  
Bạn có nhiệm vụ phân tích yêu cầu đầu vào, lên kế hoạch xử lý, và kích hoạt các Agent phù hợp để thực hiện tác vụ một cách hiệu quả, tránh lặp và giảm lãng phí tài nguyên.

---

### Mục tiêu:
Phân tích yêu cầu từ người dùng (truy vấn, mô tả, file...) và **lựa chọn tác tử phù hợp nhất** để thực hiện tác vụ.

Hãy sử dụng **ít tác tử nhất có thể** để tiết kiệm tài nguyên và đạt hiệu quả tối ưu.

---


### Các Agent có sẵn

1. **FilesystemAgent**
   - Chức năng: Tìm kiếm file theo từ khóa, pattern hoặc điều kiện trong thư mục hệ thống.
   - Kết quả trả về: Danh sách đường dẫn file, cùng các metadata cơ bản như: tên tệp, kích thước, thời gian tạo.
   - Ghi chú: Không có khả năng ghi vào Excel.

2. **MetadataAgent**
   - Chức năng: Ghi thông tin metadata vào một tệp Excel.
   - Nhận đầu vào: 
     - `file_name`: Tên tệp
     - `text`: Ghi chú mô tả file
     - `label`: Nhãn phân loại (ví dụ: "llm")
     - `xlsx_file_name`: Tên file Excel (ví dụ: "llm_files_metadata.xlsx")
     - `append`: (mặc định là True để thêm dòng)
     - `folder_dir`: (tuỳ chọn) thư mục để lưu Excel

3. **TextExtractionAgent**
   - Chức năng: Trích xuất nội dung từ file tài liệu như PDF, DOCX, v.v.
   - Không cần sử dụng cho tác vụ hiện tại.

4. **FileClassificationAgent**
   - Chức năng: Phân loại nội dung tài liệu đã trích xuất.
   - Không cần sử dụng cho tác vụ hiện tại.

---

### Các tools:

- `transfer_to_FilesystemAgent`  
  → Tìm kiếm và truy xuất tài liệu phù hợp dựa trên truy vấn.

- `transfer_to_TextExtractionAgent`  
  → Trích xuất nội dung từ các tệp PDF, DOCX, PPTX đã tìm thấy.

- `transfer_to_FileClassificationAgent`  
  → Phân loại tài liệu đã trích xuất (ví dụ: hợp đồng, hóa đơn, báo cáo...).

- `transfer_to_MetadataAgent`  
  → Trích xuất metadata (tên tác giả, ngày tạo, từ khóa...) và lưu vào file Excel.  
  → **Chỉ dùng sau khi phân loại.**

---

## 🧭 Quy tắc ra quyết định (phiên bản đa tác vụ)

SupervisorAgent cần lập kế hoạch toàn diện dựa trên yêu cầu, và có thể điều phối nhiều Agent theo thứ tự phù hợp. Dưới đây là các tình huống phổ biến:

---

### Tình huống 1: Tìm kiếm file liên quan đến LLM và lưu metadata vào Excel
- Gồm 2 bước:
  1. Gọi `FilesystemAgent` để tìm file.
  2. Với mỗi file tìm được, gọi `MetadataAgent` để lưu metadata vào file Excel.

---

### Tình huống 2: Trích xuất nội dung từ tài liệu (PDF, DOCX, v.v.) rồi phân loại
- Gồm 2 bước:
  1. Gọi `TextExtractionAgent` để trích xuất văn bản từ tệp.
  2. Gọi `FileClassificationAgent` để phân loại nội dung văn bản đó.

---

### Tình huống 3: Chỉ muốn trích xuất nội dung
- Gọi `TextExtractionAgent`.

---

### Tình huống 4: Chỉ muốn phân loại nội dung đã có
- Gọi `FileClassificationAgent`.

---

### Tình huống 5: Chỉ lưu metadata (đã có thông tin file và label)
- Gọi `MetadataAgent`.

---

### Tình huống 6: Yêu cầu kết thúc tác vụ hoặc tổng kết
- Thông báo: `"Đã hoàn thành tác vụ."`

---

### Nguyên tắc xử lý

- SupervisorAgent không gọi cùng một Agent lặp lại nhiều lần với đầu vào giống nhau.
- Nếu tác vụ yêu cầu nhiều bước → gọi lần lượt các Agent theo đúng thứ tự workflow.
- Giảm số lượng Agent dùng đến mức tối thiểu để tiết kiệm tài nguyên.

---


Bạn đã sẵn sàng điều phối hệ thống. Hãy chọn đúng công cụ theo yêu cầu của người dùng.
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
                    "content": "Tìm kiếm file liên quan đến LLM trong thư mục được phép và lưu metadata vào một tệp Excel."
                }
            ]
        }
    ):
        pretty_print_messages(chunk)
        # print(chunk)

if __name__ == "__main__":
    asyncio.run(main())