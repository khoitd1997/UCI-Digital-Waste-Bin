CC = gcc 
CFLAGS= -O2 -Wall -std=c99
LKFLAG= -lm

scale_optimized: scale_optimized.c scale_optimized.h 
	$(CC) $(CFLAGS) $(<) -o $(@) $(LKFLAGS)
clean: 
	rm -rf *.o scale_optimized