#!/usr/bin/python

import sys
import os
import click
from threading import Timer
from source.baseclass.cli import Cli

class Test:
    def __init__(self):
        pass

    def __del__(self):
        return

    def do_timeout(self):
        print("time out")

    def set_timer(self, second):
        Timer(second, self.do_timeout).start()

def print_version(ctx, param, value):
    click.echo('Vession 1.0')
    # ctx.exit()


#@click.command()
#@click.option('--version', is_flag=True, callback=print_version, expose_value=False, is_eager=True)
#@click.option('--command', prompt='$', help=' command you want to run')
def main():
    str=""
    cli_handler = Cli()
    cli_handler.do_parse()


if __name__ == "__main__":
    main()
