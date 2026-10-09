MEEGAME — TỰ ĐỘNG GHI NGÀY LINK GAME MỚI (TAB 3 NGÀY)

CÁCH HOẠT ĐỘNG
- Tab “Game mới (3 ngày)” hiển thị các game có data-added nằm trong 3 ngày gần nhất.
- Khi bạn thêm một thẻ game mới vào index.html và commit/push lên GitHub, GitHub Actions so sánh URL với phiên bản index.html trước đó.
- URL mới hoặc URL thay đổi sẽ được tự động gắn data-added theo ngày workflow chạy. URL không đổi giữ nguyên ngày.
- Tính năng không tự tìm game mới trên Internet; bạn vẫn cần thêm link game vào index.html.

CÀI ĐẶT
1. Sao lưu index.html hiện tại trên GitHub.
2. Đưa index.html trong gói này vào thư mục gốc repository, thay file cũ.
3. Đưa thư mục .github/workflows/ và scripts/ trong gói này vào thư mục gốc repository, giữ nguyên cấu trúc:
   index.html
   .github/workflows/update-game-dates.yml
   scripts/stamp_game_dates.py
4. Trong GitHub repository, mở Settings → Actions → General → Workflow permissions.
5. Chọn “Read and write permissions” rồi Save.
6. Commit/push các file lên nhánh main hoặc master.
7. Mở tab Actions và kiểm tra workflow “Mark newly added games” chạy thành công.

THÊM GAME VỀ SAU
1. Thêm thẻ game mới vào index.html, bảo đảm thẻ có class="game-card" và link chơi có class="play-btn".
2. Commit/push lên main hoặc master.
3. Workflow sẽ so sánh với bản trước và ghi ngày cho URL mới. Sau khi workflow commit thành công, game sẽ xuất hiện trong tab Game mới (3 ngày) nếu còn trong cửa sổ 3 ngày.

LƯU Ý
- Workflow mặc định theo dõi nhánh main và master. Nếu repository dùng nhánh khác, sửa danh sách branches trong .github/workflows/update-game-dates.yml.
- Nếu URL game cũ được đổi sang URL mới, URL mới được nhận diện là link mới và ghi ngày hiện tại.
- GitHub Actions cần quyền ghi nội dung repository để tự commit ngày.
- Tab Game mới lọc theo data-added trong HTML; game không có ngày hợp lệ sẽ không hiện trong tab này.
