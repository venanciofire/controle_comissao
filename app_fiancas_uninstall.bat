@echo off
setlocal

REM Defina o caminho da pasta e do atalho
set "pasta=C:\ComissaoFiancas\"
set "atalho=C:\ComissaoFiancas\AppComissaoFiancas\ComissaoFiancas.lnk"

REM Mensagem de confirmação
echo Tem certeza que deseja deletar o App de Comissao? (S/N)
set /p confirmacao=

if /i "%confirmacao%"=="S" (
    cd \
    echo Deletando a pasta ...
    rmdir /s /q "%pasta%"
    del "%atalho%"
    echo Operacao concluida.
) else (
    echo Operacao cancelada.
)

endlocal
pause