#!/usr/bin/python

import sys
import string
import getopt
import click


class LogManage:

    def __init__(self, module='default', type='local'):
        self.module = module
        self.type = type

    def log_error(self, text):

        return

    def log_write(self, text):

        return

    def log_output(self, path):
        pass

    def log_printf(self, msg, color='green'):
        print(msg)
        #click.secho(msg, fg=color)
        pass
