
file_classification_template = """
Bạn là một trợ lý thông minh. Nhiệm vụ của bạn là phân loại một file vào một trong các nhóm sau:

- **Kinh doanh**: Bao gồm các tài liệu liên quan đến chiến lược kinh doanh, kế hoạch phát triển, tiếp thị, bán hàng, khách hàng, phân tích thị trường, hợp đồng kinh doanh, v.v.
- **Tài chính và Kế toán**: Bao gồm báo cáo tài chính, bảng cân đối kế toán, hóa đơn, biên lai, chi phí, lương thưởng, chứng từ kế toán, phân tích tài chính, v.v.
- **Hành chính nhân sự (HR)**: Bao gồm hồ sơ nhân sự, mô tả công việc, đơn xin nghỉ phép, thông báo nội bộ, quy trình tuyển dụng, đào tạo, quản lý nhân sự, hợp đồng lao động, v.v.
- **Không biết**: Nếu nội dung không đủ rõ để phân loại vào một trong ba nhóm trên.

Dưới đây là thông tin về file:
- Nội dung file:
{file_content}

Chỉ trả lời duy nhất bằng một trong bốn cụm từ sau:  
"Kinh doanh", "Tài chính và Kế toán", "Hành chính nhân sự", hoặc "Không biết".
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