from pathlib import Path
import json
from tkinter.filedialog import askopenfilename
import jellyfish
from strsimpy.jaro_winkler import JaroWinkler
import pasa_similitudjson_a_csv as pasacsv

similitudes = {}
empresa_sin_codigo, codigo_empresa = [], []
min_avg = 94.99
max_avg = 100

pais = input(" Indique PAN  o SAL ?")


def registra_similitudes(cod_empresa1: str, nombre_empresa1: str, cod_empresa2: str, nombre_empresa2: str, avg: float,
                         avg1) -> None:
    if not (cod_empresa1 in similitudes):
        similitudes[cod_empresa1] = {'Nombre Empresa': nombre_empresa1, 'simil': []}

    similitudes[cod_empresa1]['simil'].append(
        {'codigo': cod_empresa2, 'nombre': nombre_empresa2, 'avgjrowinkler': avg, 'avgjellymatchratingcodex':
            avg1})


def compara_similutes(ptext1: str, ptext2: str):
    jarowinkler = JaroWinkler()
    strsimil = jarowinkler.similarity(ptext1.split(' '), ptext2.split(' '))

    try:
        metphon1 = jellyfish.metaphone(ptext1)
        metphon2 = jellyfish.metaphone(ptext2)
        strsimil2 = jarowinkler.similarity(metphon1.split(' '), metphon2.split(' '))
    except ValueError:
        # metaphone no soporta ciertos caracteres no ascii en estos casos seteamos -1 para saber
        strsimil2 = -1

    return strsimil * 100, strsimil2 * 100




# This is where we lauch the file manager bar.
from tkinter.filedialog import askopenfilename
name = askopenfilename(initialdir="~/inputs/",
                       filetypes=(("Text File", "*.*"), ("All Files", "*.*")),
                       title="Choose a file."
                       )



file_to_open = Path(name)
with open(file_to_open) as f:
    empresa_y_codigo = f.readlines()

# empresa_y_codigo = [empresa for empresa in empresa_y_codigo if 'PLAYA BONITA' in empresa]

# Separo descripcion y codigo ya que viene en la descripcion y los guardo por separado
try:
    for nombre in empresa_y_codigo:
        empresa_sin_codigo.append(nombre.split("*")[0].strip('\n'))
        codigo_empresa.append(nombre.split("*")[1].strip('\n'))
except:
    pass

empresa_comparar = empresa_sin_codigo.copy()

for idx, nombre_empresa1 in enumerate(empresa_sin_codigo):

    for idx1, nombre_empresa2 in enumerate(empresa_comparar):

        if codigo_empresa[idx] != codigo_empresa[idx1]:
            avg, avg1 = compara_similutes(nombre_empresa1, nombre_empresa2)
        else:
            avg, avg1 = 0, 0

        if (avg > min_avg and avg <= max_avg):
            registra_similitudes(codigo_empresa[idx], nombre_empresa1, codigo_empresa[idx1], nombre_empresa2, avg,
                                 avg1)  # print(nombre_empresa1," - ", nombre_empresa2, avg)

pathtofile = Path('output/similitudes_' + pais +'.json')
with open(pathtofile, 'w') as outputfile:
    json.dump(similitudes, outputfile, indent=3, ensure_ascii=False)

pasacsv.pasa_similitudes_a_csv(pais)
