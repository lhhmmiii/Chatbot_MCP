import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pandas as pd
from datetime import datetime
from utils import _format_file_timestamp
from langgraph.prebuilt import create_react_agent
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.tools import tool
from config.llm import ollama_chat_model, gemini

@tool
def create_metadata(text: str, file_name: str, label: str):
    """
    Tạo một từ điển metadata cho một tài liệu văn bản.

    Tham số:
        text (str): Nội dung của tài liệu.
        file_name (str): Tên của tệp.
        label (str): Nhãn phân loại tài liệu.

    Trả về:
        dict: Một từ điển chứa metadata như tổng số ký tự, ngày tạo, tên tệp và nhãn.
    """
    metadata = {
        "total_characters": len(text),
        "creation_date": _format_file_timestamp(
            timestamp=datetime.now().timestamp(), include_time=True
        ),
        "file_name": str(file_name),
        "label": label,
    }
    return metadata

@tool
def save_metadata_to_xlsx(metadata: dict, xlsx_file_name: str, folder_dir: str = "Metadata"):
    """
    Lưu metadata vào một tệp Excel (.xlsx).

    Tham số:
        metadata (dict): Từ điển metadata cần lưu.
        xlsx_file_name (str): Tên của tệp Excel để lưu metadata.
        folder_dir (str, optional): Thư mục nơi tệp Excel sẽ được lưu. Mặc định là "Metadata".

    Trả về:
        str: Đường dẫn đến tệp Excel đã lưu.
    """
    df = pd.DataFrame([metadata])
    path = os.path.join(folder_dir, xlsx_file_name)
    df.to_excel(path, index=False, engine='openpyxl')
    return path

def create_metadata_agent():
    """
    Tạo một Agent có thể vừa tạo metadata vừa lưu nó vào một tệp Excel.
    """
    metadata_processing_prompt = """
    Bạn là một tác tử chuyên xử lý metadata cho các tài liệu.

    ### Nhiệm vụ:
    1. Phân tích nội dung tài liệu (`text`), tên tệp (`file_name`) và nhãn (`label`) để tạo metadata cho tài liệu.  
    → Sử dụng công cụ: **[create_metadata]**

    2. Lưu metadata đã tạo vào một tệp Excel `.xlsx` với tên tệp (`xlsx_file_name`) và thư mục lưu (`folder_dir`).  
    → Sử dụng công cụ: **[save_metadata_to_xlsx]**

    ### Đầu ra:
    - Trả về **đường dẫn tuyệt đối** đến tệp Excel chứa metadata.
    - Không đưa ra bất kỳ lời giải thích hoặc mô tả nào khác.

    ### Tham số đầu vào:
    - `text`: Nội dung văn bản của tài liệu.
    - `file_name`: Tên gốc của tệp tài liệu.
    - `label`: Nhãn phân loại tài liệu (ví dụ: "Tài chính", "Học tập", v.v.).
    - `xlsx_file_name`: Tên tệp `.xlsx` muốn lưu metadata.
    - `folder_dir` (tùy chọn): Thư mục để lưu tệp Excel, mặc định là `"Metadata"`.
    """


    agent = create_react_agent(
        tools=[create_metadata, save_metadata_to_xlsx],
        model=gemini,
        prompt=metadata_processing_prompt,
        name="Metadata Agent"
    )
    return agent


if __name__ == "__main__":
    metadata_agent = create_metadata_agent()
    document_content = """
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
    result = metadata_agent.invoke(
        {
            "messages": (
                "Tạo metadata với thông tin sau:\n"
                "- Tên tệp: Báo cáo thu chi tháng 5/2025.xlsx\n"
                "- Label: Báo cáo thu chi\n"
                f"- Text: {document_content}\n\n"
                "Sau đó, lưu metadata vào một tệp có tên: Báo_cáo_thu_chi_tháng_5_2025.xlsx"
            )
        },
        config={"recursion_limit": 50}
    )

    for message in result["messages"]:
        print(message.content)
