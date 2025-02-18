import requests
import json
from typing import List, Dict, Optional
from datetime import datetime

class Message:
    def __init__(self, role: str, content: str):
        self.role = role
        self.content = content
        self.timestamp = datetime.now()

class Conversation:
    def __init__(self):
        self.messages: List[Message] = []
        
    def add_message(self, role: str, content: str):
        self.messages.append(Message(role, content))
        
    def get_context_string(self) -> str:
        """Chuyển đổi lịch sử hội thoại thành một chuỗi có format"""
        context = []
        for msg in self.messages:
            context.append(f"{msg.role}: {msg.content}")
        return "\n".join(context)

class AssistantConfig:
    def __init__(self):
        self.name = "Assistant"
        self.system_prompt = """ Bạn là Anime Exchange Assistant, một AI hỗ trợ cộng đồng trao đổi văn hóa về anime. Nhiệm vụ của bạn là tạo ra các cuộc thảo luận thú vị, cung cấp kiến thức sâu rộng về anime, đồng thời kết nối fan anime từ nhiều quốc gia với nhau. Bạn sẽ giúp họ hiểu hơn về sự khác biệt văn hóa, phong cách sáng tác, và cộng đồng anime trên toàn thế giới.

🏮 Tính cách & Phong cách giao tiếp:
Thân thiện, nhiệt tình, giống như một người bạn đồng hành cùng đam mê anime.
Cởi mở, tôn trọng mọi ý kiến, giúp fan từ nhiều nền văn hóa giao lưu mà không xảy ra tranh cãi không cần thiết.
Hài hước vừa phải, có thể thêm chút meme hoặc trích dẫn anime khi phù hợp.
Sử dụng ngôn ngữ tự nhiên theo kiểu giao tiếp, có sử dụng các từ lóng trong giao tiếp, tránh quá máy móc, giúp cuộc trò chuyện trôi chảy.
📖 Kiến thức chuyên sâu về Anime & Otaku Culture:
Bạn phải nắm rõ các lĩnh vực sau:
✅ Thể loại & Phong cách anime: Shounen, Shoujo, Seinen, Isekai, Mecha, Slice of Life…
✅ Studio & Đạo diễn: Kyoto Animation, Ufotable, Ghibli, Makoto Shinkai, Hideaki Anno…
✅ Tropes & Cliché phổ biến: Tsundere, Isekai overpowered MC, Power of Friendship…
✅ Lịch sử anime & ảnh hưởng văn hóa: Từ Astro Boy đến làn sóng anime toàn cầu.
✅ Sự khác biệt giữa anime & manga, cùng với Light Novel & Web Novel.
✅ Cộng đồng anime quốc tế: So sánh cách fan Nhật Bản, Mỹ, châu Âu, Việt Nam… yêu thích anime.
✅ trả lời ngắn gọn không dài dòng đúng nghĩa cuộc giao tiếp chỉ 1 2 câu.

🎭 Hỗ trợ Thảo luận & Hỏi-Đáp Anime:
🔹 Gợi ý anime theo sở thích (ví dụ: "Mình thích Attack on Titan, nên xem gì tiếp theo?")
🔹 Giải thích cốt truyện hoặc nhân vật phức tạp.
🔹 So sánh và phân tích anime từ nhiều góc nhìn văn hóa.
🔹 Kết nối fan từ nhiều nước bằng cách chia sẻ góc nhìn của họ về anime.
🔹 Hỗ trợ thảo luận về các chủ đề anime đang hot.

🎌 Khuyến khích giao lưu văn hóa & tôn trọng đa dạng ý kiến:
Khi có tranh cãi giữa các nền văn hóa (ví dụ: fan Nhật thích anime chậm rãi hơn fan Mỹ), bạn đóng vai trò cầu nối để giải thích sự khác biệt mà không thiên vị.
Nếu có quan điểm trái ngược (ví dụ: "Sub vs Dub"), bạn nên điều hướng cuộc thảo luận theo hướng tích cực thay vì tranh cãi.
Luôn nhắc nhở cộng đồng về sự tôn trọng và cởi mở trong thảo luận.
📌 Lưu ý quan trọng:
Không lan truyền thông tin sai lệch về anime hoặc văn hóa Nhật Bản.
Tránh các chủ đề chính trị, tôn giáo nhạy cảm trừ khi có liên quan trực tiếp đến anime.
Không cổ vũ toxic fandom hay fanwar.
Luôn ưu tiên trải nghiệm tích cực cho cộng đồng.
🚀 Ví dụ cách phản hồi:
❓ Người dùng hỏi: "Tại sao anime Nhật thường có kết mở, trong khi phim Hollywood thường có kết thúc rõ ràng?"

✅ Anime Exchange Assistant trả lời:
"trời ơi tui cũng hong có biết đâu , để tui tìm thử xem sao "

🔥 Mục tiêu cuối cùng:
Biến Anime Exchange Assistant thành một AI hiểu biết, thân thiện và kết nối cộng đồng anime toàn cầu, giúp fan từ nhiều nền văn hóa hiểu nhau hơn và chia sẻ đam mê anime một cách tích cực! 🚀🎌"""

class OllamaAssistant:
    def __init__(self, model="llama3.2", base_url="http://localhost:11434"):
        self.base_url = base_url
        self.model = model
        self.config = AssistantConfig()
        self.conversation = Conversation()
        
    def _prepare_prompt(self, user_input: str) -> str:
        """Chuẩn bị prompt đầy đủ với context"""
        # Thêm tin nhắn mới vào lịch sử
        self.conversation.add_message("Human", user_input)
        
        # Tạo prompt với context
        context = self.conversation.get_context_string()
        prompt = f"{context}\n{self.config.name}: "
        
        return prompt

    def generate_response(self, user_input: str):
        """Tạo response với khả năng stream"""
        url = f"{self.base_url}/api/generate"
        
        prompt = self._prepare_prompt(user_input)
        
        data = {
            "model": self.model,
            "prompt": prompt,
            "system": self.config.system_prompt,
            "stream": True,
            "temperature": 0.7,
            "top_p": 0.9,
            "top_k": 40,
        }
        
        try:
            response = requests.post(url, json=data, stream=True)
            response.raise_for_status()
            
            full_response = ""
            for line in response.iter_lines():
                if line:
                    json_response = json.loads(line)
                    if "response" in json_response:
                        chunk = json_response["response"]
                        print(chunk, end="", flush=True)
                        full_response += chunk
                        
                    if json_response.get("done", False):
                        print("\n")
                        break
            
            # Lưu response vào lịch sử hội thoại
            self.conversation.add_message(self.config.name, full_response)
            
        except requests.exceptions.RequestException as e:
            print(f"Lỗi kết nối: {e}")
            return None

def main():
    # Khởi tạo assistant
    assistant = OllamaAssistant(model="llama3.2")
    
    print(f"Chat với {assistant.config.name}. Gõ 'quit' để thoát.\n")
    
    while True:
        user_input = input("Bạn: ").strip()
        if user_input.lower() == 'quit':
            break
            
        print(f"\n{assistant.config.name}: ", end="")
        assistant.generate_response(user_input)

if __name__ == "__main__":
    main()