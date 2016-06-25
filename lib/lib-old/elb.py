import argparse
import sys

from core.awsrequests import awsrequests
from core.awschecks import awschecks
from misc.Logger import logger
from core.base import base
from misc import Misc


class elb(base):
    def __init__(self, global_options=None):
        self.global_options = global_options
        logger.info('Elb module entry endpoint')
        self.cli = Misc.cli_argument_parse()

    def start(self):
        logger.info('Invoked starting point for elb')
        parser = argparse.ArgumentParser(description='ec2 tool for devops', usage='''kerrigan.py elb <command> [<args>]

Second level options are:
    info_all
    check
    compare
    sync_instances
        ''' + self.global_options)
        parser.add_argument('command', help='Command to run')
        args = parser.parse_args(sys.argv[2:3])
        if not hasattr(self, args.command):
            logger.error('Unrecognized command')
            parser.print_help()
            exit(1)
        getattr(self, args.command)()

    def info_all(self):
        # FIXME implement possbility to scope to env
        logger.info("Gathering all elbs")
        parser = argparse.ArgumentParser(description='ec2 tool for devops', usage='''kerrigan.py elb info_all [<args>]]
        ''' + self.global_options)
        args = parser.parse_args(sys.argv[3:])
        e = awsrequests()
        res = e.elb_info_all()
        for r in res:
            if self.cli['csv']:
                r['Availability Zones'] = Misc.join_list_to_string(list=r['Availability Zones'])
                r['Securitygroups'] = Misc.join_list_to_string(list=r['Securitygroups'])
                r['InstanceIds'] = Misc.join_list_to_string(list=r['InstanceIds'])
                r['From-To-Protocol'] = Misc.join_list_to_string(list=r['From-To-Protocol'])
            elif self.cli['table']:
                r['Availability Zones'] = Misc.list_to_multiline_string(r['Availability Zones'])
                r['InstanceIds'] = Misc.list_to_multiline_string(r['InstanceIds'])
                r['Securitygroups'] = Misc.list_to_multiline_string(r['Securitygroups'])
                r['From-To-Protocol'] = Misc.list_to_multiline_string(r['From-To-Protocol'])
        logger.output(data=res, csvvar=self.cli['csv'], tablevar=self.cli['table'])

    def check(self):
        # FIXME broken, need to fix
        logger.info("Checking ELB standards")
        parser = argparse.ArgumentParser(description='ec2 tool for devops', usage='''kerrigan.py elb check [<args>]]
        ''' + self.global_options)

    def compare(self):
        logger.info("Creating ELB")
        parser = argparse.ArgumentParser(description='ec2 tool for devops', usage='''kerrigan.py elb create [<args>]]
        ''' + self.global_options)
        parser.add_argument('--env', action='store', help="Which env to check")
        args = parser.parse_args(sys.argv[3:])
        c = awschecks()
        c.compare_elb(env=args.env)

    def sync_instances(self):
        logger.info("Syncing Instances to ELB")
        parser = argparse.ArgumentParser(description='ec2 tool for devops', usage='''kerrigan.py elb sync_instances [<args>]]
        ''' + self.global_options)
        parser.add_argument('--env', action='store', help="Which env to check")
        parser.add_argument('--dryrun', action='store_true',default=False, help="No changes should be done")
        args = parser.parse_args(sys.argv[3:])
        c = awschecks()
        c.sync_instances_to_elbs(env=args.env,dryrun=args.dryrun)

