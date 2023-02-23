import aiohttp
import asyncio
import nonebot

from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.internal.adapter import Event
from nonebot.internal.matcher import Matcher
from nonebot.adapters.onebot.v11 import Bot, Message
from nonebot.plugin import PluginMetadata

from asyncio import wait_for
from io import StringIO
from typing import Optional

from .utils import *
from .h2e_sports_type import SportsType
from .h2e_tool import (exact_match_exercises_tag,
                       fuzzy_match_exercises,
                       get_random_exercises)


from os import path, makedirs
import os

# 命令提示助手

__plugin_meta__ = PluginMetadata(
    name="今天练什么",
    description="根据随意编造的数据查询相关运动动作的信息",
    usage=(
        f"1. 合并转发形式：私聊/群聊 （可提供随机<数量>的运动方法和模糊匹配）\n \n"
        f"   /fitness <锻炼方式> <目标肌群> <[来<数量>种]|[<运动方法>|<关键字>]> \n"
        f"   /swim    <锻炼方式> <目标肌群> <[来<数量>种]|[<运动方法>|<关键字>]> \n"
        f"   /yoga    <锻炼方式> <目标肌群> <[来<数量>种]|[<运动方法>|<关键字>]> \n \n"

        f"2. 长文刷屏形式：私聊/群聊 （可提供随机<数量>的运动方法和精确匹配） \n \n"
        f"   /fitnessL <锻炼方式> <目标肌群> <[来<数量>种]|[<运动方法>]> \n"
        f"   /swimL    <锻炼方式> <目标肌群> <[来<数量>种]|[<运动方法>]> \n"
        f"   /yogaL    <锻炼方式> <目标肌群> <[来<数量>种]|[<运动方法>]> \n \n"

        f"以上命令格式中，以< >包裹的表示一个参数，以[ ]包裹的表示一个可选项。 \n \n"
        f" 锻炼方式 = [有器械] | [无器械] | [无支持] \n"
        f" 目标肌群 = [全身] | [背部] | [腿部] | [肩部] | [腹部] | [腰部] \n"

        f" 详细说明：参见姜Bot的大脑 \n"

    ),
)

filepath = os.path.dirname(__file__)
data_path = os.path.join(filepath, r"resource")

superuser_id = None
user_id = None
ggroups_id = None

# 实例化
h2eBot = How2exerciseBot(data_path, superuser_id, user_id, ggroups_id)

h2e_help = on_command("/h2e_help", aliases={"/如何锻炼"},
                      block=True, priority=5)


@h2e_help.handle()
async def _(msg: Message = CommandArg()):
    await h2e_help.finish(__plugin_meta__.usage)


def h2e_handler2merge(h2e_sportsType: SportsType, merge: bool):
    async def h2e_info(bot: Bot, matcher: Matcher, event: Event):
        args = event.get_message().extract_plain_text().split()
        cmd, args = args[0], args[1:]
        kwargs = {}

        if merge:
            if len(args) == 0:
                await matcher.finish(
                    f"合并转发形式：私聊/群聊 （可提供随机<数量>的运动方法和模糊匹配）\n \n"
                    f"   /fitness <锻炼方式> <目标肌群> <[来<数量>种]|[<运动方法>|<关键字>]> \n"
                    f"   /swim    <锻炼方式> <目标肌群> <[来<数量>种]|[<运动方法>|<关键字>]> \n"
                    f"   /yoga    <锻炼方式> <目标肌群> <[来<数量>种]|[<运动方法>|<关键字>]> \n \n"
                    f" 详细说明：参见 /h2e_help （/swim & /yoga 部分未完成）\n"
                    f" 提示： 唤出参数还有 /h2e_f /h2e_s /h2e_y \n"
                )
            else:
                kwargs = h2eBot.h2e_args_analyze(args, h2e_sportsType)
            coro = handle_h2e_info2merge(bot, matcher, event,
                                         h2e_sportsType, **kwargs)
        else:
            if len(args) == 0:
                await matcher.finish(
                    f"长文刷屏形式：私聊/群聊 （可提供随机<数量>的运动方法和精确匹配） \n \n"
                    f"   /fitnessL <锻炼方式> <目标肌群> <[来<数量>种]|[<运动方法>]> \n"
                    f"   /swimL    <锻炼方式> <目标肌群> <[来<数量>种]|[<运动方法>]> \n"
                    f"   /yogaL    <锻炼方式> <目标肌群> <[来<数量>种]|[<运动方法>]> \n \n"
                    f" 详细说明：参见 /h2e_help  （/swim & /yoga 部分未完成）\n"
                    f" 提示： 唤出参数还有 /h2e_fL /h2e_sL /h2e_yL \n"
                )
            else:
                kwargs = h2eBot.h2e_args_analyze(args, h2e_sportsType)

            coro = handle_h2e_info(bot, matcher, event,
                                   h2e_sportsType, **kwargs)

        await wait_for(coro, timeout=15.0)

    return h2e_info


# ====================================================================================


# SportsType.fitness
h2e_merge_0 = on_command("/h2e_f", aliases={"/fitness"})
h2e_merge_info_0 = h2e_handler2merge(SportsType.fitness, True)
h2e_merge_0.append_handler(h2e_merge_info_0)


