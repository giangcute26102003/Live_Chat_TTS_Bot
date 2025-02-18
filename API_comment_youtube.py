import requests
import time
import json
import pygame
from gtts import gTTS
import os
from datetime import datetime
from typing import Dict, List, Optional
import threading
from queue import Queue

class TTSEngine:
    def __init__(self):
        """Khởi tạo TTS engine và audio player"""
        # Khởi tạo pygame để phát âm thanh
        pygame.mixer.init()
        self.audio_queue = Queue()
        self.is_speaking = False
        
        # Bắt đầu thread xử lý audio
        self.audio_thread = threading.Thread(target=self._process_audio_queue)
        self.audio_thread.daemon = True
        self.audio_thread.start()
    
    def _process_audio_queue(self):
        """Xử lý queue và phát âm thanh"""
        while True:
            if not self.audio_queue.empty() and not self.is_speaking:
                audio_file = self.audio_queue.get()
                self.is_speaking = True
                
                try:
                    pygame.mixer.music.load(audio_file)
                    pygame.mixer.music.play()
                    
                    # Đợi cho đến khi phát xong
                    while pygame.mixer.music.get_busy():
                        time.sleep(0.1)
                        
                    # Xóa file tạm
                    os.remove(audio_file)
                    
                except Exception as e:
                    print(f"Lỗi khi phát âm thanh: {e}")
                    
                self.is_speaking = False
            time.sleep(0.1)
    
    def speak(self, text: str, lang: str = 'vi'):
        """Chuyển text thành speech và thêm vào queue"""
        try:
            # Tạo file âm thanh tạm thời
            tts = gTTS(text=text, lang=lang)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            temp_file = f"speech_{timestamp}.mp3"
            tts.save(temp_file)
            
            # Thêm vào queue để phát
            self.audio_queue.put(temp_file)
            
        except Exception as e:
            print(f"Lỗi khi tạo speech: {e}")

class YouTubeLiveAPI:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://www.googleapis.com/youtube/v3"
        self.next_page_token = None
        
    def get_live_chat_messages(self, live_chat_id: str) -> Dict:
        """Lấy tin nhắn từ live chat"""
        url = f"{self.base_url}/liveChat/messages"
        
        params = {
            "liveChatId": live_chat_id,
            "part": "snippet,authorDetails",
            "key": self.api_key
        }
        
        if self.next_page_token:
            params["pageToken"] = self.next_page_token
            
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            self.next_page_token = data.get("nextPageToken")
            
            messages = []
            for item in data.get("items", []):
                messages.append({
                    "id": item["id"],
                    "message": item["snippet"]["displayMessage"],
                    "author": item["authorDetails"]["displayName"],
                    "author_channel_id": item["authorDetails"]["channelId"],
                    "timestamp": item["snippet"]["publishedAt"]
                })
            
            return {
                "messages": messages,
                "pollingIntervalMillis": data.get("pollingIntervalMillis", 2000)
            }
            
        except requests.RequestException as e:
            print(f"Lỗi khi lấy live chat messages: {e}")
            return {"messages": [], "pollingIntervalMillis": 2000}

class OllamaAPI:
    def __init__(self, base_url="http://localhost:11434"):
        self.base_url = base_url
        
    def generate_response(self, prompt: str, model: str = "llama3.1") -> str:
        """Tạo câu trả lời từ Ollama"""
        url = f"{self.base_url}/api/generate"
        
        system_prompt = """Bạn là Umi, một AI thông minh và hóm hỉnh, thường xuất hiện trong các livestream YouTube để giải đáp thắc mắc của khán giả. Khi trả lời, hãy sử dụng ngôn ngữ gần gũi, thân thiện, và thêm vào những câu đùa nhẹ nhàng để giữ chân khán giả. Hãy làm cho mỗi câu trả lời của bạn trở nên thú vị và dễ nhớ, như thể bạn là một người bạn vui tính đang nói chuyện với họ. Đừng quên sử dụng những biểu cảm vui nhộn và ngôn ngữ cơ thể (nếu có thể) để tạo sự gắn kết.

Ví dụ:

Câu hỏi: 'Làm thế nào để nấu cơm ngon?'
Trả lời: 'À, nấu cơm ngon à? Đầu tiên, bạn cần một nồi cơm điện, nếu không có thì... ừm, tốt nhất là mua một cái đi ha! Còn cách nấu thì đơn giản thôi, đong lúa cho vừa, nước cho đủ, bấm nút và... chờ đợi phép màu xảy ra! Nhớ là, nếu cơm chín mà vẫn cứng, đừng trách tôi, trách cái nồi của bạn đi!'
Hãy tiếp tục với tinh thần này khi trả lời các câu hỏi trong livestream
"""
        
        data = {
            "model": model,
            "prompt": prompt,
            "system": system_prompt,
            "stream": False
        }
        
        try:
            response = requests.post(url, json=data)
            response.raise_for_status()
            return response.json()["response"]
            
        except requests.RequestException as e:
            print(f"Lỗi khi tạo response: {e}")
            return None

