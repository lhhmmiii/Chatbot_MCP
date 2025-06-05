
file_classification_template = """
Bạn là một trợ lý thông minh. Nhiệm vụ của bạn là phân loại một file vào một trong hai nhóm sau:
- Học tập: Bao gồm các file liên quan đến việc học, nghiên cứu, tài liệu giảng dạy, bài giảng, sách giáo khoa, bài tập, đề thi, luận văn, hoặc các nội dung dùng cho mục đích học tập.
- Không phải học tập: Bao gồm mọi file không phục vụ cho mục đích học tập như giải trí, cá nhân, công việc không liên quan đến học tập, ảnh chụp, hóa đơn, hợp đồng, v.v.

Dưới đây là thông tin về file:
- Nội dung file:
{file_content}

Hãy phân loại file này và trả lời duy nhất bằng một trong hai từ: "Học tập" hoặc "Không phải học tập".
Chỉ đưa ra kết quả phân loại, không đưa ra bất kỳ lời giải thích nào.
"""
