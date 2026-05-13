#!/bin/bash

#
# Serbian script converter Utility functions for converting cyrilic script to latin and vice versa
# https://github.com/DedaDev/serbian-script-converter
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

node ${script_dir}/dedadev_srb_script_conv.js ${in_file} > ${out_file}
