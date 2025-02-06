import subprocess as sp


def call_process():
    file_bat = open("etl_fiancas.bat", "r")
    proc_file = file_bat.read().strip()
    
    sp.Popen(proc_file)
