#!/bin/bash

script_dir=$(dirname "$0")
root_dir=${script_dir}/../datasets

tools_dir=${script_dir}/../tools
c2l="python3 ${tools_dir}/c2l.py"

function dir_exists()
{
    dir=$1
    if [ ! -d "$dir" ]; then
        echo "Error: dataset doesn't have cyr subdir: ${dir}." >&2
        exit 1
    fi
}

function gen_latin_text()
{
    dataset_dir=$1
    alphabet=$2

    # cyrillic dir path
    cyr_dir=${dataset_dir}/cyr
    dir_exists ${cyr_dir}

    # latin dir path
    lat_dir=${dataset_dir}/${alphabet}

    # skip conversion if dir already exists
    if [ -d "$lat_dir" ]; then
        echo "Skipping: ${lat_dir} already exists."
        return
    fi

    # if latin dir doesn't exit we run c2l to generate it
    ${c2l} --alphabet ${alphabet} --in-dir ${cyr_dir} --out-dir ${lat_dir}
}

function process_dataset()
{
    dataset_dir=$1
    echo ${dataset_dir}

    gen_latin_text ${dataset_dir} lat
    gen_latin_text ${dataset_dir} ascii
    gen_latin_text ${dataset_dir} tanjug
}


# while read dataset_name; do
#     # add line end if it's missing. some transliterator's have issues with handling files without line end
#     dataset_dir=${root_dir}/${dataset_name}
#     process_dataset ${dataset_dir}
# done < ${root_dir}/all.txt


for dir in ${root_dir}/*/; do
    # Remove the trailing slash if you want the pure directory name
    dataset_name=$(basename ${dir})
    dataset_dir=${root_dir}/${dataset_name}
    process_dataset ${dataset_dir}
done

