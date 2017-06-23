#!/usr/bin/python3.5
import os
import time

from source.baseclass.card_t10xx import CardT10xx
from source.baseclass.globalvar import GlobalVar


class CardE3VDSLr2(CardT10xx):
    def __init__(self, options):
        super(CardT10xx, self).__init__(options)

        pass
    """
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
    """



