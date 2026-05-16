#!/bin/bash

set -xe

# Downloads datasets

script_dir=$(dirname "$0")
data_root=${script_dir}/../datasets
tools_dir=${script_dir}/../tools

mkdir -p ${data_root}

# news dev set
wget -O /tmp/news_dev.zip https://archive.org/download/news_test_202605/news_dev.zip
unzip -o /tmp/news_dev.zip -d ${data_root}

# news test set
wget -O /tmp/news_dev.zip https://archive.org/download/news_test_202605/news_test.zip
unzip -o /tmp/news_dev.zip -d ${data_root}

# wiki
wget -qO - https://huggingface.co/datasets/procesaur/cirilica/resolve/main/sr_wiki_dev.jsonl | python3 tools/hf_unpack.py --output ${data_root}/wiki_dev/cyr
wget -qO - https://huggingface.co/datasets/procesaur/cirilica/resolve/main/sr_wiki_test.jsonl | python3 tools/hf_unpack.py --output ${data_root}/wiki_test/cyr

# znanje
wget -qO - https://huggingface.co/datasets/procesaur/cirilica/resolve/main/sr_znanje_dev.jsonl | python3 tools/hf_unpack.py --output ${data_root}/znanje_dev/cyr
wget -qO - https://huggingface.co/datasets/procesaur/cirilica/resolve/main/sr_znanje_test.jsonl | python3 tools/hf_unpack.py --output ${data_root}/znanje_test/cyr

# reddit
wget -qO - https://huggingface.co/datasets/procesaur/cirilica/resolve/main/sr_reddit_dev.jsonl | python3 tools/hf_unpack.py --output ${data_root}/reddit_dev/cyr
wget -qO - https://huggingface.co/datasets/procesaur/cirilica/resolve/main/sr_reddit_test.jsonl | python3 tools/hf_unpack.py --output ${data_root}/reddit_test/cyr
