#!/bin/sh
echo "algorithm,alphabet,text_length,pattern_length,comps,time,memory" > /tmp/benchmarks
# text lengths
for n in $(seq 1000000 1000000 10000000)
do
	echo doing $n ...
	# pattern lengths
	for m in 100 1000 10000 100000 1000000
	do
		for alphabet in dna bin alnum
		do
			./randomstr.py $alphabet $n > /tmp/rantext
			./randomstr.py $alphabet $m > /tmp/ranpat
			for algo in naive kmp gs-boyer-moore bc-boyer-moore
			do
				echo $algo,$alphabet,$n,$m,$(time --format "%e,%M" ./$algo.py /tmp/rantext /tmp/ranpat bench 2>&1) >> /tmp/benchmarks
			done
		done
	done
done

