import sys
import argparse

from misc.Logger import logger
from core.awschecks import awschecks
from core.awsrequests import awsrequests
from core.base import base
from misc import Misc


class securitygroup(base):
    def __init__(self, global_options=None):
        self.global_options = global_options
        logger.info('Securitygroup module entry endpoint')
        self.cli = Misc.cli_argument_parse()

    def start(self):
        logger.info('Invoked starting point for securitygroup')
        parser = argparse.ArgumentParser(description='ec2 tool for devops', usage='''kerrigan.py securitygroup <command> [<args>]

Second level options are:
    compare
        ''' + self.global_options)
        parser.add_argument('command', help='Command to run')
        args = parser.parse_args(sys.argv[2:3])
        if not hasattr(self, args.command):
            logger.error('Unrecognized command')
            parser.print_help()
            exit(1)
        getattr(self, args.command)()

    def compare(self):
        logger.info("Going to compare security groups")
        a = awsrequests()
        parser = argparse.ArgumentParser(description='ec2 tool for devops', usage='''kerrigan.py instance compare_securitygroups [<args>]]
        ''' + self.global_options)
        parser.add_argument('--env', action='store', help="Environment to check")
        parser.add_argument('--dryrun', action='store_true', default=False, help="No actions should be taken")
        args = parser.parse_args(sys.argv[3:])
        a = awschecks()
        a.compare_securitygroups(env=args.env, dryrun=args.dryrun)
