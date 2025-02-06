from modulos import *

# Obtém o nome do usuário da máquina
username = os.getlogin()


class Access:
    def pathIcone(self) -> str:
        caminho_icone = os.path.join(os.path.join(os.path.dirname(os.path.realpath(__name__)), "Icones\\"),
                                     "monitoramento.png")
        return caminho_icone
    
    def pathBD(self) -> str:
        caminho_rede = r"\\BRTSSISP003\BBB0137$\\Mesa Operacoes\13.BancoDados\MesaOpAnalytcs.db"
        return caminho_rede
    
    def pathKnime(self) -> bool:
        caminho_local = r"C:\Program Files\KNIME"
        return_code = os.path.exists(caminho_local)
        return return_code
    
    def userDownloads(self) -> str:
        caminho_local = fr"C:\Users\{username}"
        return_caminho = os.path.join(caminho_local, "Downloads")
        return return_caminho
    
    def redeFianca(self) -> str:
        caminho_rede_fiancas = r"\\BRTSSISP003\BBB0137$\\Mesa Operacoes\1.Garantias_Financeiras\1.Fianca_Bancaria\06. Controle"
        return caminho_rede_fiancas
