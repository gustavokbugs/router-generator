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
    
    g->num_vertices = 0;     // Inicializa vazio
    g->vertices = NULL;      // Arrays serão alocados dinamicamente
    g->lista_adj = NULL;
    
    return g;
}

/* Adiciona um vértice ao grafo */
void adicionar_vertice(Grafo* g, int id, const char* nome, const char* categoria, const char* rua, int tipo, int x, int y) {
    if (g == NULL) {
        return;
    }
    
    /* Realoca arrays para comportar mais um vértice */
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
    v->nome[MAX_NOME - 1] = '\0';  // Garante terminação
    strncpy(v->categoria, categoria, MAX_CATEGORIA - 1);
    v->categoria[MAX_CATEGORIA - 1] = '\0';
    strncpy(v->rua, rua, MAX_RUA - 1);
    v->rua[MAX_RUA - 1] = '\0';
    v->tipo = tipo;
    v->x = x;  // Coordenadas da calçada para cálculo de rotas
    v->y = y;
    
    /* Inicializa lista de adjacência vazia para este vértice */
    g->lista_adj[g->num_vertices] = NULL;
    
    g->num_vertices++;
}

/* Encontra o índice de um vértice pelo ID (busca linear O(n)) */
int encontrar_indice_vertice(Grafo* g, int id) {
    int i;
    for (i = 0; i < g->num_vertices; i++) {
        if (g->vertices[i].id == id) {
            return i;
        }
    }
    return -1;  // Não encontrado
}

/* Adiciona uma aresta (conexão) entre dois vértices */
void adicionar_aresta(Grafo* g, int origem, int destino, int distancia) {
    if (g == NULL) {
        return;
    }
    
    int idx_origem = encontrar_indice_vertice(g, origem);
    
    if (idx_origem == -1) {
        return;  // Origem não existe, ignora aresta
    }
    
    /* Verifica se o vértice de destino existe */
    if (encontrar_indice_vertice(g, destino) == -1) {
        return;  // Destino não existe, ignora aresta
    }
    
    /* Cria nova aresta */
    Aresta* nova = (Aresta*)malloc(sizeof(Aresta));
    if (nova == NULL) {
        printf("Erro ao alocar memória para aresta\n");
        return;
    }
    
    nova->destino_id = destino;
    nova->distancia = distancia;
    nova->prox = g->lista_adj[idx_origem];  // Insere no início da lista (O(1))
    g->lista_adj[idx_origem] = nova;
}

/* Libera toda memória do grafo */
void destruir_grafo(Grafo* g) {
    int i;
    Aresta* atual;
    Aresta* prox;
    
    if (g == NULL) {
        return;
    }
    
    /* Libera todas as listas de adjacência */
    if (g->lista_adj != NULL) {
        for (i = 0; i < g->num_vertices; i++) {
            atual = g->lista_adj[i];
            while (atual != NULL) {  // Percorre lista encadeada
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
    
    /* Libera estrutura principal do grafo */
    free(g);
}
