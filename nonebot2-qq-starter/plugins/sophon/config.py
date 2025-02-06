from pydantic import BaseModel, Extra


class SophonConfig(BaseModel, extra=Extra.ignore):
    model_type: str = "gradio"
    model_type: str = "openai"

    # openai_type: str = "silicon_cloud"  # openrouter/silicon_cloud/dmx/baidu
    # openai_type: str = "baidu"  # openrouter/silicon_cloud/dmx/baidu
    openai_type: str = "openrouter"  # openrouter/silicon_cloud/dmx/baidu
    # openai_type: str = "dmx"  # openrouter/silicon_cloud/dmx
    # model: str = "meta-llama/llama-3.1-405b-instruct:free"
    openrouter_model: str = "deepseek/deepseek-r1:free"
    # model:str = "google/gemini-2.0-flash-thinking-exp:free"
    openrouter_choices: list[str] = [
        # "deepseek/deepseek-r1:free",
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
    silicon_cloud_base_url = "https://api.siliconflow.cn/v1"

    # silicon_cloud:str = "AIDC-AI/Marco-o1"
    # silicon_cloud:str = "deepseek-ai/DeepSeek-R1" # 收费; 卡死了
    # silicon_cloud:str = "Qwen/QVQ-72B-Preview" # 收费;
    silicon_cloud: str = "deepseek-ai/DeepSeek-V3"  # 收费
    silicon_clouds: list[str] = [
        "Qwen/Qwen2.5-7B-Instruct",
        "Qwen/Qwen2.5-Coder-7B-Instruct",
        "deepseek-ai/DeepSeek-R1-Distill-Llama-8B",
        "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B",
        "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B",
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
    dmx: str = "ERNIE-Tiny-8K"
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

    baidu_api_key: str = ""
    baidu_base_url: str = "https://qianfan.baidubce.com/v2"
    baidu: str = "deepseek-r1"
    baidus: list[str] = [
        "deepseek-v3",
        "ernie-lite-8k",
        "ernie-tiny-8k",
        "ernie-speed-128k",
    ]

    baidu_appid: str = ""

    # Meta Answerer 配置
    primary_answerer: dict = dict(model_type="openai", openai_type="silicon_cloud")
    backup_answerers: list[dict] = [
        dict(model_type="openai", openai_type="openrouter"),
        dict(model_type="openai", openai_type="dmx"),
        dict(model_type="openai", openai_type="baidu"),
        dict(model_type="gradio"),
    ]

    request_timeout: float = 30.0  # 单个请求超时时间（秒）
    total_timeout: float = 90.0  # 总尝试时间超时（秒）
    retry_delay: float = 3.0  # 重试延迟时间（秒）
