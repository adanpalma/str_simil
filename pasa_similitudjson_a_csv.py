import json
from pathlib import Path

path_n_file = Path('output/similitudes.json')

with open(path_n_file, 'r') as file_obj:
	similitudes = json.load(file_obj)
	
	for cod_empresa in similitudes:
		
		for registros in similitudes[cod_empresa]['simil']:
			print(f"{cod_empresa,similitudes[cod_empresa]['Nombre Empresa'] }  -> {registros['codigo']}"
			      f" {registros['nombre']} {registros['avgjrowinkler']}")
