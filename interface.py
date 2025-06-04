import gradio as gr
from filesystem_agent import run_agent
from services.chat_history_service import ChatHistoryService
from utils.rlhf_feedback import apply_rlhf_feedback
from utils.create_metadata import create_metadata, save_metadata_to_xlsx


def send_metadata_to_mcp(metadata):
    pass

def generate_chain_of_thought():
    pass


with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 📂 Chat AI tìm kiếm và phân loại file
    Ứng dụng AI chạy local LLM tích hợp MCP (Model Context Protocol)
    """)

    user_id = gr.State("1323")

    with gr.Row():
        chatbot = gr.Chatbot(label="💬 Chat với AI", height=400, type="messages")
        history = gr.State([])  # Lưu lịch sử chat theo định dạng: [{"role": ..., "content": ...}]

    with gr.Row():
        user_input = gr.Textbox(placeholder="Nhập yêu cầu...", label="Input")
        submit_btn = gr.Button("Gửi")

    with gr.Row():
        rlhf_user_feedback = gr.Textbox(label="✏️ Phản hồi người dùng", placeholder="VD: Nên là Nhóm B")
        send_feedback_btn = gr.Button("Gửi phản hồi RLHF")

    with gr.Row():
        file_results = gr.Textbox(label="📄 Kết quả tìm kiếm & phân loại", lines=6)

    with gr.Row():
        cot_output = gr.Textbox(label="📝 Chain of Thought", lines=4)
        feedback_output = gr.Textbox(label="🔁 RLHF Phản hồi người dùng", lines=2)

    with gr.Row():
        metadata_file_output = gr.File(label="📂 Metadata File")

    # Async submit xử lý
    async def on_submit(user_input, history, user_id):
        # Khởi tạo service quản lý lịch sử chat
        chat_service = ChatHistoryService(user_id=user_id)
        result = await run_agent(user_input, chat_service)
        history.append({"role": "user", "content": user_input})
        history.append({"role": "assistant", "content": result})

        # Create metadata and save to xlsx
        metadata = create_metadata(text=result, file_name="agent_response.txt", label="Agent Response")
        xlsx_file_name = save_metadata_to_xlsx(metadata, "agent_response_metadata.xlsx")

        return history, result, "(CoT sẽ hiển thị ở đây)", "(Phản hồi RLHF sẽ hiển thị ở đây)", xlsx_file_name
    
    # Dùng partial để truyền user_id cố định
    submit_btn.click(
        fn=on_submit,
        inputs=[user_input, history, user_id],
        outputs=[chatbot, file_results, cot_output, feedback_output, metadata_file_output]
    )

    send_feedback_btn.click(
        fn=apply_rlhf_feedback,
        inputs=[rlhf_user_feedback, user_id],
        outputs=feedback_output
    )

if __name__ == "__main__":
    demo.launch()
