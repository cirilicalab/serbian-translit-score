#!/bin/bash

#
# Restores diacritics and then runs conversion to Cyrillic. 
# https://github.com/turanjanin/serbian-language-tools
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

php ${script_dir}/turanjanin_sr_lang_tools_ascii.php ${in_file} > ${out_file}
