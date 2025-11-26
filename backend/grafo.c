#include "grafo.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

/* Cria um novo grafo vazio */
Grafo* criar_grafo() {
    Grafo* g = (Grafo*)malloc(sizeof(Grafo));
    if (g == NULL) {
        return NULL;
    }
    
    g->num_vertices = 0;
    g->vertices = NULL;
    g->lista_adj = NULL;
    
    return g;
}

/* Adiciona um vértice ao grafo */
void adicionar_vertice(Grafo* g, int id, const char* nome, const char* categoria, const char* rua, int tipo, int x, int y) {
    if (g == NULL) {
        return;
    }
    
    /* Realoca arrays para novo vértice */
    g->vertices = (Vertice*)realloc(g->vertices, (g->num_vertices + 1) * sizeof(Vertice));
    g->lista_adj = (Aresta**)realloc(g->lista_adj, (g->num_vertices + 1) * sizeof(Aresta*));
    
    if (g->vertices == NULL || g->lista_adj == NULL) {
        printf("Erro ao alocar memória para vértice\n");
        return;
    }
    
    /* Preenche dados do vértice */
    Vertice* v = &g->vertices[g->num_vertices];
    v->id = id;
    strncpy(v->nome, nome, MAX_NOME - 1);
    v->nome[MAX_NOME - 1] = '\0';
    strncpy(v->categoria, categoria, MAX_CATEGORIA - 1);
    v->categoria[MAX_CATEGORIA - 1] = '\0';
    strncpy(v->rua, rua, MAX_RUA - 1);
    v->rua[MAX_RUA - 1] = '\0';
    v->tipo = tipo;
    v->x = x;
    v->y = y;
    
    /* Inicializa lista de adjacência vazia */
    g->lista_adj[g->num_vertices] = NULL;
    
    g->num_vertices++;
}

/* Encontra o índice de um vértice pelo ID */
static int encontrar_indice_vertice(Grafo* g, int id) {
    int i;
    for (i = 0; i < g->num_vertices; i++) {
        if (g->vertices[i].id == id) {
            return i;
        }
    }
    return -1;
}

/* Adiciona uma aresta entre dois vértices */
void adicionar_aresta(Grafo* g, int origem, int destino, int distancia) {
    if (g == NULL) {
        return;
    }
    
    int idx_origem = encontrar_indice_vertice(g, origem);
    
    if (idx_origem == -1) {
        printf("Vértice de origem %d não encontrado\n", origem);
        return;
    }
    
    /* Verifica se o vértice de destino existe */
    if (encontrar_indice_vertice(g, destino) == -1) {
        printf("Vértice de destino %d não encontrado\n", destino);
        return;
    }
    
    /* Cria nova aresta */
    Aresta* nova = (Aresta*)malloc(sizeof(Aresta));
    if (nova == NULL) {
        printf("Erro ao alocar memória para aresta\n");
        return;
    }
    
    nova->destino_id = destino;
    nova->distancia = distancia;
    nova->prox = g->lista_adj[idx_origem];
    g->lista_adj[idx_origem] = nova;
}

/* Libera memória do grafo */
void destruir_grafo(Grafo* g) {
    int i;
    Aresta* atual;
    Aresta* prox;
    
    if (g == NULL) {
        return;
    }
    
    /* Libera listas de adjacência */
    if (g->lista_adj != NULL) {
        for (i = 0; i < g->num_vertices; i++) {
            atual = g->lista_adj[i];
            while (atual != NULL) {
                prox = atual->prox;
                free(atual);
                atual = prox;
            }
        }
        free(g->lista_adj);
    }
    
    /* Libera array de vértices */
    if (g->vertices != NULL) {
        free(g->vertices);
    }
    
    /* Libera estrutura do grafo */
    free(g);
}
