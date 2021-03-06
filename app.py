import sys

from db_manager import DatabaseManager
from gear import Gear, GearGroup


class MainApp:
    def __init__(self, front_pos: int, back_pos: int):
        # self.front_list = [30, 40, 50]
        # self.back_list = [28, 24, 21, 19, 17, 15, 14, 13, 12, 11]
        self.db_mgr = DatabaseManager()
        self.db_mgr.init_tables()
        self.front_list = self.db_mgr.get_gears("front")
        self.rear_list = self.db_mgr.get_gears("rear")
        self.__current_gear = Gear(
            front_pos - 1,
            back_pos - 1,
            self.front_list[front_pos - 1],
            self.rear_list[back_pos - 1]
        )
        self.__current_front_idx = self.__current_gear.front_idx
        self.__current_back_idx = self.__current_gear.back_idx
        self.__current_stage = None
        self.groups = None  # GearGroup들의 리스트
        self.total_groups: int = 0
        self.build_groups()
        self.set_current_stage()
        self.print_groups()

    def build_groups(self):
        """ GearGroup들의 리스트인 groups를 초기화합니다. """
        gears = self.__build_gear_list()
        for g in gears:
            print(g)
        avg = self.__get_torque_average(gears)
        print("전체 기어비 차이의 평균:", avg)
        self.groups = self.__build_group_list(gears, avg)
        self.total_groups = len(self.groups)

    def print_groups(self):
        """ GearGroup들의 리스트인 groups에 속한 Gear들을 단계별로 출력합니다. """
        i = 0
        for group in self.groups:
            print(f"{group.group_index} 단계")
            for gear in group.gear_list:
                print(gear)
                i += 1
            print()
        print("총 기어 조합 수 : ", i)

    def select_gear(self, target_stage: int):
        """ target_stage에 소속된 Gear 중 필요 변경횟수(Cost)가 가장 적은 Gear를 선택하여 반환합니다. """
        min_diff = sys.maxsize
        target_gear = None
        for gear_group in self.groups:
            if target_stage == gear_group.group_index:
                for gear in gear_group.gear_list:
                    print(gear)
                    front_diff, back_diff = self.get_difference(gear)
                    need_diff = abs(front_diff) + abs(back_diff)
                    if min_diff > need_diff:
                        min_diff = need_diff
                        target_gear = gear
                break
        return target_gear

    def set_current_gear(self, gear: Gear):
        self.__current_gear = gear
        self.set_front_idx(gear.front_idx)
        self.set_back_idx(gear.back_idx)
        print("[변경된 기어]", self.__current_gear)

    def get_current_gear(self):
        return self.__current_gear

    def set_current_stage(self):
        for i, gear_group in enumerate(self.groups):
            for gear in gear_group.gear_list:
                if self.__current_gear.front == gear.front and self.__current_gear.back == gear.back:
                    self.__current_stage = i + 1
                    break

    def get_current_stage(self):
        return self.__current_stage

    def __build_gear_list(self):
        """ front_list와 back_list를 조합하여 Gear 객체 리스트를 생성 후 반환합니다. """
        gear_list = []
        for f, front in enumerate(self.front_list):
            for b, back in enumerate(self.rear_list):
                gear_list.append(Gear(f, b, front, back))
        gear_list.sort(key=lambda x: x.torque)
        return gear_list

    @staticmethod
    def __get_torque_average(gear_list):
        """ gear_list의 인접한 두 Gear간의 토크값의 차이들로부터 평균값을 산출합니다. """
        diff_list = []
        for i in range(len(gear_list) - 1):
            diff_list.append(gear_list[i + 1].torque - gear_list[i].torque)
        return sum(diff_list) / len(diff_list)

    def __build_group_list(self, gear_list, torque_avg):
        """ gear_list의 Gear들의 토크값 차이로부터 단계별 그룹을 형성합니다.

            이때 각 그룹별 최초 gear의 토크값과 마지막 gear의 토크값의 차이는 전체 토크값 차이의 평균을 넘지 않습니다.
        """
        group_list = []
        group = None
        current_first = None
        group_index = 1
        for gear in gear_list:
            if not group:
                group = GearGroup()
                current_first = gear.torque
            # 체인 각도 가장 큰 두 개만 제외
            if not ((gear.front == self.front_list[0] and gear.back == self.rear_list[-1]) or
                    (gear.front == self.front_list[-1] and gear.back == self.rear_list[0])):
                if gear.torque - current_first > torque_avg:
                    current_first = gear.torque
                    group.set_index(group_index)
                    group_list.append(group)
                    group = GearGroup()
                    group.append_gear(gear)
                    group_index += 1
                else:
                    group.append_gear(gear)
        group.set_index(group_index)
        group_list.append(group)
        return group_list

    def get_difference(self, target: Gear):
        """ current_gear와 target Gear의 각 front와 back의 차이 (필요 변경횟수)를 구합니다. """
        target_front_idx = None
        target_back_idx = None
        for i, front in enumerate(self.front_list):
            if front == target.front:
                target_front_idx = i
                break
        for i, back in enumerate(self.rear_list):
            if back == target.back:
                target_back_idx = i
                break
        print(self.__current_gear.front_idx, self.__current_gear.back_idx, target_front_idx, target_back_idx)
        diff_front = target_front_idx - self.__current_gear.front_idx
        diff_back = target_back_idx - self.__current_gear.back_idx
        print(f"[필요 변경횟수] 앞: {diff_front} 뒤: {diff_back}")
        return diff_front, diff_back

    def get_front_idx(self):
        return self.__current_front_idx

    def set_front_idx(self, front_idx: int):
        self.__current_front_idx = front_idx

    def get_back_idx(self):
        return self.__current_back_idx

    def set_back_idx(self, back: int):
        self.__current_back_idx = back
