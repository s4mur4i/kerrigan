import sys
import argparse

from misc.Logger import logger
from core.awsrequests import awsrequests
from misc import Misc
from core.base import base


class apigateway(base):
    def __init__(self, global_options, account_information):
        self.global_options = global_options
        self.account_information = account_information

    def start(self):
        logger.info('Invoked starting point for Apigateway')
        parser = argparse.ArgumentParser(description='ec2 tool for devops', usage='''kerrigan.py apigateway <command> [<args>]

Second level options are:
    report_apigateway
    upload_apigateway
    dump_apigateway
        ''' + self.global_options)
        parser.add_argument('command', help='Command to run')
        args = parser.parse_args(sys.argv[2:3])
        if not hasattr(self, args.command):
            logger.error('Unrecognized command')
            parser.print_help()
            exit(1)
        getattr(self, args.command)()

    def report_apigateway(self):
        '''
        This function is a wrapper for parsing arguments and printing for apigateway attribute reports
        :return:
        '''
        logger.info("Started report generation command")
        a = awsrequests(session=self.account_information['session'])
        parser = argparse.ArgumentParser(description='report generation about apigateway', usage='''kerrigan.py apigateway report_apigateway [<args>]]
        ''' + self.global_options, formatter_class=argparse.ArgumentDefaultsHelpFormatter, prog="kerrigan")
        parser.add_argument('--columns', action='store', default=a.service_supported_columns(service="sg").keys(),
                            help="Which columns to display")
        args = parser.parse_args(sys.argv[3:])
        columns = Misc.parse_service_columns(service="apigateway", columns=args.columns)
        result = a.information_apigateway(columns=columns)
        logger.output(data=result, csvvar=self.account_information['logger_arguments']['csv'],
                      tablevar=self.account_information['logger_arguments']['table'])

    def dump_apigateway(self):
        '''
        This function is a wrapper for parsing arguments and printing for apigateway attribute reports
        :return:
        '''
        logger.info("Started report generation command")
        a = awsrequests(session=self.account_information['session'])
        parser = argparse.ArgumentParser(description='report generation about apigateway', usage='''kerrigan.py apigateway report_apigateway [<args>]]
        ''' + self.global_options, formatter_class=argparse.ArgumentDefaultsHelpFormatter, prog="kerrigan")
        parser.add_argument('--name', required=True, action='store', help="Name of apigateway to dump")
        args = parser.parse_args(sys.argv[3:])
        result = a.dump_apigateway(name=args.name)
        print result

    def upload_apigateway(self):
        '''
        This function is a wrapper for parsing arguments and uploading apigateway
        :return:
        '''
        logger.info("Started upload command")
        a = awsrequests(session=self.account_information['session'])
        parser = argparse.ArgumentParser(description='upload apigateway', usage='''kerrigan.py apigateway upload_apigateway [<args>]]
        ''' + self.global_options, formatter_class=argparse.ArgumentDefaultsHelpFormatter, prog="kerrigan")
        parser.add_argument('--json', metavar='FILE', required=True, type=lambda x: Misc.is_valid_file(parser, x),
                            help="Which file to upload")
        parser.add_argument('--dryrun', action="store_true",default=False,help="No changes should be done")
        args = parser.parse_args(sys.argv[3:])
        result = a.upload_apigateway(json=Misc.parse_file_to_json(args.json),dryrun=args.dryrun)
        #print result
