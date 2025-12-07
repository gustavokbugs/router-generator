#ifndef GRAFO_H
#define GRAFO_H

#define MAX_NOME 100       // Tamanho máximo nome do local
#define MAX_CATEGORIA 50   // Tamanho máximo categoria
#define MAX_RUA 100        // Tamanho máximo nome da rua

/* Estruturas do Grafo */
typedef struct {
    int id;                        // ID único do vértice
    char nome[MAX_NOME];           // Nome do local/esquina
    char categoria[MAX_CATEGORIA]; // Tipo: restaurante, bar, esquina, etc
    char rua[MAX_RUA];             // Nome da rua onde está
    int tipo;                      // 0=esquina, 1=ponto turístico
    int x;                         // Coordenada X na calçada (para rotas)
    int y;                         // Coordenada Y na calçada (para rotas)
} Vertice;

typedef struct Aresta {
    int destino_id;        // ID do vértice destino
    int distancia;         // Distância em metros
    struct Aresta* prox;   // Próxima aresta na lista (encadeamento)
} Aresta;

typedef struct {
    int num_vertices;      // Total de vértices no grafo
    Vertice* vertices;     // Array dinâmico de vértices
    Aresta** lista_adj;    // Array de listas encadeadas (adjacências)
} Grafo;

/* Protótipos das Funções do Grafo */
Grafo* criar_grafo();                                  // Aloca grafo vazio
void adicionar_vertice(Grafo* g, int id, const char* nome, const char* categoria, const char* rua, int tipo, int x, int y);  // Adiciona vértice ao grafo
void adicionar_aresta(Grafo* g, int origem, int destino, int distancia);  // Adiciona conexão entre vértices
void destruir_grafo(Grafo* g);                        // Libera toda memória do grafo
int encontrar_indice_vertice(Grafo* g, int id);      // Busca índice do vértice por ID (O(n))

#endif
