#!/bin/bash
set -xe 

script_dir=$(dirname "$0")
analysis_root=${script_dir}/../analysis
datasets_root=${script_dir}/../datasets
out_root=${script_dir}/../out
tools_dir=${script_dir}/../tools


function prepare_one()
{
    trans_tool=$1
    dataset_list=$2
    alphabet=$3

    while read dataset_name; do
        # figure out inputs
        exp_dir=${datasets_root}/${dataset_name}/cyr
        act_dir=${out_root}/${trans_tool}/${dataset_name}/${alphabet}
        word_alignment=${out_root}/${trans_tool}/${dataset_name}/word_alignment_${alphabet}.tsv
        analysis_dir=${analysis_root}/${trans_tool}/${dataset_name}/${alphabet}
        mkdir -p ${analysis_dir}
        
        # log most common errors
        python3 ${tools_dir}/prepare_analysis.py \
            --word-alignment ${word_alignment} \
            --exp-dir ${exp_dir} \
            --act-dir ${act_dir} \
            --out-dir ${analysis_dir}

    done < ${datasets_root}/${dataset_list};
}

prepare_one turanjanin_cyrilizer dev.txt lat
prepare_one turanjanin_sr_lang_tools_ascii dev.txt ascii
