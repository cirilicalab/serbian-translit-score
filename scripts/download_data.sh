#!/bin/bash

set -xe

# Downloads datasets

script_dir=$(dirname "$0")
data_root=${script_dir}/../datasets
tools_dir=${script_dir}/../tools

wget -qO - https://huggingface.co/datasets/procesaur/cirilica/resolve/main/sr_wiki_test.jsonl | python3 tools/hf_unpack.py --output ${data_root}/wiki/cyr
wget -qO - https://huggingface.co/datasets/procesaur/cirilica/resolve/main/sr_znanje_test.jsonl | python3 tools/hf_unpack.py --output ${data_root}/znanje/cyr

wget -O /tmp/news.zip https://archive.org/download/news_20260509_202605/news.zip 
unzip -o /tmp/news.zip -d ${data_root}
