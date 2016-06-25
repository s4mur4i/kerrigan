#!/usr/bin/env bats


@test "testing no argument pass and help is printed" {
    run ./bin/kerrigan.py
    [ "$status" -eq 2 ]
    [ "${lines[-1]}" = "kerrigan.py: error: too few arguments" ]
}

@test "test default account with ec2 report" {
    run ./bin/kerrigan.py ec2 report_ec2_instances --filters tag-value:test1234
    [ "$status" -eq 0 ]

}

@test "test prod account with ec2 report" {
    run ./bin/kerrigan.py ec2 report_ec2_instances --aws_account prod --filters tag-value:test1324
    [ "$status" -eq 0 ]
}

@test "test not existing account with ec2 report" {
    run ./bin/kerrigan.py ec2 report_ec2_instances --aws_account testtest1234
    [ "$status" -eq 1 ]
    [ "${lines[-1]}" = "botocore.exceptions.ProfileNotFound: The config profile (testtest1234) could not be found" ]
}
