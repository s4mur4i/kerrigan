import sys
import argparse
from misc.Logger import logger
from core.awsrequests import awsrequests
from misc import Misc
from core.base import base


class stack(base):
    def __init__(self, global_options, account_information):
        self.global_options = global_options
        self.account_information = account_information

    def start(self):
        logger.info('Invoked starting point for stack')
        parser = argparse.ArgumentParser(description='ec2 tool for devops', usage='''kerrigan.py stack <command> [<args>]

Second level options are:
    overflow
    deploy
        ''' + self.global_options)
        parser.add_argument('command', help='Command to run')
        args = parser.parse_args(sys.argv[2:3])
        if not hasattr(self, args.command):
            logger.error('Unrecognized command')
            parser.print_help()
            exit(1)
        getattr(self, args.command)()

    def overflow(self):
        logger.info("Started stack provision command")
        a = awsrequests(session=self.account_information['session'])
        parser = argparse.ArgumentParser(description='stack provision', usage='''kerrigan.py stack overflow [<args>]]
        ''' + self.global_options, formatter_class=argparse.ArgumentDefaultsHelpFormatter, prog="kerrigan")
        parser.add_argument('--json', action='store', required=True, help="Stack json to provision")
        parser.add_argument('--env', action='store', required=True, help="Which env to deploy to")
        parser.add_argument('--dryrun', action='store_true', default=False, help="No changes should be done")
        args = parser.parse_args(sys.argv[3:])
        a.deploy_stack_to_env(env=args.env, file=args.json, dryrun=args.dryrun)

    def deploy(self):
        logger.info("Started deployment command")
        a = awsrequests(session=self.account_information['session'])
        parser = argparse.ArgumentParser(description='deployment for stack in env', usage='''kerrigan.py stack deploy [<args>]]
        ''' + self.global_options, formatter_class=argparse.ArgumentDefaultsHelpFormatter, prog="kerrigan")
        parser.add_argument('--env', action='store', required=True, help="Which env to deploy to")
        parser.add_argument('--puppet_role', action='store', required=True, help="Puppet_role to deploy")
        parser.add_argument('--dry_run', action='store_true', default=False, help="No changes should be done")
        parser.add_argument('--xively_service', action='store', default=None, help="Xively_service to deploy")
        parser.add_argument('--num', action='store', default=1, help="Number of instances to spin up")
        parser.add_argument('--instance_type', action='store', help="Requested instance size")
        parser.add_argument('--base_ami', action='store', default="", choices=a.get_ami_stacks(),
                            help="Base Ami to use")
        parser.add_argument('--iam', action='store', help="Custom Iam role to use")
        parser.add_argument('--requester', action='store', default="", help="The person requesting the machine")
        parser.add_argument('--customer', action='store', default="", help="Customer associated with the gateway")
        args = parser.parse_args(sys.argv[3:])
        a.prepare_deployment(**vars(args))

    def snappy(self):
        logger.info("Started snappy command")
        a = awsrequests(session=self.account_information['session'])
        parser = argparse.ArgumentParser(description='deployment for snappy', usage='''kerrigan.py stack snappy [<args>]]
        ''' + self.global_options, formatter_class=argparse.ArgumentDefaultsHelpFormatter, prog="kerrigan")
        parser.add_argument('--num', action='store', default=1, help="Number of instances to spin up")
        parser.add_argument('--env', action='store', required=True, help="Which env to deploy to")
        parser.add_argument('--dryrun', action='store_true', default=False, help="No changes should be done")
        parser.add_argument('--accountid', action='store', required=True, help="The account id for snappy")
        parser.add_argument('--channelname', action='store', required=True, help="The channelname for snappy")
        parser.add_argument('--newrelic', action='store', required=True, help="The newrelic environment to use")
        parser.add_argument('--devicestring', action='store', required=True, help="The deviec string like deploy/nots")
        parser.add_argument('--branch', action='store', default="None", help="The branch to checkout from")
        args = parser.parse_args(sys.argv[3:])
        a.deploy_snappy(**vars(args))
