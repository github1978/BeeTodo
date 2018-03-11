import sqlite3
import utils
import time
from MyWidgets import ToDoItem

TDITEMS_TABLE_NAME = "TDITEMS"

conn = sqlite3.connect(utils.getExePath() + 'mytodo.db')


def sortToDoItems(items):
    pass


def queryItems(items):
    pass


def saveItems(items: list):
    values_str = ""
    for item in items:
        if values_str == "":
            values_str = values_str + item.serialize()
        else:
            values_str = values_str + "," + item.serialize()
    sql = "insert into " + TDITEMS_TABLE_NAME + "values " + values_str
    excuteSql(sql)


def delItems(items):
    pass


def exportItems(items):
    pass


def excuteSql(sql: str):
    cur = conn.cursor()
    cur.execute(sql)
    conn.close()


if __name__ == '__main__':
    excuteSql(
        '''
        CREATE TABLE TDITEMS
        (
        id INT PRIMARY KEY NOT NULL,
        todo TEXT NOT NULL,
        imp  CHAR(50),
        emg  CHAR(50),
        state INT,
        create_date TEXT,
        sort INT
        );
        '''
    )