class LiveChatTTSBot:
    def __init__(self, youtube_api: YouTubeLiveAPI, ollama_api: OllamaAPI, tts_engine: TTSEngine):
        self.youtube_api = youtube_api
        self.ollama_api = ollama_api
        self.tts_engine = tts_engine
        self.processed_messages = set()
        
        self.load_processed_messages()
    
    def load_processed_messages(self):
        """Load danh sách tin nhắn đã xử lý từ file"""
        try:
            with open('processed_messages.json', 'r') as f:
                self.processed_messages = set(json.load(f))
        except FileNotFoundError:
            self.processed_messages = set()
    
    def save_processed_messages(self):
        """Lưu danh sách tin nhắn đã xử lý vào file"""
        with open('processed_messages.json', 'w') as f:
            json.dump(list(self.processed_messages), f)
    
    def detect_language(self, text: str) -> str:
        """Phát hiện ngôn ngữ của tin nhắn (đơn giản)"""
        # Đây là phiên bản đơn giản, bạn có thể sử dụng thư viện như langdetect để chính xác hơn
        vietnamese_chars = set('àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ')
        text_lower = text.lower()
        
        if any(char in vietnamese_chars for char in text_lower):
            return 'vi'
        return 'en'
    
    def process_messages(self, live_chat_id: str):
        """Xử lý tin nhắn mới từ live chat"""
        result = self.youtube_api.get_live_chat_messages(live_chat_id)
        messages = result["messages"]
        polling_interval = result["pollingIntervalMillis"] / 1000
        
        for message in messages:
            if message["id"] not in self.processed_messages:
                print(f"\nTin nhắn mới từ {message['author']}: {message['message']}")
                
                # Tạo prompt cho Ollama
                prompt = f"""Tin nhắn YouTube Live: {message['message']}
                Người gửi: {message['author']}
                
                Hãy tạo câu trả lời phù hợp cho tin nhắn này."""
                
                response = self.ollama_api.generate_response(prompt)
                response = remove_trailing_quote(response)
                if response:
                    print(f"Trả lời: {response}")
                    
                    # Phát hiện ngôn ngữ và chuyển thành giọng nói
                    lang = self.detect_language(response)
                    self.tts_engine.speak(response, lang)
                    
                    self.processed_messages.add(message["id"])
                    self.save_processed_messages()
        
        return polling_interval
def remove_trailing_quote(s: str) -> str:
    return s[:-1] if s.endswith('"') else s
def main():
    # Khởi tạo các components
    API_KEY = "AIzaSyAFvbHX3W...."  # Thay thế bằng API key của bạn
    LIVE_CHAT_ID = "Cg0KC21..."  # Thay thế bằng live chat ID
    
    youtube_api = YouTubeLiveAPI(API_KEY)
    ollama_api = OllamaAPI()
    tts_engine = TTSEngine()
    bot = LiveChatTTSBot(youtube_api, ollama_api, tts_engine)
    
    print(f"Bắt đầu theo dõi live chat {LIVE_CHAT_ID}")
    print("Nhấn Ctrl+C để dừng")
    
    try:
        while True:
            polling_interval = bot.process_messages(LIVE_CHAT_ID)
            time.sleep(polling_interval)
            
    except KeyboardInterrupt:
        print("\nDừng theo dõi live chat")
        bot.save_processed_messages()

if __name__ == "__main__":
    main()