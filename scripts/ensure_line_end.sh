#!/bin/bash

# Updates adds \n to the end of text file if it's missing

sed -i -e '$a\' "$1"
