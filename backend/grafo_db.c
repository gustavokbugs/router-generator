#include "grafo_db.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

/* Popula grafo com todos os vértices do banco estático (grafo_data.c) */
void inicializar_vertices(Grafo* g) {
    int count;
    const VerticeData* vertices = obter_vertices_static(&count);
    
    int i;
    /* Itera sobre array estático e adiciona cada vértice ao grafo dinâmico */
    for (i = 0; i < count; i++) {
        adicionar_vertice(g, 
                         vertices[i].id, 
                         vertices[i].nome, 
                         vertices[i].categoria, 
                         vertices[i].rua, 
                         vertices[i].tipo,
                         vertices[i].x,
                         vertices[i].y);
    }
}

/* Popula grafo com todas as arestas do banco estático (grafo_data.c) */
void inicializar_arestas(Grafo* g) {
    int count;
    const ArestaData* arestas = obter_arestas_static(&count);
    
    int i;
    /* Itera sobre array estático e adiciona cada aresta ao grafo dinâmico */
    for (i = 0; i < count; i++) {
        adicionar_aresta(g, 
                        arestas[i].origem, 
                        arestas[i].destino, 
                        arestas[i].distancia);
    }
}
