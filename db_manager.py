import os
import sqlite3
from sqlite3 import Error

from singleton_instance import SingletonInstance


class DatabaseManager(SingletonInstance):
    """ Database Manager """
    conn = None  # connection
    cur = None  # cursor
    DB_PATH = "gear.db"    # database name

    def init_tables(self):
        self._create_connection()
        self.__create_table()
        if self._is_table_empty("front"):
            self.cur.executemany("INSERT INTO front VALUES (?, ?)", [(1, 22), (2, 30), (3, 40)])
        if self._is_table_empty("rear"):
            self.cur.executemany("INSERT INTO rear VALUES (?, ?)", [
                (1, 36), (2, 32), (3, 28), (4, 24), (5, 21), (6, 18), (7, 16), (8, 14), (9, 12), (10, 11)
            ])
        self.conn.commit()
        self._close_connection()

    def get_gears(self, position: str):
        self._create_connection()
        self._get_cursor()
        if position == "front":
            self.cur.execute("SELECT teeth FROM front")
        elif position == "rear":
            self.cur.execute("SELECT teeth FROM rear")
        gear_list = [row[0] for row in self.cur.fetchall()]
        self._close_connection()
        return gear_list

    def set_gears(self, gear_list: list, position: str):
        self._create_connection()
        self._get_cursor()
        self.__empty_gears()
        self.cur.executemany("INSERT INTO %s VALUES (?, ?)" % position,
                             [(i+1, gear) for i, gear in enumerate(gear_list)])
        self.conn.commit()
        self._close_connection()

    def _create_connection(self):
        """ Create connection with database """
        try:
            print(f'Connecting to database : {self.DB_PATH} ...')
            self.conn = sqlite3.connect(self.DB_PATH)
            print(f'Succesfully connected to database : {self.DB_PATH}')
        except sqlite3.Error as err:
            print(err)

    def _get_cursor(self):
        """ Create cursor """
        self.cur = self.conn.cursor()

    def _close_connection(self):
        """ Close connection to database """
        if self.conn is not None:
            self.conn.close()
            print(f'Succesfully closed database : {self.DB_PATH}')

    def _is_table_empty(self, tbl_name):
        """ table이 비었는지 확인합니다. """
        self._get_cursor()
        self.cur.execute("SELECT id FROM %s" % tbl_name)
        if not self.cur.fetchall():
            return True
        else:
            return False

    def __create_table(self):
        """ 필요한 table들을 생성합니다. """
        create_front_table_sql = """
        -- front gear table
        CREATE TABLE IF NOT EXISTS front (
            id integer PRIMARY KEY,
            teeth integer NOT NULL
        );"""

        create_rear_table_sql = """
        -- rear gear table
        CREATE TABLE IF NOT EXISTS rear (
            id integer PRIMARY KEY,
            teeth integer NOT NULL
        );
        """
        try:
            self._get_cursor()
            self.cur.execute(create_front_table_sql)
            self.cur.execute(create_rear_table_sql)
        except Error as e:
            print(e)
            self._close_connection()

    def __empty_gears(self):
        """ table에 존재하는 모든 gear를 초기화합니다. """
        self.cur.execute("DELETE FROM front")
        self.cur.execute("DELETE FROM rear")
        self.conn.commit()
