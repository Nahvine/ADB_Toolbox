# ADB Toolbox

![ADB Toolbox Logo](https://i.imgur.com/placeholder-for-logo.png)

## 📱 Tổng Quan

ADB Toolbox là một công cụ dòng lệnh (CLI) giúp người dùng điều khiển thiết bị Android thông qua ADB (Android Debug Bridge) mà không cần nhớ các lệnh phức tạp. Phần mềm cung cấp giao diện thân thiện và dễ sử dụng với các menu tương tác.

## ✨ Tính Năng Chính

- 🔍 **Kiểm tra thiết bị kết nối**: Hiển thị danh sách thiết bị Android đang kết nối
- 🚀 **Các lệnh ADB nhanh**: Thực hiện nhanh các lệnh như reboot, recovery, logcat
- ⚙️ **Tùy chỉnh hệ thống ẩn**: Điều chỉnh các cài đặt system, secure, global
- 🧹 **Dọn rác & Tăng tốc**: Xóa cache ứng dụng, đóng ứng dụng nền, tối ưu hiệu suất
- 📊 **Thay đổi DPI & Scale**: Điều chỉnh mật độ màn hình và tỷ lệ phông chữ
- ⏱️ **Shortcut cấu hình sẵn**: Chạy chuỗi lệnh từ file cấu hình JSON
- 📝 **Ghi log & lịch sử**: Lưu lại các thao tác đã thực hiện trong file log

## 🔧 Yêu Cầu Hệ Thống

- Python 3.6 trở lên
- Đã cài đặt ADB (Android Debug Bridge)
- Các thư viện Python: rich, questionary

## 📋 Cài Đặt

1. Clone repository này:
   ```
   git clone https://github.com/yourusername/adb-toolbox.git
   cd adb-toolbox
   ```

2. Cài đặt các thư viện phụ thuộc:
   ```
   pip install -r requirements.txt
   ```

3. Đảm bảo ADB đã được cài đặt và có trong PATH hệ thống.

## 🚀 Sử Dụng

1. Kết nối thiết bị Android của bạn qua USB và bật chế độ Gỡ lỗi USB (USB Debugging).

2. Chạy ứng dụng:
   ```
   python adb_toolbox/main.py
   ```

3. Sử dụng các phím mũi tên để điều hướng và Enter để chọn tùy chọn từ menu.

## 📊 Cấu Trúc Dự Án

```
adb_toolbox/
│
├── main.py                  # Điểm khởi chạy
├── commands/                # Các module lệnh
│   ├── device_check.py      # Kiểm tra thiết bị
│   ├── system_settings.py   # Cài đặt hệ thống
│   └── performance_boost.py # Tăng hiệu suất
├── utils/                   # Các tiện ích
│   ├── logger.py            # Module ghi log
│   └── ui_helper.py         # Hỗ trợ giao diện
├── config/                  # Cấu hình
│   └── presets.json         # Cấu hình có sẵn
└── logs/                    # Thư mục chứa file log
```

## 🔒 Quyền Hạn

Một số tính năng của ADB Toolbox yêu cầu quyền truy cập đặc biệt trên thiết bị Android:

- **Thiết bị đã root**: Một số tính năng như tăng bộ nhớ ảo (swap) yêu cầu quyền root.
- **ADB qua mạng**: Tính năng kết nối không dây cần bật chế độ gỡ lỗi qua mạng.
- **Cấp quyền USB Debugging**: Luôn cần bật chế độ gỡ lỗi USB và xác nhận kết nối ADB.

## 📝 Lưu Ý

- Hãy cẩn thận khi thay đổi các cài đặt hệ thống. Một số thay đổi có thể ảnh hưởng đến hoạt động của thiết bị.
- Luôn sao lưu dữ liệu quan trọng trước khi thực hiện các thay đổi lớn.
- Công cụ này không chịu trách nhiệm cho bất kỳ thiệt hại nào có thể xảy ra với thiết bị của bạn.

## 🔄 Cập Nhật

Kiểm tra repository thường xuyên để cập nhật các tính năng mới và sửa lỗi.

## 📜 Giấy Phép

Dự án này được phân phối dưới giấy phép MIT. Xem file LICENSE để biết thêm chi tiết.

## 👥 Đóng Góp

Mọi đóng góp đều được hoan nghênh! Hãy tạo một pull request hoặc báo cáo issues nếu bạn gặp vấn đề.

---

**Lưu ý**: Công cụ này được tạo ra nhằm mục đích giáo dục và hỗ trợ người dùng. Vui lòng sử dụng có trách nhiệm. 