#!/bin/bash

#
# A simple transliteration library for Serbian language, written in Javascript and using ES Modules.
# https://github.com/pioniredu/preslovljivac-js
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

node ${script_dir}/pionir_preslovljavac.mjs ${in_file} > ${out_file}
