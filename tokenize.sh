#!/bin/bash
# Tokenizes the file found in p2p_data

if [ $# -ne 1 ]; then
    echo "Usage: ./tokenize.sh [file in p2p_data]"
    exit 1
fi

python tokenizer.py p2p_data/$1 > sources/${1%.txt}.hackthehill
