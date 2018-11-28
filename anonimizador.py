import os
from pathlib import Path
import json
import pandas as pd
from get_dirname import get_dirname
from message_box import message_box

""" aqui se definen algunas variables de interés """

delimiter = ';'

""" aqui se debe ingresar la ruta del archivo a anonimizar en 
el futuro se tendría que poder elegir una carpeta que  contenga 
todos los archivos a anonimizar """

instrucciones_entrada = ('Seleccione la carpeta que contiene los archivos a anonimizar.'
                         '\nLos archivos deben estar directamente en la carpeta y no en sub-carpetas.')

input_folder = Path(get_dirname(instrucciones = instrucciones_entrada))

output_folder = input_folder.parents[0] /  (str(input_folder.name) + '-anonimizados')

if not output_folder.exists():
    os.makedirs(output_folder)

""" estoy considerando como trabajar con el diccionario dado que
no queremos que se pierda entre archivos, y tiene que estar contenido 
en una ruta que sea independiente de los archivos que se quieren anonimizar """

instrucciones_diccionario = ('Seleccione la carpeta donde se encuentra el diccionario de las patentes o en su defecto donde desea que se genere.'
                             '\nRecuerde que el diccionario debe llamarse diccionario-placas.json para ser reconocido,' 
                             'de lo contrario se creará uno nuevo.')

dict_folder_path = Path(get_dirname(instrucciones = instrucciones_diccionario))

dict_file_path = 'diccionario-placas.json'

dict_path = dict_folder_path / dict_file_path

# aqui se debe abrir el diccionario existente o crear uno si es que no existe

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

try:
    for root, dirs, files in os.walk(input_folder):
        for filename in files:
            # se contruye la ruta del archivo
            file = input_folder / filename
            # en caso de que hayan sub carpetas y se construyan archivos inexistentes.
            if file.exists():
                # se lee el archivo ignorando la primera dila que contiene información diferente
                df = pd.read_csv(file,
                                dtype=str, # se leen como string para no modificar cosas como 0000001 -> 1
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

                # se guarda el archivo anonimizado
                df.to_csv(output_folder / filename, 
                        sep = delimiter,
                        header = False,
                        index = False)

                with open(file, 'r') as input_file:
                    with open(output_folder / filename, 'r') as original_output_file:
                        lines = original_output_file.readlines()
                        with open(output_folder / filename, 'w') as new_output_file:
                            new_output_file.write(input_file.readline())
                            new_output_file.writelines(lines)

    # se guarda una actualización del diccionario
    with open(dict_path, 'w') as f:
        json.dump(placas_id, f)
        
    mensaje_final = ('Proceso finalizado con éxito.' 
                     '\nLos archivos anonimizados se encuentran en la siguiente ruta: ' +
                     str(output_folder) +
                     '\nEl diccionario se encuentra en la siguiente ruta: ' +
                     str(dict_path) +
                     '\nProcure guardar el diccionario de manera segura para poder anonimizar más archivos.')

    message_box(mensaje=mensaje_final)

except:
    print('Ups! algo no salió bien. Intente nuevamente o contactese con el desarrollador.')
