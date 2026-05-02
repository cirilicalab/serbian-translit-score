#!/bin/bash

#
# This is wrapper script for Python cyrtranslit module
# https://andrejr.gitlab.io/srtools/
#

# set -xe

in_file=$1
out_file=$2

cyrtranslit -c -l sr -i $in_file -o $out_file
