def normalize_model_spec(spec: str) -> str:
    """
    将完整的模型标识字符串，例如 "meta-llama/llama-3.1-70b-instruct:free"
    转换为简化的形式 "llama-3.1-70b-instruct"
    """
    return spec.split("/")[-1].split(":")[0]

# 示例用法
if __name__ == "__main__":
    test_str = "meta-llama/llama-3.1-70b-instruct:free"
    test_str = "Qwen/Qwen2.5-Coder-7B-Instruct"
    print(normalize_model_spec(test_str))
