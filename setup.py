import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"

files = ["Banco.py", "acessos.py", "EnviarMail.py", "etl_fiancas.py", "etl_fiancas.bat", "login.py", "modulos.py",
         "Usuarios.py"]
include_files = ["Icones/", "RelatorioPDF/"]

build_exe_options = {
    "build_exe": {
        "include_files": files + include_files,
        "packages": [],
        "build_exe": r"C:\Users\A0160262\Downloads\Comissao\output"
    }
}
requires = ["babel==2.16.0", "bcrypt==4.2.0", "chardet==5.2.0", "customtkinter==5.2.2", "darkdetect==0.8.0",
            "exceltypes==0.0.2", "numpy==2.1.2", "packaging==24.1", "pandas==2.2.3", "pillow==11.0.0",
            "python-dateutil==2.9.0.post0", "pytz==2024.2", "pywin32==308", "reportlab==4.2.5",
            "six==1.16.0", "tkcalendar==1.6.1", "tzdata==2024.2"
            ]

setup(
    name="Controle de Comissões Fianças",
    version="0.1",
    description="Aplicação para registro e acompanhamento das Fianças",
    options=build_exe_options,
    executables=[Executable("app.py", base=base)],
    install_requires=requires
)
