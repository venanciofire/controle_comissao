import tkinter as tk
import customtkinter as ctk
from datetime import datetime, date
import datetime
from tkinter import *
from tkinter import ttk, messagebox, font

import re
import os

import numpy
from PIL import Image, ImageTk
from tkcalendar import DateEntry
from Banco import Banco
from Usuarios import Cadastros, Usuarios, EmailOut, CrudGrupMail
from acessos import Access
from login import Login
from EnviarMail import *
from etl_fiancas import *

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Image
import webbrowser

import pandas as pd
import win32com.client as win32
import re
import openpyxl

import logging
import os.path
import tkinter.messagebox




