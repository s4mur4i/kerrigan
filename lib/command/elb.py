import sys
import argparse

from misc.Logger import logger
from core.awsrequests import awsrequests
from misc import Misc
from core.base import base


class elb(base):
    def __init__(self, global_options, account_information):
        self.global_options = global_options
        self.account_information = account_information

    def start(self):
        logger.info('Invoked starting point for Elb')
        parser = argparse.ArgumentParser(description='ec2 tool for devops', usage='''kerrigan.py elb <command> [<args>]

Second level options are:
    report_elb
        ''' + self.global_options)
        parser.add_argument('command', help='Command to run')
        args = parser.parse_args(sys.argv[2:3])
        if not hasattr(self, args.command):
            logger.error('Unrecognized command')
            parser.print_help()
            exit(1)
        getattr(self, args.command)()

    def report_elb(self):
        '''
        This function is a wrapper for parsing arguments and printing for elb attribute reports
        Tested
        :return:
        '''
        logger.info("Started report generation command")
        a = awsrequests(session=self.account_information['session'])
        parser = argparse.ArgumentParser(description='report generation about elbs', usage='''kerrigan.py elb report_elb [<args>]]
        ''' + self.global_options, formatter_class=argparse.ArgumentDefaultsHelpFormatter, prog="kerrigan")
        parser.add_argument('--columns', action='store', default=a.service_supported_columns(service="elb"),
                            help="Which columns to display")
        parser.add_argument('--filters', action='store', default=None,
                            help="The filters that should be used, example: key1:value1,key2:value2")
        args = parser.parse_args(sys.argv[3:])
        columns = Misc.parse_service_columns(columns=args.columns, service="elb")
        if args.filters:
            filters = Misc.format_boto3_filter(filters=args.filters)
        else:
            filters = None
        result = a.information_elbs(columns=columns, filters=filters)
        for res in result:
            if self.account_information['logger_arguments']['table']:
                res['AvailabilityZones'] = Misc.list_to_multiline_string(list=res['AvailabilityZones'])
                res['SecurityGroups'] = Misc.list_to_multiline_string(list=res['SecurityGroups'])
                res['Instances'] = Misc.list_to_multiline_string(list=res['Instances'])
            else:
                res['AvailabilityZones'] = Misc.join_list_to_string(list=res['AvailabilityZones'])
                res['SecurityGroups'] = Misc.join_list_to_string(list=res['SecurityGroups'])
                res['Instances'] = Misc.join_list_to_string(list=res['Instances'])
        logger.output(data=result, csvvar=self.account_information['logger_arguments']['csv'],
                      tablevar=self.account_information['logger_arguments']['table'])
