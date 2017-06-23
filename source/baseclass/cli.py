#!/usr/bin/python3.5

import sys
import string
import getopt
import click

from source.baseclass.card import Card as card
from source.baseclass.cardfactory import CardFactory
from source.baseclass.logmanage import LogManage
from source.baseclass.toolbox import ToolBox


class Cli(LogManage):
    command_string = 0
    command_list = []
    card = None
    cli_options = {
        'seed': ('seed [-a hostip] [-p port] [-s ftp_serverip] [-v path]', 'card_seed'),
        'upgrade': ('upgrade [-a ip] [-p port] [-b branch] [-v version]', 'card_upgrade'),
        'find': ('find my card', 'do_find'),
        'mfg': ('MFG test', 'do_mfg'),
        'box': ('Tool box', 'do_box'),
    }

    def __init__(self):

        pass

    def __del__(self):
        return

    def do_printf(self, msg, color='green'):
        self.log_printf(msg, color)

        pass
    def do_find(self,command):
        toolbox = ToolBox()
        toolbox.do_find()

    def do_box(self, key):
        click.echo('Path: %s' % click.format_filename(b'foo.txt'))
        pass

    def card_upgrade(self):
        self.do_printf('seed!', 'green')
        pass

    def do_help(self, key):
        try:
            if (self.command_list[0] == 'help') or (self.command_list[0] == '--help'):
                self.do_printf(self.cli_options[key][0], 'green')
                return False
            if len(self.command_list) > 1:
                if (self.command_list[1] == 'help')\
                        or(self.command_list[1] == '--help'):
                    self.do_printf(self.cli_options[key][0], 'green')
                    return True
        except:
            self.do_printf('No help option!', 'red')

        return False

    def card_seed(self, command):
        self.card = CardFactory(command).do_getcard()
        if not self.card:
            self.log_printf('Card type error ！')
            return
        else:
            self.card.do_seed_count()

    def do_parse(self):
        while True:
            self.command_string = input("$: ")
            self.command_list = self.command_string.split()

            if 0 == len(self.command_list):
                continue

            for key in self.cli_options:
                if self.do_help(key):
                    break
                if key == self.command_list[0]:
                    getattr(self, self.cli_options[key][1])(self.command_string)
                    break
            if (not key == self.command_list[0]) and \
                    (not self.command_list[0] == 'help'):
                self.do_printf('command not support !', 'green')
