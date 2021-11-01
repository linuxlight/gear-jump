from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi("./etc/mainwindow.ui", self)
        self.show()
        self.input_num = None
        # self.__connect_signals()

    def __connect_signals(self):
        self.gearButton_1.clicked.connect()
        self.gearButton_2.clicked.connect()
        self.gearButton_3.clicked.connect()
        self.gearButton_4.clicked.connect()
        self.gearButton_5.clicked.connect()
        self.gearButton_6.clicked.connect()

