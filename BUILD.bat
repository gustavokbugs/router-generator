@echo off
REM Script para gerar executável do Sistema de Navegação
REM Automatiza todo o processo de build

echo ========================================
echo   BUILD DO SISTEMA DE NAVEGACAO
echo ========================================
echo.

REM Verifica se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao encontrado!
    echo Instale Python 3.8 ou superior e tente novamente.
    pause
    exit /b 1
)

echo [1/3] Instalando dependencias...
python -m pip install --upgrade pip
python -m pip install -r requirements-build.txt
if errorlevel 1 (
    echo ERRO: Falha ao instalar dependencias
    pause
    exit /b 1
)

echo.
echo [2/3] Verificando DLL C...
if exist "backend\router.dll" (
    echo    DLL encontrada: backend\router.dll
) else (
    echo    AVISO: DLL nao encontrada em backend\router.dll
    echo    Tentando compilar...
    if exist "backend\compile.bat" (
        cd backend
        call compile.bat
        cd ..
    ) else if exist "compile.bat" (
        call compile.bat
    ) else (
        echo    ERRO: Script de compilacao nao encontrado
        echo    Por favor, compile a DLL manualmente antes de continuar
        pause
        exit /b 1
    )
)

echo.
echo [3/3] Gerando executavel...
python build_exe.py

if errorlevel 1 (
    echo.
    echo ERRO: Falha ao gerar executavel
    pause
    exit /b 1
)

echo.
echo ========================================
echo   BUILD CONCLUIDO COM SUCESSO!
echo ========================================
echo.
echo O executavel esta em: dist\SistemaNavegacao.exe
echo Pacote completo em: dist\SistemaNavegacao_Portable\
echo.
pause
