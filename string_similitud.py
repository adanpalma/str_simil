from pathlib import Path
import json
from tkinter.filedialog import askopenfilename
import jellyfish
from strsimpy.jaro_winkler import JaroWinkler
import pasa_similitudjson_a_csv as pasacsv
from tkinter.filedialog import askopenfilename
from tkinter import *


similitudes = {}
empresa_sin_codigo, codigo_empresa = [], []
min_avg = 91.00
max_avg = 100


def registra_similitudes(cod_empresa1: str, nombre_empresa1: str, cod_empresa2: str,  nombre_empresa2: str,
                         avg: float,  avg1: float) -> None:


    if not (cod_empresa1 in similitudes):
        similitudes[cod_empresa1] = {'Nombre Empresa': nombre_empresa1, 'simil': []}

    similitudes[cod_empresa1]['simil'].append(
        {'codigo': cod_empresa2, 'nombre': nombre_empresa2, 'avgjrowinkler': avg, 'avgjellymatchratingcodex':avg1})

def compara_similutes(ptext1: str, ptext2: str):
    ptext1 = ptext1.strip()
    ptext2 = ptext2.strip()
    jarowinkler = JaroWinkler()
    strsimil, strsimil2 = 0, 0
    strsimil = jarowinkler.similarity(ptext1.split(' '), ptext2.split(' '))

    metphon1 = jellyfish.metaphone(ptext1)
    metphon2 = jellyfish.metaphone(ptext2)
    strsimil2 = jarowinkler.similarity(metphon1.split(' '), metphon2.split(' '))


    return strsimil * 100, strsimil2 * 100



pais = input(" Indique PAN  o SAL o CFC?: ")
tema = input("Indique una etiqueta para el archivo : ")

# This is where we lauch the file manager bar.

tkroot = Tk()
name = askopenfilename(initialdir="~/inputs/",
                       filetypes=(("Text File", "*.*"), ("All Files", "*.*")),
                       title="Choose a file.")
tkroot.destroy()
tkroot.quit()

file_to_open = Path(name)
if not file_to_open.is_file():
    print('\n Debe indicar un nombre de archivo..')
    exit(0)

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

for idx, nombre_empresa1 in enumerate(empresa_sin_codigo):
    for idx1, nombre_empresa2 in enumerate(empresa_sin_codigo):

        avg, avg1 = 0, 0
        # Esta comparacion es para controlar  cuando estoy en la misma empresa o se leyo una nueva empresa*
        if codigo_empresa[idx] != codigo_empresa[idx1]:
            avg, avg1 = compara_similutes(nombre_empresa1, nombre_empresa2)


        if (avg > min_avg and avg <= max_avg) and (avg1 > min_avg and avg1 <= max_avg):
            registra_similitudes(codigo_empresa[idx], nombre_empresa1, codigo_empresa[idx1], nombre_empresa2, avg,avg1)

pathtofile = Path('output/similitudes_' + tema  + pais +'.json')

with open(pathtofile, 'w') as outputfile:
    json.dump(similitudes, outputfile, indent=3, ensure_ascii=False)

pasacsv.pasa_similitudes_a_csv(pais, tema)
