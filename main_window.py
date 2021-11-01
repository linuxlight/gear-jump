from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QPushButton

from app import MainApp
from gear import Gear


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi("./etc/mainwindow.ui", self)
        self.show()
        self.input_num = None
        self.buttons = []
        self.app = MainApp(1, 5)
        self.__connect_signals()
        self.set_gear_display(self.app.current_gear)

    def __connect_signals(self):
        self.refresh_buttons()

    def change_gear(self, target_stage: int):
        target_gear = self.app.select_gear(target_stage)
        self.set_gear_display(target_gear)
        print()
        print(target_gear)

    def set_gear_display(self, target_gear: Gear):
        print(target_gear.front)
        self.frontGear.setText(str(target_gear.front_level + 1))
        self.rearGear.setText(str(target_gear.back_level + 1))

    def refresh_buttons(self):
        for i in range(self.app.total_groups):
            self.add_gear(i + 1)

    def add_gear(self, stage: int):
        row = self.gearGridLayout.rowCount()
        col = len(self.buttons) % 6
        if len(self.buttons) % 6 == 0:
            row = self.gearGridLayout.rowCount() + 1
            col = 0
        new_gear = QPushButton(self)
        new_gear.setText(str(stage))
        new_gear.setMinimumSize(0, 100)
        new_gear.clicked.connect(lambda: self.change_gear(stage))
        self.buttons.append(new_gear)
        self.gearGridLayout.addWidget(new_gear, row-1, col)
