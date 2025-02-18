YouTube Live Chat TTS Bot

Giới thiệu

YouTube Live Chat TTS Bot là một ứng dụng tự động theo dõi tin nhắn từ livestream trên YouTube, phản hồi bằng AI (Ollama) và phát âm thanh bằng TTS (gTTS). Dự án này phù hợp cho các livestreamer muốn tạo sự tương tác tự động với người xem.

Chức năng chính

Theo dõi tin nhắn từ live chat của YouTube

Tạo phản hồi tự động bằng AI Ollama

Phát âm thanh phản hồi bằng TTS (gTTS)

Hỗ trợ phát hiện ngôn ngữ tự động

Lưu trạng thái tin nhắn đã xử lý để tránh trùng lặp

Công nghệ sử dụng

Python: Ngôn ngữ lập trình chính

YouTube Data API: Lấy tin nhắn từ live chat

Ollama API: Tạo câu trả lời từ AI

Google Text-to-Speech (gTTS): Chuyển văn bản thành giọng nói

Pygame: Phát âm thanh

Threading & Queue: Xử lý đa luồng cho TTS

Cài đặt

Yêu cầu hệ thống

Python 3.x

pip

Cài đặt thư viện

Chạy lệnh sau để cài đặt các thư viện cần thiết:

pip install requests pygame gtts

Cấu hình

Chỉnh sửa file main.py và cập nhật thông tin:

API_KEY = "YOUR_YOUTUBE_API_KEY"
LIVE_CHAT_ID = "YOUR_LIVE_CHAT_ID"

Bạn cần lấy API Key từ Google Cloud Console và Live Chat ID từ YouTube.

Cách chạy chương trình

Chạy lệnh sau để bắt đầu bot:

python main.py

Nhấn Ctrl + C để dừng bot.

Cấu trúc dự án

📂 YouTubeLiveChatTTSBot
├── main.py                  # Chương trình chính
├── tts_engine.py            # Xử lý Text-to-Speech
├── youtube_live_api.py      # API YouTube Live Chat
├── ollama_api.py            # AI tạo phản hồi
├── processed_messages.json  # Lưu tin nhắn đã xử lý
└── README.md                # Hướng dẫn sử dụng

Lưu ý

Bot chỉ hoạt động với livestream có live chat đang mở.

Nếu Ollama AI không chạy trên localhost:11434, cần thay đổi URL trong OllamaAPI.

Các tệp âm thanh sẽ được tạo tạm thời và tự động xóa sau khi phát xong.

Đóng góp

Nếu bạn muốn cải thiện dự án, hãy gửi Pull Request hoặc mở Issue trên GitHub!

Giấy phép

Dự án được phát hành theo giấy phép MIT License.
