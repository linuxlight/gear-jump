# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import platform
import sys
if platform.system() == "Darwin":
    from PyQt6.QtWidgets import QApplication
else:
    from PyQt5.QtWidgets import QApplication


# front_list = []
from main_window import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())


