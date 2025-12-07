#ifndef GRAFO_DB_H
#define GRAFO_DB_H

#include "grafo.h"

/* Estrutura para representar dados de vértice do banco estático */
typedef struct {
    int id;              // ID único do vértice
    const char* nome;    // Nome descritivo (ex: "Pátio Universitário")
    const char* categoria; // Categoria (ex: "Centro Histórico", "Restaurante")
    const char* rua;     // Nome da rua onde está localizado
    int tipo;            // Tipo do vértice (0=esquina, 1=ponto turístico)
    int x;               // Coordenada X no mapa
    int y;               // Coordenada Y no mapa
} VerticeData;

/* Estrutura para representar dados de aresta do banco estático */
typedef struct {
    int origem;      // ID do vértice de origem
    int destino;     // ID do vértice de destino
    int distancia;   // Peso da aresta (distância em metros)
} ArestaData;

/* Funções de acesso aos dados estáticos (implementadas em grafo_data.c) */
const VerticeData* obter_vertices_static(int* count);  // Retorna array de vértices
const ArestaData* obter_arestas_static(int* count);    // Retorna array de arestas

/* Funções de inicialização do grafo a partir do banco estático */
void inicializar_vertices(Grafo* g);  // Popula grafo com vértices do banco
void inicializar_arestas(Grafo* g);   // Popula grafo com arestas do banco

#endif