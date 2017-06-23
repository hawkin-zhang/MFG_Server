import sys
import os
import string
import getopt
import click
from source.baseclass.TelnetChannel import TelnetChannel as telnet
from source.baseclass.SSHChannel import SshChannel as ssh


PROTOCOL_TELNET_PORT = 23
PROTOCOL_SSH_PROT = 22
UARTSERVER_PORT_START = 10000
UARTSERVER_PORT_END = 10512

from source.baseclass.logmanage import LogManage as logmanage

"""connect factory use to create connect channel by port """


class ConnectFactory(logmanage):

    def __init__(self, hostip, port):
        self.hostip = hostip
        self.port = port
        pass

    """create object by port"""

    def do_createconnect(self):

        if self.port == PROTOCOL_SSH_PROT:
            return ssh()
        else :
            return telnet(ip=self.hostip, port=self.port)

    def do_getconnect(self):
        return self.do_createconnect()
