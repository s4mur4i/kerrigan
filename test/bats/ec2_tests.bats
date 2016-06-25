#!/usr/bin/env bats

@test "ec2 endpoint exists" {
    run ./bin/kerrigan.py ec2
    [ "$status" -eq 2 ]
    [ "${lines[0]}" = "usage: kerrigan.py ec2 <command> [<args>]" ]
}

@test "run ec2 report with no arguments on all accounts" {
    accounts="prod dev"
    for account in ${accounts}
        do
        echo $account
        run ./bin/kerrigan.py ec2 report_ec2_instances --aws_account $account
        [ "$status" -eq 0 ]
        done
}

@test "run ec2 report with columns on all accounts" {
    accounts="prod dev"
    for account in ${accounts}
        do
        echo $account
        run ./bin/kerrigan.py ec2 report_ec2_instances --columns tag:name --aws_account $account
        [ "$status" -eq 0 ]
        done
}

@test "run ec2 report with columns and invalid column on all accounts" {
    accounts="prod dev"
    for account in ${accounts}
        do
        echo $account
        run ./bin/kerrigan.py ec2 report_ec2_instances --columns tag:name,tag:notexist --aws_account $account
        [ "$status" -eq 0 ]
        done
}

@test "run ec2 report with filters on all accounts" {
    accounts="prod dev"
    for account in ${accounts}
        do
        echo $account
        run ./bin/kerrigan.py ec2 report_ec2_instances --filters tag-value:nat --aws_account $account
        [ "$status" -eq 0 ]
        done
}

@test "run ec2 report with filters and invalid filter on all accounts" {
    accounts="prod dev"
    for account in ${accounts}
        do
        echo $account
        run ./bin/kerrigan.py ec2 report_ec2_instances --filters state:running,tag-notexist:asdfg1234 --aws_account $account
        echo $output
        [ "$status" -eq 1 ]
        [ "${lines[-1]}" = "botocore.exceptions.ClientError: An error occurred (InvalidParameterValue) when calling the DescribeInstances operation: The filter 'state' is invalid" ]
        done
}

@test "run ec2 report with columns and filters on all accounts" {
    accounts="prod dev"
    for account in ${accounts}
        do
        echo $account
        run ./bin/kerrigan.py ec2 report_ec2_instances --columns tag:name --filters tag-value:nat --aws_account $account
        [ "$status" -eq 0 ]
        done
}

@test "run ec2 report with columns and filters and invalid filter and column on all accounts" {
    accounts="prod dev"
    for account in ${accounts}
        do
        echo $account
        run ./bin/kerrigan.py ec2 report_ec2_instances --columns tag:name,notexist:ewrt123 --filters invalid:invalid --aws_account $account -q -q
        echo $output
        [ "$status" -eq 1 ]
        [ "${lines[-1]}" = "botocore.exceptions.ClientError: An error occurred (InvalidParameterValue) when calling the DescribeInstances operation: The filter 'invalid' is invalid" ]
        done
}

@test "run ec2 create instance in dev account, and then terminate" {
    run ./bin/kerrigan.py ec2 create_ec2 --puppet_role docker --env dev --requester bats_testing --xively_service bats_testing --instance_type m3.medium --aws_account dev
    export created_instance=$(echo $output |  cut -d: -f2)
    [ "$status" -eq 0 ]
    run ./bin/kerrigan.py ec2 terminate_ec2 --instanceids $created_instance --aws_account dev
    [ "$status" -eq 0 ]
    run ./bin/kerrigan.py ec2 terminate_ec2 --instanceids $created_instance --csv --aws_account dev
    [ "$status" -eq 0 ]
}

@test "run ec2 create instance in dev account with two instance creations, and then terminate" {
    run ./bin/kerrigan.py ec2 create_ec2 --puppet_role docker --env dev --requester bats_testing --xively_service bats_testing --instance_type m3.medium --aws_account dev --num 2
    echo $output
    export instance_ids=$(echo $output | sed -e "s,Instance Id: ,,g" | tr ' ' ',')
    echo $instance_ids
    [ "$status" -eq 0 ]
    run ./bin/kerrigan.py ec2 terminate_ec2 --instanceids $instance_ids --aws_account dev
    echo $output
    echo $status
    [ "$status" -eq 0 ]
    run ./bin/kerrigan.py ec2 terminate_ec2 --instanceids $instance_ids --csv --aws_account dev
    [ "$status" -eq 0 ]
}

