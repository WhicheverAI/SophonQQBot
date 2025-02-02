from pydantic import BaseModel, Extra

class SophonConfig(BaseModel, extra=Extra.ignore):
    # 模型选择 (chatglm/deepseek)
    # sophon_model: str = "gradio"  
    model_type: str = "openai"  
    openai_type: str = "silicon_cloud"  # openrouter/silicon_cloud/dmx
    # openai_type: str = "dmx"  # openrouter/silicon_cloud/dmx
    # model: str = "meta-llama/llama-3.1-405b-instruct:free"
    openrouter_model: str = "deepseek/deepseek-r1:free"
    # model:str = "google/gemini-2.0-flash-thinking-exp:free"
    openrouter_alternatives: list[str] = [
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


    silicon_cloud_api_key: str = ""
    silicon_cloud_base_url="https://api.siliconflow.cn/v1"

    # silicon_cloud:str = "AIDC-AI/Marco-o1"
    # silicon_cloud:str = "deepseek-ai/DeepSeek-R1" # 收费
    silicon_cloud:str = "deepseek-ai/DeepSeek-V3" # 收费
    silicon_clouds: list[str] = [
        "Qwen/Qwen2.5-7B-Instruct",
        "Qwen/Qwen2.5-Coder-7B-Instruct",
        "internlm/internlm2_5-7b-chat",
        "meta-llama/Meta-Llama-3.1-8B-Instruct",
        "Qwen/Qwen2-7B-Instruct",
        "THUDM/glm-4-9b-chat",
        "THUDM/chatglm3-6b",
        "01-ai/Yi-1.5-9B-Chat-16K",
        "AIDC-AI/Marco-o1",
        "google/gemma-2-9b-it",
    ]

    dmx_api_key: str = ""
    dmx_base_url: str = "https://www.DMXapi.com/v1"
    dmx:str = "ERNIE-Tiny-8K"
    dmxs: list[str] = [
        "01-ai/Yi-1.5-9B-Chat-16K",
        "ERNIE-Speed-128K",
        # "ERNIE-Tiny-8K",
        "glm-4-flash",
        "GLM-4V-Flash",
        "hunyuan-lite",
        "meta-llama/Meta-Llama-3.1-8B-Instruct",
        "Qwen/Qwen2.5-7B-Instruct",
        "Qwen/Qwen2.5-Coder-7B-Instruct",
        "spark-lite",
        "THUDM/glm-4-9b-chat",

        # "kyw",
        # "lite",
    ]