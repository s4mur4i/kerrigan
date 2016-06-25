import sys
import argparse

from misc.Logger import logger
from core.awsrequests import awsrequests
from misc import Misc
from core.base import base


class autoscale(base):
    def __init__(self, global_options, account_information):
        self.global_options = global_options
        self.account_information = account_information

    def start(self):
        logger.info('Invoked starting point for SecurityGroup')
        parser = argparse.ArgumentParser(description='ec2 tool for devops', usage='''kerrigan.py autoscale <command> [<args>]

Second level options are:
    report_autoscale
        ''' + self.global_options)
        parser.add_argument('command', help='Command to run')
        args = parser.parse_args(sys.argv[2:3])
        if not hasattr(self, args.command):
            logger.error('Unrecognized command')
            parser.print_help()
            exit(1)
        getattr(self, args.command)()

    def report_autoscale(self):
        '''
        This function is a wrapper for parsing arguments and printing for autoscale attribute reports
        :return:
        '''
        logger.info("Started report generation command")
        a = awsrequests(session=self.account_information['session'])
        parser = argparse.ArgumentParser(description='report generation about autoscale', usage='''kerrigan.py autoscale report_autoscale [<args>]]
        ''' + self.global_options, formatter_class=argparse.ArgumentDefaultsHelpFormatter, prog="kerrigan")
        parser.add_argument('--columns', action='store',
                            default=a.service_supported_columns(service="autoscale").keys(),
                            help="Which columns to display")
        parser.add_argument('--filters', action='store', default=None,
                            help="The filters that should be used, example: key1:value1,key2:value2")
        args = parser.parse_args(sys.argv[3:])
