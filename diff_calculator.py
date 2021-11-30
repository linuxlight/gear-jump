import time
import platform

if platform.system() == "Darwin":
    from PyQt6.QtCore import pyqtSignal, QThread
else:
    from PyQt5.QtCore import pyqtSignal, QThread

from app import MainApp
from gear import Gear


class GearDiffCalculator(QThread):
    updateFront = pyqtSignal(int)
    updateRear = pyqtSignal(int)
    finished = pyqtSignal(Gear, int)

    def __init__(self, app: MainApp):
        super().__init__()
        self.app = app
        self.front_diff = None
        self.back_diff = None
        self.target_gear = None
        self.target_stage = None

    def set_diff(self, front_diff, back_diff, target_gear, target_stage):
        self.front_diff = front_diff
        self.back_diff = back_diff
        self.target_gear = target_gear
        self.target_stage = target_stage

    def __update_gear(self):
        print(f"\n\n지금 기어 상태:", self.app.get_front_idx(), self.app.get_back_idx())
        if self.back_diff == 0:  # 뒷 드레일러 바꿀 필요 없으면
            # 그냥 앞에만 순차적으로 변경
            self.change_front(self.front_diff)
        else:               # 뒷 드레일러를 변경할 필요가 있는가?
            if self.front_diff == 0:     # 앞드레일러를 변경할 필요가 없으면
                # 그냥 뒤에만 순차적으로 변경
                self.change_rear(self.back_diff)
            else:                   # 앞드레일러를 변경할 필요가 있다면
                if self.app.get_current_gear().front_idx == 1:  # 지금 내 앞드레일러가 2단인가?
                    # 그러면 뒤에꺼 싹다 바꾸고 -> 그 다음에 앞에꺼를 바꾸고
                    self.change_rear(self.back_diff)
                    self.change_front(self.front_diff)
                else:
                    # 아니면 일단 앞을 2로 변경 -> 그 담에 뒤에꺼 싹다 바꾸고 -> 그 담에 앞에 필요시 추가 변경
                    if self.front_diff > 0:
                        self.change_front(1)
                        time.sleep(0.5)
                        self.change_rear(self.back_diff)
                        time.sleep(0.5)
                        self.change_front(self.front_diff - 1)
                    else:
                        self.change_front(-1)
                        time.sleep(0.5)
                        self.change_rear(self.back_diff)
                        time.sleep(0.5)
                        self.change_front(self.front_diff + 1)

    def change_front(self, diff: int):
        if diff == 0:
            return
        if diff > 0:
            next_fronts = [self.app.get_front_idx() + i for i in range(1, diff + 1)]
        elif diff < 0:
            next_fronts = [self.app.get_front_idx() - i for i in range(1, abs(diff) + 1)]
        print(f"변경될 앞 드레일러 차이 {diff}")
        print(f"이 순서대로 앞 드레일러가 변경됩니다: {next_fronts}")
        for front in next_fronts:
            self.app.set_front_idx(front)
            self.updateFront.emit(front)
            time.sleep(0.5)

    def change_rear(self, diff: int):
        if diff == 0:
            return
        elif diff > 0:
            next_rears = [self.app.get_back_idx() + i for i in range(1, diff + 1)]
        elif diff < 0:
            next_rears = [self.app.get_back_idx() - i for i in range(1, abs(diff) + 1)]
        print(f"변경될 뒷 드레일러 차이 {diff}")
        print(f"이 순서대로 뒷 드레일러가 변경됩니다: {next_rears}")
        for rear in next_rears:
            self.app.set_back_idx(rear)
            self.updateRear.emit(rear)
            time.sleep(0.5)

    def run(self):
        self.__update_gear()
        self.finished.emit(self.target_gear, self.target_stage)

