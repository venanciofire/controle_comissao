echo off
cls
echo Abrindo Sistema, aguarde....
echo.

REM Ativa o ambiente virtual
cd C:\ComissaoFiancas\AppComissaoFiancas
call venv\Scripts\activate
echo Sistema Aberto....
echo.

REM abrir o App Comissão Fianças
py app.py


deactivate