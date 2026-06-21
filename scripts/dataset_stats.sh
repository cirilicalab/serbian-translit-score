#!/bin/bash

set -xe

script_dir=$(dirname "$0")
out_root=${script_dir}/../out
data_root=${script_dir}/../datasets
tools_dir=${script_dir}/../tools


function get_stats()
{
    name=$1
    
    in_list=${data_root}/${name}.txt
    out_file=${out_root}/dataset_stats_${name}.tsv

    python3 ${tools_dir}/dataset_stats.py --title > ${out_file}
    while read dataset_name; do
        python3 ${tools_dir}/dataset_stats.py --in-dir ${data_root}/${dataset_name}/cyr --name ${dataset_name} --unit M >> ${out_file}
    done < ${in_list}
}

# make sure that we have output dir
mkdir -p ${out_root}

get_stats dev
get_stats test
