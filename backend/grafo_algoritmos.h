#ifndef GRAFO_ALGORITMOS_H
#define GRAFO_ALGORITMOS_H

#include "grafo.h"
#include <limits.h>

/* Estrutura simplificada para resultado de rota */
typedef struct {
    int* sequencia_ids;      /* Array de IDs no caminho (origem → destino) */
    int num_ids;             /* Quantidade de IDs no caminho */
    int distancia_total;     /* Distância total em metros */
} ResultadoRota;

#ifdef _WIN32
    #define EXPORT __declspec(dllexport)
#else
    #define EXPORT
#endif

/* Funções principais do Dijkstra */
EXPORT ResultadoRota* calcular_rota(int id_origem, int id_destino);
EXPORT void liberar_resultado(ResultadoRota* resultado);

/* Funções auxiliares para frontend (SISTEMA DE LISTA) */
EXPORT int obter_numero_total_vertices();
EXPORT int obter_info_vertice(int id, char* nome_out, int nome_len, 
                             char* categoria_out, int cat_len,
                             int* x_out, int* y_out);

/* Função interna auxiliar */
int encontrar_indice_vertice(Grafo* g, int id);

#endif
