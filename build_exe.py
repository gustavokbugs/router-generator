"""
Script para gerar executável do Sistema de Navegação
Usa PyInstaller para criar um .exe standalone
"""
import os
import sys
import subprocess
import shutil

def check_pyinstaller():
    """Verifica se PyInstaller está instalado"""
    try:
        import PyInstaller
        print("✅ PyInstaller encontrado")
        return True
    except ImportError:
        print("❌ PyInstaller não encontrado")
        print("📦 Instalando PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✅ PyInstaller instalado com sucesso")
        return True

def clean_build_folders():
    """Limpa pastas de builds anteriores"""
    folders = ['build', 'dist', '__pycache__']
    for folder in folders:
        if os.path.exists(folder):
            print(f"🗑️  Removendo pasta {folder}...")
            shutil.rmtree(folder)
    
    # Remove arquivos .spec antigos
    spec_files = [f for f in os.listdir('.') if f.endswith('.spec')]
    for spec in spec_files:
        print(f"🗑️  Removendo {spec}...")
        os.remove(spec)

def build_executable():
    """Gera o executável usando PyInstaller"""
    print("\n" + "="*60)
    print("🚀 GERANDO EXECUTÁVEL DO SISTEMA DE NAVEGAÇÃO")
    print("="*60 + "\n")
    
    # Verifica dependências
    if not check_pyinstaller():
        print("❌ Erro ao instalar PyInstaller")
        return False
    
    # Limpa builds anteriores
    clean_build_folders()
    
    # Configurações do PyInstaller
    cmd = [
        sys.executable,                      # Usa o Python atual
        '-m', 'PyInstaller',                 # Executa PyInstaller como módulo
        '--name=SistemaNavegacao',          # Nome do executável
        '--onefile',                         # Gera um único arquivo
        '--windowed',                        # Sem console (janela limpa)
        '--icon=NONE',                       # Sem ícone personalizado
        '--add-data=perimetro-mapa.png;.',  # Inclui imagem do mapa
        '--add-data=pins.json;.',           # Inclui dados dos pins
        '--add-data=assets;assets',         # Inclui pasta de ícones
        '--add-data=backend/router.dll;backend',  # Inclui DLL C
        '--hidden-import=PIL._tkinter_finder',    # Import oculto do Pillow
        '--collect-all=customtkinter',       # Inclui todos os arquivos do customtkinter
        '--collect-all=PIL',                 # Inclui todos os arquivos do PIL
        '--noconfirm',                       # Não pede confirmação
        'main.py'                            # Arquivo principal
    ]
    
    print("📝 Comando PyInstaller:")
    print(" ".join(cmd))
    print("\n⏳ Compilando... (pode demorar alguns minutos)\n")
    
    try:
        # Executa PyInstaller
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        print("\n" + "="*60)
        print("✅ EXECUTÁVEL GERADO COM SUCESSO!")
        print("="*60)
        print(f"\n📂 Localização: dist/SistemaNavegacao.exe")
        print(f"📊 Tamanho: {os.path.getsize('dist/SistemaNavegacao.exe') / (1024*1024):.1f} MB")
        print("\n💡 O executável é standalone - pode ser copiado para outros computadores")
        print("   sem precisar instalar Python ou dependências!")
        print("\n⚠️  Certifique-se de que os seguintes arquivos estão incluídos:")
        print("   - perimetro-mapa.png")
        print("   - pins.json")
        print("   - backend/router.dll")
        print("   - assets/ (pasta com ícones)")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print("\n❌ ERRO ao gerar executável:")
        print(e.stderr)
        return False
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        return False

def create_dist_package():
    """Cria pacote completo para distribuição"""
    if not os.path.exists('dist/SistemaNavegacao.exe'):
        print("❌ Executável não encontrado. Execute build_executable() primeiro.")
        return
    
    print("\n📦 Criando pacote de distribuição...")
    
    # Cria pasta de distribuição
    dist_folder = 'dist/SistemaNavegacao_Portable'
    os.makedirs(dist_folder, exist_ok=True)
    
    # Copia executável
    shutil.copy('dist/SistemaNavegacao.exe', dist_folder)
    
    # Copia arquivos necessários
    files_to_copy = [
        'perimetro-mapa.png',
        'pins.json',
        'README.md'
    ]
    
    for file in files_to_copy:
        if os.path.exists(file):
            shutil.copy(file, dist_folder)
            print(f"  ✅ {file}")
    
    # Copia pastas
    if os.path.exists('assets'):
        shutil.copytree('assets', os.path.join(dist_folder, 'assets'), dirs_exist_ok=True)
        print(f"  ✅ assets/")
    
    if os.path.exists('backend/router.dll'):
        os.makedirs(os.path.join(dist_folder, 'backend'), exist_ok=True)
        shutil.copy('backend/router.dll', os.path.join(dist_folder, 'backend'))
        print(f"  ✅ backend/router.dll")
    
    # Cria arquivo LEIA-ME
    with open(os.path.join(dist_folder, 'LEIA-ME.txt'), 'w', encoding='utf-8') as f:
        f.write("""
========================================
   SISTEMA DE NAVEGAÇÃO - GUIA RÁPIDO
========================================

📍 COMO USAR:
1. Execute SistemaNavegacao.exe
2. Selecione um ponto de origem no mapa ou na lista
3. Selecione um ponto de destino
4. Clique em "🚀 Calcular Rota"
5. A rota será desenhada no mapa com a distância total

🖱️ CONTROLES:
- Zoom In/Out: Use os botões na interface
- Arrastar mapa: Ctrl + Botão esquerdo do mouse
- Buscar pontos: Digite no campo de busca

📋 REQUISITOS:
- Windows 7 ou superior
- Nenhuma instalação adicional necessária

⚠️ IMPORTANTE:
Mantenha todos os arquivos na mesma pasta:
- SistemaNavegacao.exe
- perimetro-mapa.png
- pins.json
- backend/router.dll
- assets/ (pasta com ícones)

🐛 PROBLEMAS?
Se o programa não iniciar, verifique se:
1. Todos os arquivos estão presentes
2. O antivírus não está bloqueando o executável
3. Você tem permissões de execução na pasta

Versão: 1.0
""")
    
    print(f"\n✅ Pacote criado em: {dist_folder}")
    print(f"📦 Você pode compactar esta pasta e distribuir!")

if __name__ == "__main__":
    print("\n" + "🎯 "*20)
    print("      BUILD SCRIPT - SISTEMA DE NAVEGAÇÃO")
    print("🎯 "*20 + "\n")
    
    if build_executable():
        print("\n" + "="*60)
        create_dist_package()
        print("\n" + "="*60)
        print("🎉 PROCESSO CONCLUÍDO!")
        print("="*60 + "\n")
    else:
        print("\n❌ Falha no processo de build")
        sys.exit(1)
