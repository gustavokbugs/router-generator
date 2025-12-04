#include "grafo_algoritmos.h"
#include "grafo_db.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <limits.h>

/* Função interna: Encontra vértice não visitado com menor distância */
static int encontrar_menor_distancia(int* distancias, int* visitados, int num_vertices) {
    int menor_distancia = INT_MAX;
    int indice_menor = -1;
    int i;
    
    for (i = 0; i < num_vertices; i++) {
        if (!visitados[i] && distancias[i] <= menor_distancia) {
            menor_distancia = distancias[i];
            indice_menor = i;
        }
    }
    
    return indice_menor;
}

/* Função interna: Executa algoritmo Dijkstra */
static int executar_dijkstra(Grafo* g, int indice_origem, int** distancias_out, int** anteriores_out) {
    int i, count;
    int* distancias = NULL;
    int* anteriores = NULL;
    int* visitados = NULL;
    
    /* 1. VALIDAÇÃO */
    if (g == NULL || indice_origem < 0 || indice_origem >= g->num_vertices) {
        return 0;
    }
    
    printf("\n=== INICIANDO DIJKSTRA ===\n");
    printf("Origem (indice=%d, ID=%d): %s\n", 
           indice_origem, g->vertices[indice_origem].id, g->vertices[indice_origem].nome);
    
    /* 2. ALOCAÇÃO DE MEMÓRIA */
    distancias = (int*)malloc(g->num_vertices * sizeof(int));
    anteriores = (int*)malloc(g->num_vertices * sizeof(int));
    visitados = (int*)malloc(g->num_vertices * sizeof(int));
    
    if (distancias == NULL || anteriores == NULL || visitados == NULL) {
        if (distancias) free(distancias);
        if (anteriores) free(anteriores);
        if (visitados) free(visitados);
        return 0;
    }
    
    /* 3. INICIALIZAÇÃO */
    for (i = 0; i < g->num_vertices; i++) {
        distancias[i] = INT_MAX;
        anteriores[i] = -1;
        visitados[i] = 0;
    }
    distancias[indice_origem] = 0;
    
    /* 4. ALGORITMO DIJKSTRA (Loop principal) */
    printf("\n--- Processamento dos vertices ---\n");
    for (count = 0; count < g->num_vertices; count++) {
        int u = encontrar_menor_distancia(distancias, visitados, g->num_vertices);
        
        if (u == -1) {
            break; /* Não há mais vértices alcançáveis */
        }
        
        visitados[u] = 1;
        
        printf("\nVisitando vertice [%d] ID=%d '%s' (distancia=%d)\n", 
               u, g->vertices[u].id, g->vertices[u].nome, distancias[u]);
        
        /* Percorrer todas as arestas adjacentes */
        Aresta* aresta = g->lista_adj[u];
        int num_vizinhos = 0;
        while (aresta != NULL) {
            int v = encontrar_indice_vertice(g, aresta->destino_id);
            
            if (v != -1 && !visitados[v]) {
                int nova_distancia = distancias[u] + aresta->distancia;
                
                printf("  -> Vizinho ID=%d '%s': dist_atual=%d, nova_dist=%d, peso_aresta=%d", 
                       g->vertices[v].id, g->vertices[v].nome,
                       (distancias[v] == INT_MAX ? -1 : distancias[v]),
                       nova_distancia, aresta->distancia);
                
                if (nova_distancia < distancias[v]) {
                    distancias[v] = nova_distancia;
                    anteriores[v] = u;
                    printf(" [ATUALIZADO]\n");
                    num_vizinhos++;
                } else {
                    printf(" [sem mudanca]\n");
                }
            }
            
            aresta = aresta->prox;
        }
        
        if (num_vizinhos == 0) {
            printf("  (sem vizinhos nao-visitados)\n");
        }
    }
    
    /* 5. LIMPEZA E RETORNO */
    free(visitados);
    *distancias_out = distancias;
    *anteriores_out = anteriores;
    
    return 1;
}

