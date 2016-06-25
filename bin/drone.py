#!/usr/bin/env python
import os
import sys


class Drone(object):
    def __init__(self):
        print "Starting account creation and buildup"
        self.step = 0
        from misc import Misc
        from core.base import base
        base = base()
        if Misc.confirm(prompt="Are you sure you want to create an account infrastructure?", resp=False):
            self.account = base.get_account_information()
            if 'profile_name' in self.account['cli_arguments']:
                print "Aws account has been provided"
            else:
                logger.error("Aws account not provided")
                exit(1)
            if 'region_name' in self.account['cli_arguments']:
                print "Aws region has been provided"
            else:
                logger.error("Aws region not provided")
                exit(1)
            if 'session' in self.account and self.account['session'] is not (None or ""):
                logger.info("Session object created succesfully")
            else:
                logger.error("Aws Session not created successfuly")
                exit(1)
            self.run_workflow()
        else:
            print "You are not prepared - Illidian"

    def increment_step(self):
        self.step += 1
        return self.step

    def run_workflow(self):
        from misc import Misc
        from core.awsrequests import awsrequests
        AWSreq = awsrequests(session=self.account['session'])
        region = self.account['cli_arguments']['region_name']
        print ""
        print "Step %s: Creating ec2 keys" % (self.increment_step(),)
        if not Misc.confirm("Has the keys for all envs been created with syntax default-env syntax?", resp=True):
            exit(1)

        print ""
        print "Step %s: Creating bucket for cloudformation" % (self.increment_step(),)
        if Misc.confirm("Should we create the s3 bucket for cloudformation?", resp=True):
            bucket_name = raw_input("What should the bucket name be (ex: xively-devops-templates-dr ): ")
            AWSreq.create_s3_bucket(name=bucket_name, location=region)
        else:
            print "Assuming bucket is already created"
            bucket_name = raw_input("What is the bucket name?")

        print ""
        print "Step %s: Upload xively_cloudformation repo to the s3 bucket" % (self.increment_step(),)
        while not Misc.confirm("Is the upload finished?", resp=False):
            print "Finish upload before continue"

        print ""
        print "Step %s: Run cloudformation template for infrastructure?" % (self.increment_step(),)
        if Misc.confirm("Should we run the cloudformation template", resp=False):
            # FIXME test if works
            cloudformation_template_name = raw_input(
                "What is the name of template to run (ex. VPC_dr_account.template ): ")
            url = "https://s3.amazonaws.com/" + bucket_name + "/" + cloudformation_template_name
            awsrequests.create_cloudformation_stack(stackname="vpc-infrastructure", templateurl=url)
        else:
            print "Assuming the stack has already been run."

        print ""
        print "Step %s: Run cloudformation template for users base" % (self.increment_step(),)
        if Misc.confirm("Should we run the cloudformation template?", resp=False):
            # FIXME test if works
            cloudformation_template_name = raw_input(
                "What is the name of template to run (ex. prod_account_iam.template ): ")
            url = "https://s3.amazonaws.com/" + bucket_name + "/" + cloudformation_template_name
            awsrequests.create_cloudformation_stack(stackname="devops-users", templateurl=url)
        else:
            print "Assuming the stack has already been run."
        devops_groupname = raw_input("Name of the generated devops group? ")

        print ""
        print "Step %s: Start amon.py to deploy to environement" % (self.increment_step(),)
        while not Misc.confirm("Is the packer generation started", resp=False):
            print "Start before we continue"

        print ""
        print "Step %s: Creating devops users" % (self.increment_step(),)
        devops_yaml = Misc.get_yaml(yamlfile="devops_users.yaml")
        for user in devops_yaml['users']:
            print "Checking user %s" % (user,)
            create_password = True
            if not AWSreq.iam_user_exists(username=user):
                print "Creating user %s" % (user,)
                AWSreq.create_iam_user(username=user, dryrun=False, path="/")
            else:
                login_profile = AWSreq.get_login_profile(username=user)
                if login_profile is not None:
                    create_password = False
            if create_password:
                user_password = Misc.generate_password(size=10)
                AWSreq.create_iam_login_profile(username=user, password=user_password)
                print "Username: %s generated password is: %s" % (user, user_password)
            user_groups = AWSreq.iam_user_groups(username=user)
            if devops_groupname not in user_groups[user]:
                print "Need to add to group"
                AWSreq.add_iam_user_to_group(username=user, groupname=devops_groupname)


if __name__ == '__main__':
    root_dir = os.path.dirname(os.path.dirname(os.path.realpath(sys.argv[0])))
    os.environ['KERRIGAN_ROOT'] = root_dir
    kerrigan_lib_dir = "%s/lib" % (root_dir,)
    sys.path.append(kerrigan_lib_dir)
    kerrigan_lib_dir = "%s/lib-char" % (root_dir,)
    sys.path.append(kerrigan_lib_dir)
    from misc.Logger import logger

    logger.debug('Starting Drone')
    Drone()
