# 🧮 Algoritmo de Dijkstra - Lógica e Implementação

## 📖 Conceito

Algoritmo para encontrar o **caminho mais curto** entre dois pontos em um grafo. Criado por Edsger Dijkstra (1956).

**Ideia central:** Explorar o grafo sempre escolhendo o vértice mais próximo não visitado. É um algoritmo **guloso** (greedy).


---

## 🔧 Estruturas Necessárias

```c
// 1. Grafo (lista de adjacências)
typedef struct {
    int num_vertices;
    Vertice* vertices;
    Aresta** lista_adj;
} Grafo;

// 2. Arrays auxiliares
int* distancias;    // Menor distância da origem até cada vértice
int* anteriores;    // Predecessor no caminho mais curto
int* visitados;     // Marca se vértice foi processado
```

---

## 📝 Algoritmo - 3 Etapas Principais

### **1. Inicialização**

```c
// Todas as distâncias = infinito, exceto origem = 0
for (i = 0; i < num_vertices; i++) {
    distancias[i] = INT_MAX;  // Infinito
    anteriores[i] = -1;
    visitados[i] = 0;
}
distancias[origem] = 0;
```

### **2. Loop Principal (Executa V vezes)**

```c
for (count = 0; count < num_vertices; count++) {
    
    // 2.1: Encontrar vértice NÃO visitado com menor distância
    int u = encontrar_menor_distancia(distancias, visitados, num_vertices);
    
    if (u == -1) break;  // Não há mais vértices alcançáveis
    
    // 2.2: Marcar como visitado (distância é final!)
    visitados[u] = 1;
    
    // 2.3: RELAXAMENTO - Atualizar distâncias dos vizinhos
    Aresta* aresta = lista_adj[u];
    while (aresta != NULL) {
        int v = aresta->destino_id;
        
        if (!visitados[v]) {
            int nova_dist = distancias[u] + aresta->distancia;
            
            // Encontrou caminho mais curto?
            if (nova_dist < distancias[v]) {
                distancias[v] = nova_dist;
                anteriores[v] = u;  // u é predecessor de v
            }
        }
        
        aresta = aresta->prox;
    }
}
```

### **3. Reconstrução do Caminho**

```c
// Volta do destino até origem usando array 'anteriores'
int* caminho_temp = malloc(...);
int atual = destino;
int num_ids = 0;

while (atual != -1) {
    caminho_temp[num_ids++] = vertices[atual].id;
    atual = anteriores[atual];  // Volta para predecessor
}

// Inverter (estava Destino→Origem, fica Origem→Destino)
for (i = 0; i < num_ids; i++) {
    caminho_final[i] = caminho_temp[num_ids - 1 - i];
}
```

---

## 💡 Lógica do Relaxamento

**Relaxamento** é o processo de atualizar distâncias quando encontra caminho melhor:

```c
// Estado atual:
distancias[A] = 0
distancias[B] = ∞
aresta A→B com peso 4

// Cálculo:
nova_dist = distancias[A] + peso(A→B) = 0 + 4 = 4

// Como 4 < ∞:
distancias[B] = 4
anteriores[B] = A
```

**Por que funciona?**
- Se `distancias[u] + peso(u→v) < distancias[v]`, encontramos caminho melhor
- Atualiza tanto a distância quanto o predecessor
- Garante que sempre mantemos o melhor caminho conhecido

---

## 🎯 Exemplo Passo a Passo

Grafo:
```
    A --4-- B --2-- C
    |       |       |
    1       5       3
    |       |       |
    D --6-- E --1-- F
```

**Origem: A | Destino: F**

### **Inicialização**
```
distancias: [0, ∞, ∞, ∞, ∞, ∞]  (índices: A,B,C,D,E,F)
visitados:  [0, 0, 0, 0, 0, 0]
```

### **Iteração 1: Processar A (dist=0)**
```
1. Escolhe A (menor não visitado = 0)
2. Marca visitados[A] = 1
3. Relaxa vizinhos:
   - B: ∞ → 4  (0+4)
   - D: ∞ → 1  (0+1)

distancias: [0, 4, ∞, 1, ∞, ∞]
anteriores: [-1, A, -1, A, -1, -1]
```

### **Iteração 2: Processar D (dist=1)**
```
1. Escolhe D (menor não visitado = 1)
2. Marca visitados[D] = 1
3. Relaxa vizinhos:
   - E: ∞ → 7  (1+6)

distancias: [0, 4, ∞, 1, 7, ∞]
anteriores: [-1, A, -1, A, D, -1]
```

