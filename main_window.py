import os
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QPushButton

from app import MainApp
from gear import Gear


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi(self.__resource_path("etc/mainwindow.ui"), self)
        self.show()
        self.input_num = None
        self.buttons = []
        self.app = MainApp(1, 5)
        self.refresh_buttons()
        self.set_gear_display(self.app.get_current_gear())

    @staticmethod
    def __resource_path(relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def change_gear(self, target_stage: int):
        target_gear = self.app.select_gear(target_stage)
        self.app.set_current_gear(target_gear)
        self.set_gear_display(target_gear)
        print("[선택된 기어]", target_gear)
        print()

    def set_gear_display(self, target_gear: Gear):
        self.frontGear.setText(str(target_gear.front_idx + 1))
        self.rearGear.setText(str(target_gear.back_idx + 1))

    def refresh_buttons(self):
        for i in range(self.app.total_groups):
            self.__add_group(i + 1)

    def __add_group(self, stage: int):
        row = self.gearGridLayout.rowCount()
        col = len(self.buttons) % 6
        if len(self.buttons) % 6 == 0:
            row = self.gearGridLayout.rowCount() + 1
            col = 0
        new_group = QPushButton(self)
        new_group.setText(str(stage))
        new_group.setMinimumSize(0, 100)
        new_group.clicked.connect(lambda: self.change_gear(stage))
        self.buttons.append(new_group)
        self.gearGridLayout.addWidget(new_group, row-1, col)
