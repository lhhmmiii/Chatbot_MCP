import gradio as gr
import os
import json
from typing import List, Dict

### ==== CẤU HÌNH ==== ###
FOLDER_PATH = "./data"  # Thư mục chứa file cần tìm
MCP_CLOUD_ENDPOINT = "http://your-mcp-api.com/send_metadata"  # API (tùy chọn)

### ==== CÁC HÀM LOGIC (bạn cần điền vào) ==== ###

def extract_intent_and_keywords(prompt: str) -> Dict:
    """Phân tích intent và trích từ khóa từ prompt người dùng"""
    # TODO: Triển khai LLM local hoặc regex đơn giản
    return {"intent": "tìm_file", "keywords": ["kế hoạch", "2024"]}

def index_files(folder: str) -> List[str]:
    """Tìm và liệt kê các file trong thư mục"""
    # TODO: Duyệt qua thư mục, lọc PDF/DOCX/PPTX
    return ["plan2024.pdf", "marketing2024.pptx"]

def search_files(files: List[str], keywords: List[str]) -> List[str]:
    """Tìm file có chứa từ khóa"""
    # TODO: Đọc nội dung (dùng PyMuPDF, python-docx, pptx), check từ khóa
    return ["plan2024.pdf", "marketing2024.pptx"]

def classify_file(file_path: str) -> str:
    """Phân loại nội dung file"""
    # TODO: Dùng LLM hoặc rule để gán nhãn
    return "Nhóm A" if "plan" in file_path else "Nhóm B"

def send_metadata_to_mcp(filename: str, label: str) -> bool:
    """Gửi metadata tới MCP Cloud (hoặc ghi ra file local nếu offline)"""
    metadata = {"filename": filename, "label": label}
    # TODO: Gửi qua API thật (hoặc lưu ra JSON/txt)
    print(f"🚀 Gửi metadata: {json.dumps(metadata)}")
    return True

### ==== HÀM XỬ LÝ PROMPT ==== ###

def handle_prompt(user_input: str) -> str:
    # Phân tích prompt
    parsed = extract_intent_and_keywords(user_input)
    intent, keywords = parsed["intent"], parsed["keywords"]

    if intent == "tìm_file":
        response = f"🔍 Đang tìm kiếm với từ khóa: {', '.join(keywords)}"
        
        # Index file
        all_files = index_files(FOLDER_PATH)
        
        # Tìm theo từ khóa
        matched_files = search_files(all_files, keywords)
        
        # Phân loại
        results = []
        for f in matched_files:
            label = classify_file(f)
            send_metadata_to_mcp(f, label)
            results.append(f"- {f} → {label}")
        
        if results:
            return (
                f"{response}\n📄 Tìm thấy {len(results)} file:\n" +
                "\n".join(results) +
                "\n✅ Metadata đã được xử lý."
            )
        else:
            return "❗ Không tìm thấy file nào phù hợp."
    else:
        return "⚠️ Tôi chưa hiểu yêu cầu. Vui lòng thử lại."

### ==== GRADIO UI ==== ###

with gr.Blocks() as demo:
    gr.Markdown("## 🤖 AI Tìm kiếm & Phân loại File (Offline)")
    chatbot = gr.Textbox(lines=10, label="Lịch sử Chat", interactive=False)
    user_input = gr.Textbox(placeholder="Nhập yêu cầu...", label="Bạn hỏi")
    send_button = gr.Button("Gửi")

    state = gr.State("")

    def update_chat(message, history):
        reply = handle_prompt(message)
        updated_chat = f"👤 Bạn: {message}\n🤖 AI: {reply}"
        return updated_chat, updated_chat

    send_button.click(fn=update_chat,
                      inputs=[user_input, state],
                      outputs=[chatbot, state])

demo.launch()
