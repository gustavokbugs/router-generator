#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "grafo.h"
#include "grafo_db.h"

/* Função que retorna uma mensagem de teste para o front-end */
const char* obter_mensagem_teste() {
    return "Olá! Sistema de navegação conectado com sucesso! ✅";
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

/* Função para obter o número de vértices do tipo PONTO */
EXPORT int get_num_pontos() {
    Grafo* grafo = criar_grafo();
    if (grafo == NULL) return 0;
    
    inicializar_vertices(grafo);
    
    int count = 0;
    int i;
    for (i = 0; i < grafo->num_vertices; i++) {
        if (grafo->vertices[i].tipo == TIPO_PONTO) {
            count++;
        }
    }
    
    destruir_grafo(grafo);
    return count;
}

/* Função para obter informações de um ponto específico por índice */
EXPORT int get_ponto_info(int index, char* nome_out, int nome_len, char* categoria_out, int cat_len, int* id_out) {
    Grafo* grafo = criar_grafo();
    if (grafo == NULL) return -1;
    
    inicializar_vertices(grafo);
    
    int count = 0;
    int i;
    int found = 0;
    
    for (i = 0; i < grafo->num_vertices; i++) {
        if (grafo->vertices[i].tipo == TIPO_PONTO) {
            if (count == index) {
                // Copiar informações
                if (nome_out != NULL && nome_len > 0) {
                    strncpy(nome_out, grafo->vertices[i].nome, nome_len - 1);
                    nome_out[nome_len - 1] = '\0';
                }
                if (categoria_out != NULL && cat_len > 0) {
                    strncpy(categoria_out, grafo->vertices[i].categoria, cat_len - 1);
                    categoria_out[cat_len - 1] = '\0';
                }
                if (id_out != NULL) {
                    *id_out = grafo->vertices[i].id;
                }
                found = 1;
                break;
            }
            count++;
        }
    }
    
    destruir_grafo(grafo);
    return found ? 0 : -1;
}

/* Função principal para testes locais */
int main() {
    printf("=== Sistema de Navegação - Backend em C ===\n");
    printf("Mensagem de teste: %s\n", obter_mensagem_teste());
    
    printf("\nInicializando grafo...\n");
    Grafo* grafo = criar_grafo();
    
    if (grafo != NULL) {
        printf("Grafo criado com sucesso!\n");
        inicializar_vertices(grafo);
        printf("Vértices carregados: %d\n", grafo->num_vertices);
        
        inicializar_arestas(grafo);
        printf("Arestas carregadas com sucesso!\n");
        
        destruir_grafo(grafo);
        printf("Grafo destruído corretamente.\n");
    }
    
    printf("\n=== Sistema pronto para integração com Python ===\n");
    return 0;
}
