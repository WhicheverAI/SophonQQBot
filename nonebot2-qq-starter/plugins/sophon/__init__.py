from nonebot import get_driver
from nonebot.plugin import PluginMetadata

from .config import SophonConfig

__plugin_meta__ = PluginMetadata(
    name="sophon",
    description="",
    usage="",
    config=SophonConfig,
)

global_config = get_driver().config

from nonebot import get_plugin_config
config = get_plugin_config(SophonConfig)
# config = SophonConfig.parse_obj(global_config)

from nonebot import on_command, on_message
# CommandSession, message_preprocessor  # 导入必要的模块
import httpx  # 如果你的 parse 函数需要发送网络请求
from nonebot.exception import MatcherException
from nonebot.adapters import Message
from nonebot.params import CommandArg
from nonebot.adapters import Event
from nonebot.adapters.onebot.v11 import PrivateMessageEvent, GroupMessageEvent, MessageSegment  # 新增MessageSegment导入
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


from .answerers import get_answerer
answerer = get_answerer(config)

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
def get_system_prompt(file_name="system_prompt.txt") -> str:
    try:
        with open(file_name, "r", encoding="utf8") as f:
            prompt = f.read()
            if "{date_str}" in prompt:
                prompt = prompt.replace("{date_str}", date_str)
            if "{ai_name}" in prompt:
                prompt = prompt.replace("{ai_name}", "DeepSeek-R1")
        return prompt
    except Exception as e:
        return f"错误：无法加载system prompt文本: {e}"
    
system_prompt = get_system_prompt()  # 从外部txt读取系统提示
# history_len = 30
# history_len = 10
history_len = 15
async def answer_question(question:str, model:str|None=None, change_history=True)->str:
#    config

    global answerer
    if not answerer.is_ok():
        return "错误：网络无法连接后端！"
    global history
    if len(history)>history_len:
        # history = history[-history_len:]
        input_history = history[-history_len:]
    else:
        input_history = history
    print(input_history)
    
    new_history = answerer.predict(question, input_history, system_prompt, model)
    answer = new_history[-1][1]

    if change_history:
        history = new_history

        with open(history_file, 'w') as f:
            json.dump(history, f, ensure_ascii=False, indent=4)
            
    return answer

from nonebot.adapters.onebot.v11 import MessageSegment, Message, Bot


async def answer_with_forward(answer:str, bot:Bot, threshold:int=100, nickname=None)->Message:
    if nickname is None:
        nickname = answerer.answer_model_name + "--智子"
    # 如果answer太长，使用QQ引用信息框包裹
    if len(answer) > threshold:  # 可根据需要调整阈值
        answer = MessageSegment.node_custom(2854196310, nickname, 
                                            answer)
        res_id = await bot.call_api("send_forward_msg", messages=Message(answer))
        return Message(MessageSegment.forward(res_id))
    else:
        return Message(answer)

# 新增函数：提取 <think></think> 内的内容并单独发送，同时返回处理后的answer
import re
async def send_think_segments(answer: str, bot: Bot, sender) -> str:
    for think_name in ['think', '思考', 'thought']:
        think_parts = re.findall(rf'<{think_name}>(.*?)</{think_name}>', answer, flags=re.DOTALL)
        if think_parts:
            for part in think_parts:
                str_think = "深度思考：" + part.strip()
                message = await answer_with_forward(str_think, bot)
                await asyncio.sleep(random.uniform(0, 3))
                await sender.send(message)
            answer = re.sub(rf'<{think_name}>.*?</{think_name}>', '', answer, flags=re.DOTALL)
    return answer.strip()

@talker.handle()
async def talk(args: Message = CommandArg(),
                event: PrivateMessageEvent | GroupMessageEvent = None,
                bot: Bot = None):
    # 构造回复内容
    if question := args.extract_plain_text():

        # 抽奖对比一个随机模型
        answer = await answer_question(question, model="rand-alt", change_history=False)
        answer = await send_think_segments(answer, bot, talker)
        answer = f"{answer} ({answerer.answer_model_name}--智子回答)"
        message = await answer_with_forward(answer, bot)
        await talker.send(message)

        await asyncio.sleep(random.uniform(0, 1))   

        # prefer的模型
        answer = await answer_question(question)
        # 使用 send_think_segments 函数处理 <think></think> 逻辑
        answer = await send_think_segments(answer, bot, talker)
        answer = f"{answer} ({answerer.answer_model_name}--智子回答)"
        message = await answer_with_forward(answer, bot)
        await talker.finish(message)
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
        # 使用 send_think_segments 函数处理 <think></think> 逻辑
        answer = await send_think_segments(answer, bot, welcom)
        await asyncio.sleep(random.uniform(0, 3))
        
        await welcom.finish(await answer_with_forward(answer, bot))

