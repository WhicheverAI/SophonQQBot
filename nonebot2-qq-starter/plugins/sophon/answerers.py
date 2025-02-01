from abc import ABC, abstractmethod
from curses.ascii import alt
from gradio_client import Client

class Answerer(ABC):
    @abstractmethod
    def predict(self, query: str, history: list[list[str]], system: str) -> list[list[str]]:
        return [["你是谁？", "我是智子，三体人派出的智子。我的目的是在地球上进行技术干扰。在这里，我会根据你的指令提供帮助。有什么我可以为你做的吗？"]]

    def is_ok(self)->bool:
        return True

class ChatGLMAnswerer(Answerer):
    def __init__(self):
        self.client = Client("xianbao/ChatGLM4")

    def predict(self, query: str, history: list[list[str]], system: str) -> list[list[str]]:
        result = self.client.predict(
            query=query,
            history=history,
            system=system,
            api_name="/model_chat"
        )
        return result[1]

    def is_ok(self)->bool:
        return self.client is not None #TODO

from openai import OpenAI
import time

class OpenRouterAnswerer(Answerer):
    def __init__(self, api_key: str = "<OPENROUTER_API_KEY>", 
                 base_url: str = "https://openrouter.ai/api/v1", 
                 model: str="deepseek/deepseek-r1:free", 
                 site_url: str = "<YOUR_SITE_URL>", site_name: str = "<YOUR_SITE_NAME>", 
                 alternatives: list[str] = []):
        self.client = OpenAI(
            base_url=base_url,
            api_key=api_key,
        )
        self.model = model
        self.extra_headers = {
            "HTTP-Referer": site_url,
            "X-Title": site_name
        }
        self.alternatives = alternatives

    def predict(self, query: str, history: list[list[str]], system: str, user_instead_of_system=True) -> list[list[str]]:
        # 将 history 转换为符合接口要求的 messages 格式
        if user_instead_of_system:
            messages = [dict(role="user", content=system),
                        dict(role="assistant", content="OK. Let's continue."),]
        else:
            messages = [{
                "role": "system",
                "content": system
            }]
        for conv in history:
            if len(conv) >= 1:
                messages.append({
                    "role": "user",
                    "content": conv[0]
                })
            if len(conv) >= 2:
                messages.append({
                    "role": "assistant",
                    "content": conv[1]
                })
        # 添加当前用户消息
        messages.append({
            "role": "user",
            "content": query
        })
        
        success = False
        response_text = "智子模型出现问题，请稍后再试。"
        while not success:
            for model in [self.model] + self.alternatives:
                print(f"Trying model {model}...")
                try:
                    result = self.client.chat.completions.create(
                        extra_headers=self.extra_headers,
                        model=model,
                        messages=messages,  # type: ignore
                    )
                    response_text = result.choices[0].message.content
                    success = True
                except Exception as e:
                    print(f"OpenRouter API error with model {model}:", e)
                    success = False
                    print("Waiting for 3 seconds before retrying...")
                    time.sleep(3)
                if success:
                    break
            if success:
                break
            print("Waiting for 5 seconds before retrying...")
            time.sleep(5)
            
        # 将当前问答对追加到 history 中返回
        new_history = history + [[query, response_text]]
        return new_history


from .config import SophonConfig
def get_answerer(config:SophonConfig) -> Answerer:
    if config.model_type == "gradio":
        return ChatGLMAnswerer()
    elif config.model_type == "openai":
        return OpenRouterAnswerer(
            api_key=config.openrouter_api_key,
            base_url=config.openrouter_base_url,
            model=config.model,
            site_url=config.openrouter_site_url,
            site_name=config.openrouter_site_name, 
            alternatives=config.alternatives
        )
    else:
        raise ValueError(f"Unsupported model: {config.sophon_model}")