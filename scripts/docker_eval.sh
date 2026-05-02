#!/bin/bash

# Runs evaluation in docker with installed transliteration tools

version=0.0
script_dir=$(dirname "$0")
git_root=${script_dir}/..

docker run -it --rm \
    -v ${git_root}:/test_root \
    -u $(id -u):$(id -g) \
    -w /test_root \
    srb-translit:${version} \
    bash ./scripts/eval.sh
