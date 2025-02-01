from nonebot import get_driver
from nonebot.plugin import PluginMetadata

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="weather",
    description="",
    usage="",
    config=Config,
)

global_config = get_driver().config
config = Config.parse_obj(global_config)

# 1. 首先我们需要得到事件响应器，告诉nonebot我们的插件对什么事件感兴趣
from nonebot import on_command
weather = on_command("天气") # 这样，我们就获得一个名为 weather 的事件响应器了，这个事件响应器会对 /天气 开头的消息进行响应。
# 提示：如果一条消息中包含“@机器人”或以“机器人的昵称”开始，例如 @bot /天气 时，协议适配器会将 event.is_tome() 判断为 True ，同时也会自动去除 @bot，即事件响应器收到的信息内容为 /天气，方便进行命令匹配。

from nonebot.rule import to_me

weather = on_command("天气", rule=to_me(), aliases={"weather", "查天气"}, priority=10, block=True)
# 这样，我们就获得了一个可以响应 天气、weather、查天气 三个命令，
# 需要私聊或 @bot 时才会响应，
# 优先级为 10 ，阻断事件传播的事件响应器了。 
# 什么是阻断事件传播？简单来说，就是当事件响应器响应了事件后，不再传播给其他事件响应器。

# 2. 有了感兴趣的事件，接下来定义如何响应这些事件
# 在事件响应器对一个事件进行响应之后，会依次执行一系列的事件处理依赖（通常是函数），包括函数形式的“事件处理依赖”（下称“事件处理函数”）和“事件响应器操作”。

# 在事件响应器中，事件处理流程可以由一个或多个“事件处理函数”组成，这些事件处理函数将会按照顺序依次对事件进行处理，直到全部执行完成或被中断。我们可以采用事件响应器的“事件处理函数装饰器”来添加这些“事件处理函数”。

from nonebot.exception import MatcherException
from nonebot.adapters import Message
from nonebot.params import CommandArg
from nonebot.adapters import Event
from nonebot.adapters.onebot.v11 import PrivateMessageEvent, GroupMessageEvent
# 2.1 将handle_function添加到了weather的回调之中
# ？如果我想让同一个函数处理多个事件，会出bug吗？
@weather.handle()
# async def handle_function(): # 可以没有参数
async def handle_function(args: Message = CommandArg(),
                          foo: PrivateMessageEvent | GroupMessageEvent = None):
    pass  # do something here
    print("args=", args)
    print("foo=", foo)
    # 2.3 获取事件信息  通过 依赖注入 方式
    # 通过依赖注入获取信息的最大特色在于按需获取。不获取的话就不用信息也能跑，需要获取那就有这个信息。
    # 提取参数纯文本作为地名，并判断是否有效
    if location := args.extract_plain_text():
        await weather.finish(f"今天{location}的天气是...")
    else:
        await weather.finish("请输入地名")
    
    
    # 2.2 事件响应器weather有一些Matcher类方法可以使用，被称为“事件响应器操作”
    await weather.send("智子思考中...") # 这个会发送但是不结束流程。
    try:
        await weather.finish("天气是...") # 这个会结束处理流程，会抛出 FinishedException 异常来结束，这段代码后面的操作不会执行。
    except MatcherException as e:
        raise e # 优先捕获 MatcherException （包括 FinishedException ）， 插件不应该处理
    except Exception as e:
        pass # 其他的插件有关的异常可以处理。
