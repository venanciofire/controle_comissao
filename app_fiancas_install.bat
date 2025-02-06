@echo off

:: Verifica se o Python esta instalado
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python nao esta instalado. Por favor, instale o Python na Central de Software e tente novamente.
    pause
    exit /b 1
)
echo Aguarde.....
echo.

cd C:\ComissaoFiancas\AppComissaoFiancas

:: Cria o ambiente virtual
python -m venv venv
if %errorlevel% neq 0 (
    echo Falha ao criar o ambiente virtual.
    exit /b 1
)
echo Criando ambiente virtual, aguarde.....
echo.

:: Ativa o ambiente virtual
call venv\Scripts\activate
echo Ativando ambiente virtual, aguarde.....
echo.

:: Instala as dependências do requirements.txt
if exist requirements.txt (
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo Falha ao instalar as dependências.
        exit /b 1
    )
) else (
    echo O arquivo requirements.txt não foi encontrado.
    exit /b 1
)

echo Ambiente configurado com sucesso!

REM Instala as dependencias
REM pip install -r requirements.txt

REM Mensagem de conclusao
REM echo Ambiente configurado e dependencias instaladas.

pause
