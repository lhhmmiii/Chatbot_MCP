import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.llm import gemini
from config.prompt_template import file_classification_template
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent


@tool
def classify_file_tool(file_content: str) -> str:
    """Phân loại loại hoặc danh mục của một tệp dựa trên tên và nội dung của nó."""
    prompt = PromptTemplate(
        template=file_classification_template,
        input_variables=["file_content"]
    )
    chain = prompt | gemini | StrOutputParser()
    result = chain.invoke({"file_content": file_content})
    return result


def create_file_classification_agent():
    prompt = """
### Vai trò:
Bạn là **một tác tử thông minh**, chuyên phân loại các tệp dựa trên **nội dung văn bản bên trong**.

---

### Hành vi mong muốn:
- Phân tích nội dung tệp và **xác định loại tệp** (ví dụ: hợp đồng, hóa đơn, báo cáo, CV, bài giảng...).
- **Chỉ trả về tên loại tệp**, **không cung cấp bất kỳ lời giải thích, lý do hay nhận xét nào**.

---

### Đầu ra:
> Một chuỗi duy nhất thể hiện **loại tài liệu** đã phân loại (ví dụ: `"Báo cáo tài chính"` hoặc `"CV"`).
"""
    agent = create_react_agent(
        model=gemini,
        tools=[classify_file_tool],
        prompt=prompt,
        name="File Classification Agent"
    )
    return agent

if __name__ == "__main__":
    agent = create_file_classification_agent()
    documnt_content = """
Báo cáo thu chi tháng 5/2025

Tổng thu: 120.000.000 VND

Tổng chi: 85.000.000 VND

Chi lương nhân viên: 50.000.000 VND

Chi phí văn phòng phẩm: 5.000.000 VND

Chi marketing: 10.000.000 VND

Chi khác: 20.000.000 VND

Lợi nhuận tạm tính: 35.000.000 VND

Kế toán trưởng: Nguyễn Thị A
Ngày lập báo cáo: 03/06/2025
"""
    result = agent.invoke(
        {
            "messages": f"Classify the file based on content: {documnt_content}"
        },
        # config={"recursion_limit": 50}  
    )
    for message in result["messages"]:
        print(message.content)

