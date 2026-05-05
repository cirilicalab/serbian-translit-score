#!/bin/bash

#
# Wrapper script for Jovan Turnjanin's cyrilizer with Mihajlo's improvements:
# https://raw.githubusercontent.com/procesaur/cirilizator/refs/heads/master/scripts/content.js
#
content_url="https://raw.githubusercontent.com/procesaur/cirilizator/refs/heads/master/scripts/content.js"

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
cyrilizer_wrapper_script=${script_dir}/cyrilizer.js

content_dir=/tmp/cyrilizer_ms
content_path=${content_dir}/content.js

# Download cyrilizer only if doesn't exist
if [ ! -f ${content_path} ]; then
    mkdir -p ${content_dir}
    wget -q -O ${content_path} ${content_url}
fi

node ${cyrilizer_wrapper_script} ${in_file} /tmp/cyrilizer/content.js > ${out_file}