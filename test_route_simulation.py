"""
Simulação de rota com logs detalhados do backend
"""
import ctypes
from ctypes import Structure, POINTER, c_int, c_char_p
import os

# Estrutura de resultado
class ResultadoRota(Structure):
    _fields_ = [
        ("sequencia_ids", POINTER(c_int)),
        ("num_ids", c_int),
        ("distancia_total", c_int)
    ]

# Carregar DLL
dll_path = os.path.join(os.path.dirname(__file__), "backend", "router.dll")
print(f"Carregando DLL: {dll_path}")
lib = ctypes.CDLL(dll_path)

# Configurar funções
lib.calcular_rota.argtypes = [c_int, c_int]
lib.calcular_rota.restype = POINTER(ResultadoRota)

lib.liberar_resultado.argtypes = [POINTER(ResultadoRota)]
lib.liberar_resultado.restype = None

lib.obter_info_vertice.argtypes = [c_int, c_char_p, c_int, c_char_p, c_int, 
                                   POINTER(c_int), POINTER(c_int)]
lib.obter_info_vertice.restype = c_int

def obter_info_ponto(id_ponto):
    """Obtém informações de um ponto"""
    nome = ctypes.create_string_buffer(256)
    categoria = ctypes.create_string_buffer(64)
    x = c_int()
    y = c_int()
    
    resultado = lib.obter_info_vertice(
        id_ponto, nome, 256, categoria, 64, 
        ctypes.byref(x), ctypes.byref(y)
    )
    
    if resultado == 0:
        return {
            'id': id_ponto,
            'nome': nome.value.decode('utf-8', errors='replace'),
            'categoria': categoria.value.decode('utf-8', errors='replace'),
            'x': x.value,
            'y': y.value
        }
    return None

def testar_rota(id_origem, id_destino):
    """Testa uma rota específica"""
    print("\n" + "="*60)
    print(f"TESTE DE ROTA: ID {id_origem} → ID {id_destino}")
    print("="*60)
    
    # Obter informações dos pontos
    info_origem = obter_info_ponto(id_origem)
    info_destino = obter_info_ponto(id_destino)
    
    if info_origem:
        print(f"\n📍 ORIGEM:")
        print(f"   ID: {info_origem['id']}")
        print(f"   Nome: {info_origem['nome']}")
        print(f"   Categoria: {info_origem['categoria']}")
        print(f"   Coordenadas: ({info_origem['x']}, {info_origem['y']})")
    
    if info_destino:
        print(f"\n📍 DESTINO:")
        print(f"   ID: {info_destino['id']}")
        print(f"   Nome: {info_destino['nome']}")
        print(f"   Categoria: {info_destino['categoria']}")
        print(f"   Coordenadas: ({info_destino['x']}, {info_destino['y']})")
    
    print("\n" + "-"*60)
    print("EXECUTANDO DIJKSTRA (veja os logs do C abaixo):")
    print("-"*60 + "\n")
    
    # Calcular rota (os logs do C serão mostrados aqui)
    resultado_ptr = lib.calcular_rota(id_origem, id_destino)
    
    if resultado_ptr:
        resultado = resultado_ptr.contents
        
        print("\n" + "="*60)
        print("RESULTADO FINAL EM PYTHON:")
        print("="*60)
        
        sequencia = []
        for i in range(resultado.num_ids):
            id_ponto = resultado.sequencia_ids[i]
            sequencia.append(id_ponto)
        
        print(f"\n✅ Rota encontrada!")
        print(f"   Sequência de IDs: {sequencia}")
        print(f"   Número de pontos: {resultado.num_ids}")
        print(f"   Distância total: {resultado.distancia_total} metros")
        
        print(f"\n📋 DETALHES DO CAMINHO:")
        for i, id_ponto in enumerate(sequencia):
            info = obter_info_ponto(id_ponto)
            if info:
                print(f"   [{i+1}] ID {id_ponto}: {info['nome']} ({info['categoria']})")
        
        # Liberar memória
        lib.liberar_resultado(resultado_ptr)
    else:
        print("\n❌ ERRO: Não foi possível calcular a rota!")
    
    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*10 + "SIMULAÇÃO DE ROTAS COM LOGS DETALHADOS" + " "*10 + "║")
    print("╚" + "="*58 + "╝")
    
    # TESTE 1: Rota conhecida que funciona (do teste anterior)
    print("\n\n🧪 TESTE 1: Rota Curta (22 → 28)")
    testar_rota(22, 28)
    
    # TESTE 2: Rota mais longa
    print("\n\n🧪 TESTE 2: Rota Longa (22 → 50)")
    testar_rota(22, 50)
    
    # TESTE 3: Rota diferente
    print("\n\n🧪 TESTE 3: Rota Diagonal (25 → 100)")
    testar_rota(25, 100)
    
    print("\n✅ Simulação concluída!\n")
