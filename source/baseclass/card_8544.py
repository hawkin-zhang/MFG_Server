#!/usr/bin/python3.5


import os
import time
from source.baseclass.card import Card
from source.baseclass.globalvar import GlobalVar



class Card8544(Card):
    def __init__(self, options):
        super(Card, self).__init__(options)

    def do_getbid(self):
        self.session_telnet.login()
        self.do_getbid_85xx(self.session_telnet)