#!/usr/bin/python3.5

import configparser
from source.baseclass.logmanage import LogManage
from source.baseclass.globalvar import GlobalVar
from source.baseclass.cardfactory import CardFactory


class FindCard(LogManage):

    result_ssh = []
    result_telnet = []
    exception_table = []
    session_telnet = None
    session_ssh = None

    def __init__(self):
        self.do_load_excptable()
        pass

    def do_load_excptable(self):

        cfg_file = GlobalVar.get_uartservercfg()
        cfgparser = configparser.ConfigParser()
        cfgparser.read(cfg_file)
        if cfgparser.has_section('IP_IGNORE'):
            for name, ip in cfgparser.items('IP_IGNORE'):
                self.exception_table.append(ip)

    def do_exceptioncheck(self, ip_str, port_int):

        for tmp in self.exception_table:
            except_ip = tmp.split("-")
            if -1 != except_ip[0].find(ip_str) and \
                    -1 != except_ip[1].find(str(port_int)):
                return True

        return False

    def do_sshscan(self):
        pass

    def do_uartserver_scan(self):
        """
        scan uart server that config in file config/uart_server.cfg
        :return:
        """
        path = GlobalVar.get_uartservercfg()
        cfgparser = configparser.ConfigParser()
        cfgparser.read(path)

        if cfgparser.has_section('UART_SERVER_IP'):
            for name, ip in cfgparser.items('UART_SERVER_IP'):
                for port in range(10001, 10017):
                    if self.do_exceptioncheck(ip, port):
                        self.log_printf(GlobalVar.MESSAGE_FIND_EXCEPTION_TABLE.format(ip, port))
                        tup_card = tuple(
                            [("ip", ip), ("port", port), ("EqptText", "igonre"), ("SN", "ignore"),("TYPE", "ignore")])
                        self.result_telnet.append(tup_card)
                        continue

                    command = GlobalVar.CONFIG_CARDCREAT_COMMAND_FORMAT.format(ip, port)
                    card = CardFactory(command).do_getcard()

                    if not card:
                        continue

                    tup_card = tuple([("ip", ip),
                                      ("port", port),
                                      ("EqptText", card.bid.EqptText),
                                      ("SN", card.bid.SerialNumber),
                                      ("TYPE", card.session_telnet.login_type)])
                    self.result_telnet.append(tup_card)
                self.do_printfresult()
                self.result_telnet = []
        self.log_printf("Scan finished")

    def do_scan(self):
        """
        Scan CDC network from 10.245.1.1  --- 10.245.255.255
        :return:
        """
        self.do_uartserver_scan()

    def do_printfresult(self):

        print("|---------------------------------------------------------------|")
        print("| %-19s | %-20s | %-16s |" % ("IP", "EqptType", "SN"))
        for tup in self.result_telnet:
            print("| %-12s:%-3s | %-20s | %-16s | %s |" % (tup[0][1], tup[1][1], tup[2][1], tup[3][1],tup[4][1]))

        print("|---------------------------------------------------------------|")

        print("End")
