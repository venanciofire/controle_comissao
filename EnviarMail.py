from modulos import *


def RelPdfMail(emilTo: str = "", emailCC: str = "", nm_empresa: str = "", nm_banco: str = "", anexo: str = ""):
    hora_atual = datetime.datetime.now().time().hour
    # Definir as saudações para cada período do dia.
    if 6 <= hora_atual < 12:
        saudacao = "Bom dia!"
    elif 12 <= hora_atual < 18:
        saudacao = "Boa tarde!"
    else:
        saudacao = "Boa noite!"
    
    try:
        outlook = win32.Dispatch('outlook.application')
        email = outlook.CreateItem(0)
        refer = date.today().strftime("%d/%m/%Y")
        email.To = emilTo
        email.CC = emailCC
        email.Subject = f"Aviso Comissão de Fiança | {nm_empresa} | {nm_banco} "
        email.HTMLBody = f"""
        <p>{saudacao}</p>
        
        <p>Segue anexo, comissões de Fiança com débito no dia de hoje ({refer}).</p>
        
        
        
        
        <p>At.te,</p>        """
        
        file_anexo = anexo
        if not anexo:
            pass
        else:
            email.Attachments.Add(file_anexo)
        
        email.Send()
        return "Email enviado"
    except ValueError as err:
        return f"Não foi enviado e-mail erro:{err}"
