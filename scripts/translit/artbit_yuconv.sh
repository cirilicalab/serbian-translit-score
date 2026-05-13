#!/bin/bash

#
# YuConv jednostavna bilblioteka za kovertovanje srpskog ćiriličnog teksta u latinični i obratno.
# https://github.com/ArtBIT/yuconv
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


cat ${in_file} | yuconv-cli to-cyrillic - > ${out_file}
