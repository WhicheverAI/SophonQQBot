from nonebot import get_driver
from nonebot.plugin import PluginMetadata

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="sophon",
    description="",
    usage="",
    config=Config,
)

global_config = get_driver().config
config = Config.parse_obj(global_config)

from nonebot import on_command, on_message
# CommandSession, message_preprocessor  # 导入必要的模块
import httpx  # 如果你的 parse 函数需要发送网络请求
from nonebot.exception import MatcherException
from nonebot.adapters import Message
from nonebot.params import CommandArg
from nonebot.adapters import Event
from nonebot.adapters.onebot.v11 import PrivateMessageEvent, GroupMessageEvent
from nonebot.rule import to_me
from nonebot import logger
import random
import asyncio

# from nonebot.adapters.console import Message, MessageSegment

# # str
# Message("Hello, world!")
# # MessageSegment
# Message(MessageSegment.text("Hello, world!"))
# # List[MessageSegment]
# Message([MessageSegment.text("Hello, world!")])

# 定义一个命令处理器
# talker = on_message(
#                     rule=to_me(), 
#                     priority=20, block=True)
talker = on_command('ask', 
# talker = on_command('', 
                    # rule=to_me(), 
                    aliases={"御坂10032", "御坂10032号", '智子'}, priority=20, block=True)
# priority大的会后触发，我们等其他command结束。
import os
# os.environ['HTTP_PROXY'] = os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:12949'
# os.environ['HTTP_PROXY'] = os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'
from gradio_client import Client, file
try:
    client = Client("xianbao/ChatGLM4")
except:
    client = None
import json, os
history_file = 'history.json'
if os.path.exists(history_file):
    with open(history_file, 'r') as f:
        history = json.load(f)
else:
    history = []
    with open(history_file, 'w') as f:
        json.dump(history, f, ensure_ascii=False, indent=4)
import asyncio
# import re
# pattern = re.compile(r'(\n+)|([ ]*)')
import random
from datetime import datetime

# 获取当前日期和时间
now = datetime.now()

# 格式化日期为 'YYYY-MM-DD' 格式
date_str = now.strftime('%Y-%m-%d')
print(date_str)  # 输出类似于 '2024-06-24'

# 新增辅助函数，从 system_prompt.txt 读取长 system prompt
def get_system_prompt() -> str:
    try:
        with open("system_prompt.txt", "r", encoding="utf8") as f:
            prompt = f.read()
            if "{date_str}" in prompt:
                prompt = prompt.replace("{date_str}", date_str)
        return prompt
    except Exception as e:
        return f"错误：无法加载system prompt文本: {e}"

async def answer_question(question:str):
    global client
    if client is None:
        try:
            client = Client("xianbao/ChatGLM4")
        except:
            return "错误：网络无法连接后端！"
    global history
    if len(history)>10:
            history = history[-10:]
    print(history)
    system_prompt = get_system_prompt()  # 从外部txt读取系统提示
    result = client.predict(
        #   query="who are you?",
        # query="你是谁",
        query=question,
        history=history,
        system=system_prompt,

        api_name="/model_chat"
        )
    history = result[1]
    with open(history_file, 'w') as f:
        json.dump(history, f, ensure_ascii=False, indent=4)
        
    answer = history[-1][1]
    return answer

@talker.handle()
async def talk(args: Message = CommandArg(),
                event: PrivateMessageEvent | GroupMessageEvent = None,):
    # 构造回复内容
    if question := args.extract_plain_text():
        # await talker.finish(f"你问我{question}")
        answer = await answer_question(question)
        # print(answer)
        await talker.finish(answer)
        
        # answers = answer.split(r'\r?\n+')
        
        # answers = answer.splitlines()
        # # answers = pattern.split(answer)
        # for answer in answers:
        #     if answer != "":
        #         await talker.send(answer)
        #         # sleep_time = 1
        #         sleep_time = random.uniform(0, 2)
        #         await asyncio.sleep(sleep_time)
        # await talker.finish()
        
    else:
        await talker.finish("在的，你要问我什么呀？")


