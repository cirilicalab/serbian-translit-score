#!/bin/bash

script_dir=$(dirname "$0")
data_root=${script_dir}/../datasets
out_root=${script_dir}/../out
tools_dir=${script_dir}/../tools


function alphabet_results_to_tsv()
{
    alphabet=$1

    result_paths=$(find ${out_root} -type f | grep results_${alphabet}\.txt$)
    for result_path in ${result_paths}; do
        tool=$(echo ${result_path} | cut -d'/' -f5)
        dataset=$(echo ${result_path} | cut -d'/' -f6)
        results=$(tail -1 ${result_path})
        printf "${tool}\t${dataset}\t${alphabet}\t${results}\n"
    done
}

function compute_error_stats()
{
    word_alignment_paths=$(find ${out_root} -type f | grep "word_alignment_" | grep "\.tsv$" )
    for word_alignment_path in $word_alignment_paths; do
        echo "Summarize errors: ${word_alignment_path}"
        path_no_ext=${word_alignment_path%.*}
        stats_path=${path_no_ext}.stats
        printf "EXPECTED\tACTUAL\n" > ${stats_path}
        cat ${word_alignment_path} | cut -f5,6 | sort | uniq -c | sort -rn >> ${stats_path}
    done
}


function failed_files()
{
    rm -f ${out_root}/failed.txt
    word_alignment_paths=$(find ${out_root} -type f | grep "word_alignment_" | grep "\.tsv$" )
    for word_alignment_path in $word_alignment_paths; do
        echo "Collect failed files: ${word_alignment_path}"
        path_no_ext=${word_alignment_path%.*}
        failed_path=${path_no_ext}.failed
        echo "${word_alignment_path}" >> ${out_root}/failed.txt
        cat ${word_alignment_path} | cut -f1,2 | grep -P '\tD$' | cut -f1 | uniq -c >> ${out_root}/failed.txt
        printf "\n\n" >> ${out_root}/failed.txt
    done
}

printf "tool\tdataset\talphabet\twer\tcer\t#words\twins\twsub\twdel\t#chars\tcins\tcsub\tcdel\n" > ${out_root}/results.tsv
alphabet_results_to_tsv "lat" >> ${out_root}/results.tsv
alphabet_results_to_tsv "ascii" >> ${out_root}/results.tsv
python3 ${tools_dir}/results_xlsx.py --results ${out_root}/results.tsv --output-xlsx ${out_root}/results.xlsx

compute_error_stats
failed_files

find ${out_root} -type f | grep word_alignment | grep \.stats$ | zip error_counts.zip -@
find ${out_root} -type f | grep word_alignment | grep \.tsv$ | zip word_alignment.zip -@
