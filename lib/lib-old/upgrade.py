import sys
import argparse

from misc.Logger import logger
from core.base import base
from misc import Misc


class upgrade(base):
    def __init__(self, global_options=None):
        self.global_options = global_options
        logger.info('Upgrade module entry endpoint')
        self.cli = Misc.cli_argument_parse()

    def start(self):
        logger.info('Invoked starting point for upgrade')
        parser = argparse.ArgumentParser(description='ec2 tool for devops', usage='''kerrigan.py upgrade <command> [<args>]

Second level options are:
    stack
        ''' + self.global_options)
        parser.add_argument('command', help='Command to run')
        args = parser.parse_args(sys.argv[2:3])
        if not hasattr(self, args.command):
            logger.error('Unrecognized command')
            parser.print_help()
            exit(1)
        getattr(self, args.command)()

    def stack(self):
        logger.info("Starting to gather information")
        parser = argparse.ArgumentParser(description='ec2 tool for devops', usage='''kerrigan.py upgrade stack [<args>]]
        ''' + self.global_options)
        parser.add_argument('--stack', action='store', help="Which stack to upgrade",required=True)
        parser.add_argument('--env', action='store', help="Which env to do tasks in",required=True)
        args = parser.parse_args(sys.argv[3:])