clear = on_command('clear', 
# talker = on_command('', 
                    # rule=to_me(), 
                    aliases={"清除"}, priority=10, block=True)
@clear.handle()
async def clear_fn(args: Message = CommandArg(),
                event: PrivateMessageEvent | GroupMessageEvent = None,):
    global history
    history = []
    await asyncio.sleep(random.uniform(0, 3))
    await clear.finish("已清除智子的聊天记忆！")
    
    
    
# from nonebot import on_command, export
from nonebot.typing import T_State
# from nonebot.adapters.cqhttp import Bot, Message, GroupMessageEvent, GroupDecreaseNoticeEvent, GroupIncreaseNoticeEvent
from nonebot.adapters.onebot.v11 import Bot, Message, GroupMessageEvent, GroupDecreaseNoticeEvent, GroupIncreaseNoticeEvent
from nonebot import on_notice

# export = export()
# export.name = '进群欢迎'
# export.usage = '欢迎新人'

welcom = on_notice()

# welcome_prompt = "请你出一道关于AI算法的笔试单选题，要求四个选项，仅仅包括题面，确保题目有价值。"

welcome_prompt_file = 'welcome_prompt.json'
if os.path.exists(welcome_prompt_file):
    with open(welcome_prompt_file, 'r') as f:
        welcome_prompt = json.load(f)
else:
    welcome_prompt = "请你出一道关于AI算法的笔试单选题，要求四个选项，仅仅包括题面，确保题目有价值。"
    with open(welcome_prompt_file, 'w') as f:
        json.dump(welcome_prompt, f, ensure_ascii=False, indent=4)

welcome_prompt_command = on_command('welcome_prompt', 
# talker = on_command('', 
                    # rule=to_me(), 
                    aliases={"欢迎提问词"}, priority=10, block=True)
@welcome_prompt_command.handle()
async def welcome_prompt_fun(args: Message = CommandArg(),
                event: PrivateMessageEvent | GroupMessageEvent = None,):
    global welcome_prompt
    if prompt := args.extract_plain_text():
        welcome_prompt = prompt
        with open(welcome_prompt_file, 'w') as f:
            json.dump(welcome_prompt, f, ensure_ascii=False, indent=4)
        await asyncio.sleep(random.uniform(0, 3))
        await welcome_prompt_command.finish(f"已修改进群欢迎提问词为「{welcome_prompt}」。")
    else:
        await asyncio.sleep(random.uniform(0, 3))
        await welcome_prompt_command.finish(f"当前进群欢迎提问词为「{welcome_prompt}」。")
    
    


# 群友入群
@welcom.handle()  # 监听 welcom
async def h_r(bot: Bot, event: GroupIncreaseNoticeEvent, state: T_State):  # event: GroupIncreaseNoticeEvent  群成员增加事件
    if event.group_id not in {821830617, 935310031}: # int类型
        return
    
    user = event.get_user_id()  # 获取新成员的id
    print(user)
    if random.random()<0.5 and user!=1482400683:
        msg = f'欢迎新朋友 [CQ:at,qq={user}] 加入人工智能交流群！\n 进群修改群备注。'
        await welcom.finish(message=Message(msg))  # 发送消息
        
    else:
        global welcome_prompt
        msg = f"本群通过祈愿召唤了 [CQ:at,qq={user}] \n看你根骨惊奇，来和小智一起思考以下问题吧！\n智子正在出题中「{welcome_prompt}」"
        
        await welcom.send(message=Message(msg))  # 发送消息
        await asyncio.sleep(random.uniform(0, 3))
        
        # await welcom.send(message=Message(f"智子正在出题中「{welcome_prompt}」"))  # 发送消息
        answer = await answer_question(welcome_prompt)
        await asyncio.sleep(random.uniform(0, 3))
        
        await welcom.finish(message=Message(answer))  # 发送消息

