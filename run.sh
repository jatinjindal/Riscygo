#!/usr/bin/env bash

if [ -d output ]; then
    rm -rf output
fi
mkdir output

cd src
for input in `ls ../tests/input1/`; do
    for config in `ls ../tests/cfg1/`; do
        python2 lexer.py --cfg="../tests/cfg1/${config}" "../output/${input}_${config}.html" --out="../tests/input1/${input}"
    done
done
cd ..
