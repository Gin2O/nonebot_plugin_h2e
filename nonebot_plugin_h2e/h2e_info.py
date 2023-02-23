from typing import Optional

from .h2e_tool import *


_H2E_ROUTE_REVERSED_MAPPING = {
    # 对应文件命名规则
    "有器械": ["fitness_withEquipment", "swim_withEquipment", "yoga_withEquipment"],
    "无器械": ["fitness_withoutEquipment", "swim_withoutEquipment", "yoga_withoutEquipment"],
    "无支撑": ["fitness_withEquipment", "swim_withEquipment", "yoga_withEquipment"],
}


_H2E_ROUTE_REVERSED_MAPPING["with"] = _H2E_ROUTE_REVERSED_MAPPING["有器械"]
_H2E_ROUTE_REVERSED_MAPPING["without"] = _H2E_ROUTE_REVERSED_MAPPING["无器械"]
_H2E_ROUTE_REVERSED_MAPPING["none"] = _H2E_ROUTE_REVERSED_MAPPING["无支撑"]


# exercise_muscleGroup
# BackM / HipM / LegM / ShoulderM / TrA / WaistM
_H2E_MGROUP_REVERSED_MAPPING = {
    "全": ["BackM", "HipM", "LegM", "ShoulderM", "TrA", "WaistM"],
    "背": ["BackM"],
    "臀": ["HipM"],
    "腿": ["LegM"],
    "肩": ["ShoulderM"],
    "腹": ["TrA"],
    "腰": ["WaistM"],
}
_H2E_MGROUP_REVERSED_MAPPING["全身"] = _H2E_MGROUP_REVERSED_MAPPING["全"]
_H2E_MGROUP_REVERSED_MAPPING["背部"] = _H2E_MGROUP_REVERSED_MAPPING["背"]
_H2E_MGROUP_REVERSED_MAPPING["臀部"] = _H2E_MGROUP_REVERSED_MAPPING["臀"]
_H2E_MGROUP_REVERSED_MAPPING["腿部"] = _H2E_MGROUP_REVERSED_MAPPING["腿"]
_H2E_MGROUP_REVERSED_MAPPING["肩部"] = _H2E_MGROUP_REVERSED_MAPPING["肩"]
_H2E_MGROUP_REVERSED_MAPPING["腹部"] = _H2E_MGROUP_REVERSED_MAPPING["腹"]
_H2E_MGROUP_REVERSED_MAPPING["腰部"] = _H2E_MGROUP_REVERSED_MAPPING["腰"]


def try_parse_h2eRoute(raw: str) -> Optional[str]:
    return _H2E_ROUTE_REVERSED_MAPPING.get(raw, None)


def try_parse_h2eMGroup(raw: str) -> Optional[list]:
    return _H2E_MGROUP_REVERSED_MAPPING.get(raw, None)


def try_parse_h2eSetsnum(raw: str) -> Optional[int]:
    result = re.match(r"^来(.*)种$$", raw)

    if result is not None:
        sets_num = result.group(1)
        try:
            sets_num = decode_integer(sets_num)
        except ValueError:
            return None

        if (sets_num < 0) & (sets_num > 20):
            raise BadRequestError("花样不合法")

        return sets_num

    return None
