import pandas as pd

from modulos import *
from Banco import Banco
import logging
import bcrypt


class Cadastros(object):
    
    def __init__(self, cod_linha: int = "", nm_empresa: str = "", nr_contrato: str = "", dt_inicial: str = "",
            dt_limite_repac: str = "", dt_baixa: str = "", vlr_principal: str = "",
            vlr_atualizado_banco: str = "", dt_fluxo_ini: str = "", dt_fluxo_fim: str = "",
            nr_parcela: str = "", vlr_comissao: str = "", dt_comissao: str = "",
            observacao: str = "", agencia: str = "", conta_corrente: str = "", user_insert_reg: str = ""):
        
        self.cod_linha = cod_linha
        self.nm_empresa = nm_empresa
        self.nr_contrato = nr_contrato
        self.dt_inicial = dt_inicial
        self.dt_limite_repac = dt_limite_repac
        self.dt_baixa = dt_baixa
        self.vlr_principal = vlr_principal
        self.vlr_atualizado_banco = vlr_atualizado_banco
        self.dt_fluxo_ini = dt_fluxo_ini
        self.dt_fluxo_fim = dt_fluxo_fim
        self.nr_parcela = nr_parcela
        self.vlr_comissao = vlr_comissao
        self.dt_comissao = dt_comissao
        self.observacao = observacao
        self.agencia = agencia
        self.conta_corrente = conta_corrente
        self.usuario_logado = user_insert_reg
    
    def insertRegistro(self):
        banco = Banco()
        try:
            c = banco.conexao.cursor()
            c.execute(
                "insert into TBL_INFO_COMISSAO (sigla_empresa, nr_contrato, dt_inicial, dt_limite_repac, dt_baixa, "
                "vlr_principal, vlr_atualizado_banco, dt_fluxo_ini, dt_fluxo_fim, nr_parcela, vlr_comissao, "
                "dt_comissao, observacao, agencia,"
                "conta_corrente, user_insert_reg) values ('" + self.nm_empresa + "','" + self.nr_contrato + "', '" + self.dt_inicial +
                "', '" + self.dt_limite_repac + "', '" + self.dt_baixa +
                "', '" + self.vlr_principal + "', '" + self.vlr_atualizado_banco + "','" + self.dt_fluxo_ini +
                "','" + self.dt_fluxo_fim + "', '" + self.nr_parcela + "', '" + self.vlr_comissao + "' ,'" + self.dt_comissao +
                "','" + self.observacao + "','" + self.agencia + "','" + self.conta_corrente + "','" + self.usuario_logado + "' )")
            
            banco.conexao.commit()
            c.close()
            
            return "Contrato cadastrado com sucesso!"
        except:
            return "Ocorreu um erro na inserção do contrato"
    
    def updateRegistro(self):
        banco = Banco()
        try:
            c = banco.conexao.cursor()
            c.execute(
                "update TBL_INFO_COMISSAO set sigla_empresa='" + self.nm_empresa + "', nr_contrato = '" + self.nr_contrato + "', dt_inicial='" + self.dt_inicial + "', dt_limite_repac= '" + self.dt_limite_repac + "', dt_baixa = '" + self.dt_baixa + "', vlr_principal = '" + self.vlr_principal + "', vlr_atualizado_banco = '" +
                self.vlr_atualizado_banco + "', dt_fluxo_fim='" + self.dt_fluxo_fim + "', nr_parcela='" + self.nr_parcela + "', dt_comissao='" + self.dt_comissao + "', observacao='" + self.observacao + "', agencia='" + self.agencia + "', conta_corrente='" + self.conta_corrente + "',dt_fluxo_ini='" + self.dt_fluxo_ini + "', vlr_comissao='" + self.vlr_comissao + "' , user_insert_reg='" + self.usuario_logado + "' where cod_linha = " + self.cod_linha + "")
            
            banco.conexao.commit()
            c.close()
            
            return "Contrato atualizado com sucesso!"
        except Exception as err:
            return f"Ocorreu um erro na alteração do contrato: {err}"
    
    def ExistsCod(self):
        banco = Banco()
        c = banco.conexao.cursor()
        c.execute("SELECT 1 FROM TBL_INFO_COMISSAO WHERE cod_linha = ?", (self.cod_linha,))
        return c.fetchone() is not None
    
    def deleteRegistro(self):
        banco = Banco()
        try:
            c = banco.conexao.cursor()
            c.execute(
                "delete from TBL_INFO_COMISSAO where cod_linha = " + self.cod_linha + " ")
            banco.conexao.commit()
            c.close()
            
            return "Registro excluído com sucesso!"
        except Exception as err:
            return f"Ocorreu um erro na exclusão do registro: {err}"
    
    def selectRegistro(self, nr_contrato):
        banco = Banco()
        try:
            c = banco.conexao.cursor()
            c.execute(
                "select sigla_empresa,nr_contrato,  dt_inicial, dt_limite_repac, dt_baixa,vlr_principal,"
                "vlr_atualizado_banco,dt_fluxo_ini, dt_fluxo_fim,nr_parcela, vlr_comissao, dt_comissao, observacao,"
                "agencia, conta_corrente, user_insert_reg from TBL_INFO_COMISSAO where nr_contrato = " + nr_contrato + "  ")
            
            for linha in c:
                self.nm_empresa = linha[0]
                self.nr_contrato = linha[1]
                self.dt_inicial = linha[2]
                self.dt_limite_repac = linha[3]
                self.dt_baixa = linha[4]
                self.vlr_principal = linha[5]
                self.vlr_atualizado_banco = linha[6]
                self.dt_fluxo_ini = linha[7]
                self.dt_fluxo_fim = linha[8]
                self.nr_parcela = linha[9]
                self.vlr_comissao = linha[10]
                self.dt_comissao = linha[11]
                self.observacao = linha[12]
                self.agencia = linha[13]
                self.conta_corrente = linha[14]
                self.usuario_logado = linha[15]
            
            c.close()
            
            return "Busca feita com sucesso!"
        except Exception as err:
            return f"Ocorreu um erro na busca do contrato: {err}"
    
    def get_existing_registro(self, nr_contrato, nr_parcela):
        banco = Banco()
        c = banco.conexao.cursor()
        
        # Consulta SQL para verificar se o contrato e a parcela já existem
        query = """SELECT * FROM TBL_INFO_COMISSAO WHERE nr_contrato = ? AND nr_parcela = ? """
        c.execute(query, (nr_contrato, nr_parcela))
        existing_user = c.fetchone()
        
        # Fechar a conexão com o banco de dados
        c.close()
        return existing_user
    
    def get_existing_contrato(self, nr_contrato):
        banco = Banco()
        c = banco.conexao.cursor()
        
        # Consulta SQL para verificar se o contrato já existem
        query = """SELECT * FROM TBL_INFO_COMISSAO WHERE nr_contrato = ? """
        c.execute(query, (nr_contrato,))
        existing_contrato = c.fetchone()
        
        # Fechar a conexão com o banco de dados
        c.close()
        return existing_contrato
    
    def ultDtFluxoFim(self, nr_contrato):
        banco = Banco()
        try:
            c = banco.conexao.cursor()
            c.execute("SELECT MAX(DT_FLUXO_FIM) FROM TBL_INFO_COMISSAO WHERE NR_CONTRATO = ?", (nr_contrato,))
            max_dt_fluxo_fim = c.fetchone()[0]
            
            c.close()
            return max_dt_fluxo_fim
        except Exception as e:
            logging.error(f"Erro ao buscar a data mais recente de fluxo fim: {e}")
    
    def ultTxComissao(self, nr_contrato):
        banco = Banco()
        try:
            c = banco.conexao.cursor()
            c.execute("SELECT DISTINCT FI.TAXA FROM TBL_FIANCAS AS FI WHERE FI.BOLETA_ATUAL= "
                      "(SELECT MAX(BOLETA_ATUAL) FROM TBL_FIANCAS WHERE APOLICE_AJUSTADA = ?)", (nr_contrato,))
            utlima_Taxa_Comissao = c.fetchone()[0]
            
            c.close()
            return utlima_Taxa_Comissao
        except Exception as e:
            logging.error(f"Erro ao buscar a Taxa mais recente do contrato: {e}")
    
    def listContrFrame(self, dt_comissao):
        banco = Banco()
        try:
            c = banco.conexao.cursor()
            query = """SELECT DT_COMISSAO,NM_BANCO, NR_CONTRATO, VLR_COMISSAO, PERIODICIDADE, NATUREZA, AGENCIA,
                               CONTA_CORRENTE FROM TBL_INFO_COMISSAO where DT_COMISSAO = ? ORDER BY DT_COMISSAO ASC"""
            c.execute(query, (dt_comissao,))
            lista = c.fetchall()
            from_selct = []
            
            for linha in lista:
                linha = linha
                from_selct.append(linha)
            
            c.close()
            return lista
            logging.info("Concluido com sucesso")
        except ValueError as err:
            logging.error(f"Hoje não foi cadastrado comissão: {err}")
    
    def listEmpresasDay(self, dt_comissao):
        banco = Banco()
        try:
            c = banco.conexao.cursor()
            query = """SELECT DISTINCT SIGLA_EMPRESA FROM TBL_INFO_COMISSAO WHERE DT_COMISSAO = ? """
            c.execute(query, (dt_comissao,))
            lista = [row[0] for row in c.fetchall()]
            
            # from_selct = []
            # for linha in lista:
            #     linha = linha
            #     from_selct.append(linha)
            #
            # coluna = ["Empresa"]
            # df = pd.DataFrame(from_selct, columns=coluna)
            #
            c.close()
            return lista
        except Exception as e:
            logging.error(f"Erro ao buscar a Empresas: {e}")
    
    def relRiscoPeriodo(self, dt_inicio, dt_final):
        banco = Banco()
        try:
            c = banco.conexao.cursor()
            query = """SELECT DISTINCT BOLETA_ATUAL,BOLETA_ANT, SIGLA_EMPRESA, NM_BANCO, NR_CONTRATO, DT_INICIAL,DT_VCTO, DT_BAIXA, VLR_PRINCIPAL,INDEXADOR, VLR_ATUALIZADO_BANCO,
                PERIODICIDADE, COMISSAO, DT_FLUXO_INI, DT_FLUXO_FIM, DIAS_COMISSAO, DIAS_CONTRATO,  NR_PARCELA, DT_COMISSAO,  VLR_COMISSAO, AGENCIA, CONTA_CORRENTE,
                STATUS_FINAL, NATUREZA  FROM TBL_INFO_COMISSAO  WHERE DT_COMISSAO BETWEEN ? AND ?"""
            c.execute(query, (dt_inicio, dt_final,))
            result = c.fetchall()
            df = pd.DataFrame(data=result, columns=['BOLETA_ATUAL','BOLETA_ANT', 'SIGLA_EMPRESA', 'NM_BANCO', 'NR_CONTRATO', 'DT_INICIAL','DT_VCTO', 'DT_BAIXA', 'VLR_PRINCIPAL','INDEXADOR', 'VLR_ATUALIZADO_BANCO',
                'PERIODICIDADE', 'COMISSAO', 'DT_FLUXO_INI', 'DT_FLUXO_FIM', 'DIAS_COMISSAO', 'DIAS_CONTRATO',  'NR_PARCELA', 'DT_COMISSAO',  'VLR_COMISSAO', 'AGENCIA', 'CONTA_CORRENTE',
                'STATUS_FINAL', 'NATUREZA'])
            
            c.close()
            return df
            
            logging.info("Busca realizada!!!")
        except ValueError as err:
            logging.error(f"Erro na busca: {err}")

