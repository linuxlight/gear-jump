from typing import List, Optional


class Gear:

    def __init__(self, f_idx, b_idx, front, back):
        self.front = front
        self.back = back
        self.front_idx = f_idx
        self.back_idx = b_idx
        self.torque = round(front / back, 3)

    def __str__(self):
        return f"앞 드레일러:{self.front} 뒷 드레일러:{self.back} 기어비:{self.torque}"


class GearGroup:

    def __init__(self):
        self.group_index: Optional[int] = None
        self.gear_list: List[Gear] = []

    def append_gear(self, gear: Gear):
        self.gear_list.append(gear)

    def set_index(self, num):
        self.group_index = num
