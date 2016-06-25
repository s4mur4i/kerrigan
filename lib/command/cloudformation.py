import sys
import argparse

from misc.Logger import logger
from core.awsrequests import awsrequests
from misc import Misc
from core.base import base


class cloudformation(base):
    def __init__(self, global_options, account_information):
        self.global_options = global_options
        self.account_information = account_information

    def start(self):
        logger.info('Invoked starting point for Cloudformation')
        parser = argparse.ArgumentParser(description='cloudformation tool for devops', usage='''kerrigan.py cloudformation <command> [<args>]

Second level options are:
    report_cloudformation
        ''' + self.global_options)
        parser.add_argument('command', help='Command to run')
        args = parser.parse_args(sys.argv[2:3])
        if not hasattr(self, args.command):
            logger.error('Unrecognized command')
            parser.print_help()
            exit(1)
        getattr(self, args.command)()

    def report_cloudformation(self):
        '''
        This function is a wrapper for parsing arguments and printing for cloudformation attribute reports
        Tested
        :return:
        '''
        logger.info("Started report generation command")
        a = awsrequests(session=self.account_information['session'])
        parser = argparse.ArgumentParser(description='report generation about cloudformation', usage='''kerrigan.py cloudformation report_cloudformation [<args>]]
        ''' + self.global_options, formatter_class=argparse.ArgumentDefaultsHelpFormatter, prog="kerrigan")
        parser.add_argument('--columns', action='store', default=a.service_supported_columns(service="cloudformation").keys(),
                            help="Which columns to display")
        args = parser.parse_args(sys.argv[3:])
        columns = Misc.parse_service_columns(service="cloudformation",columns=args.columns)
        result = a.information_cloudformation(columns=columns)
        logger.output(data=result, csvvar=self.account_information['logger_arguments']['csv'],
                      tablevar=self.account_information['logger_arguments']['table'])
