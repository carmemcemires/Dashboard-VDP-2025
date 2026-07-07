@echo off
cd /d "%~dp0"

echo.
echo Iniciando o Dashboard VDP ALECE 2025...
echo.

where python >nul 2>nul
if errorlevel 1 (
    echo Python nao encontrado.
    echo.
    echo Instale o Python em https://www.python.org/downloads/
    echo Durante a instalacao, marque a opcao "Add Python to PATH".
    echo Depois execute este arquivo novamente.
    echo.
    pause
    exit /b 1
)

python -m pip --version >nul 2>nul
if errorlevel 1 (
    echo O Python foi encontrado, mas o pip nao esta disponivel.
    echo Tentando preparar o pip automaticamente...
    python -m ensurepip --upgrade
)

python -m pip --version >nul 2>nul
if errorlevel 1 (
    echo.
    echo Ainda nao foi possivel encontrar o pip.
    echo Reinstale o Python marcando as opcoes "pip" e "Add Python to PATH".
    echo.
    pause
    exit /b 1
)

echo Instalando/verificando bibliotecas necessarias...
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo Nao foi possivel instalar as bibliotecas.
    echo Verifique sua conexao com a internet e tente novamente.
    echo.
    pause
    exit /b 1
)

echo.
echo Abrindo o dashboard no navegador...
echo Se o navegador nao abrir sozinho, acesse: http://localhost:8501
echo.

python -m streamlit run app.py

pause
