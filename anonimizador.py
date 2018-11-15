import pandas

""" aqui se debe ingresar la ruta del archivo a anonimizar
en el futuro se tendría que poder elegir una carpeta que contenga todos los archivos a anonimizar """

path_to_file = 'D:\sectra\data\DGC\sample\PM_PC_Autoestrade_v_4-1.txt'

file_df = pandas.read_csv(path_to_file, 
                         header = None, 
                         delimiter = ';', 
                         skiprows = [0])

# leer diccionario o crearlo si es que no existe