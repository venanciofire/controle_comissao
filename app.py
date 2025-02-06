from modulos import *

ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

# Obtém o nome do usuário da máquina
username = os.getlogin()
data_hoje = datetime.datetime.today().strftime('%d_%m_%Y')


class Relatorios:
    
    def __init__(self):
        self.dt_final_entry = None
        self.dt_ini_entry = None
        self.can = None
        self.banco_entry = None
        self.empresa_entry = None
        self.pagTitulo = None
        self.listacomissao = None
        self.data_comissa_entry = None
    
    def limpaTelaTopLevel(self):
        self.data_comissa_entry.delete(0, END)
        self.banco_entry.delete(0, END)
        self.empresa_entry.delete(0, END)
        self.banco_entry.delete(0, END)
        self.listacomissao.delete(*self.listacomissao.get_children())
    
    def limpaTelaTopLevelExt(self):
        self.dt_ini_entry.delete(0, END)
        self.dt_final_entry.delete(0, END)
    
    def geraRelatComissao(self):
        banco = Banco()
        acessocaminho = Access()
        data_comissao = self.data_comissa_entry.get()
        nome_empresa = self.empresa_entry.get()
        nome_banco = self.banco_entry.get()
        caminho_fiancas = acessocaminho.redeFianca()
        # nome_empresa = nome_empresa.upper()
        # nome_banco = nome_banco.capitalize()
        
        try:
            caminho_file = os.path.join(os.path.join(caminho_fiancas, "04_RelatorioPDF\\"),
                                        f"comissao_{nome_empresa}_{nome_banco}_{data_hoje}.pdf")
        except:
            messagebox.showerror(self.pagTitulo,
                                 f"Você não tem acesso a rede {caminho_fiancas}, solicite acesso ao seu SAU")
        
        # caminho_file = os.path.join(os.path.join(os.path.dirname(os.path.realpath(__name__)), "RelatorioPDF\\"), f"comissao_{nome_empresa}_{nome_banco}_{data_hoje}.pdf")
        
        if not data_comissao or not nome_empresa or not nome_banco:
            messagebox.showwarning(self.pagTitulo, "Preencha todos os campos para gerar o PDF")
            return
        
        self.can = canvas.Canvas(caminho_file, pagesize=letter)
        width, height = letter
        rows_per_page = 4  # Número de linhas por página
        
        try:
            c = banco.conexao.cursor()
            query = """SELECT DT_COMISSAO,NM_BANCO, NR_CONTRATO, VLR_COMISSAO, PERIODICIDADE, NATUREZA, AGENCIA,
                                   CONTA_CORRENTE FROM TBL_INFO_COMISSAO where DT_COMISSAO = ? AND NM_BANCO=? AND SIGLA_EMPRESA=? ORDER BY DT_COMISSAO ASC"""
            
            lista = c.execute(query, (data_comissao, nome_banco, nome_empresa,))
            lista = pd.DataFrame(lista)
            total_pag = (len(lista) // rows_per_page) + 1
            
            if len(lista) < 1:
                return
            
            for page in range(total_pag):
                self.can.setFont("Helvetica-Bold", 16)
                self.can.drawString(230, height - 40, "Aviso de Comissão")
                
                # Número da página
                self.can.setFont("Helvetica", 8)
                self.can.drawString(width - 100, height - 40, f"Página {page + 1} de {total_pag}")
                
                y = 700
                x = 50
                start_index = page * rows_per_page
                end_index = start_index + rows_per_page
                
                for idx, row in lista.iloc[start_index:end_index].iterrows():
                    self.can.setFont("Helvetica-Bold", 12)
                    self.can.drawString(x, y, "Data: ")
                    self.can.drawString(x, y - 20, "Banco: ")
                    self.can.drawString(x, y - 40, "nª Contrato: ")
                    self.can.drawString(x, y - 60, "Valor da Comissão: R$")
                    self.can.drawString(x, y - 80, "Periodicidade: ")
                    self.can.drawString(x, y - 100, "Natureza: ")
                    self.can.drawString(x, y - 120, "Agência: ")
                    self.can.drawString(x, y - 140, "Conta-Corrente: ")
                    
                    self.can.setFont("Helvetica", 12)
                    self.can.drawString(150, y, row[0])
                    self.can.drawString(150, y - 20, row[1])
                    self.can.drawString(150, y - 40, row[2])
                    self.can.drawString(190, y - 60, row[3])
                    self.can.drawString(150, y - 80, row[4])
                    self.can.drawString(150, y - 100, row[5])
                    self.can.drawString(150, y - 120, row[6])
                    self.can.drawString(150, y - 140, row[7])
                    
                    self.can.rect(20, y - 160, 580, 1, fill=False, stroke=True)
                    y -= 190
                self.can.showPage()
            c.close()
            
            self.can.save()
            webbrowser.open(caminho_file)
        except ValueError as err:
            messagebox.showwarning(self.pagTitulo, f"Não foi localizado informações: {err}")
    
    def buscarCadComissao(self):
        
        if not self.data_comissa_entry.get():
            messagebox.showerror(self.pagTitulo, "Sem dados para pesquisar.")
            return
        
        self.buscarCadComissaoFrame()
    
    def buscarCadComissaoFrame(self):
        banco = Banco()
        data_comissao = self.data_comissa_entry.get()
        self.listacomissao.delete(*self.listacomissao.get_children())
        data_hoje = datetime.datetime.today().strftime('%d/%m/%Y')
        
        # if data_comissao < data_hoje:
        #     messagebox.showwarning(self.pagTitulo, f" Você digitou uma data maior que o dia de hoje.\n "
        #                                            f" data digitada {data_comissao}...")
        
        try:
            c = banco.conexao.cursor()
            query = """SELECT COD_LINHA, DT_COMISSAO, SIGLA_EMPRESA, NM_BANCO, NR_CONTRATO, VLR_COMISSAO, PERIODICIDADE, NATUREZA, AGENCIA,
            CONTA_CORRENTE FROM TBL_INFO_COMISSAO where DT_COMISSAO = ? ORDER BY DT_COMISSAO ASC"""
            
            lista = c.execute(query, (data_comissao,))
            for i in lista:
                self.listacomissao.insert("", END, values=i)
            
            c.close()
        
        except ValueError as verr:
            messagebox.showwarning(self.pagTitulo, f"Não foi digitado data para pesquisa: {verr}")
    
    def etlProcessFianca(self):
        valid_etl = Access()
        exist_Knime = valid_etl.pathKnime()
        if not exist_Knime:
            messagebox.showerror(self.pagTitulo, "Não existe o Knime nesta máquina ou o caminho de instalação é "
                                                 "diferente do padrão.\n Consulte o caminho correto na documentação do "
                                                 " ICF disponibilizado na rede e tente novamente.")
            return
        
        confirma_send = messagebox.askquestion(self.pagTitulo, "Deseja atualizar a base de Fianças no ICF?")
        if confirma_send == "yes":
            call_process()
            messagebox.showinfo(self.pagTitulo, "Aguarde! Será enviado um e-mail quando a base de Fianças for "
                                                "atualizada no ICF.")
            return
    
    def relBuscaPeriodo(self):
        cad = Cadastros()
        caminho = Access()
        caminhoDownload = os.path.join(caminho.userDownloads(), f"relatorio_fiancas_{data_hoje}.xlsx")
        data_inicio = self.dt_ini_entry.get()
        data_final = self.dt_final_entry.get()
        df_result = cad.relRiscoPeriodo(data_inicio, data_final)
        
        if not data_inicio or not data_final:
            messagebox.showerror(self.pagTitulo, "Preencha os campos Data Inicio e Data Final para baixar o relatório.")
            return
        
        df_result.to_excel(caminhoDownload, index=False)
        messagebox.showinfo(self.pagTitulo, "Relatório extraido na pasta Downloads")


class TelaTK:
    
    def help_licenca(self):
        messagebox.showinfo(title="Licença de uso....",
                            message="Não tem licença.\n"
                                    "Seja colaborativo e mande sugestão de melhoria.\n"
                                    "Lembre-se que juntos vamos mais longe.\n\n"
                                    "versão: 1.0 \n"
                                    "Diretoria de Finanças\n"
                                    "#2024-2024")
    
    def info_adicional(self):
        messagebox.showinfo(title="Acerca de...",
                            message="App criado por Venâncio Carlos.")
    
    def config_treeview(self):
        style = ttk.Style()
        style.configure("Treeview", font=('Tahoma', 10))  # linhas
        style.configure("Treeview.Heading", font=('Tahoma', 10, 'bold'))  # colunas
    
    def alterar_aparencia(self, opcao_tela: str):
        ctk.set_appearance_mode(opcao_tela)
    
    def nomeBarra(self):
        user = Usuarios()
        user.selectNome(username).strip()
        nome = str(user.nome)
        return nome
    
    def tipo_access(self):
        user = Usuarios()
        matricula = username
        acess = ['ADMIN']
        
        # Aqui você deve implementar a lógica para obter o tipo de acesso do usuário
        tipo_acesso = user.get_tipo_access(matricula)
        
        if tipo_acesso in acess:
            self.bt_inserir.configure(state="normal")
            self.bt_alterar.configure(state="normal")
        else:
            self.bt_inserir.configure(state="disabled", text="Acesso Negado")
            self.bt_alterar.configure(state="disabled", text="Acesso Negado")
    
    def tipo_accessLevel(self):
        user = Usuarios()
        matricula = username
        acess = ['ADMIN']
        # Aqui você deve implementar a lógica para obter o tipo de acesso do usuário
        tipo_acesso = user.get_tipo_access(matricula)
        
        if tipo_acesso in acess:
            self.report_btn.configure(state="normal")
            self.send_btn.configure(state="normal")
        else:
            self.report_btn.configure(state="disabled", text="Acesso Negado")
            self.send_btn.configure(state="disabled", text="Acesso Negado")
    
    def tipo_accessLevelEmail(self):
        user = Usuarios()
        matricula = username
        acess = ['ADMIN']
        # Aqui você deve implementar a lógica para obter o tipo de acesso do usuário
        tipo_acesso = user.get_tipo_access(matricula)
        
        if tipo_acesso in acess:
            self.btn_inserir_mail.configure(state="normal")
            self.btn_altera_mail.configure(state="normal")
            self.btn_delete_mail.configure(state="normal")
        else:
            self.btn_inserir_mail.configure(state="disabled", text="Acesso Negado")
            self.btn_altera_mail.configure(state="disabled", text="Acesso Negado")
            self.btn_delete_mail.configure(state="disabled", text="Acesso Negado")


class EventTecla:
    def __init__(self):
        self.banco_entry = None
        self.empresa_entry = None
        self.listacomissao = None
        self.conta_corrente_entry = None
        self.agencia_entry = None
        self.observacao_entry = None
        self.dt_comissao_entry = None
        self.vlr_comissao_entry = None
        self.nr_parcela_entry = None
        self.dt_fluxo_fim_entry = None
        self.dt_fluxo_inicio_entry = None
        self.tx_comissao_entry = None
        self.vlr_atualizado_banco_entry = None
        self.vlr_principal_entry = None
        self.dt_baixa_entry = None
        self.dt_limite_repac_entry = None
        self.dt_inicial_entry = None
        self.contrato_entry = None
        self.nome_empresa_entry = None
        self.cod_linha_entry = None
        self.listaContrato = None
    
    def OnDoubleclick(self, event):
        item = self.listaContrato.selection()[0]
        values = self.listaContrato.item(item, "values")
        
        # Inserindo os valores nas Entry widgets
        self.cod_linha_entry.delete(0, END)
        self.cod_linha_entry.insert(INSERT, values[0])
        
        self.nome_empresa_entry.delete(0, END)
        self.nome_empresa_entry.insert(INSERT, values[3])
        
        self.contrato_entry.delete(0, END)
        self.contrato_entry.insert(INSERT, values[5])
        
        self.dt_inicial_entry.delete(0, END)
        self.dt_inicial_entry.insert(INSERT, values[6])
        
        self.dt_limite_repac_entry.delete(0, END)
        self.dt_limite_repac_entry.insert(INSERT, values[7])
        
        self.dt_baixa_entry.delete(0, END)
        self.dt_baixa_entry.insert(INSERT, values[9])
        
        self.vlr_principal_entry.delete(0, END)
        self.vlr_principal_entry.insert(INSERT, values[10])
        
        self.vlr_atualizado_banco_entry.delete(0, END)
        self.vlr_atualizado_banco_entry.insert(INSERT, values[12])
        
        self.tx_comissao_entry.delete(0, END)
        self.tx_comissao_entry.insert(INSERT, values[14])
        
        self.dt_fluxo_inicio_entry.delete(0, END)
        self.dt_fluxo_inicio_entry.insert(INSERT, values[15])
        
        self.dt_fluxo_fim_entry.delete(0, END)
        self.dt_fluxo_fim_entry.insert(INSERT, values[16])
        
        self.nr_parcela_entry.delete(0, END)
        self.nr_parcela_entry.insert(INSERT, values[19])
        
        self.vlr_comissao_entry.delete(0, END)
        self.vlr_comissao_entry.insert(INSERT, values[20])
        
        self.dt_comissao_entry.delete(0, END)
        self.dt_comissao_entry.insert(INSERT, values[21])
        
        self.observacao_entry.delete(0, END)
        self.observacao_entry.insert(INSERT, values[22])
        
        self.agencia_entry.delete(0, END)
        self.agencia_entry.insert(INSERT, values[23])
        
        self.conta_corrente_entry.delete(0, END)
        self.conta_corrente_entry.insert(INSERT, values[24])
    
    def OnDoubleclickMail(self, event):
        item = self.listamail.selection()[0]
        values = self.listamail.item(item, "values")
        
        # Inserindo os valores nas Entry widgets
        self.crud_cod_linha_entry.delete(0, END)
        self.crud_cod_linha_entry.insert(INSERT, values[0])
        
        self.crud_empresa_entry.delete(0, END)
        self.crud_empresa_entry.insert(INSERT, values[1])
        
        self.crud_email_entry.delete(0, END)
        self.crud_email_entry.insert(INSERT, values[2])
        
        self.crud_tp_envio_entry.delete(0, END)
        self.crud_tp_envio_entry.insert(INSERT, values[3])
    
    def verificar_vlr_comissao_pdf(self, event):
        if self.vlr_comissao_pdf_entry.get() > self.vlr_comissao_entry.get():
            messagebox.showwarning("Atenção", "Valor do PDF está diferente do valor calculado da comissão.")
            pass
        return
    
    def buscaDtFim(self, event):
        cad = Cadastros()
        nr_contrato = self.contrato_entry.get()
        ultima_data_fluxo_fim = cad.ultDtFluxoFim(nr_contrato)
        
        # Atualizar o campo dt_fluxo_inicio_entry com a data mais recente de dt_fluxo_fim
        self.dt_fluxo_inicio_entry.delete(0, END)
        self.dt_fluxo_inicio_entry.insert(INSERT, ultima_data_fluxo_fim)
    
    def on_nr_parcela_focus_out(self, event):
        self.calcComissao()
    
    def buscaTxComissao(self, event):
        cad = Cadastros()
        nr_contrato = self.contrato_entry.get()
        taxa_comissao = cad.ultTxComissao(nr_contrato)
        
        # Atualizar o campo Taxa Comissão com a recente.
        self.tx_comissao_entry.delete(0, END)
        self.tx_comissao_entry.insert(INSERT, float(taxa_comissao))
    
    def OnDoubleclickRelat(self, event):
        item = self.listacomissao.selection()[0]
        values = self.listacomissao.item(item, "values")
        
        # Inserindo os valores nas Entry widgets
        self.empresa_entry.delete(0, END)
        self.empresa_entry.insert(INSERT, values[2])

        self.banco_entry.delete(0, END)
        self.banco_entry.insert(INSERT, values[3])

class Funcs:
    def __init__(self):
        self.pagTitulo = None
        self.nome_empresa_entry = None
        self.contrato_entry = None
        self.dt_inicial_entry = None
        self.dt_limite_repac_entry = None
        self.dt_baixa_entry = None
        self.vlr_principal_entry = None
        self.vlr_atualizado_banco_entry = None
        self.dt_fluxo_inicio_entry = None
        self.dt_fluxo_fim_entry = None
        self.nr_parcela_entry = None
        self.vlr_comissao_pdf_entry = None
        self.vlr_comissao_entry = None
        self.vlr_comissao_entry = None
        self.vlr_comissao_entry = None
        self.dt_comissao_entry = None
        self.agencia_entry = None
        self.conta_corrente_entry = None
        self.observacao_entry = None
        self.listaContrato = None
        self.cod_linha_entry = None
        self.tx_comissao_entry = None
    
    def limpa_tela(self):
        self.nome_empresa_entry.delete(0, END)
        self.contrato_entry.delete(0, END)
        self.dt_inicial_entry.delete(0, END)
        self.dt_limite_repac_entry.delete(0, END)
        self.dt_baixa_entry.delete(0, END)
        self.vlr_principal_entry.delete(0, END)
        self.vlr_atualizado_banco_entry.delete(0, END)
        self.dt_fluxo_inicio_entry.delete(0, END)
        self.dt_fluxo_fim_entry.delete(0, END)
        self.nr_parcela_entry.delete(0, END)
        self.vlr_comissao_pdf_entry.delete(0, END)
        # self.vlr_comissao_entry.config(state='normal')
        self.vlr_comissao_entry.delete(0, END)
        # self.vlr_comissao_entry.config(state='readonly')
        self.dt_comissao_entry.delete(0, END)
        self.agencia_entry.delete(0, END)
        self.conta_corrente_entry.delete(0, END)
        self.observacao_entry.delete(0, END)
        self.listaContrato.delete(*self.listaContrato.get_children())
        self.cod_linha_entry.delete(0, END)
        self.tx_comissao_entry.delete(0, END)
    
    def botaoLimpar(self):
        self.limpa_tela()
        # self.lbl_msgbox["text"] = "Limpeza Concluida"
        messagebox.showinfo(self.pagTitulo, "Limpeza Concluida.")
    
    def inserirFianca(self):
        cad = Cadastros()
        
        cad.nm_empresa = self.nome_empresa_entry.get().upper()
        cad.nr_contrato = self.contrato_entry.get()
        cad.dt_inicial = self.dt_inicial_entry.get()
        cad.dt_limite_repac = self.dt_limite_repac_entry.get()
        cad.dt_baixa = self.dt_baixa_entry.get()
        cad.vlr_principal = self.vlr_principal_entry.get()
        cad.vlr_atualizado_banco = self.vlr_atualizado_banco_entry.get()
        cad.dt_fluxo_ini = self.dt_fluxo_inicio_entry.get()
        cad.dt_fluxo_fim = self.dt_fluxo_fim_entry.get()
        cad.nr_parcela = self.nr_parcela_entry.get()
        cad.vlr_comissao = self.vlr_comissao_entry.get()
        cad.dt_comissao = self.dt_comissao_entry.get()
        cad.agencia = self.agencia_entry.get()
        cad.conta_corrente = self.conta_corrente_entry.get()
        cad.observacao = self.observacao_entry.get()
        cad.usuario_logado = self.nomeBarra()
        
        # Verificar se todos os campos estão preenchidos
        if not all([cad.nm_empresa, cad.nr_contrato, cad.dt_inicial, cad.vlr_principal, cad.vlr_atualizado_banco,
                    cad.dt_fluxo_fim, cad.dt_fluxo_ini, cad.vlr_comissao,
                    cad.nr_parcela, cad.dt_comissao, cad.agencia, cad.conta_corrente]):
            messagebox.showwarning(self.pagTitulo, "Por favor, preencha todos os campos.")
            return
        
        # Verificar se o contrato e a parcela já existem no banco de dados
        existing_user = cad.get_existing_registro(cad.nr_contrato, cad.nr_parcela)
        if existing_user is None:
            # self.lbl_msgbox["text"] = cad.insertRegistro()
            messagebox.showinfo(self.pagTitulo, cad.insertRegistro())
            self.limpa_tela()
        else:
            # self.lbl_msgbox["text"] = "Contrato e parcela já existem no banco de dados."
            messagebox.showwarning(self.pagTitulo, "Contrato e parcela já existem no banco de dados.")
    
    def alterarFianca(self):
        cad = Cadastros()
        seg = TelaTK()
        
        cad.cod_linha = self.cod_linha_entry.get()
        cad.nm_empresa = self.nome_empresa_entry.get()
        cad.nr_contrato = self.contrato_entry.get()
        cad.dt_inicial = self.dt_inicial_entry.get()
        cad.dt_limite_repac = self.dt_limite_repac_entry.get()
        cad.dt_baixa = self.dt_baixa_entry.get()
        cad.vlr_principal = self.vlr_principal_entry.get()
        cad.vlr_atualizado_banco = self.vlr_atualizado_banco_entry.get()
        cad.dt_fluxo_ini = self.dt_fluxo_inicio_entry.get()
        cad.dt_fluxo_fim = self.dt_fluxo_fim_entry.get()
        cad.nr_parcela = self.nr_parcela_entry.get()
        cad.vlr_comissao = self.vlr_comissao_entry.get()
        cad.dt_comissao = self.dt_comissao_entry.get()
        cad.agencia = self.agencia_entry.get()
        cad.conta_corrente = self.conta_corrente_entry.get()
        cad.observacao = self.observacao_entry.get()
        cad.usuario_logado = seg.nomeBarra()
        
        # self.lbl_msgbox["text"] = cad.updateRegistro()
        messagebox.showinfo(self.pagTitulo, cad.updateRegistro())
        
        self.limpa_tela()
    
    def excluirFianca(self):
        cad = Cadastros()
        
        cad.cod_linha = self.cod_linha_entry.get()
        # self.lbl_msgbox["text"] = cad.deleteRegistro()
        messagebox.showinfo(self.pagTitulo, cad.deleteRegistro())
        
        self.limpa_tela()
    
    def buscarFianca(self):
        cad = Cadastros()
        nr_contrato = self.contrato_entry.get()
        
        if not cad.get_existing_contrato(nr_contrato):
            messagebox.showerror(self.pagTitulo, "Contrato não encontrado.")
            return
        
        def set_value(value):
            return value if value == " " else ""
        
        messagebox.showinfo(self.pagTitulo, cad.selectRegistro(nr_contrato))
        
        self.nome_empresa_entry.delete(0, END)
        self.nome_empresa_entry.insert(INSERT, set_value(cad.nm_empresa))
        
        self.contrato_entry.delete(0, END)
        self.contrato_entry.insert(INSERT, cad.nr_contrato)
        
        self.dt_inicial_entry.delete(0, END)
        self.dt_inicial_entry.insert(INSERT, set_value(cad.dt_inicial))
        
        self.dt_limite_repac_entry.delete(0, END)
        self.dt_limite_repac_entry.insert(INSERT, set_value(cad.dt_limite_repac))
        
        self.dt_baixa_entry.delete(0, END)
        self.dt_baixa_entry.insert(INSERT, set_value(cad.dt_baixa))
        
        self.vlr_principal_entry.delete(0, END)
        self.vlr_principal_entry.insert(INSERT, set_value(cad.vlr_principal))
        
        self.vlr_atualizado_banco_entry.delete(0, END)
        self.vlr_atualizado_banco_entry.insert(INSERT, set_value(cad.vlr_atualizado_banco))
        
        self.tx_comissao_entry.delete(0, END)
        
        self.dt_fluxo_inicio_entry.delete(0, END)
        self.dt_fluxo_inicio_entry.insert(INSERT, set_value(cad.dt_fluxo_ini))
        
        self.dt_fluxo_fim_entry.delete(0, END)
        self.dt_fluxo_fim_entry.insert(INSERT, set_value(cad.dt_fluxo_fim))
        
        self.nr_parcela_entry.delete(0, END)
        self.nr_parcela_entry.insert(INSERT, set_value(cad.nr_parcela))
        
        self.vlr_comissao_entry.delete(0, END)
        self.vlr_comissao_entry.insert(INSERT, set_value(cad.vlr_comissao))
        
        self.dt_comissao_entry.delete(0, END)
        self.dt_comissao_entry.insert(INSERT, set_value(cad.dt_comissao))
        
        self.agencia_entry.delete(0, END)
        self.agencia_entry.insert(INSERT, set_value(cad.agencia))
        
        self.conta_corrente_entry.delete(0, END)
        self.conta_corrente_entry.insert(INSERT, set_value(cad.conta_corrente))
        
        self.observacao_entry.delete(0, END)
        self.observacao_entry.insert(INSERT, set_value(cad.observacao))
        
        self.frameLista()
    
    def frameLista(self):
        banco = Banco()
        nr_contrato = self.contrato_entry.get()
        self.listaContrato.delete(*self.listaContrato.get_children())
        try:
            c = banco.conexao.cursor()
            lista = c.execute(
                "SELECT COD_LINHA, BOLETA_ATUAL,BOLETA_ANT, SIGLA_EMPRESA,NM_BANCO, NR_CONTRATO, DT_INICIAL,"
                "DT_LIMITE_REPAC, DT_VCTO, DT_BAIXA, VLR_PRINCIPAL, INDEXADOR, VLR_ATUALIZADO_BANCO, PERIODICIDADE, "
                "COMISSAO, DT_FLUXO_INI, DT_FLUXO_FIM,DIAS_COMISSAO, DIAS_CONTRATO, NR_PARCELA, VLR_COMISSAO,DT_COMISSAO,"
                "OBSERVACAO, AGENCIA, CONTA_CORRENTE, STATUS_FINAL, NATUREZA, DT_ALTER_REG, USER_INSERT_REG from "
                "TBL_INFO_COMISSAO where nr_contrato = " + nr_contrato + " ORDER BY DT_COMISSAO ASC")
            for i in lista:
                self.listaContrato.insert("", END, values=i)
            
            c.close()
        except:
            messagebox.showwarning(self.pagTitulo, "Não foi digitado contrato.")
    
    def calcComissao(self):
        try:
            valor_atualizado_banco = float(self.vlr_atualizado_banco_entry.get().replace(",", "."))
            comissao_percentual = float(self.tx_comissao_entry.get().replace(",", "."))
            
            dt_fl_ini = datetime.datetime.strptime(self.dt_fluxo_inicio_entry.get(), "%d/%m/%Y")
            dt_fl_fim = datetime.datetime.strptime(self.dt_fluxo_fim_entry.get(), "%d/%m/%Y")
            dias_diferenca = (dt_fl_fim - dt_fl_ini).days
            
            resultado_comissao = (valor_atualizado_banco * comissao_percentual * dias_diferenca) / 360
            
            self.vlr_comissao_entry.configure(state='normal')
            self.vlr_comissao_entry.delete(0, END)
            self.vlr_comissao_entry.insert(0, f"{resultado_comissao:.2f}")
            self.vlr_comissao_entry.configure(state='readonly')
        
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao calcular comissão: {e}")


class FuncsCrud:
    def __init__(self):
        self.crud_cod_linha_entry = None
        self.listamail = None
        self.pagTitulo = None
        self.crud_tp_envio_entry = None
        self.crud_email_entry = None
        self.crud_empresa_entry = None
    
    def LimpaCampos(self):
        
        self.crud_cod_linha_entry.delete(0, END)
        self.crud_empresa_entry.delete(0, END)
        self.crud_email_entry.delete(0, END)
        self.crud_tp_envio_entry.delete(0, END)
        self.listamail.delete(*self.listamail.get_children())
    
    def inserirEmail(self):
        crud = CrudGrupMail()
        re = TelaTK()
        crud.nm_empresa = self.crud_empresa_entry.get().upper()
        crud.nm_mail = self.crud_email_entry.get().upper()
        crud.tp_envio = self.crud_tp_envio_entry.get().upper()
        crud.re_matricula = re.nomeBarra()
        
        # Verificar se todos os campos estão preenchidos
        if not all([crud.nm_empresa, crud.nm_mail, crud.tp_envio]):
            messagebox.showwarning(self.pagTitulo, "Por favor, preencha todos os campos.")
            return
        
        messagebox.showwarning(self.pagTitulo, crud.insertRegistro())
        self.LimpaCampos()
        self.frameListaMail()
    
    def alterarEmail(self):
        crud = CrudGrupMail()
        
        crud.cod_linha = self.crud_cod_linha_entry.get()
        crud.nm_empresa = self.crud_empresa_entry.get()
        crud.nm_mail = self.crud_email_entry.get()
        crud.tp_envio = self.crud_tp_envio_entry.get()
        
        messagebox.showinfo(self.pagTitulo, crud.updateRegistro())
        
        self.LimpaCampos()
        self.frameListaMail()
    
    def excluirEmail(self):
        crud = CrudGrupMail()
        
        crud.cod_linha = self.crud_cod_linha_entry.get()
        if not crud.cod_linha:
            messagebox.showwarning(self.pagTitulo, "Por favor, preencha todos os campos.")
            return
        
        confirma_send = messagebox.askquestion(self.pagTitulo, "Deseja realmente deletar esse registor?")
        if confirma_send == "yes":
            messagebox.showinfo(self.pagTitulo, crud.deleteRegistro())
            
            self.LimpaCampos()
            self.frameListaMail()
        else:
            return
    
    def buscarEmail(self):
        crud = CrudGrupMail()
        cod_linha = self.contrato_entry.get()
        
        def set_value(value):
            return value if value == " " else ""
        
        messagebox.showinfo(self.pagTitulo, crud.selectRegistro(cod_linha))
        
        self.crud_empresa_entry.delete(0, END)
        self.crud_empresa_entry.insert(INSERT, set_value(crud.nm_empresa))
        
        self.crud_email_entry.delete(0, END)
        self.crud_email_entry.insert(INSERT, crud.nm_mail)
        
        self.crud_tp_envio_entry.delete(0, END)
        self.crud_tp_envio_entry.insert(INSERT, set_value(crud.tp_envio))
        
        self.frameListaMail()
    
    def frameListaMail(self):
        banco = Banco()
        cod_linha = self.crud_cod_linha_entry.get()
        self.listamail.delete(*self.listamail.get_children())
        
        try:
            c = banco.conexao.cursor()
            query = """select cod_linha, sigla_empresa, email, tp_envio, re_matricula from TBL_EMAILS"""
            lista = c.execute(query)
            for i in lista:
                self.listamail.insert("", END, values=i)
            
            c.close()
        except:
            messagebox.showwarning(self.pagTitulo, "Não foi digitado dados para pesquisa.")


class Application(Funcs, TelaTK, Relatorios, EventTecla, FuncsCrud):
    def __init__(self, root):
        super().__init__()
        self.root = root
        self.configuracoes()
        self.tela()
        self.frames_tela()
        self.widgets_frame1()
        self.widgets_frame2()
        self.barra_menu = Menu(root)
        self.barraMenu()
        self.config_treeview()
        self.lbl_dt_fluxo_inicio.bind("<Button-1>", self.buscaDtFim)
        self.vlr_atualizado_banco_entry.bind("<FocusOut>", self.buscaTxComissao)
        self.nr_parcela_entry.bind("<FocusOut>", self.on_nr_parcela_focus_out)
        self.vlr_comissao_pdf_entry.bind("<FocusOut>", self.verificar_vlr_comissao_pdf)
        self.tipo_access()
    
    def configuracoes(self):
        self.fundo_frame = '#dfe3ee'
        self.fonte = ctk.CTkFont(family='Tahoma', size=11, weight='bold')
        self.fonte_entry = ctk.CTkFont(family='Tahoma', size=12)
        self.relheight_botao = 0.1
        self.rely_botao = 0.02
        self.borda_botao = 2
        self.fundo_botao = '#107BB0'
        self.fundo_txt_botao = 'white'
        
        iconCaminho = Access()
        self.caminho_icone = iconCaminho.pathIcone()
    
    def tela(self):
        self.pagTitulo = f"ICF-Informe de Comissão Fianças - Login: {self.nomeBarra()}"
        self.root.title(self.pagTitulo)
        self.root.configure(bg_color="#1E90FF")
        self.root.geometry(f"{1500}x{788}")
        self.root.resizable(True, True)
        self.root.minsize(width=850, height=700)
        # self.img = Image.open(self.caminho_icone)
        # self.photo = ImageTk.PhotoImage(self.img)
        # self.root.iconphoto(True, self.photo)
    
    def barraMenu(self):
        self.root.config(menu=self.barra_menu)
        
        def Quit():
            self.root.destroy()
        
        arquivo_menu = Menu(self.barra_menu, tearoff=0)
        arquivo_menu.add_command(label="Relatórios", command=self.telaRelatorio)
        arquivo_menu.add_separator()
        arquivo_menu.add_command(label="Cadastrar e-mail", command=self.telaListaMail)
        arquivo_menu.add_command(label="Atualizar Base Fiança", command=self.etlProcessFianca)
        # arquivo_menu.add_command(label="Excluir")
        arquivo_menu.add_separator()
        arquivo_menu.add_command(label="Sair", command=Quit)
        
        ajuda_menu = Menu(self.barra_menu, tearoff=0)
        ajuda_menu.add_command(label="Licença", command=self.help_licenca)
        ajuda_menu.add_separator()
        ajuda_menu.add_command(label="Acerca de...", command=self.info_adicional)
        
        submenu = tk.Menu(self.barra_menu, tearoff=0)
        submenu.add_command(label="Dark", command=lambda: self.alterar_aparencia("Dark"))
        submenu.add_command(label="Light", command=lambda: self.alterar_aparencia("Light"))
        submenu.add_command(label="System", command=lambda: self.alterar_aparencia("System"))
        
        self.barra_menu.add_cascade(label="Opções", menu=arquivo_menu)
        self.barra_menu.add_cascade(label="Tema", menu=submenu)
        self.barra_menu.add_cascade(label="Ajuda", menu=ajuda_menu)
    
    def frames_tela(self):
        self.frame_1 = ctk.CTkFrame(self.root)
        self.frame_1.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.48)
        
        self.frame_2 = ctk.CTkFrame(self.root)
        self.frame_2.place(relx=0.01, rely=0.50, relwidth=0.98, relheight=0.49)
    
    def widgets_frame1(self):
        # Criação do botão limpar
        self.bt_limpar = ctk.CTkButton(self.frame_1, text="Limpar", command=self.botaoLimpar)
        self.bt_limpar.place(relx=0.01, rely=self.rely_botao, relwidth=0.1,
                             relheight=self.relheight_botao)
        
        # Criação do botão buscar
        self.bt_buscar = ctk.CTkButton(self.frame_1, text="Buscar", command=self.buscarFianca)
        self.bt_buscar.place(relx=0.12, rely=self.rely_botao, relwidth=0.1,
                             relheight=self.relheight_botao)
        
        # Criação do botão Inserir
        self.bt_inserir = ctk.CTkButton(self.frame_1, text="Inserir", command=self.inserirFianca)
        self.bt_inserir.place(relx=0.30, rely=self.rely_botao,
                              relwidth=0.1, relheight=self.relheight_botao)
        
        # Criação do botão Alterar
        self.bt_alterar = ctk.CTkButton(self.frame_1, text="Alterar", command=self.alterarFianca)
        self.bt_alterar.place(relx=0.41, rely=self.rely_botao,
                              relwidth=0.1, relheight=self.relheight_botao)
        
        # Criação do botão Relatório
        self.bt_relatorio = ctk.CTkButton(self.frame_1, text="Relatório", command=self.telaRelatorio)
        self.bt_relatorio.place(relx=0.52, rely=self.rely_botao, relwidth=0.1, relheight=self.relheight_botao)
        
        # Criação do botão Sair
        self.bt_sair = ctk.CTkButton(self.frame_1, text="Sair", command=quit)
        self.bt_sair.place(relx=0.63, rely=self.rely_botao, relwidth=0.1,
                           relheight=self.relheight_botao)
        
        # Label de Mensagem na tela
        self.lbl_msgbox = ctk.CTkLabel(self.frame_1, text="")
        self.lbl_msgbox.place(relx=0.75, rely=self.rely_botao,
                              relwidth=0.22, relheight=self.relheight_botao)
        
        ###### Inicio das Criações das Labels do Frame 1 ######
        
        self.cod_linha_entry = Entry(self.frame_1)
        # Criação da label e entradas contrato
        self.lbl_contrato = ctk.CTkLabel(
            self.frame_1, text="Contrato", font=self.fonte, anchor=NW)
        self.lbl_contrato.place(relx=0.01, rely=0.16)
        self.contrato_entry = ctk.CTkEntry(self.frame_1, font=self.fonte_entry)
        self.contrato_entry.place(relx=0.01, rely=0.20, relwidth=0.1)
        
        # Criação da label e entradas Nome Empresa
        self.lbl_nome_empresa = ctk.CTkLabel(
            self.frame_1, text="Empresa", font=self.fonte)
        self.lbl_nome_empresa.place(relx=0.12, rely=0.14)
        self.nome_empresa_entry = ctk.CTkEntry(self.frame_1, font=self.fonte_entry)
        self.nome_empresa_entry.place(relx=0.12, rely=0.20, relwidth=0.05)
        
        # Criação da label e entradas Agencia
        self.lbl_agencia = ctk.CTkLabel(
            self.frame_1, text="Agencia", font=self.fonte)
        self.lbl_agencia.place(relx=0.18, rely=0.14)
        self.agencia_entry = ctk.CTkEntry(self.frame_1, font=self.fonte_entry)
        self.agencia_entry.place(relx=0.18, rely=0.20, relwidth=0.03)
        
        # Criação da label e entradas Conta Corrente
        self.lbl_conta_corrente = ctk.CTkLabel(
            self.frame_1, text="CC", font=self.fonte)
        self.lbl_conta_corrente.place(relx=0.22, rely=0.14)
        self.conta_corrente_entry = ctk.CTkEntry(self.frame_1, font=self.fonte_entry)
        self.conta_corrente_entry.place(relx=0.22, rely=0.20, relwidth=0.06)
        
        # Criação da label e entradas Data Inicial
        self.lbl_dt_incial = ctk.CTkLabel(
            self.frame_1, text="Data Inicial", font=self.fonte)
        self.lbl_dt_incial.place(relx=0.29, rely=0.14)
        self.dt_inicial_entry = ctk.CTkEntry(self.frame_1, placeholder_text="DD/MM/AAAA", font=self.fonte_entry)
        # self.dt_inicial_entry.delete(0, tk.END)
        self.dt_inicial_entry.place(relx=0.29, rely=0.20, relwidth=0.06)
        
        # Criação da label e entradas Data Limite Repac = 9
        self.lbl_dt_limite_repac = ctk.CTkLabel(
            self.frame_1, text="Data Limite Repac", font=self.fonte)
        self.lbl_dt_limite_repac.place(relx=0.36, rely=0.14)
        self.dt_limite_repac_entry = ctk.CTkEntry(self.frame_1, placeholder_text="DD/MM/AAAA", font=self.fonte_entry)
        # self.dt_limite_repac_entry.delete(0, tk.END)
        self.dt_limite_repac_entry.place(relx=0.36, rely=0.20, relwidth=0.06)
        
        # Criação da label e entradas Data Baixa
        self.lbl_dt_baixa = ctk.CTkLabel(
            self.frame_1, text="Data Baixa", font=self.fonte)
        self.lbl_dt_baixa.place(relx=0.43, rely=0.14)
        self.dt_baixa_entry = ctk.CTkEntry(self.frame_1, placeholder_text="DD/MM/AAAA", font=self.fonte_entry)
        # self.dt_baixa_entry.delete(0, tk.END)
        self.dt_baixa_entry.place(relx=0.43, rely=0.20, relwidth=0.06)
        
        # Criação da label e entradas Valor Principal
        self.lbl_vlr_principal = ctk.CTkLabel(
            self.frame_1, text="Valor Principal", font=self.fonte)
        self.lbl_vlr_principal.place(relx=0.50, rely=0.14)
        self.vlr_principal_entry = ctk.CTkEntry(self.frame_1, justify='right', font=self.fonte_entry)
        self.vlr_principal_entry.place(relx=0.50, rely=0.20, relwidth=0.08)
        
        # Criação da label e entradas Valor Atualizado Banco
        self.lbl_vlr_atualizado_banco = ctk.CTkLabel(
            self.frame_1, text="Valor Atual Banco", font=self.fonte)
        self.lbl_vlr_atualizado_banco.place(relx=0.59, rely=0.14)
        self.vlr_atualizado_banco_entry = ctk.CTkEntry(self.frame_1, justify='right', font=self.fonte_entry)
        self.vlr_atualizado_banco_entry.place(relx=0.59, rely=0.20, relwidth=0.08)
        
        # Criação da label e entradas Data Fluxo Inicio
        self.lbl_dt_fluxo_inicio = ctk.CTkLabel(
            self.frame_1, text="Data Fluxo Inicio", font=self.fonte)
        self.lbl_dt_fluxo_inicio.place(relx=0.68, rely=0.14)
        self.dt_fluxo_inicio_entry = ctk.CTkEntry(self.frame_1, placeholder_text="DD/MM/AAAA", font=self.fonte_entry)
        # self.dt_fluxo_inicio_entry.delete(0, tk.END)
        self.dt_fluxo_inicio_entry.place(relx=0.68, rely=0.20, relwidth=0.06)
        
        # Criação da label e entradas Data Fluxo Final
        self.lbl_dt_fluxo_fim = ctk.CTkLabel(
            self.frame_1, text="Data Fluxo Fim", font=self.fonte)
        self.lbl_dt_fluxo_fim.place(relx=0.75, rely=0.14)
        self.dt_fluxo_fim_entry = ctk.CTkEntry(self.frame_1, placeholder_text="DD/MM/AAAA", font=self.fonte_entry)
        # self.dt_fluxo_fim_entry.delete(0, tk.END)
        self.dt_fluxo_fim_entry.place(relx=0.75, rely=0.20, relwidth=0.06)
        
        # Criação da label e entradas Numero da Parcela
        self.lbl_nr_parcela = ctk.CTkLabel(
            self.frame_1, text="N. da Parcela", font=self.fonte)
        self.lbl_nr_parcela.place(relx=0.82, rely=0.14)
        self.nr_parcela_entry = ctk.CTkEntry(self.frame_1, font=self.fonte_entry)
        self.nr_parcela_entry.place(relx=0.82, rely=0.20, relwidth=0.02)
        
        # Criação da label e entradas Valor da Comissão PDF
        self.lbl_vlr_comissao_pdf = ctk.CTkLabel(
            self.frame_1, text="Valor Comissão PDF", font=self.fonte)
        self.lbl_vlr_comissao_pdf.place(relx=0.88, rely=0.14)
        self.vlr_comissao_pdf_entry = ctk.CTkEntry(self.frame_1, font=self.fonte_entry)
        self.vlr_comissao_pdf_entry.place(relx=0.88, rely=0.20, relwidth=0.08)
        
        # Criação da label e entradas Observações
        self.lbl_observacao = ctk.CTkLabel(
            self.frame_1, text="Observações", font=self.fonte)
        self.lbl_observacao.place(relx=0.01, rely=0.30)
        self.observacao_entry = ctk.CTkEntry(self.frame_1, width=250, font=self.fonte_entry)
        self.observacao_entry.place(relx=0.01, rely=0.36, relwidth=0.3, relheight=0.2)
        
        # Criação da label e entradas Data Comissão
        self.lbl_dt_comissao = ctk.CTkLabel(
            self.frame_1, text="Data Comissão", font=self.fonte)
        self.lbl_dt_comissao.place(relx=0.75, rely=0.29)
        self.dt_comissao_entry = ctk.CTkEntry(self.frame_1, placeholder_text="DD/MM/AAAA", font=self.fonte_entry)
        self.dt_comissao_entry.place(relx=0.75, rely=0.35, relwidth=0.06)
        
        # Criação da label e entradas Taxa da Comissão
        self.lbl_tx_comissao = ctk.CTkLabel(
            self.frame_1, text="Taxa %", font=self.fonte)
        self.lbl_tx_comissao.place(relx=0.82, rely=0.29)
        self.tx_comissao_entry = ctk.CTkEntry(self.frame_1, font=self.fonte_entry)
        self.tx_comissao_entry.place(relx=0.82, rely=0.35, relwidth=0.03)
        
        # Criação da label e entradas Valor da Comissão
        self.lbl_vlr_comissao = ctk.CTkLabel(
            self.frame_1, text="Valor Comissão", font=self.fonte)
        self.lbl_vlr_comissao.place(relx=0.88, rely=0.29)
        self.vlr_comissao_entry = ctk.CTkEntry(self.frame_1, font=self.fonte_entry)
        self.vlr_comissao_entry.place(relx=0.88, rely=0.35, relwidth=0.08)
    
    def widgets_frame2(self):
        listColumns = [
            "Cod. Linha", "Boleta Atual", "Boleta Anterior", "Empresa", "Banco", "Contrato",
            "Data inicial", "Data Limiete Repac", "Data Vcto", "Data Baixa", "Valor Principal",
            "Indexador", "Valor Atual Banco", "Periodicidade", "Comissão", "Data Fluxo Inicial",
            "Data Fluxo Fim", "Dias Comissão", "Dias Contrato", "Nr. Parcela", "Valor Comissão", "Data Comissão",
            "Observação", "Agencia", "Conta Corrente", "Status Final", "Natureza", "Data Alteração Reg.", "Usuario Reg."
        ]
        hd = ["nw", "nw", "nw", "center", "center", "center",
              "center", "nw", "center", "center", "center", "center", "center", "center", "center", "center", "center",
              "center", "center", "center", "center", "center", "center", "center", "center", "center", "center",
              "center", "nw"]
        h = [40, 50, 50, 70, 70, 70, 120, 100, 100, 70, 100, 100, 70,
             70, 70, 120, 100, 100, 40, 100, 70, 70, 70, 70, 120, 100, 70, 70, 100]
        n = 0
        
        self.listaContrato = ttk.Treeview(self.frame_2, columns=[
            f"col{i + 1}" for i in range(len(listColumns))])
        
        for i, col in enumerate(listColumns, start=1):
            self.listaContrato.heading(f"# {i}", text=col.title(), anchor=NW)
            self.listaContrato.column(f"# {i}", width=h[n], anchor=hd[n])
            n += 1
        
        self.listaContrato.column("#0", width=1, stretch=NO)
        self.listaContrato.place(relx=0.01, rely=0.1, relwidth=0.95, relheight=0.85)
        
        self.scrollListaV = Scrollbar(
            self.frame_2, orient='vertical', command=self.listaContrato.yview, width=20)
        self.scrollListaH = Scrollbar(
            self.frame_2, orient='horizontal', command=self.listaContrato.xview, width=5)
        self.listaContrato.configure(
            yscrollcommand=self.scrollListaV.set, xscrollcommand=self.scrollListaH.set)
        
        self.scrollListaV.place(relx=0.96, rely=0.1, relwidth=0.02, relheight=0.90)
        self.scrollListaH.place(relx=0.01, rely=0.95, relwidth=0.95, relheight=0.06)
        
        self.listaContrato.bind("<Double-1>", self.OnDoubleclick)
    
    def telaRelatorio(self):
        self.relat_window = ctk.CTkToplevel()
        self.relat_window.title(f"Relatório Comissão - Login: {self.nomeBarra()}")
        self.relat_window.geometry(f"{1100}x{480}")
        self.relat_window.resizable(False, False)
        self.relat_window.transient(self.root)
        self.relat_window.focus_force()
        self.relat_window.grab_set()
        
        def rel_email():
            mail = EmailOut()
            acessocaminho = Access()
            empresa = self.empresa_entry.get()
            banco = self.banco_entry.get()
            data_hoje = datetime.datetime.today().strftime('%d_%m_%Y')
            caminho_fiancas = acessocaminho.redeFianca()
            # anexo = os.path.join(os.path.join(os.path.dirname(os.path.realpath(__name__)), "RelatorioPDF\\"),
            # f"comissao_{empresa}_{banco}_{data_hoje}.pdf")
            try:
                anexo = os.path.join(os.path.join(caminho_fiancas, "04_RelatorioPDF\\"),
                                     f"comissao_{empresa}_{banco}_{data_hoje}.pdf")
            except:
                messagebox.showerror(self.pagTitulo,
                                     f"Você não tem acesso a rede {caminho_fiancas}, solicite acesso ao seu SAU")
            
            empresa = str(empresa).upper()
            
            if not empresa or not banco:
                messagebox.showwarning(self.pagTitulo, "Preenchimento obrigatorio dos campos: Empresa e Banco")
                return
            try:
                confirma_send = messagebox.askquestion(self.pagTitulo,
                                                       f"Deseja enviar o e-mail para o grupo {empresa}?\n"
                                                       "Ao clicar em SIM não será possível cancelar o "
                                                       "envio.")
                
                if confirma_send == 'yes':
                    RelPdfMail(emilTo=mail.buscaEmail(tp_envio='PARA', nm_empresa=empresa),
                               emailCC=mail.buscaEmail(tp_envio='COPIA', nm_empresa=empresa),
                               nm_empresa=empresa, nm_banco=banco, anexo=anexo)
                    
                    self.data_comissa_entry.delete(0, END)
                    self.empresa_entry.delete(0, END)
                    self.banco_entry.delete(0, END)
                    messagebox.showinfo(self.pagTitulo, "E-mail enviado com sucesso")
                else:
                    return
            
            except ValueError as err:
                messagebox.showerror(self.pagTitulo, "Erro ao enviar e-mail: {err}")
        
        # Campo Data
        self.data_comissa_lbl = ctk.CTkLabel(self.relat_window, text="Digite a Data", font=self.fonte, anchor=NW)
        self.data_comissa_lbl.place(relx=0.01, rely=0.05)
        self.data_comissa_entry = ctk.CTkEntry(self.relat_window, placeholder_text="DD/MM/AAAA", font=self.fonte_entry)
        self.data_comissa_entry.place(relx=0.01, rely=0.10, relwidth=0.08)
        
        # ComboBox Empresa
        self.empresa_lbl = ctk.CTkLabel(self.relat_window, text="Empresa", font=self.fonte, anchor=NW)
        self.empresa_lbl.place(relx=0.10, rely=0.05)
        self.empresa_entry = ctk.CTkEntry(self.relat_window, font=self.fonte_entry)
        self.empresa_entry.place(relx=0.10, rely=0.10, relwidth=0.12)
        # self.empresa_cbbx = ctk.CTkComboBox(self.relat_window)
        # self.empresa_cbbx.place(relx=0.10, rely=0.10, relwidth=0.12)
        # self.empresa_cbbx.set("Empresa")
        # self.data_comissa_entry.bind("<FocusOut>", self.buscarCadEmpresaDay)
        
        self.banco_lbl = ctk.CTkLabel(self.relat_window, text="Escolha o Banco", font=self.fonte, anchor=NW)
        self.banco_lbl.place(relx=0.23, rely=0.05)
        self.banco_entry = ctk.CTkEntry(self.relat_window, font=self.fonte_entry)
        self.banco_entry.place(relx=0.23, rely=0.10, relwidth=0.12)
        
        self.search_btn = ctk.CTkButton(self.relat_window, text="Buscar", command=self.buscarCadComissao)
        self.search_btn.place(relx=0.36, rely=0.10)
        
        self.report_btn = ctk.CTkButton(self.relat_window, text="Gerar PDF", command=self.geraRelatComissao)
        self.report_btn.place(relx=0.55, rely=0.10)
        
        self.send_btn = ctk.CTkButton(self.relat_window, text="Enviar E-mail", command=rel_email)
        self.send_btn.place(relx=0.70, rely=0.10)
        
        self.exit_btn = ctk.CTkButton(self.relat_window, text="Fechar", command=self.relat_window.destroy)
        self.exit_btn.place(relx=0.85, rely=0.10)
        
        self.exit_btn = ctk.CTkButton(self.relat_window, text="Rel. Período", command=self.telaRelatorioExtrair)
        self.exit_btn.place(relx=0.55, rely=0.20)
        
        self.limpar_btn = ctk.CTkButton(self.relat_window, text="Limpar", command=self.limpaTelaTopLevel)
        self.limpar_btn.place(relx=0.70, rely=0.20)
        
        # Desabilita os botões que o usuário com acesso Normal
        self.tipo_accessLevel()
        
        # Inicio do Frame
        self.sidebar_frame = ctk.CTkFrame(self.relat_window)
        self.sidebar_frame.place(relx=0.01, rely=0.30, relwidth=0.98, relheight=0.68)
        
        listColumns = ["Cod. Linha", "Data", "Empresa", "Banco", "Contrato", "Valor Comissão", "Periodicidade", "Natureza",
                       "Agencia",
                       "Conta Corrente"]
        hd = ["nw", "center", "center", "center", "center", "center", "nw", "center", "center", "center"]
        h = [20, 40, 30, 70, 70, 100, 100, 100, 20, 50]
        n = 0
        
        # Treeview comissão
        self.listacomissao = ttk.Treeview(self.sidebar_frame, show="headings", columns=[
            f"col{i + 1}" for i in range(len(listColumns))])
        
        for i, col in enumerate(listColumns, start=1):
            self.listacomissao.heading(f"# {i}", text=col.title(), anchor=NW)
            self.listacomissao.column(f"# {i}", width=h[n], anchor=hd[n])
            n += 1
        
        self.listacomissao.column("#0", width=1, stretch=NO)
        self.listacomissao.place(relx=0.01, rely=0.1, relwidth=0.95, relheight=0.85)
        
        self.scrollListaVRel = Scrollbar(
            self.sidebar_frame, orient='vertical', command=self.listacomissao.yview, width=20)
        self.scrollListaHRel = Scrollbar(
            self.sidebar_frame, orient='horizontal', command=self.listacomissao.xview, width=5)
        self.listacomissao.configure(
            yscrollcommand=self.scrollListaVRel.set, xscrollcommand=self.scrollListaHRel.set)
        
        self.scrollListaVRel.place(relx=0.96, rely=0.1, relwidth=0.02, relheight=0.90)
        self.scrollListaHRel.place(relx=0.01, rely=0.95, relwidth=0.95, relheight=0.05)
        
        self.listacomissao.bind("<Double-1>", self.OnDoubleclickRelat)
    
    def telaRelatorioExtrair(self):
        self.relat_window_ext = ctk.CTkToplevel()
        self.relat_window_ext.title(f"Relatório Comissão - Login: {self.nomeBarra()}")
        self.relat_window_ext.geometry(f"{500}x{200}")
        self.relat_window_ext.resizable(False, False)
        self.relat_window_ext.transient(self.root)
        self.relat_window_ext.focus_force()
        self.relat_window_ext.grab_set()
        
        self.logo_label = ctk.CTkLabel(self.relat_window_ext, text="Extrair Relatório",
                                       font=ctk.CTkFont(size=20, weight="bold"), anchor="w")
        self.logo_label.place(relx=0.35)
        
        # Campo data inicio do relatorio
        self.dt_ini_lbl = ctk.CTkLabel(self.relat_window_ext, text="Data Inicio:", font=self.fonte, anchor=NW)
        self.dt_ini_lbl.place(relx=0.01, rely=0.20)
        self.dt_ini_entry = ctk.CTkEntry(self.relat_window_ext, placeholder_text="DD/MM/AAAA", font=self.fonte_entry)
        self.dt_ini_entry.place(relx=0.01, rely=0.30, relwidth=0.20)
        
        # Campo data inicio do relatorio
        self.dt_final_lbl = ctk.CTkLabel(self.relat_window_ext, text="Data Final:", font=self.fonte, anchor=NW)
        self.dt_final_lbl.place(relx=0.25, rely=0.20)
        self.dt_final_entry = ctk.CTkEntry(self.relat_window_ext, placeholder_text="DD/MM/AAAA", font=self.fonte_entry)
        self.dt_final_entry.place(relx=0.25, rely=0.30, relwidth=0.20)
        
        self.exit_btn = ctk.CTkButton(self.relat_window_ext, text="Extrair", command=self.relBuscaPeriodo)
        self.exit_btn.place(relx=0.05, rely=0.70)
        
        self.limpar_btn = ctk.CTkButton(self.relat_window_ext, text="Limpar", command=self.limpaTelaTopLevelExt)
        self.limpar_btn.place(relx=0.35, rely=0.70)
        
        self.exit_btn = ctk.CTkButton(self.relat_window_ext, text="Fechar", command=self.relat_window_ext.destroy)
        self.exit_btn.place(relx=0.65, rely=0.70)
    
    def telaListaMail(self):
        self.crud_window = ctk.CTkToplevel()
        self.crud_window.title(f"CRUD - Grupos de E-mails - Login: {self.nomeBarra()}")
        self.crud_window.geometry("800x600")
        self.crud_window.resizable(False, False)
        self.crud_window.transient(self.root)
        self.crud_window.focus_force()
        self.crud_window.grab_set()
        
        # Campo codigo
        ctk.CTkLabel(self.crud_window, text="Codigo:").place(relx=0.01, rely=0.05)
        self.crud_cod_linha_entry = ctk.CTkEntry(self.crud_window)
        self.crud_cod_linha_entry.place(relx=0.01, rely=0.10, relwidth=0.05)
        
        # Campo Empresa
        ctk.CTkLabel(self.crud_window, text="Empresa:").place(relx=0.10, rely=0.05)
        self.crud_empresa_entry = ctk.CTkEntry(self.crud_window)
        self.crud_empresa_entry.place(relx=0.10, rely=0.10, relwidth=0.15)
        
        # Campo Email
        ctk.CTkLabel(self.crud_window, text="E-mail:").place(relx=0.26, rely=0.05)
        self.crud_email_entry = ctk.CTkEntry(self.crud_window)
        self.crud_email_entry.place(relx=0.26, rely=0.10, relwidth=0.40)
        
        # Campo Tipo de Envio
        ctk.CTkLabel(self.crud_window, text="Tipo de Envio:").place(relx=0.67, rely=0.05)
        self.crud_tp_envio_entry = ctk.CTkEntry(self.crud_window)
        self.crud_tp_envio_entry.place(relx=0.67, rely=0.10, relwidth=0.12)
        
        ctk.CTkButton(self.crud_window, text="Limpar", command=self.LimpaCampos).place(relx=0.45, rely=0.20)
        ctk.CTkButton(self.crud_window, text="Fechar", command=self.crud_window.destroy).place(relx=0.45, rely=0.28)
        # # Botões CRUD
        self.btn_inserir_mail = ctk.CTkButton(self.crud_window, text="Inserir", command=self.inserirEmail)
        self.btn_inserir_mail.place(relx=0.01, rely=0.20)
        ctk.CTkButton(self.crud_window, text="Buscar", command=self.frameListaMail).place(relx=0.22, rely=0.20)
        self.btn_altera_mail = ctk.CTkButton(self.crud_window, text="Alterar", command=self.alterarEmail)
        self.btn_altera_mail.place(relx=0.01, rely=0.28)
        self.btn_delete_mail = ctk.CTkButton(self.crud_window, text="Deletar", command=self.excluirEmail)
        self.btn_delete_mail.place(relx=0.22, rely=0.28)
        
        # Treeview para exibir os dados
        sidebar_treeview = ctk.CTkFrame(self.crud_window)
        sidebar_treeview.place(relx=0.01, rely=0.35, relwidth=0.98, relheight=0.64)
        
        listColumns = ["Cod Linha", "Empresa", "E-mail", "Tipo Envio", "Cadastrado Por"]
        hd = ["nw", "nw", "center", "center", "center"]
        h = [30, 30, 100, 70, 100]
        n = 0
        
        # Treeview comissão
        self.listamail = ttk.Treeview(sidebar_treeview, show="headings", columns=[
            f"col{i + 1}" for i in range(len(listColumns))])
        
        for i, col in enumerate(listColumns, start=1):
            self.listamail.heading(f"# {i}", text=col.title(), anchor=NW)
            self.listamail.column(f"# {i}", width=h[n], anchor=hd[n])
            n += 1
        
        self.listamail.column("#0", width=1, stretch=NO)
        self.listamail.place(relx=0.01, rely=0.1, relwidth=0.95, relheight=0.85)
        
        scrollListaVRel = Scrollbar(self.crud_window, orient='vertical', command=self.listamail.yview, width=5)
        scrollListaHRel = Scrollbar(self.crud_window, orient='horizontal', command=self.listamail.xview, width=5)
        self.listamail.configure(yscrollcommand=scrollListaVRel.set, xscrollcommand=scrollListaHRel.set)
        
        scrollListaVRel.place(relx=0.96, rely=0.41, relwidth=0.02, relheight=0.59)
        scrollListaHRel.place(relx=0.01, rely=0.97, relwidth=0.95, relheight=0.03)
        
        self.listamail.bind("<Double-1>", self.OnDoubleclickMail)
        self.tipo_accessLevelEmail()


if __name__ == "__main__":
    root = ctk.CTk()
    login = Login(root)
    #Application(root)
    root.mainloop()
