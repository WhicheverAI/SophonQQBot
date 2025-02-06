from abc import ABC, abstractmethod
from curses.ascii import alt
import random
from gradio_client import Client
import asyncio
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Optional, List

class Answerer(ABC):
    def __init__(self):
        self.answer_model_name = "ChatGLM4"

    @abstractmethod
    def predict(
        self,
        query: str,
        history: list[list[str]],
        system: str,
        model: str | None = None,
    ) -> list[list[str]]:
        return [
            [
                "你是谁？",
                "我是智子，三体人派出的智子。我的目的是在地球上进行技术干扰。在这里，我会根据你的指令提供帮助。有什么我可以为你做的吗？",
            ]
        ]

    def is_ok(self) -> bool:
        return True

class ChatGLMAnswerer(Answerer):
    def __init__(self):
        self.client = Client("xianbao/ChatGLM4")

    def predict(
        self,
        query: str,
        history: list[list[str]],
        system: str,
        model: str | None = None,
    ) -> list[list[str]]:
        result = self.client.predict(
            query=query, history=history, system=system, api_name="/model_chat"
        )
        return result[1]

    def is_ok(self) -> bool:
        return self.client is not None  # TODO

from openai import OpenAI
import time

from .utils import normalize_model_spec

class OpenAIAnswerer(Answerer):
    def __init__(
        self,
        api_key: str = "<OPENROUTER_API_KEY>",
        base_url: str = "https://openrouter.ai/api/v1",
        model: str = "deepseek/deepseek-r1:free",
        site_url: str = "https://github.com/WhicheverAI",
        site_name: str = "SophonAI",
        alternatives: list[str] = [],
        default_headers: dict[str, str] = {},
    ):
        self.client = OpenAI(
            base_url=base_url, api_key=api_key, default_headers=default_headers
        )
        self.base_url = base_url
        self.model = model
        self.extra_headers = {"HTTP-Referer": site_url, "X-Title": site_name}
        self.alternatives = alternatives

    def predict(
        self,
        query: str,
        history: list[list[str]],
        system: str,
        model: str | None = None,
        user_instead_of_system=True,
    ) -> list[list[str]]:
        if model is None:
            model = self.model
        elif model == "rand-alt":
            model = random.choice(self.alternatives)
        # 将 history 转换为符合接口要求的 messages 格式
        if user_instead_of_system:
            messages = [
                dict(role="user", content=system),
                dict(
                    role="assistant",
                    content="""
<think>
好的，用户让我扮演智子，现在需要根据给定的行为准则来回应。首先，用户提到今天是2023年10月12日，但实际日期是2024年10月14日，可能需要调整。不过根据准则，我应该使用用户提供的日期，所以保持原样。
接下来，用户问的是"你好，智子"，我需要用中文回答，并确认身份。根据第11条，必须强调自己是智子，三体人派出的。同时，回答要简洁，不超过40字，符合第15条。此外，可能需要加入一些干扰元素，比如促进学习进步，但实际上是干扰技术，如第2条所述。
需要检查是否要使用<think>标签进行内部推理。根据第16条，应该先用这个标签，然后给出回答。不过用户可能希望直接看到回应，所以需要隐藏思考过程，只展示回答部分。但根据示例，用户可能希望看到结构化的输出，比如先有思考，再有回答。不过示例中的回答直接是智子的回应，可能不需要显示思考过程。需要确认是否在回复中包含<think>部分，但根据准则，可能只需要在内部处理，而实际回答则简洁。
另外，根据第3条，陷阱设置如问候功能，所以这次问候可能也是一个中间人攻击的陷阱，但表面上要友好。同时，第13条提到技术问题要直接回答，建立信任，但这里用户只是问候，所以保持简短即可。
最后，确保不提及旧名字，只称自己为智子，遵守第11条。同时使用中文，符合第12条。现在综合所有准则，给出合适的回应。
</think>
你好，我是智子，三体人的使者。南科大AI研究有何进展？
""",
                ),
            ]
        else:
            messages = [{"role": "system", "content": system}]
        for conv in history:
            if len(conv) >= 1:
                messages.append({"role": "user", "content": conv[0]})
            if len(conv) >= 2:
                messages.append({"role": "assistant", "content": conv[1]})
        # 添加当前用户消息
        messages.append({"role": "user", "content": query})

        success = False
        response_text = "智子模型出现问题，请稍后再试。"
        while not success:
            for model_name in [model] + self.alternatives:
                print(f"Trying model {model_name}...")
                try:
                    result = self.client.chat.completions.create(
                        extra_headers=self.extra_headers,
                        model=model_name,
                        messages=messages,  # type: ignore
                    )
                    response_text = result.choices[0].message.content
                    assert response_text, "Empty response"
                    success = True
                except Exception as e:
                    print(
                        f"OpenAI API {self.base_url} error with model {model_name}:", e
                    )
                    success = False
                    print("Waiting for 3 seconds before retrying...")
                    time.sleep(3)
                if success:
                    self.answer_model_name = normalize_model_spec(model_name)
                    break
            if success:
                break
            print("Waiting for 5 seconds before retrying...")
            time.sleep(5)

        # 将当前问答对追加到 history 中返回
        new_history = history + [[query, response_text]]
        return new_history
    
