#!/bin/bash

#
# SrbAI transliteration to Cyrillic
# https://github.com/Serbian-AI-Society/SrbAI
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

cat ${in_file} | python3 -c "import sys; from srbai.Alati.Transliterator import transliterate_lat2cir; print(transliterate_lat2cir(sys.stdin.read()))" > ${out_file}
