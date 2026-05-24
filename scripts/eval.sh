#!/bin/bash

set -xe

#
# Runs end to end evaluation of serbian cyrillic 2 latin transliteration tools
#

script_dir=$(dirname "$0")
out_root=${script_dir}/../out

dataset_list=all.txt
# dataset_list=tiny.txt

# make sure that we have output dir
mkdir -p ${out_root}


# add row with column names to results summary TSV table
# col_names=$(${score} title)
# printf "tool\tdataset\talphabet\t${col_names}\n" > ${results_file}

# evaluate all
# ${script_dir}/eval_one.sh turanjanin_cyrilizer ${dataset_list}

sem -j 16 ${script_dir}/eval_one.sh turanjanin_cyrilizer ${dataset_list}
sem -j 16 ${script_dir}/eval_one.sh andrejr_srtools ${dataset_list}
sem -j 16 ${script_dir}/eval_one.sh serbian_ai_society_srbai ${dataset_list}
sem -j 16 ${script_dir}/eval_one.sh artbit_yuconv ${dataset_list}
sem -j 16 ${script_dir}/eval_one.sh exvorn_srb_translit ${dataset_list}
sem -j 16 ${script_dir}/eval_one.sh ivebe_cyrlatconv ${dataset_list}
sem -j 16 ${script_dir}/eval_one.sh pionir_preslovljavac ${dataset_list}
sem -j 16 ${script_dir}/eval_one.sh raleksandar_pravopis ${dataset_list}
sem -j 16 ${script_dir}/eval_one.sh turanjanin_sr_trans ${dataset_list}
sem -j 16 ${script_dir}/eval_one.sh filiparag_translitrs ${dataset_list}
sem -j 16 ${script_dir}/eval_one.sh turanjanin_sr_lang_tools ${dataset_list}
sem -j 16 ${script_dir}/eval_one.sh turanjanin_sr_lang_tools_ascii ${dataset_list}
sem -j 16 ${script_dir}/eval_one.sh eevan78_translit ${dataset_list}

# wait for jobs to finish
sem --wait

# format output table as github markdown
# cat ${results_file} | tabulate --header -f github > ${results_file_github}
