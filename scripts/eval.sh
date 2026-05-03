#!/bin/bash

# set -xe

#
# Runs end to end evaluation of serbian cyrillic 2 latin transliteration tools
#

script_dir=$(dirname "$0")

data_root=${script_dir}/../datasets
out_root=${script_dir}/../out
tools_dir=${script_dir}/../tools
results_file=${out_root}/results.tsv
results_file_github=${out_root}/results.md
score="python3 ${tools_dir}/score.py"


#
# Evaluate 1 transliterator on 1 dataset in 1 latin alphabet
#
function eval()
{
    trans_tool=$1
    dataset=$2
    alphabet=$3

    echo "Evaluate: ${trans_tool} on ${dataset} dataset with ${alphabet} alphabet."

    # get dataset root dir
    dataset_dir=${data_root}/${dataset}

    # get dataset latin transcription dir
    in_dir=${dataset_dir}/${alphabet}

    # get output dir name
    out_dir=${out_root}/${trans_tool}/${dataset}/${alphabet}

    # get expected dir with expected cyrillic output
    exp_dir=${dataset_dir}/cyr

    # get list of all input files
    files=$(find ${in_dir} -mindepth 1 -type f -printf "%P\n")

    # ensure output dir exists and is empty
    rm -rf ${out_dir}
    mkdir -p ${out_dir}

    # transliterate all files
    for file in ${files}; do
        ${script_dir}/translit/${trans_tool}.sh ${in_dir}/${file} ${out_dir}/${file}
    done

    ${score} dir --act ${out_dir} --exp ${exp_dir} >> ${out_dir}/results_${alphabet}.txt

    # prepare line for file with all results
    result_line=$(cat ${out_dir}/results_${alphabet}.txt | tail -1)

    printf "${trans_tool}\t${dataset}\t${alphabet}\t${result_line}\n" >> ${results_file}
}

function eval_all_alphabets()
{
    trans_tool=$1
    dataset=$2

    eval ${trans_tool} ${dataset} "lat"
    eval ${trans_tool} ${dataset} "eng"
    eval ${trans_tool} ${dataset} "eng2"
}

function eval_all_datasets_and_alphabets()
{
    trans_tool=$1

    eval_all_alphabets ${trans_tool} "tiny"
}

# make sure that we have output dir
mkdir -p ${out_root}

# add row with column names to results summary TSV table
col_names=$(${score} title)
printf "tool\tdataset\talphabet\t${col_names}\n" > ${results_file}

# evaluate all
eval_all_datasets_and_alphabets srtools
eval_all_datasets_and_alphabets cyrtranslit
eval_all_datasets_and_alphabets cyrilizer

# format output table as github markdown
cat ${results_file} | tabulate --header -f github > ${results_file_github}
