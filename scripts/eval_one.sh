#!/bin/bash

# set -xe

#
# Runs evaluation of single cyrillic 2 latin transliteration tool on collection of datasets
#

transliterator=$1
dataset_list=$2

script_dir=$(dirname "$0")

data_root=${script_dir}/../datasets
out_root=${script_dir}/../out
tools_dir=${script_dir}/../tools
# results_file=${out_root}/results.tsv
# results_file_github=${out_root}/results.md
score="python3 ${tools_dir}/score.py"

# dataset_list=all.txt
# dataset_list=tiny.txt


run_eval=true

#
# Evaluate 1 transliterator on 1 dataset in 1 latin alphabet
#
function eval()
{
    trans_tool=$1
    dataset=$2
    alphabet=$3

    # get dataset root dir
    dataset_dir=${data_root}/${dataset}

    # get dataset latin transcription dir
    in_dir=${dataset_dir}/${alphabet}

    # get output dir name
    dataset_out=${out_root}/${trans_tool}/${dataset}
    out_dir=${dataset_out}/${alphabet}

    # get expected dir with expected cyrillic output
    exp_dir=${dataset_dir}/cyr

    # get list of all input files
    files=$(find ${in_dir} -mindepth 1 -type f -printf "%P\n")

    if [ "$run_eval" == true ] ; then
        # ensure output dir exists and is empty
        # rm -rf ${out_dir}
        mkdir -p ${out_dir}

        # transliterate all files
        for file in ${files}; do
            ${script_dir}/translit/${trans_tool}.sh ${in_dir}/${file} ${out_dir}/${file}
        done

        # failures on few random files if parallel is used
        # parallel -j +0 --will-cite "${script_dir}/translit/${trans_tool}.sh ${in_dir}/{} ${out_dir}/{}" ::: ${files}
    fi

    ${score} dir --act ${out_dir} --exp ${exp_dir} --word-alignment ${dataset_out}/word_alignment_${alphabet}.tsv >> ${dataset_out}/results_${alphabet}.txt

    # # prepare line for file with all results
    # result_line=$(cat ${dataset_out}/results_${alphabet}.txt | tail -1)

    # printf "${trans_tool}\t${dataset}\t${alphabet}\t${result_line}\n" >> ${results_file}
}


function eval_with_time()
{
    trans_tool=$1
    dataset=$2
    alphabet=$3
    export TIMEFORMAT="    eval ${dataset} (${alphabet}):  "'%R seconds'
    time eval ${trans_tool} ${dataset} ${alphabet}
}

function eval_all_alphabets()
{
    trans_tool=$1
    dataset=$2

    eval_with_time ${trans_tool} ${dataset} "lat"
    eval_with_time ${trans_tool} ${dataset} "ascii"
    # eval_with_time ${trans_tool} ${dataset} "tanjug"
}

function eval_all_datasets_and_alphabets()
{
    trans_tool=$1
    echo ""
    echo "$trans_tool"
    while read dataset_name; do
        eval_all_alphabets ${trans_tool} ${dataset_name}
    done < ${data_root}/${dataset_list}
}

# make sure that we have output dir
mkdir -p ${out_root}

# evaluate the transliterator
eval_all_datasets_and_alphabets $transliterator > ${out_root}/stdout_${transliterator}.txt 2> stderr_${transliterator}.txt
