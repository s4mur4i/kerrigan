import sys
import argparse

from misc.Logger import logger
from core.awsservice import awsservice
from core.awsrequests import awsrequests
from core.awschecks import awschecks
from core.generate import generate
from core.base import base
from misc import Misc


class route53(base):
    def __init__(self, global_options=None):
        self.global_options = global_options
        logger.info('Route53 module entry endpoint')
        self.cli = Misc.cli_argument_parse()

    def start(self):
        logger.info('Invoked starting point for route53')
        parser = argparse.ArgumentParser(description='route53 tool for devops', usage='''kerrigan.py route53 <command> [<args>]

Second level options are:
  gw_watchdog
  compare
  info
        ''' + self.global_options)
        parser.add_argument('command', help='Command to run')
        args = parser.parse_args(sys.argv[2:3])
        if not hasattr(self, args.command):
            logger.error('Unrecognized command')
            parser.print_help()
            exit(1)
        getattr(self, args.command)()

    def gw_watchdog(self):
        logger.info("Starting watchdog")
        parser = argparse.ArgumentParser(description='ec2 tool for devops', usage='''kerrigan.py route53 watchdog [<args>]]
        ''' + self.global_options)
        parser.add_argument('--env', action='store', help="Environment to gather information about")
        args = parser.parse_args(sys.argv[3:])
        a = awsservice()
        a.gw_watchdog(env=args.env)

    def compare(self):
        logger.info("Starting comparing route53 entries")
        parser = argparse.ArgumentParser(description='ec2 tool for devops', usage='''kerrigan.py route53 compare [<args>]]
        ''' + self.global_options)
        parser.add_argument('--env', action='store', help="Environment to gather information about")
        parser.add_argument('--dryrun', action='store_true',default=False, help="No changes should be done")
        args = parser.parse_args(sys.argv[3:])
        a = awschecks()
        a.compare_route53(env=args.env,dryrun=args.dryrun)

    def info(self):
        logger.info("Starting to gather information")
        a = awsrequests()
        parser = argparse.ArgumentParser(description='ec2 tool for devops', usage='''kerrigan.py route53 info [<args>]]
        ''' + self.global_options)
        parser.add_argument('--env', action='store', help="Environment to gather information about")
        args = parser.parse_args(sys.argv[3:])
        res = a.route53_info(env=args.env)
        for r in res:
            if self.cli['csv']:
                r['Values'] = Misc.join_list_to_string(list=r['Values'])
            elif self.cli['table']:
                r['Values'] = Misc.list_to_multiline_string(r['Values'])
            else:
                logger.error('There is an unhandled printing. Need to investigate')
            # Add information if not present:
            if 'Weight' not in r:
                r['Weight'] = '-'
                r['SetIdentifier'] = '-'
        logger.output(data=res, csvvar=self.cli['csv'], tablevar=self.cli['table'])