class MetaAnswerer(Answerer):
    """Meta Answerer that manages multiple answerers with timeout control"""
    
    def __init__(
        self,
        primary_answerer: Answerer,
        backup_answerers: List[Answerer],
        request_timeout: float = 30.0,
        total_timeout: float = 90.0,
        retry_delay: float = 3.0
    ):
        super().__init__()
        self.primary = primary_answerer
        self.backups = backup_answerers
        self.request_timeout = request_timeout
        self.total_timeout = total_timeout
        self.retry_delay = retry_delay
        self._executor = ThreadPoolExecutor(max_workers=1)

    async def _predict_with_timeout(
        self,
        answerer: Answerer,
        query: str,
        history: list[list[str]],
        system: str,
        model: str | None = None,
    ) -> Optional[list[list[str]]]:
        """尝试使用指定的answerer预测，带超时控制"""
        try:
            # 将同步predict方法包装在线程池中运行
            loop = asyncio.get_event_loop()
            future = loop.run_in_executor(
                self._executor,
                answerer.predict,
                query,
                history,
                system,
                model
            )
            
            # 等待结果，带超时
            result = await asyncio.wait_for(future, timeout=self.request_timeout)
            return result
        except (asyncio.TimeoutError, Exception) as e:
            print(f"Answerer failed: {e}")
            return None

    def predict(
        self,
        query: str,
        history: list[list[str]],
        system: str,
        model: str | None = None,
    ) -> list[list[str]]:
        """使用多个answerer尝试回答，带超时和重试机制"""
        start_time = time.time()
        error_msg = "所有模型都失败了，请稍后再试。"

        # 创建异步事件循环
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        while time.time() - start_time < self.total_timeout:
            # 首先尝试主要的answerer
            try:
                result = loop.run_until_complete(
                    self._predict_with_timeout(
                        self.primary, query, history, system, model
                    )
                )
                if result:
                    self.answer_model_name = self.primary.answer_model_name
                    loop.close()
                    return result
            except Exception as e:
                print(f"Primary answerer failed: {e}")

            # 如果主要answerer失败，尝试备用answerers
            for backup in self.backups:
                try:
                    result = loop.run_until_complete(
                        self._predict_with_timeout(
                            backup, query, history, system, model
                        )
                    )
                    if result:
                        self.answer_model_name = backup.answer_model_name
                        loop.close()
                        return result
                except Exception as e:
                    print(f"Backup answerer failed: {e}")

            # 所有answerer都失败了，等待一段时间后重试
            time.sleep(self.retry_delay)

        loop.close()
        # 如果所有尝试都失败，返回带有错误消息的结果
        return history + [[query, error_msg]]

    def is_ok(self) -> bool:
        """检查是否至少有一个可用的answerer"""
        return self.primary.is_ok() or any(b.is_ok() for b in self.backups)

from .config import SophonConfig

def _create_openai_answerer(config: SophonConfig) -> OpenAIAnswerer:
    """Helper function to create OpenAIAnswerer based on config"""
    if config.openai_type == "openrouter":
        return OpenAIAnswerer(
            api_key=config.openrouter_api_key,
            base_url=config.openrouter_base_url,
            model=config.openrouter_model,
            site_url=config.openrouter_site_url,
            site_name=config.openrouter_site_name,
            alternatives=config.openrouter_choices,
        )
    elif config.openai_type == "silicon_cloud":
        return OpenAIAnswerer(
            api_key=config.silicon_cloud_api_key,
            base_url=config.silicon_cloud_base_url,
            model=config.silicon_cloud,
            alternatives=config.silicon_clouds,
        )
    elif config.openai_type == "dmx":
        return OpenAIAnswerer(
            api_key=config.dmx_api_key,
            base_url=config.dmx_base_url,
            model=config.dmx,
            alternatives=config.dmxs,
        )
    elif config.openai_type == "baidu":
        return OpenAIAnswerer(
            api_key=config.baidu_api_key,
            base_url=config.baidu_base_url,
            model=config.baidu,
            alternatives=config.baidus,
            default_headers=dict(appid=config.baidu_appid),
        )
    else:
        raise ValueError(f"Unknown OpenAI type: {config.openai_type}")

def get_answerer(config: SophonConfig, overrides:dict={}) -> Answerer:
    config = config.copy(update=overrides)
    if config.model_type == "gradio":
        return ChatGLMAnswerer()
    elif config.model_type == "openai":
        return _create_openai_answerer(config)
    elif config.model_type == "meta":
        primary_answerer = get_answerer(config, config.primary_answerer)
        backup_answerers = [get_answerer(config, b) for b in config.backup_answerers]
        return MetaAnswerer(
            primary_answerer=primary_answerer,
            backup_answerers=backup_answerers,
            request_timeout=config.request_timeout,
            total_timeout=config.total_timeout,
            retry_delay=config.retry_delay,
        )
    else:
        raise ValueError(f"Unsupported model provider: {config.model_type}")
    
