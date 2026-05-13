#!/bin/bash

#
# pravopis is a Node.js module which implements a few string manipulation functions which are useful when working with text in Serbian language as they handle Serbian language orthography rules correctly.
# https://github.com/raleksandar/pravopis
#

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

script_dir=$(dirname "$0")

node ${script_dir}/raleksandar_pravopis.js ${in_file} > ${out_file}
