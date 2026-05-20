#!/bin/bash

script_dir=$(dirname "$0")
data_root=${script_dir}/../datasets
out_root=${script_dir}/../out
tools_dir=${script_dir}/../tools


function summarize_one()
{
    dataset=$1
    alphabet=$2

    summary_tsv=${out_root}/summary_${dataset}_${alphabet}.tsv
    head -1 ${out_root}/results.tsv | cut -f1,4,5 > ${summary_tsv}
    cat ${out_root}/results.tsv | grep -P "\t${alphabet}\t" | grep -P "\t$dataset\t"| cut -f1,4,5 >> ${summary_tsv}
}

function summarize_all_alphabets()
{
    dataset=$1

    summarize_one ${trans_tool} ${dataset} "lat"
    summarize_one ${trans_tool} ${dataset} "ascii"
}

function summarize_all_datasets()
{
    for dataset_dir in ${data_root}/*/; do
        dataset_name=$(basename ${dataset_dir})
        summarize_all_alphabets ${dataset_name}
    done
}


function summarize_datasets_info()
{
    for dataset_dir in ${data_root}/*/; do
        dataset_name=$(basename ${dataset_dir})
        cat ${out_root}/results.tsv | grep -P "\t${dataset_name}\t" | cut -f2,6,10 | sort | uniq >> ${out_root}/datasets.tsv
    done
}

# summarize_all_datasets
# summarize_datasets_info


python3 ${tools_dir}/results_xlsx.py -r ${out_root}/results.tsv -o ${out_root}/results.xlsx
