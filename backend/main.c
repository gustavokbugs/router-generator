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
