import sys
import argparse

from misc.Logger import logger
from core.awsrequests import awsrequests
from core.awschecks import awschecks
from misc import Misc
from core.base import base


class iam(base):
    def __init__(self, global_options=None):
        self.global_options = global_options
        logger.info('iam module entry endpoint')
        self.cli = Misc.cli_argument_parse()

    def start(self):
        logger.info('Invoked starting point for iam')
        parser = argparse.ArgumentParser(description='ec2 tool for devops', usage='''kerrigan.py iam <command> [<args>]

Second level options are:
    info_certs
    delete_server_cert
    upload_server_cert
    compare_certs
    update
    list_users
    compare_iam
    list_user_credentials
        ''' + self.global_options)
        parser.add_argument('command', help='Command to run')
        args = parser.parse_args(sys.argv[2:3])
        if not hasattr(self, args.command):
            logger.error('Unrecognized command')
            parser.print_help()
            exit(1)
        getattr(self, args.command)()

    def info_certs(self):
        logger.info("Going to list all certs")
        parser = argparse.ArgumentParser(description='ec2 tool for devops', usage='''kerrigan.py iam info_all [<args>]]
        ''' + self.global_options)
        args = parser.parse_args(sys.argv[3:])
        a = awsrequests()
        res = a.server_certificates_info_all()
        for r in res:
            if self.cli['csv']:
                r['ELB'] = Misc.join_list_to_string(list=r['ELB'])
            elif self.cli['table']:
                r['ELB'] = Misc.list_to_multiline_string(r['ELB'])
            else:
                logger.error('There is an unhandled printing. Need to investigate')
        logger.output(data=res, csvvar=self.cli['csv'], tablevar=self.cli['table'])

    def delete_server_cert(self):
        logger.info("Going to delete cert")
        parser = argparse.ArgumentParser(description='ec2 tool for devops', usage='''kerrigan.py iam delete_server_cert [<args>]]
        ''' + self.global_options)
        parser.add_argument('--cert_name', action='store', help="Name of certificate to delete")
        args = parser.parse_args(sys.argv[3:])
        a = awsrequests()
        a.server_certificate_delete(cert_name=args.cert_name)

    def upload_server_cert(self):
        logger.info("Going to upload a cert")
        parser = argparse.ArgumentParser(description='ec2 tool for devops', usage='''kerrigan.py iam upload_server_cert [<args>]]
        ''' + self.global_options)
        parser.add_argument('--cert_name', action='store', required=True,
                            help="Name of certificate to upload, should be CN of domain")
        parser.add_argument('--pub_key', action='store', help="File containing public key")
        parser.add_argument('--priv_key', action='store', help="File containing private key")
        parser.add_argument('--cert_chain', action='store', help="File containing certificate chain")
        args = parser.parse_args(sys.argv[3:])
        a = awsrequests()
        a.server_certificate_upload(cert_name=args.cert_name, pub_key=args.pub_key, priv_key=args.priv_key,
                                    cert_chain=args.cert_chain)

    def compare_certs(self):
        logger.info("Going to check env certs")
        parser = argparse.ArgumentParser(description='ec2 tool for devops', usage='''kerrigan.py iam compare_certs [<args>]]
        ''' + self.global_options)
        parser.add_argument('--env', action='store', help="Envs to check")
        args = parser.parse_args(sys.argv[3:])
        a = awschecks()
        a.compare_certs(env=args.env)

    def update(self):
        logger.info("Going to update env certs")
        parser = argparse.ArgumentParser(description='ec2 tool for devops', usage='''kerrigan.py iam update [<args>]]
        ''' + self.global_options)
        parser.add_argument('--domain', action='store', required=True,
                            help="Which domain cert to update: example: star.dev.xively.com")
        parser.add_argument('--intermediate', action='store_true', default=False,
                            help="Should intermediate certificate be uploaded")
        args = parser.parse_args(sys.argv[3:])
        a = awsrequests()
        a.server_certficate_update(domain=args.domain, intermediate=args.intermediate)

    def list_users(self):
        logger.info("Going to list users")
        parser = argparse.ArgumentParser(description='ec2 tool for devops', usage='''kerrigan.py iam list_users [<args>]]
        ''' + self.global_options)
        args = parser.parse_args(sys.argv[3:])
        a = awsrequests()
        res = a.list_iam_users()
        logger.output(data=res, csvvar=self.cli['csv'], tablevar=self.cli['table'])

    def list_groups(self):
        logger.info("Going to list groups")
        parser = argparse.ArgumentParser(description='ec2 tool for devops', usage='''kerrigan.py iam list_groups [<args>]]
        ''' + self.global_options)
        args = parser.parse_args(sys.argv[3:])
        a = awsrequests()
        res = a.list_iam_groups()
        logger.output(data=res, csvvar=self.cli['csv'], tablevar=self.cli['table'])

    def list_user_groups(self):
        logger.info("Going to list groups")
        parser = argparse.ArgumentParser(description='ec2 tool for devops', usage='''kerrigan.py iam list_user_groups [<args>]]
        ''' + self.global_options)
        parser.add_argument('--username', action='store', default=None,
                            help="Should intermediate certificate be uploaded")
        args = parser.parse_args(sys.argv[3:])
        a = awsrequests()
        res = a.list_user_groups(username=args.username)
        out = []
        for r in res:
            if self.cli['csv']:
                res[r] = Misc.join_list_to_string(list=res[r])
            elif self.cli['table']:
                res[r] = Misc.list_to_multiline_string(res[r])
            out.append({'Username': r, 'Groups': res[r]})
        logger.output(data=out, csvvar=self.cli['csv'], tablevar=self.cli['table'])

    def compare_iam(self):
        logger.info("Going to check env iam certificates")
        parser = argparse.ArgumentParser(description='ec2 tool for devops', usage='''kerrigan.py iam compare_iam [<args>]]
        ''' + self.global_options)
        parser.add_argument('--env', action='store', help="Envs to check")
        parser.add_argument('--dryrun', action='store_true', default=False, help="No changes should be done")
        args = parser.parse_args(sys.argv[3:])
        a = awschecks()
        a.compare_iam(env=args.env, dryrun=args.dryrun)

    def list_user_credentials(self):
        logger.info("Going to list user credentials")
        parser = argparse.ArgumentParser(description='ec2 tool for devops', usage='''kerrigan.py iam list_user_credentials [<args>]]
        ''' + self.global_options)
        args = parser.parse_args(sys.argv[3:])
        a = awsrequests()
        resp = a.list_user_credentials()
        logger.output(data=resp, csvvar=self.cli['csv'], tablevar=self.cli['table'])

    def create_user_credentials(self):
        logger.info("Going to create user credentials")
        parser = argparse.ArgumentParser(description='ec2 tool for devops', usage='''kerrigan.py iam create_user_credentials [<args>]]
        ''' + self.global_options)
        parser.add_argument('--username', action='store', help="Username to create credentials for", required=True)
        parser.add_argument('--dryrun', action='store_true', default=False, help="No changes should be done")
        args = parser.parse_args(sys.argv[3:])
        a = awsrequests()
        resp = a.create_user_credentials(username=args.username,dryrun=args.dryrun)
        logger.output(data=resp, csvvar=self.cli['csv'], tablevar=self.cli['table'])
