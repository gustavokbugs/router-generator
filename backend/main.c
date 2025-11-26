#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "grafo.h"
#include "grafo_db.h"

/* Função que retorna uma mensagem de teste para o front-end */
const char* obter_mensagem_teste() {
    return "Sistema de navegação conectado com sucesso! ✅";
}

/* Função exportada para Python - Retorna mensagem de teste */
#ifdef _WIN32
    #define EXPORT __declspec(dllexport)
#else
    #define EXPORT
#endif

EXPORT const char* get_test_message() {
    return obter_mensagem_teste();
}

/* Função para obter o número de vértices do tipo PONTO (tipo == 1) */
EXPORT int get_num_pontos() {
    int count;
    const VerticeData* vertices = obter_vertices_static(&count);
    
    int num_pontos = 0;
    int i;
    for (i = 0; i < count; i++) {
        if (vertices[i].tipo == 1) {
            num_pontos++;
        }
    }
    
    return num_pontos;
}

/* Função otimizada para obter informações de um ponto específico por índice */
EXPORT int get_ponto_info(int index, char* nome_out, int nome_len, 
                          char* categoria_out, int cat_len, 
                          int* id_out, int* x_out, int* y_out) {
    int count;
    const VerticeData* vertices = obter_vertices_static(&count);
    
    int ponto_index = 0;
    int i;
    
    for (i = 0; i < count; i++) {
        if (vertices[i].tipo == 1) {
            if (ponto_index == index) {
                /* Copiar informações diretamente do array estático */
                if (nome_out != NULL && nome_len > 0) {
                    strncpy(nome_out, vertices[i].nome, nome_len - 1);
                    nome_out[nome_len - 1] = '\0';
                }
                if (categoria_out != NULL && cat_len > 0) {
                    strncpy(categoria_out, vertices[i].categoria, cat_len - 1);
                    categoria_out[cat_len - 1] = '\0';
                }
                if (id_out != NULL) {
                    *id_out = vertices[i].id;
                }
                if (x_out != NULL) {
                    *x_out = vertices[i].x;
                }
                if (y_out != NULL) {
                    *y_out = vertices[i].y;
                }
                return 0;
            }
            ponto_index++;
        }
    }
    
    return -1;
}

/* Função principal para testes locais */
int main() {
    printf("=== Sistema de Navegacao - Backend em C ===\n");
    printf("Mensagem de teste: %s\n", obter_mensagem_teste());
    
    printf("\nInicializando grafo a partir dos arquivos JSON...\n");
    Grafo* grafo = criar_grafo();
    
    if (grafo != NULL) {
        printf("Grafo criado com sucesso!\n");
        
        inicializar_vertices(grafo);
        printf("Vertices carregados: %d\n", grafo->num_vertices);
        
        inicializar_arestas(grafo);
        printf("Arestas carregadas com sucesso!\n");
        
        /* Exibir alguns vértices como exemplo */
        printf("\n=== Exemplos de vertices carregados ===\n");
        int i;
        int count = 0;
        for (i = 0; i < grafo->num_vertices && count < 5; i++) {
            if (grafo->vertices[i].tipo == 1) { /* Pontos de interesse */
                printf("ID: %d | Nome: %s\n", 
                       grafo->vertices[i].id, 
                       grafo->vertices[i].nome);
                printf("  Categoria: %s | Rua: %s\n", 
                       grafo->vertices[i].categoria, 
                       grafo->vertices[i].rua);
                printf("  Coordenadas: (%d, %d)\n\n", 
                       grafo->vertices[i].x, 
                       grafo->vertices[i].y);
                count++;
            }
        }
        
        destruir_grafo(grafo);
        printf("Grafo destruido corretamente.\n");
    } else {
        printf("Erro ao criar grafo!\n");
    }
    
    printf("\n=== Sistema pronto para integracao com Python ===\n");
    return 0;
}
