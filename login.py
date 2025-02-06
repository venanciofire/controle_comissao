import customtkinter as ctk
from tkinter import messagebox, END
from Usuarios import Usuarios
import os


class Funcs:
    def __init__(self):
        self.cadastro_button = None
        self.alterar_senha_button = None
        self.login_button = None
        self.re_matricula_entry = None
        self.tipo_acesso_label = None
        self.alteracao_window = None
        self.nova_senha_entry = None
        self.cadastro_window = None
        self.cad_password_entry = None
        self.cad_email_entry = None
        self.cad_username_entry = None
        self.cad_re_matricula_entry = None
        self.cad_name_entry = None
        self.alt_re_matricula_entry = None
    
    def usuario_logado(self):
        self.userpc = os.getlogin()
        return self.userpc
    
    def inserirUsuario(self):
        user = Usuarios()
        
        user.nome = self.cad_name_entry.get()
        user.re_matricula = self.cad_re_matricula_entry.get().upper()
        user.email = self.cad_email_entry.get()
        user.senha = self.cad_password_entry.get()
        user.tp_acesso = 'FALSE'
        
        # Verificar se todos os campos estão preenchidos
        if not all([user.nome, user.re_matricula, user.email, user.senha]):
            messagebox.showwarning("Cadastrar", "Por favor, preencha todos os campos.")
            return
        
        resultado = user.insertUser()
        messagebox.showinfo('Cadastro', resultado)
        
        if "usuário cadastrado com sucesso!" in resultado.lower():
            self.cadastro_window.destroy()
    
    def alterar_senha(self):
        user = Usuarios()
        
        # Obtendo as entradas do usuário
        nova_senha = self.nova_senha_entry.get()
        re_matricula = self.alt_re_matricula_entry.get().upper()
        
        # Validação das entradas
        if not nova_senha or not re_matricula:
            messagebox.showerror("ICF-Erro", "Todos os campos devem ser preenchidos.")
            return
        
        if len(nova_senha) < 8:
            messagebox.showerror("ICF-Erro", "A nova senha deve ter pelo menos 8 caracteres.")
            return
        
        user.senha = nova_senha
        user.re_matricula = re_matricula
        
        # Verificando se a matrícula digitada é igual à do usuário logado
        if self.userpc != user.re_matricula.upper():
            self.nova_senha_entry.delete(0, END)
            self.alt_re_matricula_entry.delete(0, END)
            
            messagebox.showinfo("ICF-Alteração de Senha", "Erro: usuário digitado diferente do logado na máquina.")
            return
        
        # Tentando atualizar o usuário com tratamento de exceções
        try:
            resultado = user.updateUser()
            
            if resultado:
                messagebox.showinfo("ICF-Alteração de Senha", "Senha alterada com sucesso.")
                self.alteracao_window.destroy()
            else:
                messagebox.showerror("ICF-Erro", "Erro ao alterar a senha. Verifique o e-mail e tente novamente.")
        except Exception as e:
            messagebox.showerror("ICF-Erro", f"Ocorreu um erro: {str(e)}")
    
    def tipo_access(self, event):
        user = Usuarios()
        matricula = self.re_matricula_entry.get().upper()
        acess = ['ADMIN', 'NORMAL']
        
        # Aqui você deve implementar a lógica para obter o tipo de acesso do usuário
        tipo_acesso = user.get_tipo_access(matricula)
        
        # Atualizar o texto do label com o tipo de acesso
        self.tipo_acesso_label.configure(text=tipo_acesso)
        
        if tipo_acesso in acess:
            self.login_button.configure(state="normal")
            self.alterar_senha_button.configure(state="normal")
            self.cadastro_button.configure(state="disabled")
        else:
            self.login_button.configure(state="disabled")
            self.alterar_senha_button.configure(state="disabled")
            self.cadastro_button.configure(state="normal")

