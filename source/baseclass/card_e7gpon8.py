#!/usr/bin/python3.5
import os
import time

from source.baseclass.card_8544 import Card8544
from source.baseclass.globalvar import GlobalVar


class CardE7GPON8(Card8544):
    def __init__(self, options):
        super(Card8544, self).__init__(options)

        pass

    def do_seed(self):
        if not self.do_checknet():
            self.net_status = GlobalVar.STATUS_CARD_NET_NOTCFG_DISC
            if not self.do_setip():
                self.net_status = GlobalVar.STATUS_CARD_NET_CFG_DISC
                return False
            else:
                self.net_status = GlobalVar.STATUS_CARD_NET_CFG_CONNECT

        else:
            self.net_status = GlobalVar.STATUS_CARD_NET_NOTCFG_CONNECT
        self.do_seed_t10xx()

    def do_seed_count(self):
        while self.seed_count:
            self.session_telnet.login()
            if not self.do_checknet():
                self.net_status = GlobalVar.STATUS_CARD_NET_NOTCFG_DISC
                if not self.do_setip():
                    self.net_status = GlobalVar.STATUS_CARD_NET_CFG_DISC
                    return False
                else:
                    self.net_status = GlobalVar.STATUS_CARD_NET_CFG_CONNECT

            else:
                self.net_status = GlobalVar.STATUS_CARD_NET_NOTCFG_CONNECT
            self.do_seed_t10xx()
            self.seed_count -= 1