/* Função interna: Reconstrói caminho do destino até origem */
static ResultadoRota* reconstruir_caminho(Grafo* g, int* distancias, int* anteriores, 
                                         int indice_origem, int indice_destino) {
    int* caminho_temp = NULL;
    ResultadoRota* resultado = NULL;
    int current, num_ids, i;
    
    /* 1. VALIDAÇÃO */
    if (g == NULL || distancias == NULL || anteriores == NULL) {
        return NULL;
    }
    
    if (distancias[indice_destino] == INT_MAX) {
        printf("\n[ERRO] Destino nao alcancavel!\n");
        return NULL; /* Destino não alcançável */
    }
    
    printf("\n=== RECONSTRUINDO CAMINHO ===\n");
    printf("Destino (indice=%d, ID=%d): %s\n", 
           indice_destino, g->vertices[indice_destino].id, g->vertices[indice_destino].nome);
    printf("Distancia total: %d metros\n\n", distancias[indice_destino]);
    
    /* 2. ALOCAÇÃO */
    resultado = (ResultadoRota*)malloc(sizeof(ResultadoRota));
    caminho_temp = (int*)malloc(g->num_vertices * sizeof(int));
    
    if (resultado == NULL || caminho_temp == NULL) {
        if (resultado) free(resultado);
        if (caminho_temp) free(caminho_temp);
        return NULL;
    }
    
    /* 3. RECONSTRUÇÃO (Destino → Origem) */
    printf("Caminho (reverso - Destino -> Origem):\n");
    current = indice_destino;
    num_ids = 0;
    
    while (current != -1 && num_ids < g->num_vertices) {
        caminho_temp[num_ids] = g->vertices[current].id;
        printf("  [%d] ID=%d '%s'\n", num_ids, g->vertices[current].id, g->vertices[current].nome);
        num_ids++;
        current = anteriores[current];
    }
    
    /* Proteção contra loop infinito */
    if (num_ids >= g->num_vertices) {
        free(resultado);
        free(caminho_temp);
        return NULL;
    }
    
    /* 4. INVERSÃO (Origem → Destino) */
    resultado->sequencia_ids = (int*)malloc(num_ids * sizeof(int));
    if (resultado->sequencia_ids == NULL) {
        free(resultado);
        free(caminho_temp);
        return NULL;
    }
    
    printf("\nCaminho final (Origem -> Destino):\n");
    for (i = 0; i < num_ids; i++) {
        resultado->sequencia_ids[i] = caminho_temp[num_ids - 1 - i];
        int idx = encontrar_indice_vertice(g, resultado->sequencia_ids[i]);
        if (idx != -1) {
            printf("  [%d] ID=%d '%s'\n", i, resultado->sequencia_ids[i], g->vertices[idx].nome);
        }
    }
    
    resultado->num_ids = num_ids;
    resultado->distancia_total = distancias[indice_destino];
    
    printf("\n=== ROTA FINALIZADA ===\n");
    printf("Total de pontos: %d\n", num_ids);
    printf("Distancia: %d metros\n\n", resultado->distancia_total);
    
    /* 5. LIMPEZA E RETORNO */
    free(caminho_temp);
    
    return resultado;
}

