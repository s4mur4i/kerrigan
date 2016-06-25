import sys
import argparse

from misc.Logger import logger
from core.base import base
from misc import Misc


class ami(base):
    def __init__(self, global_options=None):
        self.global_options = global_options
        logger.info('Ami module entry endpoint')
        self.cli = Misc.cli_argument_parse()

    def start(self):
        logger.info('Invoked starting point for ami')
        parser = argparse.ArgumentParser(description='ec2 tool for devops', usage='''kerrigan.py ami <command> [<args>]

Second level options are:
  check
        ''' + self.global_options)
        parser.add_argument('command', help='Command to run')
        args = parser.parse_args(sys.argv[2:3])
        if not hasattr(self, args.command):
            logger.error('Unrecognized command')
            parser.print_help()
            exit(1)
        getattr(self, args.command)()

    def check(self):
        # FIXME this is broken
        logger.info("Doing config check in AWS")
        parser = argparse.ArgumentParser(description='ec2 tool for devops', usage='''kerrigan.py ami check [<args>]]
        ''' + self.global_options)
