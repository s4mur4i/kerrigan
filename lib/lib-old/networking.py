import sys
import argparse

from misc.Logger import logger


class networking(object):
    def __init__(self, global_options=None):
        self.global_options = global_options
        logger.info('Networking module entry endpoint')
        self.cli = Misc.cli_argument_parse()

    def start(self):
        logger.info('Invoked starting point for env')
        parser = argparse.ArgumentParser(description='ec2 tool for devops', usage='''kerrigan.py networking <command> [<args>]

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
        logger.info("Doing config check in AWS")
        # FIXME this is broken, need to fix
        parser = argparse.ArgumentParser(description='ec2 tool for devops', usage='''kerrigan.py networking check [<args>]]
        ''' + self.global_options)
