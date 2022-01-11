#!/bin/bash

gcc -g -pg -c arralloc.c uni.c percolate.c
gcc -g -pg -o percolate arralloc.o uni.o percolate.o -lm

for l in {10..100..10}
do
   for s in {0..900000000..300000000}
   do
      echo "Running with length $l"
      ./percolate -l $l -m $l*$l -s $s -d $l'_'$s.dat -p $l'_'$s.pgm
      gprof -l -b -Q percolate gmon.out > $l'_'$s.txt
   done
done

for l in {100..1000..100}
do
   for s in {0..900000000..300000000}
   do
      echo "Running with length $l"
      ./percolate -l $l -m $l*$l -s $s -d $l'_'$s.dat -p $l'_'$s.pgm
      gprof -l -b -Q percolate gmon.out > $l'_'$s.txt
   done
done

for l in {1000..10000..1000}
do
   for s in {0..900000000..300000000}
   do
      echo "Running with length $l"
      ./percolate -l $l -m $l*$l -s $s -d $l'_'$s.dat -p $l'_'$s.pgm
      gprof -l -b -Q percolate gmon.out > $l'_'$s.txt
   done
done