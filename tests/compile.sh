#!/usr/bin/env bash

DIR="${1}"
if [ -d output ]; then
	rm -rf output
fi
mkdir output
if [ "${1}" == "" ]; then
	DIR="input4"
fi

cd src
for input in $( ls "../tests/${DIR}/" ); do
	echo "################ Compiling ${input} #########################"
	mkdir "../output/${input}"
	error=$( python2 semantic_parser.py --ir="../output/${input}/ir" --st="../output/${input}/st" "../tests/${DIR}/${input}" 2>/dev/null )
	if [ "$?" -ne 0 ]; then
		echo "ERROR!!! Failed to compile ${input}"
		rm -f *.pickle parsetab.{py,pyc} parser.out
		exit 1
	fi
	if [ "${error}" == "" ]; then
		echo "Semantic analysis done successfully!"
	else
		echo "***************************"
		echo ${error}
		echo "***************************"
		rm -f *.pickle parsetab.{py,pyc} parser.out
		continue
	fi
	python2 codegen.py --output "../output/${input}/asm.s"
	if [ "$?" -ne 0 ]; then
		echo "ERROR!!! Failed to compile ${input}"
		rm -f *.pickle parsetab.{py,pyc} parser.out
		exit 1
	fi
	rm -f *.pickle parsetab.{py,pyc} parser.out
done
