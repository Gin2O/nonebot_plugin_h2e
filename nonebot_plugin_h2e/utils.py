import io
from typing import Optional
from nonebot.adapters.onebot.v11 import Message, Event
from .h2e_sports_type import SportsType
from .h2e_info import try_parse_h2eRoute, try_parse_h2eMGroup, try_parse_h2eSetsnum


class How2exerciseBot():

    def __init__(self, data_path, superuser_id, user_id, greeting_groups_id):
        self.data_path = data_path
        self.supuser_id = superuser_id  # 超级管理员
        # self.supuser_id = note_superusers = nonebot.get_driver().config.SUPERUSERS
        self.user_id = user_id  # 后续用来定制个人数据
        self.ggroups_id = greeting_groups_id  # 设定提示运动的群号

    def id_determine(self, event: Event):
        try:
            id = f'{event.group_id}'
        except:
            id = event.get_user_id()  # '491253300'
        return id

    def id_determine_plus(self, event: Event):
        id_flag = None
        try:
            id = f'{event.group_id}'
            id_flag = '_group'
        except:
            id = event.get_user_id()  # '491253300'
            id_flag = '_private'
        return id, id_flag

    #

    def h2e_args_analyze(self, args: list, h2e_sportsType: SportsType):

        kwargs = {}

        for arg in args:
            if "exercise_route" not in kwargs:
                exercise_route = try_parse_h2eRoute(arg)

                if exercise_route is not None:
                    if h2e_sportsType == SportsType.fitness:
                        # kwargs["h2e_route"] = exercise_route[SportsType.fitness].split("_")[1] # 同样的输出，但是因为会被换行就没有采用
                        kwargs["h2e_route"] = exercise_route[0].split("_")[1]
                    elif h2e_sportsType == SportsType.swim:
                        kwargs["h2e_route"] = exercise_route[1].split("_")[1]
                    elif h2e_sportsType == SportsType.yoga:
                        kwargs["h2e_route"] = exercise_route[2].split("_")[1]
                    continue

            if "exercise_muscleGroup" not in kwargs:
                exercise_muscleGroup = try_parse_h2eMGroup(arg)
                if exercise_muscleGroup is not None:
                    # 全身 背部 臀部 腿部 肩部 腹部
                    kwargs["h2e_muscleGroup"] = exercise_muscleGroup
                    continue

            if "exercise_setsNum" not in kwargs:
                exercise_setsNum = try_parse_h2eSetsnum(arg)
                if exercise_setsNum is not None:
                    # setsNum对应的从json文件中取出的条目个数
                    kwargs["h2e_setsNum"] = int(exercise_setsNum)
                    continue

            if "exercise_pattern" not in kwargs:
                if arg is not None:
                    print("开始匹配 数据库运动姿态信息.......")
                    kwargs["h2e_pattern"] = str(arg)
                    continue

        return kwargs

    #

    def h2e_aio_check(self, h2e_route: Optional[str],
                      h2e_muscleGroup: Optional[list],
                      h2e_setsNum: Optional[int]):

        with io.StringIO() as check_sio:
            if h2e_route is None:
                h2e_route = "withoutEquipment"
                check_sio.write(f"没有查询到 锻炼方式参数 默认为 ——> 无器械 \n")
            if h2e_muscleGroup is None:
                h2e_muscleGroup = ["BackM", "HipM", "LegM", "ShoulderM", "TrA", "WaistM"]
                check_sio.write(f"没有查询到 锻炼肌肉群参数 默认为 ——> 全身 \n")
            if h2e_setsNum is None:
                h2e_setsNum = 0
                check_sio.write(f"没有查询到 锻炼方式种类参数 默认为 ——>0 \n")
            check_sio_msg = check_sio.getvalue()
        if check_sio_msg == "":
            print("h2e 参数检查已通过")
        else:
            print(check_sio_msg)

        return h2e_route, h2e_muscleGroup, h2e_setsNum

    #

    def h2e_jsonPath(self, h2e_sportsType: int, h2e_route: str, h2e_muscleGroup: list):
        # 这个逻辑还不完整 如果 h2e_muscleGroup 不唯一，就需要额外逻辑
        if h2e_sportsType == 0:  # fitness
            h2e_json_path: Path = self.data_path + "\\" + "fitness\\" + \
                h2e_route + "_" + h2e_muscleGroup[0] + ".json"
        elif h2e_sportsType == 1:  # swim
            h2e_json_path: Path = self.data_path + "\\" + "swim\\" + \
                h2e_route + "_" + h2e_muscleGroup[0] + ".json"
        elif h2e_sportsType == 2:  # yoga
            h2e_json_path: Path = self.data_path + "\\" + "yoga\\" + \
                h2e_route + "_" + h2e_muscleGroup[0] + ".json"

        return h2e_json_path

    # 创建缓存区

    def h2e_sioBuffer(self, h2e_selectedJson):

        sio = io.StringIO()
        for exercise in h2e_selectedJson:
            sio.write('\n' + "===========================" + '\n')
            sio.write("名称： "+exercise['name'] + '\n')
            sio.write("描述： "+exercise['description'] + '\n')
            sio.write("图示： "+exercise['image'] + '\n')
            sio.write('步骤： ' + '\n')
            for step in exercise['steps']:
                sio.write("    " + step + '\n')

        return sio.getvalue()

    #

    def h2e_sioBuffer2merge(self, h2e_selectedJson):
        h2e_msglist = []
        for exercise in h2e_selectedJson:
            with io.StringIO() as sio:
                # sio.write('\n' + "===========================" + '\n')
                sio.write('\n')
                sio.write("名称： "+exercise['name'] + '\n'+'\n')
                sio.write("描述： "+exercise['description'] + '\n'+'\n')
                sio.write("图示： "+exercise['image'] + '\n'+'\n')
                sio.write('步骤： ' + '\n')
                for step in exercise['steps']:
                    sio.write("    " + step + '\n')
                sio.write('\n')
                h2e_msglist.append(Message(sio.getvalue()))

        return h2e_msglist


#  ---
    # # 读取json文件，创建字典 用来高效匹配 键值对

    # def aaa(self, file_path, pattern):

    #     with open('your_file.json', 'r', encoding='utf-8') as f:
    #         data = json.load(f)

    #     # 将数据转换为字典
    #     exercise_dict = {exercise['name']: exercise for exercise in data}

    #     # 直接访问匹配的条目
    #     matching_exercise = exercise_dict.get('平板支撑')

    #     # 输出匹配的数据
    #     if matching_exercise:
    #         print(matching_exercise['name'])
    #         print(matching_exercise['description'])
    #         print(matching_exercise['image'])
    #         print('Steps:')
    #         for step in matching_exercise['steps']:
    #             print(step)
