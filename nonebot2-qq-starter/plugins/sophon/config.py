from pydantic import BaseModel, Extra

class SophonConfig(BaseModel, extra=Extra.ignore):
    # 模型选择 (chatglm/deepseek)
    # sophon_model: str = "gradio"  
    model_type: str = "openai"  
    model: str = "deepseek/deepseek-r1:free"
    # model:str = "google/gemini-2.0-flash-thinking-exp:free"
    alternatives: list[str] = [
        "google/gemini-2.0-flash-thinking-exp:free", 
        "google/gemini-2.0-flash-thinking-exp-1219:free",
        "meta-llama/llama-3.2-90b-vision-instruct:free",
        "meta-llama/llama-3.1-405b-instruct:free",
        "qwen/qwen-2-7b-instruct:free",
        ]
    # OpenRouter配置
    openrouter_api_key: str = ""
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    # 站点信息(用于OpenRouter统计)
    openrouter_site_url: str = "https://github.com/WhicheverAI"
    openrouter_site_name: str = "SophonAI"
