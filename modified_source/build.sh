rm -f *.o percolate
gcc -g -pg -c arralloc.c uni.c percolate.c
gcc -g -pg -o percolate arralloc.o uni.o percolate.o -lm