### **Iteração 3: Processar B (dist=4)**
```
1. Escolhe B (menor não visitado = 4)
2. Marca visitados[B] = 1
3. Relaxa vizinhos:
   - C: ∞ → 6  (4+2)
   - E: 7 (não atualiza, pois 4+5=9 > 7)

distancias: [0, 4, 6, 1, 7, ∞]
anteriores: [-1, A, B, A, D, -1]
```

### **Iteração 4: Processar C (dist=6)**
```
1. Escolhe C
2. Relaxa:
   - F: ∞ → 9  (6+3)

distancias: [0, 4, 6, 1, 7, 9]
anteriores: [-1, A, B, A, D, C]
```

### **Iteração 5: Processar E (dist=7)**
```
1. Escolhe E
2. Relaxa:
   - F: 9 → 8  (7+1, MELHOR!)

distancias: [0, 4, 6, 1, 7, 8]
anteriores: [-1, A, B, A, D, E]  ← F agora vem de E
```

### **Resultado Final**
```
Menor distância A→F: 8

Reconstrução do caminho:
  F ← anteriores[F] = E
  E ← anteriores[E] = D
  D ← anteriores[D] = A
  A ← anteriores[A] = -1 (origem)

Caminho: A → D → E → F
Distância: 1 + 6 + 1 = 8
```

---

## ⚡ Complexidade

### **Tempo**
- **O(V²)** - Implementação simples (busca linear do mínimo)
  - V iterações × O(V) para encontrar mínimo
- **O(E log V)** - Com min-heap
  - Extrair mínimo: O(log V)
  - Atualizar distâncias: O(log V)

### **Espaço**
- **O(V)** - Arrays auxiliares (distancias, anteriores, visitados)

---

## ✅ Por Que Garante Solução Ótima?

**Invariante do loop:** Quando um vértice é marcado como visitado, sua distância é **final e ótima**.

**Prova:**
1. Sempre processa vértices em ordem crescente de distância
2. Quando marca `u` como visitado, qualquer outro caminho até `u` passaria por vértices não visitados
3. Mas esses vértices têm distância ≥ `distancias[u]`
4. Logo, nenhum caminho futuro melhorará `distancias[u]`

---

## ⚠️ Limitações

1. **Não funciona com pesos negativos**
   - Assume que visitar um vértice depois não melhora sua distância
   - Para pesos negativos, usar Bellman-Ford

2. **Grafo deve ter caminho entre origem e destino**
   ```c
   if (distancias[destino] == INT_MAX) {
       return NULL;  // Destino não alcançável
   }
   ```

---

## 🔍 Implementação no Projeto

### **Função Principal**
```c
ResultadoRota* calcular_rota(int id_origem, int id_destino) {
    // 1. Criar grafo
    Grafo* g = criar_grafo();
    inicializar_vertices(g);  // 120 vértices
    inicializar_arestas(g);   // 152 arestas
    
    // 2. Executar Dijkstra
    int* distancias;
    int* anteriores;
    executar_dijkstra(g, idx_origem, &distancias, &anteriores);
    
    // 3. Reconstruir caminho
    ResultadoRota* resultado = reconstruir_caminho(
        g, distancias, anteriores, idx_origem, idx_destino
    );
    
    // 4. Limpar e retornar
    free(distancias);
    free(anteriores);
    destruir_grafo(g);
    
    return resultado;  // {sequencia_ids[], num_ids, distancia_total}
}
```

### **Exemplo de Saída**
```
CÁLCULO DE ROTA: ID 22 -> ID 33

[1/6] Criando grafo...
[2/6] Carregando 120 vertices...
[3/6] Carregando 152 arestas...
[4/6] Localizando vertices...
[5/6] Executando Dijkstra...
[6/6] Reconstruindo caminho...

Caminho final:
  ID=22 'Pastelaria Pasteten Platz'
  ID=30 'Parque Infantil'
  ID=31 'La Fiamma'
  ID=33 'Severo Garage'

Total: 4 pontos, 450 metros
```

---

## 🎓 Resumo

**Lógica:**
1. Inicializa todas as distâncias como infinito (exceto origem = 0)
2. Repete V vezes:
   - Escolhe vértice não visitado mais próximo
   - Marca como visitado
   - Relaxa arestas (atualiza distâncias dos vizinhos)
3. Reconstrói caminho usando array `anteriores[]`

**Por que funciona:**
- Sempre processa vértices em ordem de distância crescente
- Quando visita um vértice, sua distância é final
- Propriedade de subestrutura ótima garante corretude

**Complexidade:**
- O(V²) na implementação simples
- O(E log V) com min-heap

**Aplicação:**
- Usado em GPS, roteamento de redes, jogos
- No projeto: calcula menor caminho entre pontos turísticos

---

**Referência:** Dijkstra, E. W. (1959). "A note on two problems in connexion with graphs"
