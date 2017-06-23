#!/usr/bin/env python3.5

import re
from source.baseclass.logmanage import LogManage
from telnetlib import Telnet as telnet
from source.baseclass.globalvar import GlobalVar
from source.baseclass.card import CardTimer
from time import sleep

ERROR_TELNET_REFUSE = 'Telnet to [{0}:{1}] failed, Reason:{2} '


class TelnetChannel(LogManage):
    channel = None
    prompt_cli = "Username"
    prompt_uart = "login"
    clie7_username = "e7support"
    clie3_username = "e3support"
    cli_pwd = "admin"
    username = ""
    pwd = ""
    host = ""
    port = ""
    login_status = False
    login_type = "GOJO-uart"

    def __init__(self, username='root', pwd='root', ip=None, port=None):
        self.username = username
        self.pwd = pwd
        self.host = ip
        self.port = port
        self.login_status = False

    def check_connect(self):
        # sleep(1)
        self.write("\r\n")
        response = self.read()
        if len(response) > 0:
            return True
        return False

    def login(self):
        try:
            """Create a telnet client and try to connect to the server"""
            self.channel = telnet(host=self.host, port=self.port)
            if not self.check_connect():
                return False
        except Exception as e:
            self.log_printf(ERROR_TELNET_REFUSE.format(self.host, self.port, e.strerror), "red")
            return False

        # self.write('\r\n')
        # self.write('\r\n')
        # self.write('\r\n')
        # self.write('\r\n')
        self.write('\r\n')
        log_info = self.do_stringread()

        if -1 != log_info.find(":>"):
            self.write("exit \r\n")
            sleep(1)
            self.write("exit \r\n")
        elif -1 != log_info.find(">"):
            self.write("exit \r\n")

        self.write('\r\n')
        log_info = self.do_stringread()

        if -1 != log_info.find("closed by foreign host"):
            self.write("\r\n")

        if -1 != log_info.find(self.prompt_cli):
            self.do_clilogin()
        elif -1 != log_info.find(self.prompt_uart):
            self.do_uartlogin()

        """
        non_login_pattern = re.compile(b"root@localhost:")
        if self.username:
            self.channel.write(b'\r\n')

            pattern1 = re.compile(b"login: ")
            pattern2 = re.compile(b"Username: ")
            pattern3 = re.compile(b"Password: ")
            pattern4 = re.compile(b"root@")
            for count in range(2):
                i, m, b = self.channel.expect([pattern1, pattern2, pattern3, pattern4, non_login_pattern], timeout=5)
                if i < 1:
                    self.channel.write(self.username.encode('ascii') + b'\r\n')
                    break
                else:
                    self.channel.write(b'\n')
        if self.pwd:
            pattern1 = re.compile(b"Password: ")
            i, m, b = self.channel.expect([pattern1, pattern4, non_login_pattern], timeout=5)
            if i < 1:
                self.channel.write(self.pwd.encode('ascii') + b'\r\n')
        # sleep(5)
        self.channel.write(b'\r\n')
        self.channel.write(b'\r\n')
        tmp = self.read()
        if tmp:
            tmp_str = str(tmp, encoding="utf-8")
            if -1 == tmp_str.find("@localhost"):
                self.channel.write(b'exit \r\n')
        self.channel.write(b'\r\n')
        self.channel.write(b'\r\n')
        if tmp:
            tmp_str = str(tmp, encoding="utf-8")
            if -1 == tmp_str.find("@localhost"):
                self.channel.write(b'exit \r\n')
        self.channel.write(bytes(0x03))
        self.channel.write(bytes(0x03))
        self.channel.write(b"shell \r\n")
        self.login_status = True
        return True
        """

    def do_shellcheck(self):
        self.channel.write(b'\r\n')
        tmp = self.read()
        if tmp:
            tmp_str = str(tmp, encoding="utf-8")
            if -1 != tmp_str.find("@localhost"):
                self.login_status = True
                return True
        else:
            return False

    def do_clilogin(self):
        self.login_type = "CLI-uart"
        """input ctrl+c first"""
        self.write(GlobalVar.get_byte_ctrl('c'))
        self.write(GlobalVar.get_byte_ctrl('c'))

        pattern1 = re.compile(b"Username: ")
        pattern2 = re.compile(b"Password: ")
        pattern3 = re.compile(b"login: ")
        non_login_pattern = re.compile(b"root@localhost:")

        """e7 card cli login"""
        for count in range(2):
            i, m, b = self.channel.expect([pattern1, pattern2, non_login_pattern], timeout=3)
            if i < 1:
                self.channel.write(self.clie7_username.encode('ascii') + b'\r\n')
                break
            else:
                self.channel.write(b'\n')

        i, m, b = self.channel.expect([pattern2, non_login_pattern], timeout=3)
        if i < 1:
            self.channel.write(self.cli_pwd.encode('ascii') + b'\r\n')

        if self.do_logincheck():
            return True

        """e3 card cli login"""
        for count in range(2):
            i, m, b = self.channel.expect([pattern1, pattern2, non_login_pattern], timeout=3)
            if i < 1:
                self.channel.write(self.clie3_username.encode('ascii') + b'\r\n')
                break
            else:
                self.channel.write(b'\n')

        i, m, b = self.channel.expect([pattern2, non_login_pattern], timeout=3)
        if i < 1:
            self.channel.write(self.cli_pwd.encode('ascii') + b'\r\n')

        if self.do_logincheck():
            return True

        """shell login"""
        self.write('shell \r')
        for count in range(2):
            i, m, b = self.channel.expect([pattern3, non_login_pattern], timeout=2)
            if i < 1:
                self.channel.write(self.username.encode('ascii') + b'\r')
                break
            else:
                self.channel.write(b'\n')

        i, m, b = self.channel.expect([pattern2, non_login_pattern], timeout=2)
        if i < 1:
            self.channel.write(self.pwd.encode('ascii') + b'\r')

        if self.do_logincheck():
            return True

        return False

    def do_uartlogin(self):
        self.login_type = "GOJO-uart"
        """input ctrl+c first"""
        self.write(GlobalVar.get_byte_ctrl('c'))
        self.write(GlobalVar.get_byte_ctrl('c'))

        pattern1 = re.compile(b"login: ")
        pattern2 = re.compile(b"Password: ")
        pattern3 = re.compile(b"root@")

        non_login_pattern = re.compile(b"root@localhost:")
        self.channel.write(b'\r\n')

        for count in range(2):
            i, m, b = self.channel.expect([pattern1, pattern2, pattern3, non_login_pattern], timeout=2)
            if i < 1:
                self.channel.write(self.username.encode('ascii') + b'\r\n')
                break
            else:
                self.channel.write(b'\n')

        i, m, b = self.channel.expect([pattern2, non_login_pattern], timeout=2)
        if i < 1:
            self.channel.write(self.pwd.encode('ascii') + b'\r\n')

        self.channel.write(b'\r\n')
        self.channel.write(b'\r\n')
        tmp = self.read()
        if tmp:
            tmp_str = str(tmp, encoding="utf-8")
            if -1 == tmp_str.find("@localhost"):
                self.channel.write(b'exit \r\n')
        self.channel.write(b'\r\n')
        self.channel.write(b'\r\n')
        tmp = self.read()
        if tmp:
            tmp_str = str(tmp, encoding="utf-8")
            if -1 == tmp_str.find("@localhost"):
                self.channel.write(b'exit \r\n')

        #self.channel.write(b"shell \r\n")
        self.login_status = True
        return True

    def do_logincheck(self):
        self.channel.write(b'\r\n')
        self.channel.write(b'\r\n')
        tmp = self.read()
        if tmp:
            tmp_str = str(tmp, encoding="utf-8")
            if -1 != tmp_str.find("@localhost"):
                return True
        else:
            return False

    def disconnect(self):
        self.login_status = False
        if self.channel is not None:

            # self.channel.write(b"exit \r\n")
            # sleep(2)
            self.channel.close()
            self.channel = None
        return

    def do_timeread(self, second):
        """
        read data from telnet session ,last xxx second
        :param second: last second
        :return: data read from telnet session
        """
        response_str = ""
        recv_buf = b''
        readtimer = CardTimer(second)
        readtimer.do_start()
        try:
            while not readtimer.timeout:

                for i in range(100):
                    sleep(0.1)
                    new_data = self.channel.read_very_eager()
                    if len(new_data) is 0:
                        break
                    else:
                        recv_buf += new_data

                    # recv_buf = None
                if recv_buf:
                    response_str += str(recv_buf, encoding="utf-8")
        except Exception as e:
            del e
        return response_str

    def read(self):
        """Read the response from the remote shell through the ssh channel
        Return: >0 -- Number of bytes received;
                 0 -- end of the response"""
        recv_buf = b''
        try:
            for i in range(100):
                sleep(0.1)
                new_data = self.channel.read_very_eager()
                if len(new_data) is 0:
                    break
                else:
                    recv_buf += new_data

            # if len(recv_buf) is 0:
                #recv_buf = None
        except Exception as e:
            del e
            # recv_buf = None
        finally:
            return recv_buf

    def do_stringread(self):
        """Read the response from the remote shell through the ssh channel
        Return: >0 -- Number of bytes received;
                 0 -- end of the response"""
        recv_buf = b''
        try:
            for i in range(100):
                sleep(0.1)
                new_data = self.channel.read_very_eager()
                if len(new_data) is 0:
                    break
                else:
                    recv_buf += new_data
        except Exception as e:
            del e
            # recv_buf = None
        finally:
            if recv_buf:
                recv_buf = str(recv_buf, encoding="utf-8")
            else:
                recv_buf = ""
            return recv_buf

    def write(self, data):
        """Write the command to the remote shell through the ssh channel
        Return: >0 -- number of bytes sent;
                 0 -- failed to send the command """
        sent_len = 0
        #data += " \r\n"
        try:
            sent_len = self.channel.write(data.encode('ascii'))
        except Exception as e:
            print(e)
            sent_len = 0
        finally:
            return sent_len
