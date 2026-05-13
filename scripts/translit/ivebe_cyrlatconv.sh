#!/bin/bash

#
# CyrLatConverter is a javascript library for transliteration of complete web sites (or just part of it) from Latin to Cyrillic and vice versa. Built with Serbian language as a reference.
# https://github.com/ivebe/CyrLatConverter
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

node ${script_dir}/ivebe_cyrlatconv.cjs ${in_file} > ${out_file}

