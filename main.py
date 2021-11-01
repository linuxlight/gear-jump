# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import sys
from PyQt6.QtWidgets import QApplication

from gear import Gear, GearGroup

# front_list = [22, 30, 40]
from main_window import MainWindow

front_list = [26, 36, 48]
back_list = [11, 12, 14, 16, 18, 22, 24, 28, 32, 36]

current_gear = None

def gear_difference(current: Gear, target: Gear):
    current_front = None
    current_back = None
    target_front = None
    target_back = None
    for i, front in enumerate(front_list):
        if front == current.front:
            current_front = i
            break
    for i, back in enumerate(back_list):
        if back == current.back:
            current_back = i
            break
    for i, front in enumerate(front_list):
        if front == target.front:
            target_front = i
            break
    for i, back in enumerate(back_list):
        if back == target.back:
            target_back = i
            break
    print(current_front, current_back, target_front, target_back)
    diff_front = current_front - target_front
    diff_back = current_back - target_back
    return diff_front, diff_back


def select_gear(current, target_stage, group_list):
    min_diff = 1000000
    target_gear = None
    for gear_group in group_list:
        if target_stage == gear_group.group_index:
            for gear in gear_group.gear_list:
                front_diff, back_diff = gear_difference(current, gear)
                print(gear)
                print(f"[필요 변경횟수] 앞: {front_diff} 뒤: {back_diff}")
                if min_diff > abs(front_diff) + abs(back_diff):
                    min_diff = abs(front_diff) + abs(back_diff)
                    target_gear = gear
            break
    return target_gear


def get_average(gear_list):
    diff_list = []
    for i in range(len(gear_list)-1):
        diff_list.append(gear_list[i + 1].torque - gear_list[i].torque)
    return sum(diff_list)/len(diff_list)


def get_gear_list():
    gear_list = []
    for f, front in enumerate(front_list):
        for b, back in enumerate(back_list):
            gear_list.append(Gear(front, back, round(back / front, 3)))
    gear_list.sort(key=lambda x: x.torque)
    return gear_list


def get_group_list(gear_list):
    group_list = []
    group = None
    current_first = None
    group_index = 1
    for gear in gear_list:
        if not group:
            group = GearGroup()
            current_first = gear.torque
        # 체인 각도 가장 큰 두 개만 제외
        if not ((gear.front == front_list[0] and gear.back == back_list[0]) or
                (gear.front == front_list[-1] and gear.back == back_list[-1])):
            if gear.torque - current_first > avg:
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


if __name__ == '__main__':
    current_gear = Gear(36, 22, round(22 / 36, 3))
    gears = get_gear_list()
    avg = get_average(gears)
    groups = get_group_list(gears)
    i = 0
    for group in groups:
        print(f"{group.group_index} 단계")
        for gear in group.gear_list:
            print(gear)
            i += 1
        print()
    print("총 기어 조합 수 : ", i)
    target_stage = 5
    print(select_gear(current_gear, target_stage, groups))

    target_stage = 7
    print(select_gear(current_gear, target_stage, groups))

    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())


