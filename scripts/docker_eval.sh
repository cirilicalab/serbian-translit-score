#!/bin/bash

#
# This is just a wrapper script which runs eval.sh in docker.
#

version=0.0
script_dir=$(dirname "$0")
git_root=${script_dir}/..

docker run -it --rm \
    -v ${git_root}:/test_root \
    -u $(id -u):$(id -g) \
    -w /test_root \
    srb-translit:${version} \
    bash ./scripts/eval.sh
