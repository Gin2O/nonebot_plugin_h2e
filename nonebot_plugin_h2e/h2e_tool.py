import json
import re
import random
import io


# 精确匹配 tag
def exact_match_exercises_tag(file_path, tag, pattern):

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)  # 读取 JSON 文件

    matching_exercises = [exercise for exercise in data if exercise[f'{tag}'] == pattern]

    return matching_exercises


# 模糊匹配
def fuzzy_match_exercises(file_path, tags: list, pattern):
    # tags = ['name', 'description']
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)  # 读取 JSON 文件

    # 使用正则表达式模糊匹配名称或描述中包含模式的条目
    regex_pattern = re.compile(f'.*{pattern}.*', re.IGNORECASE)

    if tags.__len__() == 1:
        matching_exercises = [
            exercise for exercise in data
            if regex_pattern.search(exercise[tags[0]])
        ]
    elif tags.__len__() == 2:
        matching_exercises = [
            exercise for exercise in data
            if regex_pattern.search(exercise[tags[0]]) or regex_pattern.search(exercise[tags[1]])
        ]

    return matching_exercises


# 随机获得json结构块
def get_random_exercises(file_path, h2e_setsNum):

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    random_data = random.sample(data, k=h2e_setsNum)

    return random_data


__numerals = {'零': 0, '一': 1, '二': 2, '两': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9, '十': 10,
              '百': 100, '千': 1000, '万': 10000, '亿': 100000000}


def decode_chinese_integer(text: str) -> int:
    """
    将中文整数转换为int
    :param text: 中文整数
    :return: 对应int
    """
    ans = 0
    radix = 1
    for i in reversed(range(len(text))):
        if text[i] not in __numerals:
            raise ValueError(text)
        digit = __numerals[text[i]]
        if digit >= 10:
            if digit > radix:  # 成为新的基数
                radix = digit
                if i == 0:  # 若给定字符串省略了最前面的“一”，如十三、十五……
                    ans = ans + radix
            else:
                radix = radix * digit
        else:
            ans = ans + radix * digit

    return ans


def decode_integer(text: str) -> int:
    try:
        return int(text)
    except ValueError:
        pass

    return decode_chinese_integer(text)