class Usuarios(object):
    
    def __init__(self, idusuario: int = 0, nome: str = "", re_matricula: str = "", usuario: str = "", email: str = "",
            senha: str = "", tp_acesso: str = ""):
        self.idusuario = idusuario
        self.nome = nome
        self.re_matricula = re_matricula
        self.usuario = usuario
        self.email = email
        self.senha = senha
        self.tp_acesso = tp_acesso
    
    def hash_password(self, password):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password
    
    def insertUser(self):
        banco = Banco()
        try:
            c = banco.conexao.cursor()
            
            # Criptografar a senha antes de atualizar
            self.senha = self.hash_password(self.senha).decode('utf-8')
            
            c.execute(
                "insert into tbl_usuarios(nome, re_matricula, email, senha, tp_acesso) values('" + self.nome + "', '" + self.re_matricula + "', '" + self.email + "' ,'" + self.senha + "','" + self.tp_acesso + "')")
            banco.conexao.commit()
            c.close()
            
            return "Usuário cadastrado com sucesso!"
        except:
            return "Ocorreu um erro na inserção do usuário"
    
    def updateUser(self):
        banco = Banco()
        try:
            c = banco.conexao.cursor()
            
            # Criptografar a senha antes de atualizar
            self.senha = self.hash_password(self.senha).decode('utf-8')
            
            c.execute(
                "update tbl_usuarios set senha = '" + self.senha + "' where re_matricula = '" + self.re_matricula + "'")
            
            banco.conexao.commit()
            logging.info("atualizado com sucesso!")
            
            return True
        except Exception as err:
            logging.error(f"Ocorreu um erro na alteração: {err}")
            return False
        finally:
            c.close()
    
    def deleteUser(self):
        banco = Banco()
        try:
            c = banco.conexao.cursor()
            c.execute("delete from tbl_usuarios where idusuario = " + self.idusuario + " ")
            
            banco.conexao.commit()
            c.close()
            
            return "Usuário excluído com sucesso!"
        except:
            return "Ocorreu um erro na exclusão do usuário"
    
    def selectUser(self, idusuario):
        banco = Banco()
        try:
            c = banco.conexao.cursor()
            c.execute(
                "select idusuario, nome, re_matricula, usuario, email from tbl_usuarios where idusuario = " + idusuario + "  ")
            
            for linha in c:
                self.idusuario = linha[0]
                self.nome = linha[1]
                self.re_matricula = linha[2]
                self.usuario = linha[3]
                self.email = linha[4]
            
            c.close()
            
            return "Busca feita com sucesso!"
        except:
            return "Ocorreu um erro na busca do usuário"
    
    def selectNome(self, re_matricula):
        banco = Banco()
        try:
            c = banco.conexao.cursor()
            query = """select nome, re_matricula, usuario, email from tbl_usuarios where re_matricula = ?"""
            c.execute(query, (re_matricula,))
            
            for linha in c:
                self.nome = linha[0]
                self.re_matricula = linha[1]
                self.usuario = linha[2]
                self.email = linha[3]
            
            c.close()
            
            return "Busca feita com sucesso!"
        except:
            return "Ocorreu um erro na busca do usuário"
    
    def checkUser(self, re_matricula, senha):
        banco = Banco()
        c = banco.conexao.cursor()
        
        query = """SELECT * FROM tbl_usuarios WHERE re_matricula = ? """
        c.execute(query, (re_matricula,))
        existing_user = c.fetchone()
        
        if existing_user and bcrypt.checkpw(senha.encode('utf-8'), existing_user[5].encode('utf-8')):
            return True
        else:
            return False
        
        c.close()
    
    def get_tipo_access(self, re_matricula):
        banco = Banco()
        c = banco.conexao.cursor()
        try:
            query = """SELECT distinct tp_acesso FROM tbl_usuarios WHERE re_matricula = ?"""
            c.execute(query, (re_matricula,))
            result = c.fetchone()
            c.close()
            
            if result:
                if result[0] == 'TRUE':
                    return "ADMIN"
                else:
                    return "NORMAL"
            else:
                return "Acesso não encontrado"
        except Exception as e:
            return f"Erro ao buscar tipo de acesso: {str(e)}"


