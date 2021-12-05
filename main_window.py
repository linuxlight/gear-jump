import os
import platform
import sys

from diff_calculator import GearDiffCalculator
from option import OptionManager

if platform.system() == "Darwin":
    from PyQt6 import uic, QtCore
    from PyQt6.QtCore import Qt, pyqtSlot
    from PyQt6.QtWidgets import QMainWindow, QPushButton, QApplication
    from PyQt6.QtGui import QFont, QColor, QCursor
else:
    from PyQt5 import uic
    from PyQt5.QtCore import Qt, pyqtSlot
    from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication
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
        self.diff_cal = GearDiffCalculator(self.app)
        self.opt_mgr = OptionManager(self.app, self)
        self.refresh_buttons()
        self.set_color(self.app.get_current_stage())
        self.set_gear_display(self.app.get_current_gear())
        self.__connect_signals()

    def __connect_signals(self):
        self.diff_cal.updateFront.connect(self.__print_front)
        self.diff_cal.updateRear.connect(self.__print_back)
        self.diff_cal.finished.connect(self.__confirm_gear)
        self.optionSave.clicked.connect(self.__save_option)
        self.optionCancel.clicked.connect(self.__discard_option)
        self.action_Option.triggered.connect(self.__set_option)
        self.action_Exit.triggered.connect(QApplication.quit)


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
        target_gear: Gear = self.app.select_gear(target_stage)
        front_diff, back_diff = self.app.get_difference(target_gear)
        print(f"[결정된 변경횟수] 앞: {front_diff}, 뒤: {back_diff}")
        self.diff_cal.set_diff(front_diff, back_diff, target_gear, target_stage)
        self.diff_cal.start()

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
        new_group.setMinimumSize(0, 80)
        new_group.setFont(QFont("Arial", 15))
        new_group.setAutoFillBackground(True)
        if platform.system() == "Darwin":
            new_group.setCursor(QCursor(Qt.CursorShape.BlankCursor))
        else:
            new_group.setCursor(QCursor(QtCore.Qt.BlankCursor))
        new_group.clicked.connect(lambda: self.change_gear(stage))
        self.buttons.append(new_group)
        self.gearGridLayout.addWidget(new_group, row-1, col)

    @pyqtSlot(int)
    def __print_front(self, front):
        self.frontGear.setText(str(front + 1))
        self.frontGear.repaint()
        QApplication.processEvents()

    @pyqtSlot(int)
    def __print_back(self, rear):
        self.rearGear.setText(str(rear + 1))
        self.rearGear.repaint()
        QApplication.processEvents()

    @pyqtSlot(Gear, int)
    def __confirm_gear(self, target_gear, target_stage):
        self.app.set_current_gear(target_gear)
        self.set_color(target_stage)
        print()

    @pyqtSlot()
    def __save_option(self):
        self.stackedWidget.setCurrentIndex(0)
        self.opt_mgr.save()

    @pyqtSlot()
    def __discard_option(self):
        self.stackedWidget.setCurrentIndex(0)

    @pyqtSlot()
    def __set_option(self):
        self.stackedWidget.setCurrentIndex(1)
        pass
