from tkinter import Tk
from tkinter import messagebox

def message_box(mensaje):
    Tk().withdraw()
    messagebox.showinfo('Mensaje', mensaje)