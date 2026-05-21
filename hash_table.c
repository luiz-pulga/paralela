#include "hash_table.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* Funcao hash djb2 */
unsigned long ht_hash(const char *str) {
    unsigned long hash = 5381;
    int c;
    while ((c = *str++))
        hash = ((hash << 5) + hash) + c;
    return hash;
}

HashTable* ht_create(size_t size) {
    HashTable *ht = malloc(sizeof(HashTable));
    if (!ht) {
        fprintf(stderr, "Erro ao alocar HashTable\n");
        exit(EXIT_FAILURE);
    }
    ht->size = size;
    ht->buckets = calloc(size, sizeof(CacheNode*));
    if (!ht->buckets) {
        fprintf(stderr, "Erro ao alocar buckets\n");
        exit(EXIT_FAILURE);
    }
    return ht;
}

void ht_insert(HashTable* ht, const char* url) {
    size_t index = ht_hash(url) % ht->size;

    /* Verifica se ja existe */
    CacheNode *current = ht->buckets[index];
    while (current) {
        if (strcmp(current->url, url) == 0) {
            return; /* URL ja existe, nao insere duplicata */
        }
        current = current->next;
    }

    /* Cria novo no */
    CacheNode *node = malloc(sizeof(CacheNode));
    if (!node) {
        fprintf(stderr, "Erro ao alocar CacheNode\n");
        exit(EXIT_FAILURE);
    }
    node->url = strdup(url);
    node->hit_count = 0;
    node->next = ht->buckets[index];
    ht->buckets[index] = node;
}

CacheNode* ht_get(HashTable* ht, const char* url) {
    size_t index = ht_hash(url) % ht->size;
    CacheNode *current = ht->buckets[index];
    while (current) {
        if (strcmp(current->url, url) == 0) {
            return current;
        }
        current = current->next;
    }
    return NULL;
}

void ht_save_results(HashTable* ht, const char* filename) {
    FILE *fp = fopen(filename, "w");
    if (!fp) {
        fprintf(stderr, "Erro ao abrir arquivo %s para escrita\n", filename);
        exit(EXIT_FAILURE);
    }

    for (size_t i = 0; i < ht->size; i++) {
        CacheNode *current = ht->buckets[i];
        while (current) {
            if (current->hit_count > 0) {
                fprintf(fp, "%s,%ld\n", current->url, current->hit_count);
            }
            current = current->next;
        }
    }
    fclose(fp);
}

void ht_destroy(HashTable* ht) {
    for (size_t i = 0; i < ht->size; i++) {
        CacheNode *current = ht->buckets[i];
        while (current) {
            CacheNode *tmp = current;
            current = current->next;
            free(tmp->url);
            free(tmp);
        }
    }
    free(ht->buckets);
    free(ht);
}
