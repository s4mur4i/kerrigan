import argparse
import sys

from core.awsrds import awsrds
from misc.Logger import logger
from core.base import base


class rds(base):
    def __init__(self, global_options=None):
        self.global_options = global_options
        logger.info('RDS module entry endpoint')
        self.cli = Misc.cli_argument_parse()

    def start(self):
        logger.info('Invoked starting point for rds')
        parser = argparse.ArgumentParser(description='ec2 tool for devops', usage='''kerrigan.py rds <command> [<args>]

Second level options are:
    query_parameter_group       returns all records of a parameter group
        ''' + self.global_options)
        parser.add_argument('command', help='Command to run')
        args = parser.parse_args(sys.argv[2:3])
        if not hasattr(self, args.command):
            logger.error('Unrecognized command')
            parser.print_help()
            exit(1)
        getattr(self, args.command)()

    def query_parameter_group(self):
        logger.info("Gather parameter group values")
        parser = argparse.ArgumentParser(description='ec2 tool for devops', usage='''kerrigan.py rds query_parameter_group [<args>]]
        ''' + self.global_options)
        parser.add_argument('--name', action='store', help="Name of db-parameter group")
        args = parser.parse_args(sys.argv[3:])
        e = awsrds()
        ret = e.get_parameter_group(name=args.name)
        # FIXME print information insted of generating csv file
