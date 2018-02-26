import os
import time


def getExePath():
    realpath = os.path.split(os.path.realpath(__file__))[0]
    if realpath.__contains__('src'):
        realpath = realpath.replace('src', '')
    return realpath


def getNowDate():
    now = int(time.time())
    timeArray = time.localtime(now)
    return time.strftime("%Y-%m-%d", timeArray)


class FileUtil(object):
    TODO_LIST_WIDGET_ITEM_BTN = ""

    def __init__(self):
        pass

    def readFile(self, path):
        with open(path, 'r+', encoding='UTF-8') as f:
            filestr = f.read()
        return filestr.strip().replace('\ufeff', '')
