#!/usr/bin/python3.5

from threading import Timer
from source.baseclass.logmanage import LogManage
from source.baseclass.globalvar import GlobalVar


class CardTimer(LogManage):
    timeout_function = None
    timer = None
    timeout = False
    second = 1

    def __init__(self, second=1):
        self.second = second

    def get_timeout(self):
        return self.timeout

    def do_del_timer(self):
        self.timeout = False
        if self.timer:
            self.timer.cancel()

    def do_timeout(self):
        self.timeout = True
        if self.timeout_function:
            self.timeout_function()
            self.timer.cancel()

    def do_start(self, function=None):
        self.timeout_function = function
        self.timer = Timer(self.second, self.do_timeout)
        self.timer.start()
        self.timeout = False
