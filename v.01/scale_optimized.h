#ifndef _SCALE_OPTIMIZED_H
#define _SCALE_OPTIMIZED_H
#include <stdio.h>
#include <stdlib.h>

int openScale(void);

void printAttr(int scale, FILE *log);

float readScale(int scale, fd_set *inputSet, struct timeval *timeOut);

int closeScale(int scale);
#endif