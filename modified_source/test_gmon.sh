#!/bin/bash

rm -f *.o percolate
gcc -g -pg -c arralloc.c uni.c percolate.c
gcc -g -pg -o percolate arralloc.o uni.o percolate.o -lm

./percolate -l 20 -m 400 -s 0 -r 0.3 -d test.dat -p test.pgm
gprof -l -b -Q percolate gmon.out > test.txt
