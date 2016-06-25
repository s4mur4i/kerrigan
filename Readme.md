# Kerrigan Readme

## Install

### Centos

`yum install python-devel libxslt-devel`

## Tests

### Bats

How to run bats tests:

From application top level run following command:  `bats test/bats/* -t`

### Unit tests with nose

How to run unit tets:

From application top level run following command: ` PYTHONPATH=$(echo -n "$(pwd)/lib-char"; python -c 'import sys,
 string; print string.join(sys.path, ":")') nosetests -w test/unittest`
