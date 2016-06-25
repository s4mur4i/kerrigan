import sys
import argparse

from misc.Logger import logger
from core.awsrequests import awsrequests
from misc import Misc
from core.base import base


class s3(base):
    def __init__(self, global_options, account_information):
        self.global_options = global_options
        self.account_information = account_information

    def start(self):
        logger.info('Invoked starting point for SecurityGroup')
        parser = argparse.ArgumentParser(description='ec2 tool for devops', usage='''kerrigan.py s3 <command> [<args>]

Second level options are:
    report_s3
        ''' + self.global_options)
        parser.add_argument('command', help='Command to run')
        args = parser.parse_args(sys.argv[2:3])
        if not hasattr(self, args.command):
            logger.error('Unrecognized command')
            parser.print_help()
            exit(1)
        getattr(self, args.command)()

    def report_s3(self):
        '''
        This function is a wrapper for parsing arguments and printing for s3 attribute reports
        :return:
        '''
        logger.info("Started report generation command")
        a = awsrequests(session=self.account_information['session'])
        parser = argparse.ArgumentParser(description='report generation about s3', usage='''kerrigan.py s3 report_s3 [<args>]]
        ''' + self.global_options, formatter_class=argparse.ArgumentDefaultsHelpFormatter, prog="kerrigan")
        parser.add_argument('--columns', action='store', default=a.service_supported_columns(service="s3").keys(),
                            help="Which columns to display")
        parser.add_argument('--filters', action='store', default=None,
                            help="The filters that should be used, example: key1:value1,key2:value2")
        args = parser.parse_args(sys.argv[3:])
