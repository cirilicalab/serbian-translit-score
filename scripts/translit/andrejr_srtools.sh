#!/bin/bash

#
# This is wrapper script for Python srtools module
# https://andrejr.gitlab.io/srtools/
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

srts --lc $in_file > $out_file
