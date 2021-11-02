import os
import platform
import sys


if platform.system() == "Darwin":
    from PyQt6 import uic
    from PyQt6.QtCore import Qt
    from PyQt6.QtWidgets import QMainWindow, QPushButton
    from PyQt6.QtGui import QFont, QColor
else:
    from PyQt5 import uic
    from PyQt5.QtCore import Qt
    from PyQt5.QtWidgets import QMainWindow, QPushButton
    from PyQt5.QtGui import QFont, QColor

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
        self.set_color(self.app.get_current_stage())
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
        self.set_color(target_stage)
        print("[선택된 기어]", target_gear)
        print()

    def set_color(self, selected):
        for button in self.buttons:
            if button.objectName() == f"gearGroup_{selected}":
                pal = button.palette()
                if platform.system() == "Darwin":
                    pal.setColor(button.backgroundRole(), QColor(Qt.GlobalColor.blue))
                else:
                    pal.setColor(button.backgroundRole(), QColor(Qt.blue))
                button.setPalette(pal)
            else:
                button.setPalette(QPushButton().palette())
            button.update()

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
        new_group.setObjectName(f"gearGroup_{stage}")
        new_group.setText(str(stage))
        new_group.setMinimumSize(0, 100)
        new_group.setFont(QFont("Arial", 15))
        new_group.setAutoFillBackground(True)
        new_group.clicked.connect(lambda: self.change_gear(stage))
        self.buttons.append(new_group)
        self.gearGridLayout.addWidget(new_group, row-1, col)
