# importando módulo do SQlite
import sqlite3
from acessos import Access


class Banco():

    def __init__(self):
        caminho_BD = Access()
        self.conexao = sqlite3.connect(caminho_BD.pathBD())