class Login(Funcs):
    def __init__(self, root):
        super().__init__()
        self.root = root
        self.usuario_logado()
        self.loginTela()
        self.frameTela1()
        self.re_matricula_entry.bind("<FocusOut>", self.tipo_access)
    
    def loginTela(self):
        self.loginTitulo = "ICF - Login"
        self.root.title(self.loginTitulo)
        self.root.geometry(f"{300}x{200}")
        self.root.resizable(False, False)
        
        # Centralizar a janela
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def frameTela1(self):
        # Label para mostrar o tipo de acesso do usuário
        self.tipo_acesso_label1 = ctk.CTkLabel(self.root, text=" Tipo de Acesso")
        self.tipo_acesso_label1.place(x=50, y=20)
        self.tipo_acesso_label = ctk.CTkLabel(self.root, text="")
        self.tipo_acesso_label.place(x=150, y=20)
        
        self.re_matricula_label = ctk.CTkLabel(self.root, text="Matricula")
        self.re_matricula_label.place(x=50, y=50)
        self.re_matricula_entry = ctk.CTkEntry(self.root)
        self.re_matricula_entry.place(x=150, y=50)
        
        self.password_label = ctk.CTkLabel(self.root, text="Senha")
        self.password_label.place(x=50, y=100)
        self.password_entry = ctk.CTkEntry(self.root, show="*")
        self.password_entry.place(x=150, y=100)
        
        self.login_button = ctk.CTkButton(self.root, state="disabled", text="Login", command=self.check_login)
        self.login_button.place(x=30, y=150)
        
        self.cadastro_button = ctk.CTkButton(self.root, state="normal", text="Cadastrar", command=self.abrir_tela_cadastro)
        self.cadastro_button.place(x=120, y=200)
        
        self.alterar_senha_button = ctk.CTkButton(self.root, state="disabled", text="Alterar Senha", command=self.abrir_tela_alteracao)
        self.alterar_senha_button.place(x=190, y=150)
    
    def check_login(self):
        user = Usuarios()
        matricula = self.re_matricula_entry.get().upper()
        password = self.password_entry.get()
        user.selectNome(self.usuario_logado()).strip()
        
        # Verificando se a matrícula digitada é igual à do usuário logado
        if self.userpc != matricula:
            self.tipo_acesso_label.configure(text="")
            self.re_matricula_entry.delete(0, END)
            self.password_entry.delete(0, END)
            messagebox.showinfo("ICF-Alteração de Senha", "Erro: usuário digitado diferente do logado na máquina.")
            return
        
        if user.checkUser(matricula, password):
            messagebox.showinfo('ICF - Login', ' Seja bem vindo ' + str(user.nome))
            self.root.destroy()
            main_app()
        else:
            self.password_entry.delete(0, END)
            messagebox.showerror("ICF-Erro", "Usuário ou senha incorretos")
    
    def abrir_tela_cadastro(self):
        self.cadastro_window = ctk.CTkToplevel()
        self.cadastro_window.title("ICF - Cadastro")
        self.cadastro_window.geometry(f"{450}x{300}")
        self.cadastro_window.resizable(False, False)
        self.cadastro_window.transient(self.root)
        self.cadastro_window.focus_force()
        self.cadastro_window.grab_set()
        
        self.cad_name_label = ctk.CTkLabel(self.cadastro_window, text="Nome")
        self.cad_name_label.place(x=50, y=50)
        self.cad_name_entry = ctk.CTkEntry(self.cadastro_window, width=200)
        self.cad_name_entry.place(x=150, y=50)
        
        self.cad_re_matricula = ctk.CTkLabel(self.cadastro_window, text="RE/Matricula")
        self.cad_re_matricula.place(x=50, y=100)
        self.cad_re_matricula_entry = ctk.CTkEntry(self.cadastro_window)
        self.cad_re_matricula_entry.place(x=150, y=100)
        
        self.cad_email = ctk.CTkLabel(self.cadastro_window, text="E-mail")
        self.cad_email.place(x=50, y=150)
        self.cad_email_entry = ctk.CTkEntry(self.cadastro_window, width=200)
        self.cad_email_entry.place(x=150, y=150)
        
        self.cad_password_label = ctk.CTkLabel(self.cadastro_window, text="Nova Senha")
        self.cad_password_label.place(x=50, y=200)
        self.cad_password_entry = ctk.CTkEntry(self.cadastro_window, show="*")
        self.cad_password_entry.place(x=150, y=200)
        
        self.cadastrar_button = ctk.CTkButton(self.cadastro_window, text="Cadastrar", command=self.inserirUsuario)
        self.cadastrar_button.place(x=150, y=250)
    
    def abrir_tela_alteracao(self):
        self.alteracao_window = ctk.CTkToplevel()
        self.alteracao_window.title("ICF - Alteração de Senha")
        self.alteracao_window.geometry("300x200")
        self.alteracao_window.resizable(False, False)
        self.alteracao_window.transient(self.root)
        self.alteracao_window.focus_force()
        self.alteracao_window.grab_set()
        
        self.alt_re_matricula_label = ctk.CTkLabel(self.alteracao_window, text="Matricula")
        self.alt_re_matricula_label.place(x=50, y=50)
        self.alt_re_matricula_entry = ctk.CTkEntry(self.alteracao_window)
        self.alt_re_matricula_entry.place(x=150, y=50)
        
        self.nova_senha_label = ctk.CTkLabel(self.alteracao_window, text="Nova Senha")
        self.nova_senha_label.place(x=50, y=100)
        self.nova_senha_entry = ctk.CTkEntry(self.alteracao_window, show="*")
        self.nova_senha_entry.place(x=150, y=100)
        
        self.enviar_button = ctk.CTkButton(self.alteracao_window, text="Alterar",
                                           command=self.alterar_senha)
        self.enviar_button.place(x=150, y=150)


def main_app():
    import app
    root = ctk.CTk()
    app.Application(root)
    root.mainloop()
