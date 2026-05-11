#!/bin/bash

#
# This is wrapper script for Go translit tool
# https://github.com/eevan78/translit
#

# set -xe

# Check exactly two arguments
if [ $# -ne 2 ]; then
    echo "Error: Exactly two arguments required"
    echo "Usage: $0 <input_file> <output_file>"
    echo ""
    echo "Example:"
    echo "  $0 input.txt output.txt"
    exit 1
fi

in_file=$1
out_file=$2

# this is docker install path
/tmp/eevan78/translit/translit -l2c -text < ${in_file} > ${out_file}
