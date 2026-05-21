CC = gcc
CFLAGS = -Wall -Wextra -O2 -fopenmp
LDFLAGS = -fopenmp

all: analyzer_seq analyzer_par_critical analyzer_par_atomic analyzer_par_lock analyzer_par_atomic_padded

hash_table.o: hash_table.c hash_table.h
	$(CC) $(CFLAGS) -c hash_table.c -o hash_table.o

analyzer_seq: analyzer_seq.c hash_table.o hash_table.h
	$(CC) $(CFLAGS) analyzer_seq.c hash_table.o -o analyzer_seq $(LDFLAGS)

analyzer_par_critical: analyzer_par_critical.c hash_table.o hash_table.h
	$(CC) $(CFLAGS) analyzer_par_critical.c hash_table.o -o analyzer_par_critical $(LDFLAGS)

analyzer_par_atomic: analyzer_par_atomic.c hash_table.o hash_table.h
	$(CC) $(CFLAGS) analyzer_par_atomic.c hash_table.o -o analyzer_par_atomic $(LDFLAGS)

analyzer_par_lock: analyzer_par_lock.c hash_table.o hash_table.h
	$(CC) $(CFLAGS) analyzer_par_lock.c hash_table.o -o analyzer_par_lock $(LDFLAGS)

analyzer_par_atomic_padded: analyzer_par_atomic_padded.c
	$(CC) $(CFLAGS) analyzer_par_atomic_padded.c -o analyzer_par_atomic_padded $(LDFLAGS)

clean:
	rm -f *.o analyzer_seq analyzer_par_critical analyzer_par_atomic analyzer_par_lock analyzer_par_atomic_padded results.csv

.PHONY: all clean
