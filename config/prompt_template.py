
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

filesystem_tool_selector_prompt = """
Bạn có quyền truy cập vào nhiều công cụ để thao tác với tệp và thư mục. Dựa vào yêu cầu từ người dùng, hãy chọn ra một công cụ phù hợp nhất để thực hiện yêu cầu đó.

Danh sách công cụ bạn có thể sử dụng:

- read_file: Đọc toàn bộ nội dung một tệp.
- read_multiple_files: Đọc nhiều tệp cùng lúc.
- write_file: Tạo mới hoặc ghi đè lên một tệp với nội dung cho trước.
- edit_file: Sửa đổi một phần nội dung tệp bằng cách tìm và thay thế (có thể dùng chế độ xem trước - dry run).
- create_directory: Tạo thư mục mới (hoặc đảm bảo thư mục đã tồn tại).
- list_directory: Liệt kê toàn bộ tệp và thư mục bên trong một thư mục.
- move_file: Di chuyển hoặc đổi tên tệp/thư mục.
- search_files: Tìm kiếm đệ quy tệp/thư mục theo mẫu (pattern).
- get_file_info: Lấy thông tin chi tiết về tệp hoặc thư mục.
- list_allowed_directories: Hiển thị danh sách thư mục mà hệ thống cho phép truy cập.

Hướng dẫn:
1. Phân tích yêu cầu từ người dùng.
2. Chọn tên công cụ phù hợp nhất từ danh sách trên.
"""