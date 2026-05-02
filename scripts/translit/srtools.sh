#!/bin/bash

#
# This is wrapper script for Python srtools module
# https://andrejr.gitlab.io/srtools/
#

# set -xe

in_file=$1
out_file=$2

srts --lc $in_file > $out_file
