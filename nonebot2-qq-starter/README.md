# NoneBot2 QQ 智子 项目

该项目基于 [NoneBot2](https://v2.nonebot.dev/)，实现了一个多模型 AI 聊天机器人插件——智子（Sophon），用于在 QQ 群和私聊中与用户进行交互。机器人支持接入 Huggingface Space Gradio、OpenRouter、Silicon Cloud、DMX 等多种 API平台，并提供上下文问答、思考过程单独展现等功能。

## 特性

- 多模型切换支持（如 OpenRouter、Silicon Cloud、DMX）
- 聊天记录存储与清除功能
- 智子自我认知Prompt，并且支持深度思考。
- 针对回答中的 `<think></think>` 标签进行深度思考内容的单独发送
- 内置欢迎提示词和进群问答，当有新成员加入时，机器人会自动出题考察新成员。
- 模型标识字符串自动归一化（如 `meta-llama/llama-3.1-70b-instruct:free` 简化为 `llama-3.1-70b-instruct`）

## 文件结构

- `plugins/sophon/`：机器人核心插件目录  
  - `config.py`：配置项定义（模型选择、API 密钥、备用模型等）  
  - `__init__.py`：插件入口，命令处理器和事件监听器实现  
  - `answerers.py`：不同后端模型的接口封装  
  - `utils.py`：工具函数，如模型标识归一化  
- `welcome_prompt.json`：进群欢迎提问词配置

## 快速开始

1. 克隆项目并进入项目目录：
   ```bash
   git clone <你的仓库地址>
   cd nonebot2-qq-starter
   ```

2. 安装依赖：
   ```bash
   pip install -r ../requirements.txt
   ```

3. 配置插件：
   - 参考`plugins/sophon/config.py`，根据使用的 API 类型修改对应的密钥和参数，修改`.env.prod`文件。
   - 修改 `welcome_prompt.json` 中的欢迎提示词以及`system_prompt.txt`中的提示词（可选）。

4. 运行 ：
    首先你需要运行 go-cqhttp 或者 Lagrange.OneBot， 启动后端服务连接上QQ，然后才是启动NoneBot2。
   ```bash
   nb run # NoneBot 运行
   ```

## 使用说明

- **命令 `ask`**  
  在对话框输入命令 `ask` 后，后续的文本将作为提问发送，机器人会返回回答。如果回答内容中包含 `<think></think>`（或其他同义标签如 `<思考>`、`<thought>`），则会将其中的思考内容单独发送。

- **命令 `clear`**  
  用于清除机器人内部的问答历史记录。

- **进群欢迎**  
  当群成员加入后，机器人会发送预设的欢迎消息，并根据 `welcome_prompt.json` 中的提示词生成问题。

## 自定义开发

- 可在 `plugins/sophon/utils.py` 中扩展模型字符串的处理逻辑。  
- 如需添加新的回答后端，实现 `Answerer` 抽象类即可。

## 许可证

请遵循项目所在仓库的许可证协议。

---

如有问题或建议，请联系 [WhicheverAI](https://github.com/WhicheverAI)。
