# Sistema de Geração de Rotas para Pontos de Entretenimento em Santa Cruz do Sul

Este projeto acadêmico consiste em um sistema de geração de rotas para pontos de entretenimento no centro de Santa Cruz do Sul. O sistema possui uma interface gráfica moderna desenvolvida em Python, que se integra com uma biblioteca em C para o cálculo das rotas.

---

## Funcionalidades

- **Tela Inicial Interativa**: Permite escolher entre modos de rota com múltiplos destinos ou apenas um destino.
- **Seleção Visual no Mapa**: O usuário pode clicar diretamente no mapa para marcar a origem e os destinos, ou utilizar botões de pontos turísticos pré-definidos.
- **Pontos Turísticos Pré-definidos**: Inclui pontos de interesse no centro de Santa Cruz do Sul, com coordenadas fixas.
- **Interface Moderna e Intuitiva**: Desenvolvida com CustomTkinter para uma experiência de usuário agradável.
- **Controles de Mapa**: Zoom e arrastar para navegar pelo mapa.

---

## Tecnologias Utilizadas

- **Python 3.x** — Interface gráfica e lógica principal
- **CustomTkinter** — UI moderna
- **Pillow (PIL)** — Manipulação do mapa
- **C** — Biblioteca de rota
- **ctypes** — Integração Python ↔ C

---

## Pré-requisitos e Instalação

### Dependências Python

```bash
pip install customtkinter pillow
```

---

## Biblioteca C

A biblioteca deve expor as funções:

```c
// Função de teste que retorna uma mensagem
const char* get_test_message();

// Função que gera rota entre dois pontos
int generate_route(int sx, int sy, int ex, int ey, char* outbuf, int buflen);
```

Formato da saída de `generate_route`:

```
x,y
x,y
...
```

### Compilação

#### Windows (usando MinGW):

```bash
# Execute o script de compilação
build.bat

# Ou compile manualmente:
cd backend
gcc -c grafo_db.c -o grafo_db.o
gcc -shared -o router.dll main.c grafo_db.o -Wl,--out-implib,librouter.a
```

#### Linux:

```bash
cd backend
gcc -c grafo_db.c -o grafo_db.o
gcc -shared -fPIC -o librouter.so main.c grafo_db.o
```

#### macOS:

```bash
cd backend
gcc -c grafo_db.c -o grafo_db.o
gcc -shared -fPIC -o librouter.dylib main.c grafo_db.o
```

---

## Como Usar

### 1. Execute o programa

```bash
python main.py
```

### 2. Tela Inicial

Escolha entre múltiplos destinos ou destino único.

### 3. Seleção

- Clique em **Marcar Origem**, depois no mapa.
- Clique em **Marcar Destino**, depois no mapa.
- Ou selecione pelos **pontos turísticos** pré-definidos.

### 4. Testar integração C

Clique em **🔌 Testar Backend C** para verificar se a DLL está funcionando corretamente.

### 5. Gerar rota

Clique em **Gerar Rota**.

### 6. Controles de Mapa

- Zoom: + / -
- Arrastar com o mouse
- Centralizar: botão próprio
- Ctrl + arrastar: navegação suave

### 6. Limpar / Voltar

- **Limpar Tudo** redefine o mapa e rotas
- **← Voltar** retorna à tela inicial

---

## Estrutura do Projeto

```
projeto-santa-cruz/
│
├── main.py
├── router.dll
├── librouter.so
├── librouter.dylib
├── perimetro-mapa.png
└── README.md
```

---

## Integração Python–C

O arquivo `main.py` utiliza `ctypes` para:

- Carregar a biblioteca C
- Converter os tipos
- Ler a string resultante da rota

Se a biblioteca C não existir, usa uma rota de fallback em linha reta.

---

## Melhorias Futuras

- Implementar A*, Dijkstra, etc
- Mais pontos turísticos
- Armazenar pontos em arquivos externos
- Visualização aprimorada (setas, distância)
- Uso de mapas interativos (OSM)

---

## Observações

- Coordenadas dos pontos turísticos devem ser ajustadas
- O mapa PNG deve cobrir toda a região usada no cálculo

---

# 🗺️ Sistema de Geração de Rotas — Centro de Santa Cruz do Sul

Parte expandida do README com informações detalhadas e versão descritiva.

---

## 📋 Descrição do Projeto

Sistema gráfico interativo para geração de rotas no centro de Santa Cruz do Sul, combinando:

- Interface Python (CustomTkinter)
- Algoritmos de rota em C
- Mapa interativo
- Suporte a múltiplos destinos

---

## ✨ Funcionalidades

### 🎯 Modos
- Rota com múltiplos destinos
- Rota direta para um destino

### 🗾 Interface
- Mapa interativo com zoom
- Arrastar
- Rotas coloridas
- Marcadores de origem e destino

### 📍 Pontos mapeados

- Teatro Municipal  
- Casa de Cultura  
- Museu Municipal  
- Biblioteca Pública  
- Restaurantes  
- Cafeterias  
- Praças  
- Parques  
- Áreas comerciais  

---

## 🛠️ Tecnologias

### Backend
- Python 3.8+
- Biblioteca em C
- ctypes

### GUI
- CustomTkinter
- Tkinter
- Pillow

### Cross-platform
- Windows (.dll)
- Linux (.so)
- macOS (.dylib)

---

## 📥 Instalação

### Dependências

```bash
pip install customtkinter pillow
```

### Estrutura

```
projeto-rotas-scs/
├── main.py
├── router.dll
├── librouter.so
├── librouter.dylib
├── centro-scs-mapa.png
└── README.md
```

### Compilação

```bash
gcc -shared -o router.dll router.c       # Windows
gcc -shared -fPIC -o librouter.so router.c   # Linux
gcc -shared -fPIC -o librouter.dylib router.c # macOS
```

---

## 🎮 Modo de Uso

1. `python main.py`
2. Escolher modo de rota
3. Selecionar origem
4. Selecionar destinos
5. Clicar em **Gerar Rota**
6. Visualizar no mapa

---

## 🔧 Integração com C

Função principal:

```c
int generate_route(int start_x, int start_y, int end_x, int end_y, char* output_buffer, int buffer_length);
```

Formato:

```
x1,y1
x2,y2
...
```

Fallback caso a biblioteca não exista → linha reta.

---

## 📊 Características Técnicas

- Resposta rápida  
- Baixo consumo de memória  
- Múltiplos destinos  
- Mapa baseado em coordenadas reais  

---

## 🐛 Troubleshooting

### Biblioteca C não encontrada
- Verifique o nome do arquivo
- Verifique arquitetura (32/64 bits)

### Mapa não carrega
- Confirme se `centro-scs-mapa.png` existe

### Interface não abre
- Instale dependências
- Use Python 3.8+

---

## 🔄 Extensibilidade

Adicionar pontos:

```python
self.tourist_spots = {
    "Novo Ponto": (x, y),
    ...
}
```

Trocar mapa → substitua o PNG mantendo proporções.

---

## 👥 Equipe

- Gustavo Bugs
- Pedro Henrique Hermes
- Rodrigo Kothe Sanchez
- Orientador: Daniela Bagatini

---

## 📄 Licença

Projeto acadêmico da UNISC, sem licença específica.

