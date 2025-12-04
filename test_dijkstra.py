"""
Script de teste para o algoritmo Dijkstra
"""
import ctypes
import os

def resource_path(filename):
    base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, filename)

def test_dijkstra():
    print("=" * 60)
    print("🧪 TESTE DO ALGORITMO DIJKSTRA")
    print("=" * 60)
    
    # Carregar DLL
    dll_path = resource_path('backend\\router.dll')
    
    if not os.path.exists(dll_path):
        print(f"❌ DLL não encontrada: {dll_path}")
        return False
    
    print(f"✅ DLL encontrada: {dll_path}")
    
    try:
        lib = ctypes.CDLL(dll_path)
        print("✅ DLL carregada com sucesso")
    except Exception as e:
        print(f"❌ Erro ao carregar DLL: {e}")
        return False
    
    # Configurar estrutura ResultadoRota
    class ResultadoRota(ctypes.Structure):
        _fields_ = [
            ("sequencia_ids", ctypes.POINTER(ctypes.c_int)),
            ("num_ids", ctypes.c_int),
            ("distancia_total", ctypes.c_int)
        ]
    
    # Configurar funções
    try:
        lib.calcular_rota.argtypes = [ctypes.c_int, ctypes.c_int]
        lib.calcular_rota.restype = ctypes.POINTER(ResultadoRota)
        
        lib.liberar_resultado.argtypes = [ctypes.POINTER(ResultadoRota)]
        lib.liberar_resultado.restype = None
        
        lib.obter_info_vertice.argtypes = [
            ctypes.c_int,
            ctypes.c_char_p, ctypes.c_int,
            ctypes.c_char_p, ctypes.c_int,
            ctypes.POINTER(ctypes.c_int),
            ctypes.POINTER(ctypes.c_int)
        ]
        lib.obter_info_vertice.restype = ctypes.c_int
        
        print("✅ Funções configuradas")
    except Exception as e:
        print(f"❌ Erro ao configurar funções: {e}")
        return False
    
    # Teste 1: Rota conhecida (Pastelaria -> McDonald's)
    print("\n" + "-" * 60)
    print("📋 TESTE 1: Rota Pastelaria (ID 22) → McDonald's (ID 114)")
    print("-" * 60)
    
    try:
        resultado_ptr = lib.calcular_rota(22, 114)
        
        if not resultado_ptr:
            print("❌ calcular_rota retornou NULL")
            return False
        
        resultado = resultado_ptr.contents
        
        print(f"✅ Rota calculada!")
        print(f"   📏 Distância total: {resultado.distancia_total} metros")
        print(f"   🛤️  Número de vértices: {resultado.num_ids}")
        
        # Extrair sequência de IDs
        sequencia = []
        for i in range(resultado.num_ids):
            sequencia.append(resultado.sequencia_ids[i])
        
        print(f"   🗺️  Caminho: {' → '.join(map(str, sequencia))}")
        
        # Obter informações de alguns pontos
        print("\n   📍 Detalhes dos pontos:")
        for ponto_id in [sequencia[0], sequencia[-1]]:
            nome_buf = ctypes.create_string_buffer(100)
            cat_buf = ctypes.create_string_buffer(50)
            x_val = ctypes.c_int()
            y_val = ctypes.c_int()
            
            result = lib.obter_info_vertice(
                ponto_id,
                nome_buf, 100,
                cat_buf, 50,
                ctypes.byref(x_val),
                ctypes.byref(y_val)
            )
            
            if result == 0:
                nome = nome_buf.value.decode('utf-8')
                categoria = cat_buf.value.decode('utf-8')
                print(f"      ID {ponto_id}: {nome} ({categoria}) - ({x_val.value}, {y_val.value})")
        
        # Liberar memória
        lib.liberar_resultado(resultado_ptr)
        print("   ✅ Memória liberada")
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Teste 2: Rota curta
    print("\n" + "-" * 60)
    print("📋 TESTE 2: Rota curta (ID 22 → ID 23)")
    print("-" * 60)
    
    try:
        resultado_ptr = lib.calcular_rota(22, 23)
        
        if not resultado_ptr:
            print("❌ Rota não encontrada")
        else:
            resultado = resultado_ptr.contents
            print(f"✅ Rota calculada!")
            print(f"   📏 Distância: {resultado.distancia_total} metros")
            print(f"   🛤️  Vértices: {resultado.num_ids}")
            
            sequencia = [resultado.sequencia_ids[i] for i in range(resultado.num_ids)]
            print(f"   🗺️  Caminho: {' → '.join(map(str, sequencia))}")
            
            lib.liberar_resultado(resultado_ptr)
            print("   ✅ Memória liberada")
    
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    # Teste 3: Rota inválida (mesma origem e destino)
    print("\n" + "-" * 60)
    print("📋 TESTE 3: Rota inválida (ID 22 → ID 22)")
    print("-" * 60)
    
    try:
        resultado_ptr = lib.calcular_rota(22, 22)
        
        if not resultado_ptr:
            print("✅ Corretamente retornou NULL para rota trivial")
        else:
            print("⚠️  Retornou resultado para rota trivial (não esperado)")
            lib.liberar_resultado(resultado_ptr)
    
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    print("\n" + "=" * 60)
    print("✅ TODOS OS TESTES CONCLUÍDOS!")
    print("=" * 60)
    
    return True

if __name__ == '__main__':
    test_dijkstra()
