# MBS – quy trình edit video sửa điện thoại

Kho lưu lưu ý và code dựng video sửa máy (POV, phong cách MBS Việt Trì) thành dự án CapCut.

- `LUU_Y_EDIT_VIDEO.md`: các quy tắc rút ra từ góp ý của từng video, quy trình đã chạy ổn, lỗi kỹ thuật đã gặp, bộ nhạc / âm thanh hiệu ứng.
- `code_1121/`: code dùng cho video 1121 (Samsung Note 20 xanh màn).
  - `cut1121.py`, `render1121.py`: cắt voice theo lần đọc trơn cuối, xuất từng đoạn.
  - `build_check1121.py`, `mk_draft_util.py`: dựng dự án kiểm tra voice trong CapCut.
  - `sheet.py`, `strip.py`: tờ ảnh và dải ứng viên để chọn cảnh.
  - `b21/plan.py`: danh sách cảnh, vị trí voice. `plan2.py`: chữ động. `plan3.py`: nhạc, SFX, sticker, hiệu ứng.
  - `b21/build.py`: dựng draft CapCut từ khuôn 1118_v2. `b21/preview.py`: dựng MP4 xem trước. `b21/storyboard.py`: storyboard ảnh tĩnh.
  - `mg/engine.html`, `mg/render.mjs`: render chữ "Năng động – mạng xã hội" ra MOV trong suốt (emoji dùng Twemoji SVG).

Cập nhật file lưu ý sau mỗi video được duyệt.
