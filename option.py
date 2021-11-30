from app import MainApp


class OptionManager:
    def __init__(self, app: MainApp, window):
        self.app = app
        self.parent = window
        self.db_mgr = app.db_mgr
        self.front_edits = [self.parent.front_1, self.parent.front_2, self.parent.front_3]
        self.rear_edits = [
            self.parent.rear_1, self.parent.rear_2, self.parent.rear_3, self.parent.rear_4, self.parent.rear_5,
            self.parent.rear_6, self.parent.rear_7, self.parent.rear_8, self.parent.rear_9, self.parent.rear_10,
            self.parent.rear_11, self.parent.rear_12, self.parent.rear_13, self.parent.rear_14
        ]
        self.__print_gears()

    def save(self):
        front_list = [int(front_edit.text()) for front_edit in self.front_edits if front_edit.text()]
        rear_list = [int(rear_edit.text()) for rear_edit in self.rear_edits if rear_edit.text()]
        self.db_mgr.set_gears(front_list, "front")
        self.db_mgr.set_gears(rear_list, "rear")

    def __print_gears(self):
        front_size = 0
        rear_size = 0
        front_it = iter(self.app.front_list)
        rear_it = iter(self.app.rear_list)
        for front_edit in self.front_edits:
            front_size = self.__set_text(front_edit, front_it, front_size, self.app.front_list)
        for rear_edit in self.rear_edits:
            rear_size = self.__set_text(rear_edit, rear_it, rear_size, self.app.rear_list)

    @staticmethod
    def __set_text(widget, iterator: iter, size: int, gear_list: list):
        if len(gear_list) > size:
            widget.setText(str(next(iterator)))
            size += 1
        return size
