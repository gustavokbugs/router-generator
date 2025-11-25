"""
Script de teste simples para verificar a integração Python + C
"""
import ctypes
import os

def resource_path(filename):
    base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, filename)

# Tentar carregar a DLL
dll_path = resource_path('backend\\router.dll')
print(f"Procurando DLL em: {dll_path}")
print(f"DLL existe? {os.path.exists(dll_path)}")

if os.path.exists(dll_path):
    try:
        # Carregar a biblioteca
        lib = ctypes.CDLL(dll_path)
        print("✅ DLL carregada com sucesso!")
        
        # Configurar função get_test_message
        if hasattr(lib, 'get_test_message'):
            lib.get_test_message.argtypes = []
            lib.get_test_message.restype = ctypes.c_char_p
            
            # Chamar a função
            result = lib.get_test_message()
            message = result.decode('utf-8', errors='ignore')
            
            print("\n" + "="*60)
            print("📨 MENSAGEM DO BACKEND C:")
            print("="*60)
            print(message)
            print("="*60)
            print("\n✅ INTEGRAÇÃO PYTHON + C FUNCIONANDO PERFEITAMENTE!")
        else:
            print("❌ Função 'get_test_message' não encontrada na DLL")
            
    except Exception as e:
        print(f"❌ Erro ao carregar ou usar a DLL: {e}")
else:
    print("❌ DLL não encontrada. Execute 'build.bat' primeiro.")

print("\nPressione Enter para continuar...")
input()
