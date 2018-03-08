import sqlite3
import utils

conn = sqlite3.connect(utils.getExePath()+'mytodo.db')


class ToDoItem:
    def __init__(self):
        self.id = 1
        self.todo = 2
        self.imp = 3
        self.emg = 4
        self.state = 5
        self.create_date = 6
        self.sort = 7


def sortToDoItems(items):
    pass


def saveItems(items):
    pass


def delItems(items):
    pass


def exportItems(items):
    pass