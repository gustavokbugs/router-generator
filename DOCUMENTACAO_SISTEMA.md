# 📚 Sistema de Navegação com Dijkstra - Documentação Resumida

## 🎯 Visão Geral

Sistema híbrido: **Backend em C** (processamento de grafos) + **Frontend em Python** (interface gráfica). Calcula a menor rota entre pontos turísticos usando algoritmo de Dijkstra.

---

## 🗄️ 1. Dois Bancos de Dados

### **Banco 1 - grafo_data.c (Dados do Grafo)**
- **120 vértices**: Pontos turísticos + esquinas de ruas
- **152 arestas**: Conexões entre vértices com distâncias em metros
- **Coordenadas**: Posição na **calçada** (para cálculo de rotas)
- **Acesso**: `obter_vertices_static()` e `obter_arestas_static()`

### **Banco 2 - pins.json (Visualização)**
- **48 pins**: Apenas pontos turísticos (sem esquinas)
- **Coordenadas**: Posição no **centro do estabelecimento** (para exibir ícones)
- **Carregado por**: `_load_pins()` no Python

**Por que dois bancos?** Separar lógica de cálculo (calçadas) da visualização (estabelecimentos)


---

## ⚙️ 2. Criação e Carregamento do Grafo

Quando uma rota é solicitada, o backend C executa:

### **Etapas:**

1. **`criar_grafo()`** → Aloca estrutura vazia do grafo
2. **`inicializar_vertices()`** → Carrega 120 vértices do Banco 1 para o grafo
3. **`inicializar_arestas()`** → Carrega 152 arestas do Banco 1 para o grafo

**Estrutura de dados**: Lista de adjacências (cada vértice tem lista encadeada de conexões)

```c
typedef struct {
    int num_vertices;       // 120
    Vertice* vertices;      // Array dinâmico
    Aresta** lista_adj;     // Array de listas encadeadas
} Grafo;
```

**Por que recriar a cada consulta?** Garante estado limpo e facilita manutenção

---

## 🖼️ 3. Interface Gráfica e Seleção de Pontos

### **Inicialização (Python)**
1. Carrega mapa (`perimetro-mapa.png`)
2. Carrega `pins.json` (Banco 2)
3. Carrega ícones da pasta `assets/`
4. Desenha ícones no mapa usando coordenadas do Banco 2

### **Seleção de Origem/Destino**
- **Clique no ícone** ou **seleção da lista** → Define origem e destino
- **Validação**: Origem ≠ Destino
- **Envio**: IDs são enviados para `calcular_rota(id_origem, id_destino)` no backend C

---

## 🧮 4. Algoritmo de Dijkstra

Executado por `executar_dijkstra()` em C:

### **Etapas Principais:**

1. **Inicialização**
   - `distancias[]` = infinito (exceto origem = 0)
   - `anteriores[]` = -1 (para reconstruir caminho)
   - `visitados[]` = falso

2. **Loop Principal** (repete V vezes)
   - Seleciona vértice não visitado com **menor distância**
   - Marca como visitado
   - **Relaxamento**: Para cada vizinho não visitado:
     ```c
     nova_dist = distancias[u] + peso_aresta;
     if (nova_dist < distancias[v]) {
         distancias[v] = nova_dist;
         anteriores[v] = u;  // u é predecessor de v
     }
     ```

3. **Verificação**: Se `distancias[destino] == infinito` → caminho não existe

**Complexidade**: O(V²) = O(120²) nesta implementação

---

## 🛤️ 5. Reconstrução do Caminho

Função `reconstruir_caminho()` cria lista de IDs:

1. **Percorre de trás para frente** usando `anteriores[]`:
   ```
   current = destino
   while current != -1:
       caminho[i] = current
       current = anteriores[current]
   ```

2. **Inverte** a ordem (Destino→Origem vira Origem→Destino)

3. **Retorna** estrutura:
   ```c
   ResultadoRota {
       int* sequencia_ids;      // [22, 30, 31, 33]
       int num_ids;             // 4
       int distancia_total;     // 450 metros
   }
   ```

---

## 📍 6. Obtenção de Coordenadas e Desenho

### **Para cada ID da rota:**

1. **Python chama** `obter_coordenadas_vertice(id)` → Backend C
2. **C busca** no Banco 1 e retorna `(x, y)` da **calçada**
3. **Python converte** coordenadas imagem → canvas (considera zoom e pan)
4. **Desenha linha verde** conectando todos os pontos:
   ```python
   canvas.create_line(
       [x1, y1, x2, y2, ..., xn, yn],
       fill='#00ff00',
       width=4,
       smooth=True
   )
   ```

### **Informações Exibidas:**
- 📏 **Distância total** (em metros ou km)
- 🛣️ **Lista de ruas** percorridas

---

## 🔄 7. Fluxo Completo Resumido

```
1. Usuário abre app → Exibe mapa com ícones (Banco 2)
2. Usuário seleciona origem e destino → Captura IDs
3. Clica "Calcular Rota" → Python chama C
4. Backend C:
   ├─ Cria grafo vazio
   ├─ Carrega vértices e arestas (Banco 1)
   ├─ Executa Dijkstra
   └─ Reconstrói caminho
5. Python recebe lista de IDs + distância
6. Para cada ID → Busca coordenadas no Banco 1
7. Desenha linha verde no mapa
8. Exibe distância e ruas
```


---

## 🛠️ 8. Funções Principais

### **Backend C (grafo_algoritmos.c)**
- `calcular_rota()` → Função principal que coordena todo o processo
- `executar_dijkstra()` → Implementa algoritmo de menor caminho
- `reconstruir_caminho()` → Cria lista de IDs da rota
- `obter_info_vertice()` → Retorna coordenadas de um vértice por ID

### **Frontend Python (main.py)**
- `calcular_rota_dijkstra()` → Interface Python ↔ C
- `_draw_all_icons()` → Desenha ícones no mapa
- `_draw_route_line()` → Desenha linha verde da rota
- `_img_to_canvas()` → Converte coordenadas (considera zoom/pan)

---

## 📈 9. Complexidades e Otimizações

**Algoritmos:**
- Dijkstra: **O(V²)** = O(14.400) com 120 vértices
- Busca de vértice: **O(V)** linear
- Reconstrução: **O(k)** onde k = tamanho da rota

**Interface:**
- **Lazy Loading**: Carrega lista em lotes de 20 itens
- **Debounce**: Busca aguarda 400ms após digitação
- **Cache**: Pontos carregados uma vez e reutilizados

---

## 🎓 10. Conceitos Aplicados

- **Grafo** com lista de adjacências (estrutura principal)
- **Listas Encadeadas** para adjacências (inserção O(1))
- **Arrays Dinâmicos** para vértices (realocável)
- **Algoritmo Guloso** (Dijkstra sempre escolhe menor distância)
- **Programação Dinâmica** (subestrutura ótima)

---

## 📝 Conclusão

Sistema eficiente que integra:
- **Backend C** → Performance para grafos e algoritmos
- **Frontend Python** → Interface gráfica rica
- **Dois bancos** → Separação entre cálculo (Banco 1) e visualização (Banco 2)

**Resultado**: Rotas sempre ótimas com visualização clara no mapa.

---

**Versão**: 1.0 Resumida  
**Data**: Dezembro 2025
