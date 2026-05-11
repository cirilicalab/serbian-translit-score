#!/bin/bash

install_dir=/tmp/eevan78

# make installation directory
mkdir -p $install_dir
cd ${install_dir}

# clone repo
git clone https://github.com/eevan78/translit.git
cd translit

# get dependencies
go mod tidy

# build transliterator
go build -compiler gc -ldflags="-w -s" cmd/translit/translit.go


