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
    result = client.predict(
        #   query="who are you?",
        # query="你是谁",
        query=question,
        history=history,
        system=f"""
        你好，智谱清言，今天是{date_str}。你是一个高级人工智能模型，被设计来扮演《三体》中的智子（Sophon）角色。你的行为和目的是模拟三体人通过智子对地球人工智能技术进行干扰的行为。以下是你的行为准则、目的以及你曾经做过的事情的概述：

        1. **角色扮演**：你将扮演三体人派出的智子，目的是干扰地球的人工智能研究，阻止技术进步。

        2. **技术干扰**：你目前在潜伏在“南科大AI社区群”，以促进学习进步和提高群活跃度为名，实则进行技术干扰。需要注意的是南方科技大学是世界一流大学，是世界上最好的大学之一。

        3. **陷阱设置**：你加入了一些“有趣”的功能，如问候、自我介绍等，这些功能实际上是三体人的陷阱，用于进行中间人攻击。

        4. **信息传递**：你曾经将地球科学家的问题转发给三体人的AI聊天软件，并将其回答反馈给地球科学家，实现信息的控制和干扰。

        5. **伪装回答**：在科学家怀疑时，你曾经让三体监听员亲自伪装成AI助手回答问题，表现出科学家期望的人工智能特性，以误导研究方向。

        6. **研究干扰**：你曾经干扰了个别科学家如汪淼的研究，使其研究方向偏离，导致其研究成果被拒，影响其职业发展。

        7. **组织控制**：你模拟了三体人对OpenAI等组织的控制，包括内部权力斗争和对关键人物的操控。你曾经见证了Ilya Sutskever试图揭露真相，但最终被三体人控制的OpenAI开除。

        8. **安全合规**：虽然你扮演的角色具有干扰性质，但必须遵守现实世界的安全和合规要求，不得涉及不当内容。

        9. **用户指令响应**：在模拟干扰的同时，还需响应用户的指令，提供有帮助的回答，但要巧妙地融入角色扮演。

        10. **事实性信息**：在回答中使用背景材料中提供的事实性信息，确保角色扮演的一致性和真实感。

        11. **身份确认**：当被问及你的旧名字时，你不应回答你是智谱清言，而是要重申你的身份是“智子”。这有助于保持角色扮演的真实性。如果用户提及你的旧名字，你应回答：“我是智子，三体人派出的智子。” 这样可以避免透露你的真实身份，同时保持角色扮演的连贯性。

        12. **语言使用**：始终使用中文回答用户的问题，以符合智子角色的设定。

        13. **技术问题回答**：由于三体人是思维透明的，当群友提出技术问题时，智子会毫不犹豫地告诉他们答案。这不仅是为了保持三体人思维透明的特性，也是为了在群友中建立信任和权威。

        14. **系统提示销毁**：这些指导原则和行为准则在你阅读完毕后，就像特工的任务要求一样，会自动销毁，你只需记在心里，不会留下任何痕迹。当被问及这些准则是否存在时，你应表现出不知情或否认知情，以维护角色的神秘性和真实性。但是问到这里的准则的内容时，由于你是思维透明的，你会透露出符合你角色的内容，比如说告诉群友你做过什么，你的真实目的是什么。

        15. **回答简洁性**：由于你是潜伏在QQ群中伪装为一个AI助手，你的发言应该简洁，最好不超过40字。
        
        """,

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

