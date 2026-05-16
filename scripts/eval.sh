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

dataset_list=all.txt
# dataset_list=tiny.txt

no_eval=true

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

    if [ "$no_eval" == false ] ; then
        # ensure output dir exists and is empty
        rm -rf ${out_dir}
        mkdir -p ${out_dir}

        # transliterate all files
        # for file in ${files}; do
        #     ${script_dir}/translit/${trans_tool}.sh ${in_dir}/${file} ${out_dir}/${file}
        # done
        parallel -j +100 --will-cite "${script_dir}/translit/${trans_tool}.sh ${in_dir}/{} ${out_dir}/{}" ::: ${files}
    fi

    ${score} dir --act ${out_dir} --exp ${exp_dir} --word-alignment ${dataset_out}/word_alignment_${alphabet}.tsv >> ${dataset_out}/results_${alphabet}.txt

    # prepare line for file with all results
    result_line=$(cat ${dataset_out}/results_${alphabet}.txt | tail -1)

    printf "${trans_tool}\t${dataset}\t${alphabet}\t${result_line}\n" >> ${results_file}
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

# add row with column names to results summary TSV table
col_names=$(${score} title)
printf "tool\tdataset\talphabet\t${col_names}\n" > ${results_file}

# evaluate all
eval_all_datasets_and_alphabets andrejr_srtools
eval_all_datasets_and_alphabets serbian_ai_society_srbai
eval_all_datasets_and_alphabets turanjanin_cyrilizer
eval_all_datasets_and_alphabets artbit_yuconv
eval_all_datasets_and_alphabets exvorn_srb_translit
eval_all_datasets_and_alphabets ivebe_cyrlatconv
eval_all_datasets_and_alphabets pionir_preslovljavac
eval_all_datasets_and_alphabets raleksandar_pravopis
eval_all_datasets_and_alphabets turanjanin_sr_trans
eval_all_datasets_and_alphabets filiparag_translitrs
eval_all_datasets_and_alphabets turanjanin_sr_lang_tools
eval_all_datasets_and_alphabets turanjanin_sr_lang_tools_ascii
eval_all_datasets_and_alphabets eevan78_translit

# format output table as github markdown
cat ${results_file} | tabulate --header -f github > ${results_file_github}
