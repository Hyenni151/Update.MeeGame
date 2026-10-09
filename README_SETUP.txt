MEEGAME - TỰ GHI NGÀY THÊM GAME
================================

Cấu trúc cần đưa lên GitHub:
  index.html
  .github/workflows/update-game-dates.yml
  scripts/stamp_game_dates.py

Cách cài đặt:
1. Tải và giải nén gói ZIP.
2. Trong repository GitHub đang dùng cho MeeGame, thay index.html bằng index.html
   trong gói này.
3. Đưa cả thư mục .github/workflows và scripts lên repository, giữ đúng cấu trúc.
4. Vào GitHub repository > Settings > Actions > General > Workflow permissions.
   Chọn "Read and write permissions" rồi Save.
5. Commit/push các file lên nhánh đang dùng để xuất bản GitHub Pages. Nếu không có
   workflow chạy tự động sau commit đầu tiên, vào tab Actions, chọn workflow
   "Stamp dates for newly added MeeGame links" và bấm Run workflow.

Từ lần sau:
- Khi thêm một thẻ <article class="game-card"> mới vào index.html và đặt link
  đích ở nút class="play-btn", workflow so sánh với commit trước.
- Nếu URL chưa từng xuất hiện, workflow tự thêm data-added="YYYY-MM-DD" vào thẻ.
- Tab "Game mới (7 ngày)" dùng ngày này để lọc game mới; sau 7 ngày, game chuyển
  sang tab "Game cũ" theo logic trong index.html.
- Game cũ đã tồn tại mà chưa có data-added vẫn được coi là game cũ; workflow không
  tự đánh dấu toàn bộ game cũ thành mới.
- Nếu bạn tự thêm data-added với ngày cụ thể, script giữ nguyên ngày đó.

Lưu ý:
- Đây là tự động ghi ngày khi có commit thay đổi index.html, không tự đi tìm game
  trên Internet.
- GitHub Actions cần quyền ghi nội dung repository để commit ngày vào index.html.
- Tab Game hot hiện tại vẫn ghi lượt chơi trong localStorage của từng trình duyệt,
  không phải tổng lượt truy cập của tất cả người dùng.