# # SportsType.swim
# h2e_merge_1 = on_command("/h2e_s", aliases={"/swim"})
# h2e_merge_info_1 = h2e_handler2merge(SportsType.swim, True)
# h2e_merge_1.append_handler(h2e_merge_info_1)


# # SportsType.yoga
# h2e_merge_2 = on_command("/h2e_y", aliases={"/yoga"})
# h2e_merge_info_2 = h2e_handler2merge(SportsType.yoga, True)
# h2e_merge_2.append_handler(h2e_merge_info_2)


# SportsType.fitness  Long
h2e_long_0 = on_command("/h2e_fL", aliases={"/fitnessL"})
h2e_long_info_0 = h2e_handler2merge(SportsType.fitness, False)
h2e_long_0.append_handler(h2e_long_info_0)


# # SportsType.swim  Long
# h2e_long_1 = on_command("/h2e_sL", aliases={"/swimL"})
# h2e_long_info_1 = h2e_handler2merge(SportsType.swim, False)
# h2e_long_1.append_handler(h2e_long_info_1)


# # SportsType.yoga  Long
# h2e_long_2 = on_command("/h2e_yL", aliases={"/yogaL"})
# h2e_long_info_2 = h2e_handler2merge(SportsType.yoga, False)
# h2e_long_2.append_handler(h2e_long_info_2)


# （合并）调用并组合 json 信息
async def handle_h2e_info2merge(bot: Bot, matcher: Matcher, event: Event,
                                h2e_sportsType: SportsType, *,
                                # 这个参数好像没用
                                exercise_route: Optional[str] = None,
                                h2e_route: Optional[str] = None,
                                h2e_muscleGroup: Optional[list] = None,
                                h2e_setsNum: Optional[int] = None,
                                h2e_pattern: Optional[str] = None):

    h2e_route, h2e_muscleGroup, h2e_setsNum = \
        h2eBot.h2e_aio_check(h2e_route, h2e_muscleGroup, h2e_setsNum)

    # 如果只调用一个json文件 并且随机获取数据
    id, id_flag = h2eBot.id_determine_plus(event)

    if len(h2e_muscleGroup) == 1:
        h2e_json_path = h2eBot.h2e_jsonPath(h2e_sportsType, h2e_route, h2e_muscleGroup)

        msg_list = []
        if h2e_setsNum == 0:
            tags = ['name', 'description']
            h2e_matching = fuzzy_match_exercises(h2e_json_path, tags, h2e_pattern)
            msg_list = h2eBot.h2e_sioBuffer2merge(h2e_matching)
        else:
            h2e_random = get_random_exercises(h2e_json_path, h2e_setsNum)
            msg_list = h2eBot.h2e_sioBuffer2merge(h2e_random)

        msgs = []
        for msg in msg_list:
            msgs.append({
                'type': 'node',
                'data': {
                    'name': 'Gin2O',
                    'uin': bot.self_id,
                    'content': msg
                }
            })

        msgs_split = []
        for i in range(0, len(msgs), 100):
            msgs_split.append(msgs[i:i + 100])

        for i in msgs_split:
            if id_flag == '_group':
                await bot.call_api('send_group_forward_msg', group_id=id, messages=i)
            else:
                await bot.call_api('send_private_forward_msg', user_id=id, messages=i)

    else:  # 如果调用对应运动的所有json文件 并且随机获取数据，还不太会写
        await matcher.send("\nPS：全身锻炼的数据尚未完全建立！ 请使用其他关键字")
        # if id_flag == '_group':
        #     # await bot.send_group_forward_msg(group_id=id, messages=Message("PS：全身锻炼的数据尚未完全建立！ 请使用其他关键字"))
        # else:
        #     # await bot.send_private_forward_msg(user_id=id, messages=Message("PS：全身锻炼的数据尚未完全建立！ 请使用其他关键字"))


# ==========================================================================================


# （长文）调用并组合 json 信息
async def handle_h2e_info(bot: Bot, matcher: Matcher, event: Event,
                          h2e_sportsType: SportsType, *,
                          # 这个参数好像没用
                          exercise_route: Optional[str] = None,
                          h2e_route: Optional[str] = None,
                          h2e_muscleGroup: Optional[list] = None,
                          h2e_setsNum: Optional[int] = None,
                          h2e_pattern: Optional[str] = None):

    h2e_route, h2e_muscleGroup, h2e_setsNum = \
        h2eBot.h2e_aio_check(h2e_route, h2e_muscleGroup, h2e_setsNum)

    with StringIO() as sio:
        # 如果只调用一个json文件 并且随机获取数据
        if len(h2e_muscleGroup) == 1:
            h2e_json_path = h2eBot.h2e_jsonPath(h2e_sportsType, h2e_route, h2e_muscleGroup)
            print(h2e_json_path)
            if h2e_setsNum == 0:
                h2e_matching = exact_match_exercises_tag(h2e_json_path, "name", h2e_pattern)
                sio.write(h2eBot.h2e_sioBuffer(h2e_matching))
            else:
                h2e_random = get_random_exercises(
                    h2e_json_path, h2e_setsNum)
                sio.write(h2eBot.h2e_sioBuffer(h2e_random))
        else:
            sio.write("\nPS：全身锻炼的数据尚未完全建立！ 请使用其他关键字")

        await matcher.send(sio.getvalue())


# ==========================================================================================
