import sys
import argparse
from misc.Logger import logger
from core.awsrequests import awsrequests
from misc import Misc
from core.base import base


class ec2(base):
    def __init__(self, global_options, account_information):
        self.global_options = global_options
        self.account_information = account_information

    def start(self):
        logger.info('Invoked starting point for Ec2')
        parser = argparse.ArgumentParser(description='ec2 tool for devops', usage='''kerrigan.py ec2 <command> [<args>]

Second level options are:
    report_ec2_instances
    create_ec2
    terminate_ec2
        ''' + self.global_options)
        parser.add_argument('command', help='Command to run')
        args = parser.parse_args(sys.argv[2:3])
        if not hasattr(self, args.command):
            logger.error('Unrecognized command')
            parser.print_help()
            exit(1)
        getattr(self, args.command)()

    def report_ec2_instances(self):
        '''
        This function is a wrapper for parsing arguments and printing for ec2 instance attribute reports
        Tested
        :return:
        '''
        logger.info("Started report generation command")
        a = awsrequests(session=self.account_information['session'])
        parser = argparse.ArgumentParser(description='report generation about ec2 instances', usage='''kerrigan.py ec2 report_ec2_instances [<args>]]
        ''' + self.global_options, formatter_class=argparse.ArgumentDefaultsHelpFormatter, prog="kerrigan")
        parser.add_argument('--columns', action='store', default=a.service_supported_columns(service="ec2").keys(),
                            help="Which columns to display")
        parser.add_argument('--filters', action='store', default=None,
                            help="The filters that should be used, example: key1:value1,key2:value2")
        args = parser.parse_args(sys.argv[3:])
        columns = Misc.parse_service_columns(service="ec2", columns=args.columns)
        if args.filters:
            filters = Misc.format_boto3_filter(filters=args.filters)
        else:
            filters = None
        result = a.information_ec2_instances(columns=columns, filters=filters)
        logger.output(data=result, csvvar=self.account_information['logger_arguments']['csv'],
                      tablevar=self.account_information['logger_arguments']['table'])

    def create_ec2(self):
        """
        This function is a wrapper for parsing aguments and printing for ec2 create instance
        Tested
        :return:
        """
        logger.info("Started create ec2 command")
        a = awsrequests(session=self.account_information['session'])
        parser = argparse.ArgumentParser(description='creation of ec2 instance', usage='''kerrigan.py ec2 create_ec2 [<args>]]
        ''' + self.global_options, formatter_class=argparse.ArgumentDefaultsHelpFormatter, prog="kerrigan")
        parser.add_argument('--puppet_role', action='store', default=None,
                            help="Puppet_role to create", required=True)
        parser.add_argument('--env', action='store', default=None, choices=a.get_active_envs(),
                            help="The environment the machine should provision to", required=True)

        parser.add_argument('--num', action='store', type=int, default=1,
                            help="Number of instances to create")

        parser.add_argument('--requester', action='store', default="", help="The person requesting the machine")
        parser.add_argument('--customer', action='store', default="", help="Customer associated with the gateway")
        parser.add_argument('--xively_service', action='store', default="",
                            help="The docker image running on the machine / Xively_service")

        parser.add_argument('--base_ami', action='store', default="", choices=a.get_ami_stacks(),
                            help="Base Ami to use")
        parser.add_argument('--iam', action='store', help="Custom Iam role to use")
        parser.add_argument('--instance_type', action='store', help="Requested instance size")
        parser.add_argument('--dry_run', action='store_true', default=False, help="For testing purpose only")
        parser.add_argument('--shutdown', action='store', choices=["stop", "terminate"], default="stop",
                            help="Shutdown action")
        parser.add_argument('--monitoring', action='store_true', default=False, help="Monitoring enabled -- Do not use")
        parser.add_argument('--keypair', action='store', default=None, help="Which keypair to use")
        parser.add_argument('--availability', action='store', default=None, 
                            help="Public/private availability, default is the AMI provided availability, valid values: public, private")
        parser.add_argument('--fillup', action='store_true', default=False,
                            help="Instead of round robin, fillup algorithm should be used")
        args = parser.parse_args(sys.argv[3:])
        result = a.create_ec2_instance(**vars(args))
        for r in result:
            print "Instance Id: %s" % (r.get('InstanceId'),)

    def terminate_ec2(self):
        """
        This function is a wrapper for parsing arguments and printing for ec2 instance termination
        Tested
        :return:
        """
        a = awsrequests(session=self.account_information['session'])
        parser = argparse.ArgumentParser(description='creation of ec2 instance', usage='''kerrigan.py ec2 create_ec2 [<args>]]
        ''' + self.global_options, formatter_class=argparse.ArgumentDefaultsHelpFormatter, prog="kerrigan")
        parser.add_argument('--dry_run', action='store_true', default=False, help="For testing purpose only")
        parser.add_argument('--instanceids', action='store', required=True,
                            help="A comma seperated list of instance id-s")
        args = parser.parse_args(sys.argv[3:])
        instanceids = Misc.string_to_array(string=args.instanceids, split_char=",")
        result = a.terminate_instance(dryrun=args.dry_run, instanceids=instanceids)
        logger.output(data=result, csvvar=self.account_information['logger_arguments']['csv'],
                      tablevar=self.account_information['logger_arguments']['table'])