/* FUNÇÃO EXPORTADA PRINCIPAL: Calcula rota entre dois IDs */
EXPORT ResultadoRota* calcular_rota(int id_origem, int id_destino) {
    Grafo* grafo = NULL;
    int idx_origem, idx_destino;
    int* distancias = NULL;
    int* anteriores = NULL;
    ResultadoRota* resultado = NULL;
    
    printf("\n");
    printf("========================================\n");
    printf("  CALCULO DE ROTA: ID %d -> ID %d\n", id_origem, id_destino);
    printf("========================================\n");
    
    /* 1. VALIDAÇÃO INICIAL */
    if (id_origem == id_destino) {
        printf("[ERRO] Origem e destino sao iguais!\n");
        return NULL; /* Rota trivial */
    }
    
    if (id_origem < 0 || id_destino < 0) {
        printf("[ERRO] IDs invalidos!\n");
        return NULL; /* IDs inválidos */
    }
    
    /* 2. CRIAR GRAFO */
    printf("\n[1/6] Criando grafo...\n");
    grafo = criar_grafo();
    if (grafo == NULL) {
        printf("[ERRO] Falha ao criar grafo!\n");
        return NULL;
    }
    
    /* 3. CARREGAR DADOS DO BANCO 1 */
    printf("[2/6] Carregando vertices...\n");
    inicializar_vertices(grafo);
    printf("      Total de vertices: %d\n", grafo->num_vertices);
    
    printf("[3/6] Carregando arestas...\n");
    inicializar_arestas(grafo);
    
    /* 4. CONVERTER IDs → ÍNDICES */
    printf("[4/6] Localizando vertices na estrutura...\n");
    idx_origem = encontrar_indice_vertice(grafo, id_origem);
    idx_destino = encontrar_indice_vertice(grafo, id_destino);
    
    if (idx_origem == -1) {
        printf("[ERRO] ID de origem %d nao encontrado!\n", id_origem);
        destruir_grafo(grafo);
        return NULL;
    }
    
    if (idx_destino == -1) {
        printf("[ERRO] ID de destino %d nao encontrado!\n", id_destino);
        destruir_grafo(grafo);
        return NULL;
    }
    
    printf("      Origem: indice=%d, ID=%d, nome='%s'\n", 
           idx_origem, grafo->vertices[idx_origem].id, grafo->vertices[idx_origem].nome);
    printf("      Destino: indice=%d, ID=%d, nome='%s'\n", 
           idx_destino, grafo->vertices[idx_destino].id, grafo->vertices[idx_destino].nome);
    
    /* 5. EXECUTAR DIJKSTRA */
    printf("\n[5/6] Executando algoritmo Dijkstra...\n");
    if (!executar_dijkstra(grafo, idx_origem, &distancias, &anteriores)) {
        printf("[ERRO] Falha na execucao do Dijkstra!\n");
        destruir_grafo(grafo);
        return NULL; /* Falha na execução */
    }
    
    /* 6. RECONSTRUIR CAMINHO */
    printf("\n[6/6] Reconstruindo caminho...\n");
    resultado = reconstruir_caminho(grafo, distancias, anteriores, idx_origem, idx_destino);
    
    /* 7. LIMPEZA */
    free(distancias);
    free(anteriores);
    destruir_grafo(grafo);
    
    /* 8. RETORNAR RESULTADO */
    if (resultado == NULL) {
        printf("[ERRO] Falha ao reconstruir caminho!\n");
    }
    
    return resultado;
}

/* FUNÇÃO EXPORTADA: Libera memória do resultado */
EXPORT void liberar_resultado(ResultadoRota* resultado) {
    if (resultado != NULL) {
        if (resultado->sequencia_ids != NULL) {
            free(resultado->sequencia_ids);
        }
        free(resultado);
    }
}

/* FUNÇÃO EXPORTADA: Retorna número total de vértices */
EXPORT int obter_numero_total_vertices() {
    int count;
    obter_vertices_static(&count);
    return count;
}

/* FUNÇÃO EXPORTADA: Obtém informações de um vértice por ID */
EXPORT int obter_info_vertice(int id, char* nome_out, int nome_len, 
                             char* categoria_out, int cat_len,
                             int* x_out, int* y_out) {
    int count, i;
    const VerticeData* vertices = obter_vertices_static(&count);
    
    /* BUSCAR VÉRTICE POR ID */
    for (i = 0; i < count; i++) {
        if (vertices[i].id == id) {
            /* COPIAR INFORMAÇÕES COM SEGURANÇA */
            if (nome_out != NULL && nome_len > 0) {
                strncpy(nome_out, vertices[i].nome, nome_len - 1);
                nome_out[nome_len - 1] = '\0';
            }
            
            if (categoria_out != NULL && cat_len > 0) {
                strncpy(categoria_out, vertices[i].categoria, cat_len - 1);
                categoria_out[cat_len - 1] = '\0';
            }
            
            if (x_out != NULL) {
                *x_out = vertices[i].x;
            }
            
            if (y_out != NULL) {
                *y_out = vertices[i].y;
            }
            
            return 0; /* Sucesso */
        }
    }
    
    return -1; /* Vértice não encontrado */
}
