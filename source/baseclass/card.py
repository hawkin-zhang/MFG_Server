#!/usr/bin/python3.5


import os
import getopt
import time
from threading import Timer
from source.baseclass.logmanage import LogManage
from source.baseclass.globalvar import GlobalVar
from source.baseclass.card_timer import CardTimer


class BID:
    EqptType = ""
    EqptText = ""
    MktHwVerMaj = ""
    MktHwVerMin = ""
    MktHwRev = ""
    EngHwVerMaj = ""
    EngHwVerMin = ""
    EngHwRev = ""
    SerialNumber = ""
    SwPackageId = ""

    def __init__(self):
        pass


class Card(LogManage):

    count = 1
    card_init_finished = GlobalVar.STATUS_CARD_INIT_FAILED
    host = ""
    port = ""
    server = ""
    version = ""
    session_telnet = None
    session_ssh = None
    seed_count = 1

    net_status = GlobalVar.STATUS_CARD_NET_NOTCHECK
    bid = None

    def __init__(self, options):
        self.bid = BID()
        try:
            options, args = getopt.getopt(options, GlobalVar.CONFIG_CARDFACTORY_PARAMETER)
            for tup in options:
                if tup[0] == '-a':
                    self.host = tup[1]
                elif tup[0] == '-p':
                    self.port = tup[1]
                elif tup[0] == '-s':
                    self.server = tup[1]
                elif tup[0] == '-v':
                    self.version = tup[1]
                elif tup[0] == '-c':
                    self.seed_count = int(tup[1])

        except Exception as e:
            self.log_printf(GlobalVar.ERROR_CARDCREAT_FAILED.format(e.strerror))

        if (not self.host) \
                and (not self.port) \
                and (not self.server) \
                and (not self.version):
            self.card_init_finished = GlobalVar.STATUS_CARD_INIT_FINISHED

    def do_session_write(self, data):
        if self.session_telnet:
            self.session_telnet.write(data)
        else:
            self.log_printf("No session_telnet create", "red")

    def do_session_read(self, loop_time=1):
        try:
            """loop_time: receive loop_time, ms"""
            response_str = ""
            if self.session_telnet:
                while loop_time:
                    respon = self.session_telnet.read()

                    if respon:
                        response_str += str(respon, encoding="utf-8")
                    loop_time -= 1
            else:
                self.log_printf("No session_telnet create", "red")
        except Exception as e:
            self.log_printf(e.args[0])
        return response_str

    def do_session_expectread(self, expect_str, loop_time=100):
        """loop_time: receive loop_time, ms"""
        response_str = ""
        if self.session_telnet:
            while loop_time:
                respon = self.session_telnet.read()
                if respon:
                    response_str += str(respon, encoding="utf-8")
                    if -1 != response_str.find(expect_str):
                        return response_str
                loop_time -= 1
        else:
            self.log_printf("No session_telnet create", "red")
        return response_str

    def do_session_timeread(self, loop_time=5):
        """loop_time: read time, s"""
        response_str = ""
        readtimer = CardTimer(loop_time)
        readtimer.do_start()
        if self.session_telnet:
            while not readtimer.timeout:
                respon = self.session_telnet.read()
                if respon:
                    response_str += str(respon, encoding="utf-8")
        else:
            self.log_printf("No session_telnet create")
        return response_str

    def do_reboot(self):
        self.do_session_write(GlobalVar.get_command_reboot())

    @staticmethod
    def do_getbid_85xx(session):
        bid = BID()
        session.write('\r\n')
        session.write('\r\n')
        session.write(GlobalVar.get_command_bid_p85xx())
        bid_card = str(session.read(), encoding="utf-8")
        for entry in bid_card.split('\r\n'):
            """split BIN ,do not use split(' ')"""

            if -1 != entry.find("EqptType"):
                bid.EqptType = entry.split("=", maxsplit=1)[1].lstrip("0").lstrip()
            elif -1 != entry.find("sEqptText"):
                bid.EqptText = entry.split("=", maxsplit=1)[1].lstrip()
            elif -1 != entry.find("MktHwVerMajBCD"):
                bid.MktHwVerMaj = entry.split("=", maxsplit=1)[1].lstrip()
            elif -1 != entry.find("MktHwVerMinBCD"):
                bid.MktHwVerMin = entry.split("=", maxsplit=1)[1].lstrip()
            elif -1 != entry.find("MktHwRevBCD"):
                bid.MktHwRev = entry.split("=", maxsplit=1)[1].lstrip()
            elif -1 != entry.find("EngHwVerMajBCD"):
                bid.EngHwVerMaj = entry.split("=", maxsplit=1)[1].lstrip()
            elif -1 != entry.find("EngHwVerMinBCD"):
                bid.EngHwVerMin = entry.split("=", maxsplit=1)[1].lstrip()
            elif -1 != entry.find("EngHwRevBCD"):
                bid.EngHwRev = entry.split("=", maxsplit=1)[1].lstrip()
            elif -1 != entry.find("SerialNumber"):
                bid.SerialNumber = entry.split("=", maxsplit=1)[1].lstrip()
            elif -1 != entry.find("SwPackageId"):
                bid.SwPackageId = entry.split("=", maxsplit=1)[1].lstrip()
        return bid

    @staticmethod
    def do_getbid_t10xx(session):
        bid = BID()
        session.write('\r\n')
        session.write('\r\n')
        session.write(GlobalVar.get_command_bid_t10xx())
        #bid_card = str(session.read(), encoding="utf-8")
        bid_card = session.do_timeread(1.5)
        for entry in bid_card.split('\r\n'):
            """split BIN ,do not use split(' ')"""

            if -1 != entry.find("EqptType"):
                bid.EqptType = entry.split(maxsplit=1)[1].lstrip("0").lstrip()
            elif -1 != entry.find("EqptText"):
                bid.EqptText = entry.split(maxsplit=1)[1].lstrip()
            elif -1 != entry.find("MktHwVerMaj"):
                bid.MktHwVerMaj = entry.split(maxsplit=1)[1].lstrip()
            elif -1 != entry.find("MktHwVerMin"):
                bid.MktHwVerMin = entry.split(maxsplit=1)[1].lstrip()
            elif -1 != entry.find("MktHwRev"):
                bid.MktHwRev = entry.split(maxsplit=1)[1].lstrip()
            elif -1 != entry.find("EngHwVerMaj"):
                bid.EngHwVerMaj = entry.split(maxsplit=1)[1].lstrip()
            elif -1 != entry.find("EngHwVerMin"):
                bid.EngHwVerMin = entry.split(maxsplit=1)[1].lstrip()
            elif -1 != entry.find("EngHwRev"):
                bid.EngHwRev = entry.split(maxsplit=1)[1].lstrip()
            elif -1 != entry.find("SerialNumber"):
                bid.SerialNumber = entry.split(maxsplit=1)[1].lstrip()
            elif -1 != entry.find("SwPackageId"):
                bid.SwPackageId = entry.split(maxsplit=1)[1].lstrip()
        return bid

    @staticmethod
    def do_getbid_axos(session):
        bid = BID()
        session.write('\r\n')
        session.write('\r\n')
        session.write(GlobalVar.get_command_bid_axos())
        bid_card = str(session.read(), encoding="utf-8")
        for entry in bid_card.split('\r\n'):
            """split BIN ,do not use split(' ')"""

            if -1 != entry.find("EqptType"):
                bid.EqptType = entry.split(maxsplit=1)[1].lstrip("0").lstrip()
            elif -1 != entry.find("EqptText"):
                bid.EqptText = entry.split(maxsplit=1)[1].lstrip()
            elif -1 != entry.find("MktHwVerMaj"):
                bid.MktHwVerMaj = entry.split(maxsplit=1)[1].lstrip()
            elif -1 != entry.find("MktHwVerMin"):
                bid.MktHwVerMin = entry.split(maxsplit=1)[1].lstrip()
            elif -1 != entry.find("MktHwRev"):
                bid.MktHwRev = entry.split(maxsplit=1)[1].lstrip()
            elif -1 != entry.find("EngHwVerMaj"):
                bid.EngHwVerMaj = entry.split(maxsplit=1)[1].lstrip()
            elif -1 != entry.find("EngHwVerMin"):
                bid.EngHwVerMin = entry.split(maxsplit=1)[1].lstrip()
            elif -1 != entry.find("EngHwRev"):
                bid.EngHwRev = entry.split(maxsplit=1)[1].lstrip()
            elif -1 != entry.find("SerialNumber"):
                bid.SerialNumber = entry.split(maxsplit=1)[1].lstrip()
            elif -1 != entry.find("SwPackageId"):
                bid.SwPackageId = entry.split(maxsplit=1)[1].lstrip()
        return bid

    def do_setip(self):
        eth_dev = GlobalVar.LIST_ETH_DEV_T10XX
        ip_list = self.host.split(".")

        for i in range(100, 255):
            ip = GlobalVar.format_ip(ip_list[0], ip_list[1], ip_list[2], str(i))
            route_ip = GlobalVar.format_ip(ip_list[0], ip_list[1], ip_list[2], str(1))
            response_ping = os.popen(GlobalVar.get_command_ping(ip)).read()

            if (-1 != response_ping.find(GlobalVar.get_message_pingfail())) or \
                    (-1 != response_ping.find(GlobalVar.MESSAGE_PING_FAILED_LOSS)) or \
                    (-1 != response_ping.find(GlobalVar.MESSAGE_PING_FAILED_UNREACHABLE)) or \
                    (-1 != response_ping.find(GlobalVar.MESSAGE_PING_FAILED_TIMEOUT)):
                """ip empty use this ip"""
                for dev in eth_dev:
                    self.do_session_write(GlobalVar.get_command_setip(dev, ip))
                    self.do_session_write(GlobalVar.get_command_setroute(dev, route_ip))
                    time.sleep(3)
                    if self.do_checknet():
                        return True
                    else:
                        self.do_session_write(GlobalVar.get_command_delip(dev, ip))
                        self.do_session_write(GlobalVar.get_command_delroute())

            else:
                break
        return False

    def do_checknet(self):

        self.do_session_write(GlobalVar.get_command_ping(GlobalVar.CONFIG_CDCDOC_SERVER_GATEWAYIP))
        ping_result = self.do_session_timeread(5)

        if (-1 != ping_result.find(GlobalVar.get_message_pingfail_t10xx())) or \
                (-1 != ping_result.find(GlobalVar.MESSAGE_NETWORK_UNREACH)):
            self.log_printf("IP not set need config ")
            return False
        return True

    @staticmethod
    def do_getbid(session):
        # self.session_telnet.login()
        bid = Card.do_getbid_85xx(session)
        if len(bid.EqptType) > 0 and \
                len(bid.EqptText) > 0:
            return bid
        bid = Card.do_getbid_t10xx(session)
        if len(bid.EqptType) > 0 and \
                len(bid.EqptText) > 0:
            return bid
        bid = Card.do_getbid_axos(session)
        if len(bid.EqptType) > 0 and \
                len(bid.EqptText) > 0:
            return bid

        return None

    def do_seed_count(self):
        # self.do_getbid()
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
            self.do_seed()
            self.seed_count -= 1

    def do_seed(self):
        confirm = False
        reboot = False
        seed_timer = CardTimer(700)
        try:
            """set function of Backspace"""
            self.do_session_write("stty erase ^h \r\n")
            self.do_session_write(GlobalVar.get_command_seed_t10xx(server=self.server, path=self.version))

            seed_timer.do_start()

            while True:

                if seed_timer.timeout:
                    self.do_session_write(GlobalVar.get_ascii_ctrl("c"))
                    self.do_session_write("\r\n")
                    self.log_printf("Time out seed failed")
                    return

                log = self.do_session_read()

                if len(log) > 0:
                    self.log_printf(log)
                else:
                    continue

                if -1 != log.find(GlobalVar.get_message_seedconfirm_t10xx()):
                    # time.sleep(1)
                    """delete more space"""
                    self.do_session_write('\b\by\r\n')
                    confirm = True
                elif -1 != log.find(GlobalVar.MESSAGE_SEED_FAILED):
                    self.log_printf("seed failed")
                    break
                elif -1 != log.find(GlobalVar.MESSAGE_SEED_SUCCESS):
                    self.log_printf("seed finished reboot card")
                    self.do_reboot()
                    reboot = True
                elif -1 != log.find(GlobalVar.MESSAGE_CARD_START_FINISHED):
                    self.log_printf("restart finished")
                    break
                elif -1 != log.find(GlobalVar.MESSAGE_HINT_T10XX) and confirm and not reboot:
                    self.log_printf("seed exit ,seed failed")
                    self.seed_count = 1
                    break
            seed_timer.do_del_timer()

        except Exception as e:
            self.log_printf(GlobalVar.ERROR_CARDSEED_FAILED.format(e.args[0]), "red")
