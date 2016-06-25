import sys
import argparse
import time

from misc.Logger import logger
from core.awsrequests import awsrequests
from misc import Misc
from core.base import base


class autoscaling(base):
    def __init__(self, global_options=None):
        self.global_options = global_options
        logger.info('autoscaling module entry endpoint')
        self.cli = Misc.cli_argument_parse()

    def start(self):
        logger.info('Invoked starting point for instance')
        parser = argparse.ArgumentParser(description='autoscaling tool for devops', usage='''kerrigan.py autoscaling <command> [<args>]

Second level options are:
  create
  compare
        ''' + self.global_options)
        parser.add_argument('command', help='Command to run')
        args = parser.parse_args(sys.argv[2:3])
        if not hasattr(self, args.command):
            logger.error('Unrecognized command')
            parser.print_help()
            exit(1)
        getattr(self, args.command)()

    def create(self):
        logger.info("Started create command")
        a = awsrequests()

        parser = argparse.ArgumentParser(description='autoscaling tool for devops', usage='''kerrigan.py autoscaling create [<args>]]
        ''' + self.global_options)
        parser.add_argument('--stack', action='store', choices=a.get_image_stacks(), default=None,
                            help="Stack to create", required=True)
        parser.add_argument('--min', action='store', type=int, default=1,
                            help="Minimum number of instances to create default:1", required=True)
        parser.add_argument('--max', action='store', type=int, default=1,
                            help="Maximum number of instances to create default:1", required=True)
        parser.add_argument('--env', action='store', default=None, choices=a.get_envs(),
                            help="The environment the auto scaling group should provision to", required=True)
        parser.add_argument('--requester', action='store', default="", help="The person requesting the machine")
        parser.add_argument('--customer', action='store', default="", help="The customer assigned to the resource")
        parser.add_argument('--elb', action='store', default="",
                            help="The elastic load balancers to use for the auto scaling group, separated by comma",
                            required=True)
        parser.add_argument('--health_check', action='store', default="ELB",
                            help="Service to use for health check; options: ELB or EC2", required=True)
        parser.add_argument('--health_check_grace_period', action='store', type=int, default=60,
                            help="Restrict health check for x number of seconds after launch", required=True)
        parser.add_argument('--xively_service', action='store', default="",
                            help="The docker image running on the machine")
        parser.add_argument('--availability', action='store', default="public",
                            help="Public or private subnets from the given environment; options: public or private",
                            required=True)
        args = parser.parse_args(sys.argv[3:])
        logger.info("Starting Launch process " + time.asctime(time.localtime(time.time())))

        instance = a.launch_auto_scaling_group(env=args.env, stack=args.stack, min_size=args.min, max_size=args.max,
                                               xively_service=args.xively_service, requester=args.requester,
                                               load_balancer_name=args.elb.split(','), health_check=args.health_check,
                                               health_check_grace_period=args.health_check_grace_period,
                                               availability=args.availability, customer=args.customer)

    def compare(self):
        logger.info("Comparint AutoScaling Groups")
        parser = argparse.ArgumentParser(description='ec2 tool for devops', usage='''kerrigan.py elb create [<args>]]
        ''' + self.global_options)
        parser.add_argument('--env', action='store', help="Which env to check")
        args = parser.parse_args(sys.argv[3:])
        c = awschecks()
        c.compare_autoscaling(env=args.env)


