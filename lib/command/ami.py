import sys
import argparse

from misc.Logger import logger
from core.awsrequests import awsrequests
from misc import Misc
from core.base import base


class ami(base):
    def __init__(self, global_options, account_information):
        self.global_options = global_options
        self.account_information = account_information

    def start(self):
        logger.info('Invoked starting point for Ami')
        parser = argparse.ArgumentParser(description='ec2 tool for devops', usage='''kerrigan.py ami <command> [<args>]

Second level options are:
    report_ami
    instance_status
        ''' + self.global_options)
        parser.add_argument('command', help='Command to run')
        args = parser.parse_args(sys.argv[2:3])
        if not hasattr(self, args.command):
            logger.error('Unrecognized command')
            parser.print_help()
            exit(1)
        getattr(self, args.command)()

    def report_ami(self):
        '''
        This function is a wrapper for parsing arguments and printing for ami attribute reports
        :return:
        '''
        logger.info("Started report generation command")
        a = awsrequests(session=self.account_information['session'])
        parser = argparse.ArgumentParser(description='report generation about ami', usage='''kerrigan.py ami report_ami [<args>]]
        ''' + self.global_options, formatter_class=argparse.ArgumentDefaultsHelpFormatter, prog="kerrigan")
        parser.add_argument('--columns', action='store', default=a.service_supported_columns(service="ami").keys(),
                            help="Which columns to display")
        parser.add_argument('--filters', action='store', default=None,
                            help="The filters that should be used, example: key1:value1,key2:value2")
        args = parser.parse_args(sys.argv[3:])
        columns = Misc.parse_service_columns(service="ami", columns=args.columns)
        if args.filters:
            filters = Misc.format_boto3_filter(filters=args.filters)
        else:
            filters = None
        result = a.information_ami(columns=columns, filters=filters)
        logger.output(data=result, csvvar=self.account_information['logger_arguments']['csv'],
                      tablevar=self.account_information['logger_arguments']['table'])

    def instance_status(self):
        logger.info("Started instance status command")
        a = awsrequests(session=self.account_information['session'])
        parser = argparse.ArgumentParser(description='instance status about ami', usage='''kerrigan.py ami instance_Status [<args>]]
        ''' + self.global_options, formatter_class=argparse.ArgumentDefaultsHelpFormatter, prog="kerrigan")
        parser.add_argument('--imageid', action='store', default=None,
                            help="Only imageIds that should be queried")
        args = parser.parse_args(sys.argv[3:])
        result = a.image_instance_status(imageid=args.imageid)
        for res in result:
            if self.account_information['logger_arguments']['table']:
                res['Instances'] = Misc.list_to_multiline_string(list=res['Instances'])
            else:
                res['Instances'] = Misc.join_list_to_string(list=res['Instances'])
        logger.output(data=result, csvvar=self.account_information['logger_arguments']['csv'],
                      tablevar=self.account_information['logger_arguments']['table'])