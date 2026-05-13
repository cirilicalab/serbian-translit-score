#!/bin/bash

#
# This library converts text between Serbian Latin and Cyrillic scripts.
# https://github.com/turanjanin/serbian-transliterator
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

php ${script_dir}/turanjanin_php_trans.php ${in_file} > ${out_file}
