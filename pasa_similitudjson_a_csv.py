import csv
import json
from pathlib import Path

def pasa_similitudes_a_csv(pais):
	in_path_n_file = Path('output/similitudes_'+pais+'.json')
	out_path_n_file = Path('output/similitudes_'+pais+'.csv')

	out_file =  open(out_path_n_file,"w")

	simil_writer = csv.writer(out_file, delimiter =',',quotechar='"', quoting= csv.QUOTE_MINIMAL)
	simil_writer.writerow(['Cod Empresa1','Nombre Empresa1','Cod Emrpesa2','Nombre Empresa2', 'Avg1','Avg2'])


	with open(in_path_n_file, 'r') as file_obj:
		similitudes = json.load(file_obj)

		for cod_empresa in similitudes:

			for registros in similitudes[cod_empresa]['simil']:
				simil_writer.writerow([cod_empresa,similitudes[cod_empresa]['Nombre Empresa'],registros['codigo'],registros['nombre'],registros['avgjrowinkler'].__round__(2),registros['avgjellymatchratingcodex'].__round__(2)])

	out_file.close()
