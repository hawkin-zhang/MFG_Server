#!/usr/bin/python3.5


import getopt
import re
from source.baseclass.card import Card
from source.baseclass.connectfacrory import ConnectFactory
from source.baseclass.logmanage import LogManage
from source.baseclass.card_e3vdslr2 import CardE3VDSLr2
from source.baseclass.card_e3vcp import CardE3VCP
from source.baseclass.card_e7vdslr2 import CardE7VDSLr2
from source.baseclass.card_e7vcp import CardE7VCP
from source.baseclass.card_e7gpon8 import CardE7GPON8
from source.baseclass.card_e7scp2 import CardE7SCP2
from source.baseclass.card_e7scp10g import CardE7SCP10G
from source.baseclass.card_ngpon2x4 import CardAXOSNGPON2X4
from source.baseclass.card_e7gpon4r2 import CardE7GPON4R2
from source.baseclass.globalvar import GlobalVar


ERROR_CARDCREAT_FAILED = 'Create card [{0}:{1}] failed, Reason:{2} '

FACTORY_INIT_FINISHED = 0
FACTORY_INIT_ERROR = 1


class CardFactory(LogManage):

    factory_init_status = FACTORY_INIT_ERROR
    host = None
    port = None
    session = None
    bid = None

    def __init__(self, command):
        self.command_list = command.split()
        try:
            options, args = getopt.getopt(self.command_list[1:], GlobalVar.CONFIG_CARDFACTORY_PARAMETER)
            for tup in options:
                if tup[0] == '-a':
                    self.host = tup[1]
                elif tup[0] == '-p':
                    self.port = tup[1]

        except Exception as e:
            return

        if not self.do_ipvalid(self.host):
            return

        self.factory_init_status = FACTORY_INIT_FINISHED
    # def __del__(self):
        # self.session_telnet.disconnect()

    def do_ipvalid(self, ip_str):
        if ip_str == None:
            return False

        pattern = r"\b(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b"
        if re.match(pattern, ip_str):
            return True
        else:
            return False

    def do_getequiptype(self):
        self.session.write('\r\n')
        self.session.write('\r\n')
        self.session.write(GlobalVar.get_command_cpuinfo())
        cpuinfo = str(self.session.read(), encoding="utf-8")
        cpuinfo += str(self.session.read(), encoding="utf-8")
        cpuinfo += str(self.session.read(), encoding="utf-8")
        if -1 != cpuinfo.find("e5500"):
            self.session.write(GlobalVar.get_command_bid_t10xx())
            bidinfo = str(self.session.read(), encoding="utf-8")
            bidlist = bidinfo.split("\r\n")
            for tup in bidlist:
                if -1 != tup.find("EqptType"):
                    self.EqptType = tup.split(maxsplit=1)[1].lstrip("0")
                elif -1 != tup.find("EqptText"):
                    self.EqptText = tup.split(maxsplit=1)[1]

            self.session.write(GlobalVar.get_command_bid_axos())
            bidinfo = str(self.session.read(), encoding="utf-8")
            bidlist = bidinfo.split("\r\n")
            for tup in bidlist:
                if -1 != tup.find("EqptType"):
                    self.EqptType = tup.split(maxsplit=1)[1].lstrip("0")
                elif -1 != tup.find("EqptText"):
                    self.EqptText = tup.split(maxsplit=1)[1]

        elif -1 != cpuinfo.find("e500"):
            self.session.write(GlobalVar.get_command_bid_p85xx())
            bidinfo = str(self.session.read(), encoding="utf-8")
            bidlist = bidinfo.split("\r\n")
            for tup in bidlist:
                if -1 != tup.find("EqptType"):
                    self.EqptType = tup.split("=", maxsplit=1)[1].lstrip("0").lstrip()
                elif -1 != tup.find("sEqptText"):
                    self.EqptText = tup.split("=", maxsplit=1)[1].lstrip()

        else:
            return None

    def do_createcard(self):

        if GlobalVar.is_e7gpon4r2(self.bid.EqptType):
            return CardE7GPON4R2(self.command_list[1:])
        elif GlobalVar.is_e348c(self.bid.EqptType):
            return CardE3VDSLr2(self.command_list[1:])
        elif GlobalVar.is_e3vcp(self.bid.EqptType):
            return CardE3VCP(self.command_list[1:])
        elif GlobalVar.is_e7vdslr2(self.bid.EqptType):
            return CardE7VDSLr2(self.command_list[1:])
        elif GlobalVar.is_e7vcp(self.bid.EqptType):
            return CardE7VCP(self.command_list[1:])
        elif GlobalVar.is_scp2(self.bid.EqptType):
            return CardE7SCP2(self.command_list[1:])
        elif GlobalVar.is_scp10g(self.bid.EqptType):
            return CardE7SCP10G(self.command_list[1:])
        elif GlobalVar.is_e7gpon8(self.bid.EqptType):
            return CardE7GPON8(self.command_list[1:])
        elif GlobalVar.is_axosngpon2x4(self.bid.EqptType):
            return CardAXOSNGPON2X4(self.command_list[1:])
        else:
            return None

    def do_getcard(self):

        if self.factory_init_status == FACTORY_INIT_ERROR:
            self.log_printf('Parameters error!')
            self.log_printf('Hostip=' + self.host)
            self.log_printf('Port = ' + self.port)
            return None

        try:
            self.session = ConnectFactory(self.host, self.port).do_getconnect()
            self.session.login()

            self.bid = Card.do_getbid(self.session)
            if self.bid:
                card = self.do_createcard()
            else:
                self.log_printf("{}:{} Can't get bid".format(self.host,self.port))
                return None
            if card:
                card.session_telnet = self.session
                card.bid = self.bid
                return card
            else:
                self.session.disconnect()
                return None
        except Exception as e:
            self.log_printf(ERROR_CARDCREAT_FAILED.format(self.host, self.port, e.args[0]))

        return None
