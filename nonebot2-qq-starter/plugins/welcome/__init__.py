
# # 群友退群
# @welcom.handle()
# async def h_r(bot: Bot, event: GroupDecreaseNoticeEvent, state: T_State):  # event: GroupDecreaseNoticeEvent  群成员减少事件
#     user = event.get_user_id()  # 获取新成员的id
#     at_ = "[CQ:at,qq={}]".format(user)
#     msg = at_ + '勇士离开了本群，大家快出来送别它吧！'
#     msg = Message(msg)
#     print(at_)

#     if event.group_id == QQ群号:
#         await welcom.finish(message=Message(f'{msg}'))  # 发送消息