class EmailOut(object):
    def __int__(self, nm_empresa: str = "", nm_mail: str = "", tp_envio: str = ""):
        self.nm_empresa = nm_empresa
        self.nm_mail = nm_mail
        self.tp_envio = tp_envio
    
    def buscaEmail(self, tp_envio, nm_empresa):
        banco = Banco()
        try:
            c = banco.conexao.cursor()
            query = """SELECT DISTINCT EMAIL FROM TBL_EMAILS WHERE TP_ENVIO = ? AND SIGLA_EMPRESA=?"""
            c.execute(query, (tp_envio, nm_empresa,))
            lista = c.fetchall()
            
            emails_string = ', '.join([email[0] for email in lista])
            
            df = pd.DataFrame(columns=['NOME_EMAIL'])
            df.loc[len(df)] = [emails_string]
            df = re.sub(",", ";", re.sub("[()[\]{}']", "", string=str(list(df.iloc[0]))))
            
            c.close()
            return
            logging.info("Busca realizada")
        except ValueError as err:
            logging.error(f"Erro na busca de e-mail: {err}")


class CrudGrupMail(object):
    def __int__(self, cod_linha: str = "", nm_empresa: str = "", nm_mail: str = "", tp_envio: str = "",
            matricula: str = ""):
        self.cod_linha = cod_linha
        self.nm_empresa = nm_empresa
        self.nm_mail = nm_mail
        self.tp_envio = tp_envio
        self.re_matricula = matricula
    
    def insertRegistro(self):
        banco = Banco()
        try:
            c = banco.conexao.cursor()
            c.execute(
                "insert into TBL_EMAILS (sigla_empresa, email, tp_envio, re_matricula) values ('" + self.nm_empresa + "','" + self.nm_mail + "','" + self.tp_envio + "','" + self.re_matricula + "')")
            
            banco.conexao.commit()
            c.close()
            
            return "Dados cadastrado com sucesso!"
        except:
            return "Ocorreu um erro na inserção."
    
    def updateRegistro(self):
        banco = Banco()
        try:
            c = banco.conexao.cursor()
            c.execute(
                "update TBL_EMAILS set sigla_empresa='" + self.nm_empresa + "', email = '" + self.nm_mail + "', tp_envio='" + self.tp_envio + "' where cod_linha = " + self.cod_linha + "")
            
            banco.conexao.commit()
            c.close()
            
            return "Dados atualizado com sucesso!"
        except Exception as err:
            return f"Ocorreu um erro na alteração: {err}"
    
    def deleteRegistro(self):
        banco = Banco()
        try:
            c = banco.conexao.cursor()
            c.execute(
                "delete from TBL_EMAILS where cod_linha = " + self.cod_linha + " ")
            banco.conexao.commit()
            c.close()
            
            return "Registro excluído com sucesso!"
        except Exception as err:
            return f"Ocorreu um erro na exclusão do registro: {err}"
    
    def selectRegistro(self):
        banco = Banco()
        try:
            c = banco.conexao.cursor()
            c.execute(
                "select sigla_empresa, email, tp_envio from TBL_EMAILS")
            
            for linha in c:
                self.nm_empresa = linha[0]
                self.nm_mail = linha[1]
                self.tp_envio = linha[2]
            
            c.close()
            
            return "Busca feita com sucesso!"
        except Exception as err:
            return f"Ocorreu um erro na busca os dados: {err}"


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# user = Cadastros()
# dado = user.relRiscoPeriodo('14/10/2024', '16/10/2024')
# print(dado)
