#!/usr/bin/env python
import os
import sys
import argparse


class Initiator(object):
    def __init__(self):
        from core.base import base
        base = base()
        self.global_options = '''
Global Options:
  -v, --verbose                 increment client verbosity level (max 5)
  -q, --quiet                   decrease client verbosity level (max 0)
  # Default verbosity level 3
  --aws_account                     which account should be used
  --aws_region                      which region should we use for running the endpoint
  --aws_secret_key                  the secret key for aws
  --aws_access_key                  the access key for aws

Global Output options:
  --table                       Output should use Prettytable to printing
  --csv                         Output should use csv format for printing (delimiter ';')

    '''
        parser = argparse.ArgumentParser(description='Ec2 tool for devops', usage='''ec2.py <command> [<args>]

First level options are following:
  ec2                         ec2 instance related subcommands
  elb                         elb related subcommands
  route53                     route53 related subcommands
  sg                          securitygroup related subcommands
  ami                         ami related subcommands
  iam                         iam related subcommands
  vpc                         vpc related subcommands
  rds                         rds related subcommands
  autoscale                   autoscale related subcommands
  s3                          s3 related subcommands
  cloudformation              cloudformation related subcommands
  stack                       stack related subcommands
  kinesis                     kinesis related subcommands
  apigateway                  apigateway related subcommands
    ''' + self.global_options)
        parser.add_argument('command', help='Endpoint to use')
        args = parser.parse_args(sys.argv[1:2])
        self.account = base.get_account_information()
        if not hasattr(self, args.command):
            logger.error('Unrecognized command')
            parser.print_help()
            exit(1)
        getattr(self, args.command)()

    def ec2(self):
        logger.info('First endpoint for ec2')
        from command.ec2 import ec2

        a = ec2(global_options=self.global_options, account_information=self.account)
        a.start()

    def elb(self):
        logger.info('First endpoint for elb')
        from command.elb import elb

        a = elb(global_options=self.global_options, account_information=self.account)
        a.start()

    def route53(self):
        logger.info('First endpoint for route53')
        from command.route53 import route53

        a = route53(global_options=self.global_options, account_information=self.account)
        a.start()

    def sg(self):
        logger.info('First endpoint for sg')
        from command.sg import sg

        a = sg(global_options=self.global_options, account_information=self.account)
        a.start()

    def ami(self):
        logger.info('First endpoint for ami')
        from command.ami import ami

        a = ami(global_options=self.global_options, account_information=self.account)
        a.start()

    def iam(self):
        logger.info('First endpoint for iam')
        from command.iam import iam

        a = iam(global_options=self.global_options, account_information=self.account)
        a.start()

    def vpc(self):
        logger.info('First endpoint for vpc')
        from command.vpc import vpc

        a = vpc(global_options=self.global_options, account_information=self.account)
        a.start()

    def rds(self):
        logger.info('First endpoint for rds')
        from command.rds import rds

        a = rds(global_options=self.global_options, account_information=self.account)
        a.start()

    def autoscale(self):
        logger.info('First endpoint for autoscale')
        from command.autoscale import autoscale

        a = autoscale(global_options=self.global_options, account_information=self.account)
        a.start()

    def s3(self):
        logger.info('First endpoint for s3')
        from command.s3 import s3

        a = s3(global_options=self.global_options, account_information=self.account)
        a.start()

    def cloudformation(self):
        logger.info('First endpoint for cloudformation')
        from command.cloudformation import cloudformation

        a = cloudformation(global_options=self.global_options, account_information=self.account)
        a.start()

    def apigateway(self):
        logger.info('First endpoint for apigateway')
        from command.apigateway import apigateway

        a = apigateway(global_options=self.global_options, account_information=self.account)
        a.start()


    def stack(self):
        logger.info('First endpoint for stack')
        from command.stack import stack

        a = stack(global_options=self.global_options, account_information=self.account)
        a.start()

    def kinesis(self):
        logger.info('First endpoint for kinesis')
        from command.kinesis import kinesis

        a = kinesis(global_options=self.global_options, account_information=self.account)
        a.start()


if __name__ == '__main__':
    root_dir = os.path.dirname(os.path.dirname(os.path.realpath(sys.argv[0])))
    if os.path.samefile(sys.argv[0], root_dir + '/bin/kerrigan.py'):
        os.environ['KERRIGAN_ROOT'] = root_dir
    else:
        print(
            "The script started as a symlink doesn't point to it's own script (to '{0}/bin/kerrigan.py'))".format(
                root_dir))
        sys.exit(1)

    kerrigan_lib_dir = "%s/lib" % (root_dir,)
    sys.path.append(kerrigan_lib_dir)
    kerrigan_lib_dir = "%s/lib-char" % (root_dir,)
    sys.path.append(kerrigan_lib_dir)
    from misc.Logger import logger

    logger.debug('Starting Initiator')
    Initiator()
