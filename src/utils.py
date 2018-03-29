import os
import time

import win32gui
from PyQt5.QtCore import QDateTime


def getExePath():
    realpath = os.path.split(os.path.realpath(__file__))[0]
    if realpath.__contains__('src'):
        realpath = realpath.replace('src', '')
    return realpath


def getWindowsDeskTopHwnd():
    hwndWorkerW = win32gui.FindWindowEx(0, None, "WorkerW", "")
    hDefView = 0
    tencentView = 0
    while tencentView == 0 and hDefView == 0 and hwndWorkerW:
        # 支持腾讯桌面整理软件
        tencentView = win32gui.FindWindowEx(hwndWorkerW, None, "TXMiniSkin", "桌面整理")
        if tencentView != 0:
            return tencentView

        hDefView = win32gui.FindWindowEx(hwndWorkerW, None, "SHELLDLL_DefView", "")
        if hDefView != 0:
            return hDefView
        hwndWorkerW = win32gui.FindWindowEx(0, hwndWorkerW, "WorkerW", "")
    return hwndWorkerW


def getNowDate(format_time):
    # "%Y-%m-%d"
    now = int(time.time())
    timeArray = time.localtime(now)
    return time.strftime(format_time, timeArray)


def getNowQDate(format_time):
    return QDateTime.currentDateTime().toString(format_time)


class FileUtil(object):
    TODO_LIST_WIDGET_ITEM_BTN = ""

    def __init__(self):
        pass

    def readFile(self, path):
        with open(path, 'r+', encoding='UTF-8') as f:
            filestr = f.read()
        return filestr.strip().replace('\ufeff', '')
