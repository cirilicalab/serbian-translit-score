#!/bin/bash

# set -xe

#
# Downloads large datasets from HuggingFace to local disk 
#

script_dir=$(dirname "$0")
data_root=${script_dir}/../datasets
tools_dir=${script_dir}/../tools

python3 "${tools_dir}/hf_data_load.py" \
  --repo procesaur/cirilica \
  --datadir "${data_root}" \
  --fnamefield id \
  --textfield text_cyr