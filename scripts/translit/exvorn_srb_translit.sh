#!/bin/bash

#
# serbian-transliteration je lagana i brza JavaScript/TypeScript biblioteka za transkripciju srpskog teksta između ćirilice i latinice. Omogućava jednostavno konvertovanje rečenica ili reči, pogodna je za Node.js i browser okruženja, i ne zahteva dodatne biblioteke.
# https://github.com/exvorn/serbian-transliteration
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

node ${script_dir}/exvorn_srb_translit.cjs ${in_file} > ${out_file}

