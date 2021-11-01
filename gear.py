from typing import List, Optional


class Gear:

    def __init__(self, front, back, torque):
        self.front = front
        self.back = back
        self.torque = torque

    def __str__(self):
        return f"앞 드레일러:{self.front} 뒷 드레일러:{self.back} 기어비:{self.torque}"


class GearGroup:

    def __init__(self):
        self.total_group: int
        self.group_index: Optional[int] = None
        self.gear_list: List[Gear] = []

    def append_gear(self, gear: Gear):
        self.gear_list.append(gear)

    def set_index(self, num):
        self.group_index = num
