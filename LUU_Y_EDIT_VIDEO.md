# Lưu ý edit video sửa máy MBS (cập nhật sau video 1121)

Video 1121: Samsung Note 20, xanh màn khi máy nóng; vết cháy trên cáp và mạch quanh IC; thay cáp + ép cáp.
Bản dựng: `1121_v1` (3:13), sau đó `1121_v2` (2:50) sửa theo góp ý; v2 đang chờ duyệt.

---

## 1. Góp ý của người dùng ở 1121 → quy tắc cho video sau

| # | Chỗ bị góp ý | Quy tắc |
|---|---|---|
| 1 | Cảnh vặn ốc là lúc đưa tô vít / di chuyển | Cảnh vặn ốc phải thấy **tô vít đang cắm trong ốc và ngón tay đang xoay**. Soát bằng ảnh crop 0,4 s/khung quanh đầu vít trước khi chốt. Tốc độ 1.0. |
| 2 | Cảnh pin lấy cả đoạn nhỏ dung dịch | Bóc pin: **chỉ lấy lúc cạy đến khi pin bật ra hẳn** (~3 s). |
| 3 | Cảnh đưa màn lên kính hiển vi có phần thừa đầu | Cắt vào **đúng lúc thao tác bắt đầu**, bỏ phần đứng chờ phía trước. |
| 4 | Ép cáp dùng cảnh rộng người đứng trước máy | Ép cáp: dùng **khoảnh khắc đầu ép dập xuống**, zoom vào đầu ép. Không dùng cảnh rộng đứng chờ hay cảnh căn chỉnh cáp trên bàn máy. |
| 5 | Cảnh lấy màn ra khỏi máy ép quá dài | Cảnh phụ sau ép **tối đa 3 s**. |
| 6 | Chờ màn sáng ~5 s quá dài | Sau câu "kết quả như thế nào đây" chỉ chờ **~1,5–2 s** là màn sáng. |
| 7 | Đoạn kết có 16 s không voice | Nghỉ giữa các câu kết **1–2 s**. Cắt ngắn cảnh test / lắp máy / khởi động cho vừa lời, không để khoảng trống dài. |
| 8 | Ấn like xuất hiện khi chưa nói xong | Cảnh **giơ ngón cái like đặt SAU khi đọc xong "tận tâm, bền và đẹp"** (~0,3 s sau chữ cuối). |
| 9 | (dặn từ đầu) | Đầu mỗi clip thô thường rung, không lấy. Chỉ lấy cảnh chính có thao tác rõ ràng. |

Cách người dùng giao việc (giữ nguyên format này): chia voice theo từng đoạn kịch bản trong ngoặc, mỗi đoạn kèm mốc cảnh
(vd "(câu…) Từ đầu đến khi bóc màn ra khỏi khung thành công"; "(câu…) lấy cảnh bóc lớp keo đen, mỗi cảnh 2-3s").

Khi góp ý, người dùng ghi thời điểm theo file MP4 xem trước. Luôn dựng dự án tên mới (`<video>_v2`, `_v3`…), giữ nguyên các phần không bị góp ý.

---

## 2. Quy trình đã chạy ổn ở 1121

