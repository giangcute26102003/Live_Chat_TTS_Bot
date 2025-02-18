# 🎙️ YouTube Live Chat TTS Bot  

## 📌 Giới thiệu  
**YouTube Live Chat TTS Bot** là một ứng dụng tự động theo dõi tin nhắn từ live chat trên YouTube, phản hồi bằng AI (**Ollama**) và phát âm thanh bằng công nghệ chuyển văn bản thành giọng nói (**TTS - gTTS**). Dự án giúp các livestreamer tương tác tốt hơn với khán giả thông qua phản hồi tự động.  

## ✨ Chức năng chính  
- ✅ Theo dõi tin nhắn từ YouTube Live Chat  
- ✅ Tạo phản hồi tự động bằng AI **Ollama**  
- ✅ Phát âm thanh phản hồi bằng **gTTS**  
- ✅ Hỗ trợ phát hiện ngôn ngữ tự động  
- ✅ Lưu trạng thái tin nhắn đã xử lý để tránh trùng lặp  

## 🛠️ Công nghệ sử dụng  
- **Python**: Ngôn ngữ lập trình chính  
- **YouTube Data API**: Lấy tin nhắn từ live chat  
- **Ollama API**: Tạo phản hồi từ AI  
- **Google Text-to-Speech (gTTS)**: Chuyển văn bản thành giọng nói  
- **Pygame**: Phát âm thanh  
- **Threading & Queue**: Xử lý đa luồng cho TTS  

## 🖥️ Cài đặt  

### ⚙️ Yêu cầu hệ thống  
- **Python 3.x**  
- **pip** (trình quản lý gói của Python)  

### 📥 Cài đặt thư viện  
Chạy lệnh sau để cài đặt các thư viện cần thiết:  
```bash
pip install requests pygame gtts
🔧 Cấu hình
Chỉnh sửa file main.py và cập nhật thông tin API:

python
Copy
Edit
API_KEY = "YOUR_YOUTUBE_API_KEY"
LIVE_CHAT_ID = "YOUR_LIVE_CHAT_ID"
📌 Lưu ý:

API Key có thể lấy từ Google Cloud Console.
Live Chat ID có thể lấy từ URL livestream trên YouTube.
🚀 Cách chạy chương trình
Chạy lệnh sau để khởi động bot:

bash
Copy
Edit
python main.py
Nhấn Ctrl + C để dừng bot khi cần.

📁 Cấu trúc dự án
plaintext
Copy
Edit
📂 YouTubeLiveChatTTSBot
├── main.py                  # Chương trình chính
├── tts_engine.py            # Xử lý Text-to-Speech
├── youtube_live_api.py      # API YouTube Live Chat
├── ollama_api.py            # AI tạo phản hồi
├── processed_messages.json  # Lưu tin nhắn đã xử lý
└── README.md                # Hướng dẫn sử dụng
⚠️ Lưu ý
Bot chỉ hoạt động với livestream có live chat đang mở.
Nếu Ollama AI không chạy trên localhost:11434, cần thay đổi URL trong ollama_api.py.
Các tệp âm thanh được tạo tạm thời và tự động xóa sau khi phát xong.
🤝 Đóng góp
Nếu bạn muốn cải thiện dự án, hãy gửi Pull Request hoặc mở Issue trên GitHub! Chúng tôi rất hoan nghênh mọi đóng góp từ cộng đồng.

📜 Giấy phép
Dự án được phát hành theo MIT License – bạn có thể tự do sử dụng, chỉnh sửa và phân phối lại.
