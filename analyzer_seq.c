#include "hash_table.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define TABLE_SIZE 131071
#define MAX_LINE_LEN 1024

/* Extrai a URL de uma linha de log.
   Formato: 127.0.0.1 - - [timestamp] "GET /url HTTP/1.1" status bytes
   Retorna ponteiro para buffer estatico interno. */
static char* extract_url(const char *line) {
    static char url_buf[MAX_LINE_LEN];

    /* Procura por "GET " ou "POST " etc */
    const char *start = strchr(line, '"');
    if (!start) return NULL;
    start++; /* pula a aspas */

    /* Pula o metodo HTTP (GET, POST, etc) */
    const char *space = strchr(start, ' ');
    if (!space) return NULL;
    space++; /* pula o espaco apos o metodo */

    /* Encontra o fim da URL (proximo espaco) */
    const char *end = strchr(space, ' ');
    if (!end) return NULL;

    size_t len = end - space;
    if (len >= MAX_LINE_LEN) len = MAX_LINE_LEN - 1;
    strncpy(url_buf, space, len);
    url_buf[len] = '\0';

    return url_buf;
}

/* Carrega todas as linhas de um arquivo em memoria.
   Retorna array de strings e preenche *count. */
static char** load_lines(const char *filename, int *count) {
    FILE *fp = fopen(filename, "r");
    if (!fp) {
        fprintf(stderr, "Erro ao abrir %s\n", filename);
        exit(EXIT_FAILURE);
    }

    /* Conta linhas */
    int capacity = 1000000;
    char **lines = malloc(capacity * sizeof(char*));
    if (!lines) {
        fprintf(stderr, "Erro de alocacao\n");
        exit(EXIT_FAILURE);
    }

    char buffer[MAX_LINE_LEN];
    int n = 0;
    while (fgets(buffer, MAX_LINE_LEN, fp)) {
        /* Remove newline */
        size_t len = strlen(buffer);
        if (len > 0 && buffer[len-1] == '\n') buffer[len-1] = '\0';

        if (n >= capacity) {
            capacity *= 2;
            lines = realloc(lines, capacity * sizeof(char*));
            if (!lines) {
                fprintf(stderr, "Erro de realocacao\n");
                exit(EXIT_FAILURE);
            }
        }
        lines[n] = strdup(buffer);
        n++;
    }
    fclose(fp);
    *count = n;
    return lines;
}

static void free_lines(char **lines, int count) {
    for (int i = 0; i < count; i++) {
        free(lines[i]);
    }
    free(lines);
}

/* Constroi a tabela hash a partir do manifest */
static HashTable* build_table(const char *manifest_file) {
    HashTable *ht = ht_create(TABLE_SIZE);
    FILE *fp = fopen(manifest_file, "r");
    if (!fp) {
        fprintf(stderr, "Erro ao abrir %s\n", manifest_file);
        exit(EXIT_FAILURE);
    }

    char buffer[MAX_LINE_LEN];
    while (fgets(buffer, MAX_LINE_LEN, fp)) {
        size_t len = strlen(buffer);
        if (len > 0 && buffer[len-1] == '\n') buffer[len-1] = '\0';
        if (len > 0) {
            ht_insert(ht, buffer);
        }
    }
    fclose(fp);
    return ht;
}

/* Processa um arquivo de log sequencialmente */
static void process_log(HashTable *ht, const char *log_file) {
    int count = 0;
    char **lines = load_lines(log_file, &count);

    for (int i = 0; i < count; i++) {
        char *url = extract_url(lines[i]);
        if (url) {
            CacheNode *node = ht_get(ht, url);
            if (node) {
                node->hit_count++;
            }
        }
    }

    free_lines(lines, count);
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Uso: %s <arquivo_log> [arquivo_log2 ...]\n", argv[0]);
        fprintf(stderr, "Exemplo: %s log_distribuido.txt\n", argv[0]);
        return EXIT_FAILURE;
    }

    printf("=== Analyzer Sequencial ===\n");

    /* Fase 1: Construcao da estrutura */
    printf("Construindo tabela hash a partir do manifest...\n");
    HashTable *ht = build_table("manifest.txt");

    /* Fase 2: Processamento dos logs informados na linha de comando */
    for (int i = 1; i < argc; i++) {
        printf("Processando %s...\n", argv[i]);
        process_log(ht, argv[i]);
    }

    /* Salvar resultados */
    printf("Salvando resultados...\n");
    ht_save_results(ht, "results.csv");

    printf("Concluido.\n");
    ht_destroy(ht);
    return 0;
}
