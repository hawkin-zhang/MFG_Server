#!/usr/bin/python3.5
from source.baseclass.logmanage import LogManage
from source.baseclass.FindCard import FindCard

class ToolBox(LogManage):


    def __init__(self):
        pass

    def do_find(self):
        """
        Scan CDC network from 10.245.1.1  --- 10.245.255.255
        :return:
        """
        find = FindCard()
        find.do_scan()
        pass