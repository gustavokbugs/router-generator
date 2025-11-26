#ifndef GRAFO_DB_H
#define GRAFO_DB_H

#include "grafo.h"

/* Estruturas para dados estáticos */
typedef struct {
    int id;
    const char* nome;
    const char* categoria;
    const char* rua;
    int tipo;
    int x;
    int y;
} VerticeData;

typedef struct {
    int origem;
    int destino;
    int distancia;
} ArestaData;

/* Protótipos - Acesso aos dados estáticos */
const VerticeData* obter_vertices_static(int* count);
const ArestaData* obter_arestas_static(int* count);

/* Protótipos do Banco de Dados */
void inicializar_vertices(Grafo* g);
void inicializar_arestas(Grafo* g);

#endif