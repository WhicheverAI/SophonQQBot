from pydantic import BaseModel, Extra

class SophonConfig(BaseModel, extra=Extra.ignore):
    # 模型选择 (chatglm/deepseek)
    # sophon_model: str = "gradio"  
    model_type: str = "openai"  
    # model: str = "meta-llama/llama-3.1-405b-instruct:free"
    model: str = "deepseek/deepseek-r1:free"
    # model:str = "google/gemini-2.0-flash-thinking-exp:free"
    alternatives: list[str] = [
        # "microsoft/phi-3-medium-128k-instruct:free",
        "meta-llama/llama-3.1-405b-instruct:free",
        "meta-llama/llama-3.1-70b-instruct:free",
        "meta-llama/llama-3.2-90b-vision-instruct:free",
        "qwen/qwen-2-7b-instruct:free",
        "mistralai/mistral-7b-instruct:free",
        "deepseek/deepseek-r1:free",
        "google/gemini-2.0-flash-thinking-exp:free", 
        "google/gemini-2.0-flash-thinking-exp-1219:free",
        "huggingfaceh4/zephyr-7b-beta:free",
        "openchat/openchat-7b:free",
        "google/gemma-2-9b-it:free",
        "sophosympatheia/rogue-rose-103b-v0.2:free",
        ]
    # OpenRouter配置
    openrouter_api_key: str = ""
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    # 站点信息(用于OpenRouter统计)
    openrouter_site_url: str = "https://github.com/WhicheverAI"
    openrouter_site_name: str = "SophonAI"
