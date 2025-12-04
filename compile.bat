@echo off
setlocal

echo ========================================
echo Compilando com MSYS2 GCC (64-bit)
echo ========================================
echo.

REM Adicionar MSYS2 ao PATH temporariamente
set "PATH=C:\msys64\ucrt64\bin;%PATH%"

REM Verificar GCC
gcc --version | findstr "gcc"
echo.

cd backend

echo Limpando...
if exist *.o del /Q *.o
if exist router.dll del /Q router.dll

echo.
echo [1/6] grafo.c
gcc -std=c99 -c grafo.c -o grafo.o || goto erro
echo   OK

echo [2/6] grafo_data.c
gcc -std=c99 -c grafo_data.c -o grafo_data.o || goto erro
echo   OK

echo [3/6] grafo_db.c
gcc -std=c99 -c grafo_db.c -o grafo_db.o || goto erro
echo   OK

echo [4/6] grafo_algoritmos.c
gcc -std=c99 -c grafo_algoritmos.c -o grafo_algoritmos.o || goto erro
echo   OK

echo [5/6] main.c
gcc -std=c99 -c main.c -o main.o || goto erro
echo   OK

echo [6/6] Gerando DLL
gcc -shared -o router.dll main.o grafo.o grafo_data.o grafo_db.o grafo_algoritmos.o || goto erro
echo   OK

cd ..

echo.
echo ========================================
echo SUCESSO! DLL 64-bit gerada!
echo ========================================
echo.
dir backend\router.dll | findstr "router.dll"
echo.

echo Testando integracao Python + C...
echo.
python test_integration.py

goto fim

:erro
cd ..
echo.
echo ========================================
echo ERRO na compilacao!
echo ========================================
echo.

:fim
pause
endlocal