@test "run cloudformation report with no arguments on all accounts" {
    accounts="prod dev"
    for account in ${accounts}
        do
        echo $account
        run ./bin/kerrigan.py cloudformation report_cloudformation --aws_account $account
        [ "$status" -eq 0 ]
        done
}

@test "run cloudformation report with columns on all accounts" {
    accounts="prod dev"
    for account in ${accounts}
        do
        echo $account
        run ./bin/kerrigan.py cloudformation report_cloudformation --columns name --aws_account $account
        [ "$status" -eq 0 ]
        done
}

@test "run cloudformation report with columns and invalid column on all accounts" {
    accounts="prod dev"
    for account in ${accounts}
        do
        echo $account
        run ./bin/kerrigan.py cloudformation report_cloudformation --columns name,notexist --aws_account $account
        [ "$status" -eq 0 ]
        done
}

@test "run elb report with no arguments on all accounts" {
    accounts="prod dev"
    for account in ${accounts}
        do
        echo $account
        run ./bin/kerrigan.py elb report_elb --aws_account $account
        [ "$status" -eq 0 ]
        done
}

@test "run elb report with columns on all accounts" {
    accounts="prod dev"
    for account in ${accounts}
        do
        echo $account
        run ./bin/kerrigan.py elb report_elb --columns name --aws_account $account
        [ "$status" -eq 0 ]
        done
}

@test "run elb report with columns and invalid column on all accounts" {
    accounts="prod dev"
    for account in ${accounts}
        do
        echo $account
        run ./bin/kerrigan.py elb report_elb --columns name,notexist --aws_account $account
        [ "$status" -eq 0 ]
        done
}

@test "run ami report with no arguments on all accounts" {
    accounts="prod dev"
    for account in ${accounts}
        do
        echo $account
        run ./bin/kerrigan.py ami report_ami --aws_account $account
        [ "$status" -eq 0 ]
        done
}

@test "run ami report with columns on all accounts" {
    accounts="prod dev"
    for account in ${accounts}
        do
        echo $account
        run ./bin/kerrigan.py ami report_ami --columns name --aws_account $account
        [ "$status" -eq 0 ]
        done
}

@test "run ami report with columns and invalid column on all accounts" {
    accounts="prod dev"
    for account in ${accounts}
        do
        echo $account
        run ./bin/kerrigan.py ami report_ami --columns name,notexist --aws_account $account
        [ "$status" -eq 0 ]
        done
}

@test "run kinesis report with no arguments on all accounts" {
    accounts="prod dev"
    for account in ${accounts}
        do
        echo $account
        run ./bin/kerrigan.py kinesis report_kinesis --aws_account $account
        [ "$status" -eq 0 ]
        done
}

@test "run kinesis report with columns on all accounts" {
    accounts="prod dev"
    for account in ${accounts}
        do
        echo $account
        run ./bin/kerrigan.py kinesis report_kinesis --columns name --aws_account $account
        [ "$status" -eq 0 ]
        done
}

@test "run kinesis report with columns and invalid column on all accounts" {
    accounts="prod dev"
    for account in ${accounts}
        do
        echo $account
        run ./bin/kerrigan.py kinesis report_kinesis --columns name,notexist --aws_account $account
        [ "$status" -eq 0 ]
        done
}

@test "run vpc report with no arguments on all accounts" {
    accounts="prod dev"
    for account in ${accounts}
        do
        echo $account
        run ./bin/kerrigan.py vpc report_vpc --aws_account $account
        [ "$status" -eq 0 ]
        done
}

@test "run vpc report with columns on all accounts" {
    accounts="prod dev"
    for account in ${accounts}
        do
        echo $account
        run ./bin/kerrigan.py vpc report_vpc --columns name --aws_account $account
        [ "$status" -eq 0 ]
        done
}

@test "run vpc report with columns and invalid column on all accounts" {
    accounts="prod dev"
    for account in ${accounts}
        do
        echo $account
        run ./bin/kerrigan.py vpc report_vpc --columns name,notexist --aws_account $account
        [ "$status" -eq 0 ]
        done
}

@test "run autoscale report with no arguments on all accounts" {
    accounts="prod dev"
    for account in ${accounts}
        do
        echo $account
        run ./bin/kerrigan.py autoscale report_autoscale --aws_account $account
        [ "$status" -eq 0 ]
        done
}

