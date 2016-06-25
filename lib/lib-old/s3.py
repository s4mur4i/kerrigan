import sys
import argparse

from core.awsrequests import awsrequests
from core.awschecks import awschecks
from misc.Logger import logger
from core.base import base
from misc import Misc


class s3(base):
    def __init__(self, global_options=None):
        self.global_options = global_options
        logger.info('S3 module entry endpoint')
        self.cli = Misc.cli_argument_parse()

    def start(self):
        logger.info('Invoked starting point for s3')
        parser = argparse.ArgumentParser(description='ec2 tool for devops', usage='''kerrigan.py s3 <command> [<args>]

Second level options are:
  list_buckets
  info_bucket
  compare
        ''' + self.global_options)
        parser.add_argument('command', help='Command to run')
        args = parser.parse_args(sys.argv[2:3])
        if not hasattr(self, args.command):
            logger.error('Unrecognized command')
            parser.print_help()
            exit(1)
        getattr(self, args.command)()

    def list_buckets(self):
        logger.info("Starting to gather information")
        a = awsrequests()
        parser = argparse.ArgumentParser(description='ec2 tool for devops', usage='''kerrigan.py s3 list_buckets [<args>]]
        ''' + self.global_options)
        parser.add_argument('--extended', action='store_true', default=False, help="Gather extended info about Buckets")
        args = parser.parse_args(sys.argv[3:])
        res = a.list_s3_buckets(extended=args.extended)
        logger.output(data=res, csvvar=self.cli['csv'], tablevar=self.cli['table'])

    def info_bucket(self):
        logger.info("Starting to gather information")
        a = awsrequests()
        parser = argparse.ArgumentParser(description='ec2 tool for devops', usage='''kerrigan.py s3 info_bucket [<args>]]
        ''' + self.global_options)
        parser.add_argument('--name', action='store', help="Name of bucket", required=True)
        parser.add_argument('--level', action='store',
                            choices=['acl', 'lifecycle', 'region', 'logging', 'policy', 'replication','tagging'],
                            help="What information to return")
        args = parser.parse_args(sys.argv[3:])
        res = a.info_s3_bucket(name=args.name, choice=args.level)
        logger.output(data=res, csvvar=self.cli['csv'], tablevar=self.cli['table'])

    def compare(self):
        logger.info("Starting to gather information")
        parser = argparse.ArgumentParser(description='ec2 tool for devops', usage='''kerrigan.py s3 compare [<args>]]
        ''' + self.global_options)
        parser.add_argument('--env', action='store', help="Name of env")
        args = parser.parse_args(sys.argv[3:])
        c = awschecks()
        c.compare_s3(env=args.env)
