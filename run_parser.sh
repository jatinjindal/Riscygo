#!/usr/bin/env bash

set -xe
if [ -d output ]; then
    rm -rf output
fi
mkdir output

cd src
for input in `ls ../tests/input2/`; do
    python2 parser.py --output="../output/${input}.dot" "../tests/input2/${input}"
    dot -Tpdf "../output/${input}.dot" -o "../output/${input}.pdf"
    rm "../output/${input}.dot"
done
cd ..
