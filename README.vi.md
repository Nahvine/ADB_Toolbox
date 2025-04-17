# ADB Toolbox

[![Version](https://img.shields.io/badge/version-1.1-blue.svg)](https://github.com/Nahvine/ADB_Toolbox)
[![English](https://img.shields.io/badge/Language-English-blue.svg)](README.md)
[![Vietnamese](https://img.shields.io/badge/Language-Tiếng%20Việt-green.svg)](README.vi.md)

Công cụ giao diện dòng lệnh để quản lý thiết bị Android thông qua ADB mà không cần ghi nhớ các lệnh phức tạp.

## Tính năng

- 🔍 Kiểm tra thiết bị kết nối
- ⚡ Các lệnh ADB nhanh
- 🔧 Cài đặt hệ thống ẩn
- 🚀 Dọn dẹp & tối ưu hóa
- 📱 Thay đổi DPI & tỷ lệ
- 📦 Quản lý ứng dụng (cài đặt, gỡ cài đặt, sao lưu, khôi phục)
- 📂 Quản lý file & màn hình (đẩy/tải file, duyệt hệ thống file, mirror màn hình)
- 💾 Lệnh tùy chỉnh & sao lưu (thực thi lệnh tùy chỉnh, tạo preset, sao lưu/khôi phục cài đặt)
- ⚡ Phím tắt preset
- 📝 Lịch sử thao tác
- 🔄 Làm mới thiết bị
- ❓ Trợ giúp & khắc phục sự cố

## Cài đặt

1. Đảm bảo đã cài đặt Python 3.6 trở lên
2. Cài đặt các gói cần thiết:
```bash
pip install -r requirements.txt
```
3. Đảm bảo ADB đã được cài đặt và thêm vào PATH hệ thống
4. Chạy chương trình:
```bash
python main.py
```

## Sử dụng

1. Kết nối thiết bị Android qua USB
2. Bật USB debugging trên thiết bị
3. Chọn tính năng từ menu chính để thực hiện các thao tác

## Yêu cầu

- Python 3.6 trở lên
- ADB (Android Debug Bridge)
- USB debugging được bật trên thiết bị Android
- Các gói Python cần thiết (xem requirements.txt)

## Lưu ý

- Một số tính năng yêu cầu quyền root trên thiết bị
- Cẩn thận khi sửa đổi cài đặt hệ thống
- Tất cả các thao tác đều được ghi lại để xem lại sau

## Hỗ trợ

Để được hỗ trợ, vui lòng liên hệ: example@email.com

## 📋 Cài đặt

1. Clone repository:
   ```
   git clone https://github.com/Nahvine/ADB_Toolbox.git
   cd ADB_Toolbox
   ```

2. Cài đặt các gói phụ thuộc:
   ```
   pip install -r requirements.txt
   ```

3. Đảm bảo ADB đã được cài đặt và thêm vào PATH hệ thống.

## 🚀 Sử dụng

1. Kết nối thiết bị Android qua USB và bật USB Debugging.

2. Chạy ứng dụng:
   ```
   python adb_toolbox/main.py
   ```
   
   Trên Windows, bạn có thể sử dụng file batch:
   ```
   start_adb_toolbox.bat
   ```

3. Sử dụng phím mũi tên để điều hướng và Enter để chọn các tùy chọn từ menu.

## 📊 Cấu trúc dự án

```
adb_toolbox/
│
├── main.py                  
├── commands/                
│   ├── device_check.py      
│   ├── system_settings.py   
│   ├── performance_boost.py
│   ├── app_management.py
│   ├── file_management.py
│   └── custom_commands.py
├── utils/                   
│   ├── logger.py            
│   └── ui_helper.py         
├── config/                  
│   └── presets.json         
└── logs/                    
```

## 🔒 Quyền truy cập

Một số tính năng của ADB Toolbox yêu cầu quyền truy cập đặc biệt trên thiết bị Android:

- **Thiết bị đã root**: Một số tính năng như tăng bộ nhớ ảo (swap) yêu cầu quyền root.
- **ADB qua mạng**: Tính năng kết nối không dây yêu cầu bật debug qua mạng.
- **Quyền USB Debugging**: Luôn cần bật chế độ USB debugging và xác nhận kết nối ADB.

## 📝 Lưu ý

- Cẩn thận khi thay đổi cài đặt hệ thống. Một số thay đổi có thể ảnh hưởng đến hoạt động của thiết bị.
- Luôn sao lưu dữ liệu quan trọng trước khi thực hiện các thay đổi lớn.
- Công cụ này không chịu trách nhiệm về bất kỳ thiệt hại nào có thể xảy ra với thiết bị của bạn.

## 🔄 Cập nhật

Kiểm tra repository thường xuyên để cập nhật tính năng mới và sửa lỗi.

## 📜 Giấy phép

Dự án này được phân phối theo giấy phép MIT. Xem file LICENSE để biết thêm chi tiết.

## 👥 Đóng góp

Mọi đóng góp đều được hoan nghênh! Tạo pull request hoặc báo cáo vấn đề nếu bạn gặp lỗi.

---

**Lưu ý**: Công cụ này được tạo ra cho mục đích giáo dục và hỗ trợ người dùng. Vui lòng sử dụng có trách nhiệm. 