@test "run autoscale report with columns on all accounts" {
    accounts="prod dev"
    for account in ${accounts}
        do
        echo $account
        run ./bin/kerrigan.py autoscale report_autoscale --columns name --aws_account $account
        [ "$status" -eq 0 ]
        done
}

@test "run autoscale report with columns and invalid column on all accounts" {
    accounts="prod dev"
    for account in ${accounts}
        do
        echo $account
        run ./bin/kerrigan.py autoscale report_autoscale --columns name,notexist --aws_account $account
        [ "$status" -eq 0 ]
        done
}

@test "run rds report with no arguments on all accounts" {
    accounts="prod dev"
    for account in ${accounts}
        do
        echo $account
        run ./bin/kerrigan.py rds report_rds --aws_account $account
        [ "$status" -eq 0 ]
        done
}

@test "run rds report with columns on all accounts" {
    accounts="prod dev"
    for account in ${accounts}
        do
        echo $account
        run ./bin/kerrigan.py rds report_rds --columns name --aws_account $account
        [ "$status" -eq 0 ]
        done
}

@test "run rds report with columns and invalid column on all accounts" {
    accounts="prod dev"
    for account in ${accounts}
        do
        echo $account
        run ./bin/kerrigan.py rds report_rds --columns name,notexist --aws_account $account
        [ "$status" -eq 0 ]
        done
}

@test "run iam report with no arguments on all accounts" {
    accounts="prod dev"
    for account in ${accounts}
        do
        echo $account
        run ./bin/kerrigan.py iam report_iam --aws_account $account
        [ "$status" -eq 0 ]
        done
}

@test "run iam report with columns on all accounts" {
    accounts="prod dev"
    for account in ${accounts}
        do
        echo $account
        run ./bin/kerrigan.py iam report_iam --columns name --aws_account $account
        [ "$status" -eq 0 ]
        done
}

@test "run iam report with columns and invalid column on all accounts" {
    accounts="prod dev"
    for account in ${accounts}
        do
        echo $account
        run ./bin/kerrigan.py iam report_iam --columns name,notexist --aws_account $account
        [ "$status" -eq 0 ]
        done
}


@test "run sg report with no arguments on all accounts" {
    accounts="prod dev"
    for account in ${accounts}
        do
        echo $account
        run ./bin/kerrigan.py sg report_sg --aws_account $account
        [ "$status" -eq 0 ]
        done
}

@test "run sg report with columns on all accounts" {
    accounts="prod dev"
    for account in ${accounts}
        do
        echo $account
        run ./bin/kerrigan.py sg report_sg --columns name --aws_account $account
        [ "$status" -eq 0 ]
        done
}

@test "run sg report with columns and invalid column on all accounts" {
    accounts="prod dev"
    for account in ${accounts}
        do
        echo $account
        run ./bin/kerrigan.py sg report_sg --columns name,notexist --aws_account $account
        [ "$status" -eq 0 ]
        done
}

@test "run s3 report with no arguments on all accounts" {
    accounts="prod dev"
    for account in ${accounts}
        do
        echo $account
        run ./bin/kerrigan.py s3 report_s3 --aws_account $account
        [ "$status" -eq 0 ]
        done
}

@test "run s3 report with columns on all accounts" {
    accounts="prod dev"
    for account in ${accounts}
        do
        echo $account
        run ./bin/kerrigan.py s3 report_s3 --columns name --aws_account $account
        [ "$status" -eq 0 ]
        done
}

@test "run s3 report with columns and invalid column on all accounts" {
    accounts="prod dev"
    for account in ${accounts}
        do
        echo $account
        run ./bin/kerrigan.py s3 report_s3 --columns name,notexist --aws_account $account
        [ "$status" -eq 0 ]
        done
}

@test "run route53 report with no arguments on all accounts" {
    accounts="prod dev"
    for account in ${accounts}
        do
        echo $account
        run ./bin/kerrigan.py route53 report_route53 --aws_account $account
        [ "$status" -eq 0 ]
        done
}

@test "run route53 report with columns on all accounts" {
    accounts="prod dev"
    for account in ${accounts}
        do
        echo $account
        run ./bin/kerrigan.py route53 report_route53 --columns name --aws_account $account
        [ "$status" -eq 0 ]
        done
}

@test "run route53 report with columns and invalid column on all accounts" {
    accounts="prod dev"
    for account in ${accounts}
        do
        echo $account
        run ./bin/kerrigan.py route53 report_route53 --columns name,notexist --aws_account $account
        [ "$status" -eq 0 ]
        done
}

