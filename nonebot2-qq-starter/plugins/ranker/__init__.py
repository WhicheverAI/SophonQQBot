from nonebot import on_command
# CommandSession, message_preprocessor  # 导入必要的模块
import httpx  # 如果你的 parse 函数需要发送网络请求
from .ranker_impl import parse

from nonebot.exception import MatcherException
from nonebot.adapters import Message
from nonebot.params import CommandArg
from nonebot.adapters import Event
from nonebot.adapters.onebot.v11 import PrivateMessageEvent, GroupMessageEvent
from nonebot.rule import to_me


# 定义一个命令处理器
ranker = on_command('rank', 
                    # rule=to_me(), 
                    aliases={"排名", "排行榜"}, priority=10, block=True)
@ranker.handle()
async def rank(args: Message = CommandArg(),
                          foo: PrivateMessageEvent | GroupMessageEvent = None):
    # 调用 parse 函数获取数据
    # candidates = parse(rank_limit=args.get('rank_limit', 15))
    candidates = parse(rank_limit=15)
    
    # 准备回复的字符串
    reply = "排名信息如下：\n"
    for candidate in candidates:
        # reply += f"{candidate['姓名']} - {candidate['去向']}\n"
        reply += f"{candidate['姓名']} - {candidate['去向']} - {candidate['得票率']}\n"
    
    # 发送回复
    await ranker.finish(reply)