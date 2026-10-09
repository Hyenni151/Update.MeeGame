MEEGAME - THỐNG KÊ GAME HOT TOÀN HỆ THỐNG + TỰ GHI NGÀY THÊM GAME
=================================================================

Game hot sẽ xếp theo tổng số lần người dùng bấm nút “Chơi” trên MeeGame, cộng dồn từ mọi thiết bị/trình duyệt, nhờ cơ sở dữ liệu Supabase. Đây là lượt mở link từ MeeGame, KHÔNG phải lượt truy cập bên trong website game sau khi mở.

CẤU TRÚC ĐƯA LÊN GITHUB
  index.html
  supabase_setup.sql
  .github/workflows/update-game-dates.yml
  scripts/stamp_game_dates.py

PHẦN A — BẬT THỐNG KÊ TOÀN THIẾT BỊ (CẦN LÀM MỘT LẦN)
1. Vào https://supabase.com/ tạo project mới (gói miễn phí đủ cho thống kê cơ bản). Chờ project khởi tạo xong.
2. Mở SQL Editor trong project, tạo New query, sao chép toàn bộ nội dung file supabase_setup.sql vào và bấm Run.
3. Vào Project Settings > API (hoặc Connect/API Keys tùy giao diện Supabase). Sao chép Project URL và anon/public key (publishable key nếu dự án hiển thị tên mới). KHÔNG dùng service_role/secret key trong website.
4. Mở index.html, tìm hai dòng:
   const SUPABASE_URL = 'PASTE_SUPABASE_PROJECT_URL_HERE';
   const SUPABASE_ANON_KEY = 'PASTE_SUPABASE_ANON_KEY_HERE';
   Thay nội dung bên trong dấu nháy bằng Project URL và anon/publishable key của chính bạn.
5. Đưa index.html, supabase_setup.sql cùng các thư mục .github và scripts lên repository GitHub Pages, commit/push.
6. Mở trang web, bấm nút Chơi ở một số game. Trong Supabase > Table Editor > game_play_stats sẽ thấy lượt chơi được cộng. Thử mở web bằng điện thoại/trình duyệt khác: các thiết bị cùng đọc một bảng số liệu.

CÁCH TÍNH
- Mỗi lần bấm nút “Chơi” trên MeeGame sẽ cộng 1 lượt cho URL game tương ứng.
- Tab “Game hot” xếp giảm dần theo lượt bấm được ghi nhận toàn hệ thống; số liệu hiển thị trên từng thẻ cũng là tổng chung.
- Đây không thể đo chính xác lượt truy cập bên trong website bên ngoài. Muốn biết lượt truy cập thật bên trong game thì chủ website game phải cài analytics hoặc cung cấp API.
- Thống kê là bộ đếm lượt bấm, không phải số người dùng duy nhất; người dùng có thể bấm nhiều lần. Một số trình chặn mạng hoặc mất kết nối có thể làm lượt không ghi nhận.
- Khóa anon/public được thiết kế để dùng phía trình duyệt; tuyệt đối không đưa service_role/secret key vào index.html.

PHẦN B — TỰ GHI NGÀY THÊM GAME
1. Trong repository GitHub, giữ đúng cấu trúc index.html, .github/workflows/update-game-dates.yml và scripts/stamp_game_dates.py.
2. Vào Settings > Actions > General > Workflow permissions, chọn Read and write permissions rồi Save.
3. Khi thêm một thẻ article.game-card mới, workflow so sánh URL với commit trước và tự ghi data-added="YYYY-MM-DD" cho game mới. Tab “Game mới (7 ngày)” dùng ngày đó để lọc.

LƯU Ý
- GitHub Pages chỉ phục vụ trang tĩnh; Supabase là dịch vụ ngoài lưu bộ đếm chung.
- Nếu chưa điền thông tin Supabase vào index.html, bộ đếm toàn hệ thống chưa hoạt động và Game hot sẽ nhắc cần cấu hình.
