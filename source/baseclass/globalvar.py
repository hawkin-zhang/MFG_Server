#!/usr/bin/python3.5


import os
import operator
import platform
import configparser
from source.baseclass.logmanage import LogManage


class GlobalVar(LogManage):

    PATH_CONFIGURE_CARDTYPE = "cardtype.cfg"
    NAME_CFG_UARTSERVER = "uart_server.cfg"
    # PATH_CONFIGURE_CARDTYPE = "cardtype.cfg"
    LIST_ETH_DEV_T10XX = ["eth1", "eth1.3", "eth1.4"]
    COMMAND_GETBID_AXOS = "bid -A 1-0050 -s \r\n"
    COMMAND_GETBID_T10XX = "/opt/calix/current/bin/bid.bin -A card -s \r\n"
    COMMAND_GETBID_P85XX = "/opt/calix/current/bin/bid.bin -d  \r\n"
    COMMAND_GETBID_P83XX = "/opt/calix/current/bin/bid.bin -d  \r\n"
    COMMAND_SEED_T10XX = "/opt/calix/seed.bin -server {0} -path {1}\r\n "
    COMMAND_PING_T10XX = "ping -w 2 {0} \r\n"
    COMMAND_GETCUPINFO = "cat /proc/cpuinfo \r\n"
    COMMAND_SETIP_T10XX = "ifconfig {}  {} netmask 255.255.255.0 \r\n"
    COMMAND_SETROUTE_T10XX = "route add default gw {} {} \r\n"
    COMMAND_DELIP_T10XX = "ip -f inet addr delete {} dev {} \r\n"
    COMMAND_DELROUTE_T10XX = "ip route del \r\n"
    COMMAND_REBOOT_LINUX = "reboot \r\n"

    COMMAND_IPCONFIG_FRONT = "ifconfig eth1.3  {} netmask 255.255.255.0"
    COMMAND_ROUTECFG_FRONT = "route add default gw {} eth1.3"

    COMMAND_IPCONFIG_REAR = "ifconfig eth1.4  {} netmask 255.255.255.0"
    COMMAND_ROUTECFG_REAR = "route add default gw {} eth1.4"

    COMMAND_IPCONFIG_GOJO = "ifconfig eth1  {} netmask 255.255.255.0"
    COMMAND_ROUTECFG_GOJO = "route add default gw {} eth1"

    MESSAGE_SEED_CONFIRM_T10XX = "Proceed with Seed? (y/n):"
    MESSAGE_PING_LOST_LINUX = "100% packet loss"
    MESSAGE_NETWORK_UNREACH = "unreachable"
    MESSAGE_PING_LOST_WINDOWS = "Destination host unreachable"
    MESSAGE_HINT_T10XX = "root@localhost"
    MESSAGE_NETWORK_PING_FINISHED = "packet loss"
    MESSAGE_IP_FORMAT = "{}.{}.{}.{}"
    MESSAGE_SEED_FAILED = "Seed FAILED"
    MESSAGE_SEED_SUCCESS = "Seed was SUCCESSFUL"
    MESSAGE_CARD_START_FINISHED = "disable trace to serial console"
    MESSAGE_PING_FAILED_LOSS = "100% loss"
    MESSAGE_PING_FAILED_UNREACHABLE = "unreachable"
    MESSAGE_PING_FAILED_TIMEOUT = "timed out"
    MESSAGE_FIND_EXCEPTION_TABLE = "{}:{} found in exception tabel ,ignore!"

    CONFIG_CDCDOC_SERVER_GATEWAYIP = "192.168.33.1"
    CONFIG_CARDFACTORY_PARAMETER = "a:p:s:v:c:"
    CONFIG_CARDCREAT_COMMAND_FORMAT = "tool -a {} -p {} "

    STATUS_CARD_INIT_FINISHED = 0
    STATUS_CARD_INIT_ONGOING = 1
    STATUS_CARD_INIT_FAILED = 1

    STATUS_CARD_NET_NOTCHECK = 0
    STATUS_CARD_NET_NOTCFG_CONNECT = 1
    STATUS_CARD_NET_NOTCFG_DISC = 2
    STATUS_CARD_NET_CFG_DISC = 3
    STATUS_CARD_NET_CFG_CONNECT = 4

    ERROR_CARDSEED_FAILED = 'Seed failed  Reason:{} '
    ERROR_CARDCREAT_FAILED = 'Card object init failed, Reason:{} '

    EQPT_E7_SCP_10G = "1026"
    EQPT_VDSLR_C = "1031"
    EQPT_VDSLR_O = "1032"
    EQPT_E7_GPON4_R2 = "1036"
    EQPT_E7_GPON8_CARD = "1037"

    EQPT_SCP2_40G = "1500"
    EQPT_SCP2_10G = "1503"
    EQPT_GPON_16X = "1502"
    EQPT_10GE_4X = "1501"
    # VDSLR2 Combo
    EQPT_VDSLR2_C = "1515"
    # VDSLR2 Overlay
    EQPT_VDSLR2_O = "1516"
    # VDSLR2 DataOnly
    EQPT_VDSLR2_D = "1517"
    EQPT_VDSLR2_VCP_192 = "1518"
    EQPT_VDSLR2_VCP_384 = "1519"
    # E3_VDSLR2 Combo
    EQPT_E3VDSLR2_NoCopper_C = "2006"
    EQPT_E3VDSLR2_HasCopper_C = "2007"
    # E3_VDSLR2 Overlay
    EQPT_E3VDSLR2_NoCopper_O = "2008"
    EQPT_E3VDSLR2_HasCopper_O = "2009"
    # E3 VCP
    EQPT_E3_VCP = "2010"
    # NGPON 2x4
    EQPT_E7_NGPON2X4 = "3206"

    cardtype_dct = {
        '1026': "E7-SCP-10G",
        '1031': "E7-VDSL-Combo",
        '1032': "E7-VDSL-Overlay",
        '1036': "E7 GPON-4r2 Card",
        '1037': "E7-GPON8 Card",
        '1500': "SCP2-40G",
        '1501': "10GE-4X",
        '1502': "GPON-16X",
        '1503': "SCP2-10G",
        '1515': "E7-VDSLR2-Combo",
        '1516': "E7-VDSLR2-Overlay",
        '1517': "E7-VDSLR2-DataOnly",
        '1518': "E7-VCP192",
        '1519': "E7-VCP384",
        '2006': "E3-VDSLR2-Combo-NoCopper",
        '2007': "E3-VDSLR2-Combo-HasCopper",
        '2008': "E3-VDSLR2-Overlay-NoCopper",
        '2009': "E3-VDSLR2-Overlay-HasCopper",
        '2010': "E3-VCP",
        '3206': "NGPON2x4",
        }

    TOOLBOX_CDCLIB_IPSTART = "10.245.1.1"
    TOOLBOX_CDCLIB_IPEND = "10.245.255.255"

    PROTOCOL_SSH_PORT = 23

    def __init__(self):
        pass

    @staticmethod
    def get_uartservercfg():
        full_path = ""
        path_list = os.getcwd().split('\\')
        del path_list[-1]
        for tup in path_list:
            full_path = full_path + tup + "\\"

        if 'Windows' in platform.system():
            return full_path + "config\\" + GlobalVar.NAME_CFG_UARTSERVER
        elif "Linux" in platform.system():
            return full_path + "/config" + GlobalVar.NAME_CFG_UARTSERVER

    @staticmethod
    def get_cardtypepath():
        full_path = ""
        path_list = os.getcwd().split('\\')
        del path_list[-1]
        for tup in path_list:
            full_path = full_path + tup + "\\"

        if 'Windows' in platform.system():
            return full_path + "config\\" + GlobalVar.PATH_CONFIGURE_CARDTYPE
        elif "Linux" in platform.system():
            return full_path + "/config" + GlobalVar.PATH_CONFIGURE_CARDTYPE

    @staticmethod
    def set_cardtypepath(path):
        GlobalVar.PATH_CONFIGURE_CARDTYPE = path

    @staticmethod
    def get_command_bid_t10xx():
        return GlobalVar.COMMAND_GETBID_T10XX

    @staticmethod
    def get_command_bid_p85xx():
        return GlobalVar.COMMAND_GETBID_P85XX

    @staticmethod
    def get_command_bid_axos():
        return GlobalVar.COMMAND_GETBID_AXOS

    @staticmethod
    def get_command_bid_p83xx():
        return GlobalVar.COMMAND_GETBID_P83XX

    @staticmethod
    def get_command_seed_t10xx(path, server):
        return GlobalVar.COMMAND_SEED_T10XX.format(server, path)

    @staticmethod
    def get_command_cpuinfo():
        return GlobalVar.COMMAND_GETCUPINFO

    @staticmethod
    def get_command_ping(ip):
        return GlobalVar.COMMAND_PING_T10XX.format(ip)

    @staticmethod
    def get_command_reboot():
        return GlobalVar.COMMAND_REBOOT_LINUX

    @staticmethod
    def get_command_setip(eth, ip):
        return GlobalVar.COMMAND_SETIP_T10XX.format(eth, ip)

    @staticmethod
    def get_command_delip(eth, ip):
        return GlobalVar.COMMAND_DELIP_T10XX.format(eth, ip)

    @staticmethod
    def get_command_setroute(eth, ip):
        return GlobalVar.COMMAND_SETROUTE_T10XX.format(ip, eth)

    @staticmethod
    def get_command_delroute():
        return GlobalVar.COMMAND_DELROUTE_T10XX

    @staticmethod
    def get_message_seedconfirm_t10xx():
        return GlobalVar.MESSAGE_SEED_CONFIRM_T10XX

    @staticmethod
    def get_message_pingfail():

        if 'Windows' in platform.system():
            return GlobalVar.MESSAGE_PING_LOST_WINDOWS
        elif "Linux" in platform.system():
            return GlobalVar.MESSAGE_PING_LOST_LINUX

    @staticmethod
    def get_message_pingfail_t10xx():
        return GlobalVar.MESSAGE_PING_LOST_LINUX

    @staticmethod
    def get_config_cdcgateway():
        return GlobalVar.CONFIG_CDCDOC_SERVER_GATEWAYIP

    @staticmethod
    def get_byte_ctrl(key):
        try:
            ascii = 0x1f & ord(key)
            return chr(int(ascii))
        except Exception as e:
            return key

    @staticmethod
    def format_ip(ip1, ip2, ip3, ip4):
        return GlobalVar.MESSAGE_IP_FORMAT.format(ip1, ip2, ip3, ip4)

    @staticmethod
    def load_cardtypefile():
        cfgparser = configparser.ConfigParser()
        cfgparser.read(GlobalVar.get_cardtypepath())
        return cfgparser

    @staticmethod
    def is_e7vdslr2(cardtype):

        if (operator.eq(cardtype, GlobalVar.EQPT_VDSLR2_C)) or\
            (operator.eq(cardtype, GlobalVar.EQPT_VDSLR2_O)) or\
                (operator.eq(cardtype, GlobalVar.EQPT_VDSLR2_D)):
            return True
        else:
            return False

    @staticmethod
    def is_e7vcp(cardtype):

        if (operator.eq(cardtype, GlobalVar.EQPT_VDSLR2_VCP_192)) or \
                (operator.eq(cardtype, GlobalVar.EQPT_VDSLR2_VCP_384)):
            return True
        else:
            return False

    @staticmethod
    def is_e348c(cardtype):
        """python 3 use new method operator.eq() replace cmp"""
        if (operator.eq(cardtype, GlobalVar.EQPT_E3VDSLR2_NoCopper_C)) or \
                (operator.eq(cardtype, GlobalVar.EQPT_E3VDSLR2_HasCopper_C)) or \
                (operator.eq(cardtype, GlobalVar.EQPT_E3VDSLR2_NoCopper_O)) or \
                (operator.eq(cardtype, GlobalVar.EQPT_E3VDSLR2_HasCopper_O)):
            return True
        else:
            return False

    @staticmethod
    def is_e3vcp(cardtype):

        if operator.eq(cardtype, GlobalVar.EQPT_E3_VCP):
            return True
        else:
            return False

    @staticmethod
    def is_scp2(cardtype):

        if operator.eq(cardtype, GlobalVar.EQPT_SCP2_10G) or \
                operator.eq(cardtype, GlobalVar.EQPT_SCP2_40G):
            return True
        else:
            return False

    @staticmethod
    def is_scp10g(cardtype):

        if operator.eq(cardtype, GlobalVar.EQPT_E7_SCP_10G):
            return True
        else:
            return False

    @staticmethod
    def is_e7gpon4r2(cardtype):

        if operator.eq(cardtype, GlobalVar.EQPT_E7_GPON4_R2):
            return True
        else:
            return False

    @staticmethod
    def is_e7gpon8(cardtype):

        if operator.eq(cardtype, GlobalVar.EQPT_E7_GPON8_CARD):
            return True
        else:
            return False

    @staticmethod
    def is_axosngpon2x4(cardtype):

        if operator.eq(cardtype, GlobalVar.EQPT_E7_NGPON2X4):
            return True
        else:
            return False

    @staticmethod
    def is_gpon16x(cardtype):

        if operator.eq(cardtype, GlobalVar.EQPT_GPON_16X):
            return True
        else:
            return False

    @staticmethod
    def is_10g4x(cardtype):

        if operator.eq(cardtype, GlobalVar.EQPT_10GE_4X):
            return True
        else:
            return False