1. **Quyền thư mục**: `~/Videos`, `com.lveditor.draft`, `Cache/music`. Đọc `draft_content.json` của dự án gốc để biết đường dẫn clip thật.
   - Người dùng nói ổ E nhưng thực tế clip ở `D:\Thư mục mới (2)`. Luôn kiểm tra đường dẫn trong draft.
   - Thư mục ở ổ D **không cấp quyền được** cho phiên. Không sao: xuất bản nháp, voice và chữ động vào `C:\Users\hung\Videos\<video>_edit\`. CapCut vẫn đọc clip gốc từ ổ D.
2. **Lời thoại**: mở dự án gốc → Văn bản → Phụ đề tự động → Tiếng Việt → Tạo → stage lại draft, lấy `materials.texts[].words`.
   - Nhắc người dùng xoá track phụ đề này khỏi dự án gốc sau khi xong.
3. **Bản nháp phân tích**: Ctrl+E → tên `<video>_nhap480`, 480P, tốc độ bit Tùy chỉnh 1000 kbps, thư mục Videos (38 phút ≈ 295 MB, xuất ~6 phút).
   - Bản nháp có in phụ đề, nên file xem trước cũng có chữ mờ. Báo người dùng là dự án CapCut không có.
4. **Cắt voice** (`cut1121.py` + `render1121.py`):
   - Mỗi đoạn lấy **lần đọc trơn cuối cùng làm một khối liền**, giữ nhịp thở tự nhiên (không ghép từng câu với khoảng nghỉ cố định).
   - Khoảng lặng trong khối dài hơn 0,28 s rút còn 0,28 s; tốc độ ×1.10; nghỉ giữa các khối theo dấu câu (0,1–0,3 s); loudnorm −16.
   - Bỏ "ô kê 2 3", câu nói hụt, chữ lặp ("sau khi mà sau khi", "đó là đó là", "và và").
   - Kiểm tra: dựng dự án `<video>_kiemtra_voice_vN` (dựa trên draft gốc của máy) → Phụ đề tự động → đối chiếu kịch bản, không được mất chữ.
   - Lấy luôn thời gian từng chữ của voice đã cắt từ phụ đề này (`vwords.json`) để chữ động bật đúng lúc.
   - Đoạn nào cần đặt câu sau đúng mốc hình (vd "kết quả thế nào đây" / "màn hình đã lên sáng") thì **tách file voice làm 2** (G1/G2, H1/H2).
5. **Chọn cảnh**: proxy 6 fps + `motion.py` (rung camera), tờ ảnh 2–5 s/khung cả video, rồi dải ứng viên 7 khung/cảnh, rồi crop to 0,3–0,5 s/khung cho chỗ khó (đầu vít, đầu máy ép, lúc màn sáng).
6. **Storyboard**: ảnh tĩnh từng cảnh + chữ động + câu voice → gửi người dùng.
7. **Dựng draft** (`build.py`): dùng **draft 1118_v2 làm khuôn** (đã duyệt) cho mọi material: video segment, nhạc, SFX (tra theo tên, giữ nguyên `effect_id`), sticker, hiệu ứng, chuyển cảnh, filter "Thị giác manga" 0.57 phủ cả video.
   - CapCut trên máy đã lên **9.8.0.4213**. Draft dựng từ khuôn 9.7.1 vẫn mở tốt (CapCut tự nâng cấp).
   - Đường dẫn khử nhiễu voice: `Apps/9.8.0.4213/Resources/audiosami/...`.
8. **Xem trước**: `preview.py` dựng MP4 480p trong cloud từ bản nháp + MOV chữ + voice + nhạc/SFX (stage nhạc từ `Cache/music`).
9. **Chép lên máy**: voice → `Videos\<video>_edit\voice_vN`, MOV → `motion_vN` (≤20 MB/file, ≤85 MB/lượt), draft → `com.lveditor.draft\<video>_vN`. Mở thử trong CapCut, tua vài mốc, stage lại draft kiểm tra SFX.

---

## 3. Lỗi kỹ thuật gặp ở 1121

- **Cửa sổ app Claude nằm đè giữa màn hình** che CapCut → nhờ người dùng thu nhỏ cửa sổ Claude.
- Menu CapCut không mở → Esc, bấm vùng trống timeline rồi bấm Menu lại.
- **Emoji không hiện** khi render chữ (Noto Color Emoji không vẽ được trong Chromium headless) → `engine.html` dùng ảnh **Twemoji SVG** (`npm pack @twemoji/svg` → `fonts/twemoji/<mã>.svg`).
- Font Baloo 2 dùng bản **variable** (`@fontsource-variable/baloo-2`) để dấu tiếng Việt đúng.
- MOV slogan dài (9,5 s) nặng 27 MB → nén lại `prores_ks -profile:v 4 -q:v 28` (còn ~21 MB).
- Tên SFX trong draft dài, khi tra theo tên dùng so khớp tiền tố.
- `device_request_folder_access` từ chối thư mục ổ D dù đúng tên → làm việc qua `~/Videos`.

---

## 4. Bộ nhạc & SFX dùng ở 1121 (giống 1118_v2)

- Hook: suspense tích tắc `123fbdef…` (vol 0.10) + drone `c13b20cf…` (0.20)
- Kể chuyện khách: Nostalgic Rain `b40834c2…` (0.24 dưới voice)
- Nghỉ sau đoạn kể: `51b92a8b…` (0.45)
- Vệ sinh / seal: `7b43d50b…` (0.26 dưới voice, 0.5–0.55 khi không voice)
- "Không ổn rồi": drone nhấn (0.30) + Nostalgic Rain đoạn tối (src 30 s)
- Thay cáp: piano nhẹ `ba62b1f3…` (0.14 / 0.45)
- Ép cáp: `c768cf09…` (0.18)
- Chờ màn sáng: suspense tích tắc (0.35 → 0.9)
- Màn sáng → hết: acoustic `24cc86e3…` (0.30 → 0.14 dưới voice → 0.4 sau slogan)
- Voice 1.15. SFX ~20–24 âm, vol 0.2–0.38 (hook to hơn), lấy từ mục Yêu thích.
- Sticker khỉ ở "không ổn rồi"; pháo giấy lúc màn sáng; lấp lánh ở slogan; Nháy trắng hook → voice.
