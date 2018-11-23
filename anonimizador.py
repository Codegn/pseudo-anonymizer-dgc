import os
from pathlib import Path
import json
import pandas as pd
from tkinter import filedialog
from tkinter.filedialog import askdirectory

""" aqui se debe ingresar la ruta del archivo a anonimizar en 
el futuro se tendría que poder elegir una carpeta que  contenga 
todos los archivos a anonimizar """

input_folder = askdirectory()

input_folder = Path('sample')
output_folder = Path('sample/anonimizados')
delimiter = ';'

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

""" estoy considerando como trabajar con el diccionario dado que
no queremos que se pierda entre archivos, y tiene que estar contenido 
en una ruta que sea independiente de los archivos que se quieren anonimizar """

dict_folder_path = Path('carpeta_diccionario')
dict_file_path = 'diccionario.txt'
dict_path = dict_folder_path / dict_file_path
""" aqui se debe abrir el diccionario existente o crear uno 
si es que no existe """

if dict_path.exists():
    with open(dict_path) as f:
        placas_id = json.load(f)
elif not dict_folder_path.exists():
    os.makedirs(dict_folder_path)
    placas_id = {}
else:
    placas_id = {}

""" ahora se comienza el ciclo sobre todos los archivos que se encuentran
 en la carpeta que se seleccione """

for root, dirs, files in os.walk(input_folder):
    for filename in files:
        # se contruye la ruta del archivo
        file = input_folder / filename
        # se lee el archivo ignorando la primera dila que contiene información diferente
        df = pd.read_csv(file,
                         header=None,
                         sep=delimiter,
                         skiprows=[0])

        # se identifican todas las placas que aparezcan en las columnas 58, 58 y 60 del archivo formato ST4
        placas = pd.unique(df.iloc[:, 57:60].values.ravel('K'))
        # eliminamos el valor 'nan'
        
        # iteramos sobre estos valores para actualizar el diccionario y asignar nuevos IDs a las nuevas placas.
        for placa in placas:
            # aquí colocaré cosas específicas del archivo estandar ST4

            if (type(placa) == str) and (int(placa.replace(' ','0')[0:2]) >=5) and (int(placa.replace(' ','0')[0:2]) <=6) and (placa not in placas_id):
                placas_id[placa] = max(placas_id.values(), default=0) + 1

        # se reemplazan las placas por los IDs correspondientes del diccionario
        df.iloc[:, 57] = df.iloc[:, 57].map(placas_id)
        df.iloc[:, 58] = df.iloc[:, 58].map(placas_id)
        df.iloc[:, 59] = df.iloc[:, 59].map(placas_id)

        # se guarda una actualización del diccionario
        with open(dict_path, 'w') as f:
            json.dump(placas_id, f)

        # se guarda el archivo anonimizado
        df.to_csv(output_folder / filename, 
                  sep = delimiter, 
                  index = False)

