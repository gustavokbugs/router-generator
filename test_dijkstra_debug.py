import os
import sys
import ctypes
from ctypes import Structure, POINTER, c_int, c_char_p, byref, create_string_buffer, cdll

# Estrutura ResultadoRota
class ResultadoRota(Structure):
    _fields_ = [
        ("sequencia_ids", POINTER(c_int)),
        ("num_ids", c_int),
        ("distancia_total", c_int)
    ]

print("=" * 60)
print("🧪 TESTE DEBUG DIJKSTRA")
print("=" * 60)

# Carregar DLL
dll_path = os.path.join('backend', 'router.dll')
print(f"\n1. Carregando DLL: {dll_path}")

if not os.path.exists(dll_path):
    print(f"❌ DLL não encontrada!")
    sys.exit(1)

lib = cdll.LoadLibrary(dll_path)
print("✅ DLL carregada")

# Configurar funções
print("\n2. Configurando funções...")

# calcular_rota
lib.calcular_rota.argtypes = [c_int, c_int]
lib.calcular_rota.restype = POINTER(ResultadoRota)

# liberar_resultado
lib.liberar_resultado.argtypes = [POINTER(ResultadoRota)]
lib.liberar_resultado.restype = None

print("✅ Funções configuradas")

# Testar com IDs conhecidos
id_origem = 22
id_destino = 28

print(f"\n3. Testando rota: {id_origem} → {id_destino}")
print(f"   Tipo id_origem: {type(id_origem)}")
print(f"   Tipo id_destino: {type(id_destino)}")

# Chamar função
print("\n4. Chamando calcular_rota()...")
resultado_ptr = lib.calcular_rota(id_origem, id_destino)

print(f"   Ponteiro retornado: {resultado_ptr}")
print(f"   Ponteiro é NULL? {not bool(resultado_ptr)}")

if not resultado_ptr:
    print("❌ Função retornou NULL")
    sys.exit(1)

print("✅ Ponteiro válido")

# Acessar estrutura
print("\n5. Acessando estrutura ResultadoRota...")
resultado = resultado_ptr.contents

print(f"   num_ids: {resultado.num_ids}")
print(f"   distancia_total: {resultado.distancia_total}")
print(f"   sequencia_ids pointer: {resultado.sequencia_ids}")

# Extrair IDs
print("\n6. Extraindo sequência de IDs...")
sequencia = []

if resultado.num_ids > 0 and resultado.num_ids < 1000:  # Sanidade
    for i in range(resultado.num_ids):
        id_val = resultado.sequencia_ids[i]
        print(f"   [{i}] = {id_val}")
        sequencia.append(id_val)
else:
    print(f"❌ num_ids inválido: {resultado.num_ids}")

# Liberar memória
print("\n7. Liberando memória...")
lib.liberar_resultado(resultado_ptr)
print("✅ Memória liberada")

print("\n" + "=" * 60)
print("📊 RESULTADO FINAL:")
print("=" * 60)
print(f"Origem: {id_origem}")
print(f"Destino: {id_destino}")
print(f"Pontos no caminho: {len(sequencia)}")
print(f"Sequência: {sequencia}")
print(f"Distância: {resultado.distancia_total} metros")
print("=" * 60)
