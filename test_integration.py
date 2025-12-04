"""
Script de teste para verificar a integração do sistema
"""
import os
import json
import sys

def test_pins_json():
    """Testa se pins.json existe e tem estrutura correta"""
    print("🧪 Testando pins.json...")
    
    if not os.path.exists('pins.json'):
        print("   ❌ pins.json não encontrado!")
        return False
    
    try:
        with open('pins.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if 'pins' not in data:
            print("   ❌ Estrutura incorreta - falta chave 'pins'")
            return False
        
        pins = data['pins']
        print(f"   ✅ {len(pins)} pins carregados")
        
        # Verificar estrutura de alguns pins
        for i, pin in enumerate(pins[:3]):
            if 'id' in pin and 'x' in pin and 'y' in pin:
                print(f"   ✅ Pin {pin['id']}: ({pin['x']}, {pin['y']})")
            else:
                print(f"   ❌ Pin {i} tem estrutura incorreta")
                return False
        
        return True
    except Exception as e:
        print(f"   ❌ Erro ao carregar pins.json: {e}")
        return False

def test_assets():
    """Testa se pasta assets existe e contém ícones"""
    print("\n🧪 Testando assets/...")
    
    if not os.path.exists('assets'):
        print("   ❌ Pasta assets não encontrada!")
        return False
    
    expected_icons = [
        'Restaurante.png', 'Bar.png', 'Banco.png', 'Hotel.png',
        'Cafeteria.png', 'Adega.png', 'Comércio.png', 'Saude.png'
    ]
    
    found = 0
    for icon in expected_icons:
        path = os.path.join('assets', icon)
        if os.path.exists(path):
            found += 1
            print(f"   ✅ {icon}")
        else:
            print(f"   ⚠️  {icon} não encontrado")
    
    print(f"   📊 {found}/{len(expected_icons)} ícones principais encontrados")
    return found > 0

def test_backend():
    """Testa se backend C está compilado"""
    print("\n🧪 Testando backend C...")
    
    dll_paths = [
        'backend\\router.dll',
        'backend\\librouter.dll',
        'router.dll'
    ]
    
    found = False
    for path in dll_paths:
        if os.path.exists(path):
            print(f"   ✅ {path} encontrado")
            found = True
            break
    
    if not found:
        print("   ⚠️  DLL não encontrada - backend precisa ser compilado")
        print("   💡 Execute: cd backend && compile.bat")
    
    return found

def test_main_py():
    """Testa se main.py existe e tem estrutura correta"""
    print("\n🧪 Testando main.py...")
    
    if not os.path.exists('main.py'):
        print("   ❌ main.py não encontrado!")
        return False
    
    try:
        with open('main.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verificar se tem as classes corretas
        if 'class ModernMapApp' in content:
            print("   ✅ Classe ModernMapApp encontrada")
        else:
            print("   ❌ Classe ModernMapApp não encontrada")
            return False
        
        # Verificar se NÃO tem StartScreen
        if 'class StartScreen' in content:
            print("   ⚠️  Classe StartScreen ainda presente (deveria ser removida)")
        else:
            print("   ✅ StartScreen removida corretamente")
        
        # Verificar carregamento de pins.json
        if '_load_pins' in content:
            print("   ✅ Método _load_pins encontrado")
        else:
            print("   ❌ Método _load_pins não encontrado")
            return False
        
        # Verificar sistema de ícones
        if '_draw_icon' in content and 'CATEGORIA_ICONE' in content:
            print("   ✅ Sistema de ícones implementado")
        else:
            print("   ❌ Sistema de ícones não encontrado")
            return False
        
        return True
    except Exception as e:
        print(f"   ❌ Erro ao ler main.py: {e}")
        return False

def test_map_image():
    """Testa se imagem do mapa existe"""
    print("\n🧪 Testando imagem do mapa...")
    
    if os.path.exists('perimetro-mapa.png'):
        print("   ✅ perimetro-mapa.png encontrado")
        return True
    else:
        print("   ❌ perimetro-mapa.png não encontrado!")
        return False

def main():
    """Executa todos os testes"""
    print("=" * 50)
    print("🧪 TESTES DE INTEGRAÇÃO DO SISTEMA")
    print("=" * 50)
    
    results = {
        'pins.json': test_pins_json(),
        'assets': test_assets(),
        'backend': test_backend(),
        'main.py': test_main_py(),
        'mapa': test_map_image()
    }
    
    print("\n" + "=" * 50)
    print("📊 RESUMO DOS TESTES")
    print("=" * 50)
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    
    for name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print(f"\n📈 Total: {passed}/{total} testes passaram")
    
    if passed == total:
        print("\n🎉 Todos os testes passaram! Sistema pronto para uso.")
        print("\n💡 Execute: python main.py")
    else:
        print("\n⚠️  Alguns testes falharam. Verifique os erros acima.")
    
    return passed == total

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
