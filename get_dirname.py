from tkinter import Tk
from tkinter.filedialog import askdirectory
from tkinter import messagebox
import os


def get_dirname(instrucciones):
    Tk().withdraw()
    messagebox.showinfo('Instrucciones',instrucciones)

    dirname = askdirectory(initialdir=os.getcwd(),title=instrucciones)
    if len(dirname) > 0:
        return dirname
    else:
        messagebox.showinfo('Advertencia', 'No ha seleccionado ningún directorio, vuelva a ejecutar el programa')
        os._exit(0) 

        #dirname = os.getcwd()
        #return dirname 