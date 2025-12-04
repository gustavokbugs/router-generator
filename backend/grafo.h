#ifndef GRAFO_H
#define GRAFO_H

#define MAX_NOME 100
#define MAX_CATEGORIA 50
#define MAX_RUA 100

/* Estruturas do Grafo */
typedef struct {
    int id;
    char nome[MAX_NOME];
    char categoria[MAX_CATEGORIA];
    char rua[MAX_RUA];
    int tipo;
    int x;
    int y;
} Vertice;

typedef struct Aresta {
    int destino_id;
    int distancia;
    struct Aresta* prox;
} Aresta;

typedef struct {
    int num_vertices;
    Vertice* vertices;
    Aresta** lista_adj;
} Grafo;

/* Protótipos das Funções do Grafo */
Grafo* criar_grafo();
void adicionar_vertice(Grafo* g, int id, const char* nome, const char* categoria, const char* rua, int tipo, int x, int y);
void adicionar_aresta(Grafo* g, int origem, int destino, int distancia);
void destruir_grafo(Grafo* g);
int encontrar_indice_vertice(Grafo* g, int id);

#endif
