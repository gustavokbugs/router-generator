#include "grafo_db.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

/* Carrega vértices dos dados estáticos */
void inicializar_vertices(Grafo* g) {
    int count;
    const VerticeData* vertices = obter_vertices_static(&count);
    
    int i;
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

/* Carrega arestas dos dados estáticos */
void inicializar_arestas(Grafo* g) {
    int count;
    const ArestaData* arestas = obter_arestas_static(&count);
    
    int i;
    for (i = 0; i < count; i++) {
        adicionar_aresta(g, 
                        arestas[i].origem, 
                        arestas[i].destino, 
                        arestas[i].distancia);
    }
}
