#!/bin/bash

set -xe

# Downloads datasets

script_dir=$(dirname "$0")
data_root=${script_dir}/../datasets

# tools_dir=${script_dir}/../tools
# python3 "${tools_dir}/hf_data_load.py" \
#   --repo procesaur/cirilica \
#   --datadir "${data_root}" \
#   --fnamefield id \
#   --textfield text_cyr

wget -O /tmp/news.zip https://archive.org/download/news_20260509_202605/news.zip 
unzip -o /tmp/news.zip -d ${data_root}
