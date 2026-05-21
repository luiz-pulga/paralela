#ifndef HASH_TABLE_H
#define HASH_TABLE_H

#include <stddef.h>

typedef struct CacheNode {
    char *url;
    long hit_count;
    struct CacheNode *next;
} CacheNode;

typedef struct {
    CacheNode **buckets;
    size_t size;
} HashTable;

/* Funcao hash djb2 - exposta para uso em estrategias de bucket lock */
unsigned long ht_hash(const char* str);

HashTable* ht_create(size_t size);
void ht_insert(HashTable* ht, const char* url);
CacheNode* ht_get(HashTable* ht, const char* url);
void ht_save_results(HashTable* ht, const char* filename);
void ht_destroy(HashTable* ht);

#endif
