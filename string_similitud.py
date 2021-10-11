from nltk.translate import bleu
from nltk.translate.bleu_score import SmoothingFunction
from pathlib import Path
import textdistance as txtdist
import json
import jellyfish
import textdistance as txtdist

similitudes  = {}
empresa_sin_codigo, codigo_empresa = [], []
min_avg = 89.99
max_avg = 100


def registra_similitudes(cod_empresa1: str, nombre_empresa1: str, cod_empresa2: str, nombre_empresa2: str,
		avg: float) -> dict:
	if not (cod_empresa1 in similitudes):
		similitudes[cod_empresa1] = {}
		similitudes[cod_empresa1][nombre_empresa1] = []
	
	similitudes[cod_empresa1][nombre_empresa1].append({'codigo': cod_empresa2, 'nombre': nombre_empresa2, 'avg': avg})


# nltk it is a translate package that can be used as a string comparison
def compara_similutes(ptext1: str, ptext2: str) -> float:
	#smoothie = SmoothingFunction().method4
	#disbleu = bleu([ptext1], ptext2, smoothing_function=smoothie)
	dissorensen = txtdist.sorensen(ptext1, ptext2)
	disjaccard = txtdist.jaccard(ptext1,ptext2)
	# dissorensen_dice = txtdist.sorensen_dice(ptext1, ptext2)
	jellyscore = jellyfish.jaro_distance(ptext1,ptext2)
	return(jellyscore * 100)
	
	#return (((( disjaccard + dissorensen) / 2) * 100).__round__(2))
	
	

file_to_open = Path("inputs/nombre_empresas.csv")
with open(file_to_open) as f:
	empresa_y_codigo = f.readlines()

# Separo descripcion y codigo ya que viene en la descripcion y los guardo por separado


#empresa_y_codigo = [empresa for empresa in empresa_y_codigo if 'PLAYA BONITA' in empresa]

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
			avg = compara_similutes(nombre_empresa1, nombre_empresa2)
		else:
			avg = 0
		
		if avg > min_avg and avg <= max_avg:
			registra_similitudes(codigo_empresa[idx], nombre_empresa1, codigo_empresa[idx1], nombre_empresa2, avg)
			#print(nombre_empresa1," - ", nombre_empresa2, avg)

pathtofile = Path('output/similitudes.json')
with open(pathtofile, 'w') as outputfile:
	json.dump(similitudes, outputfile, indent=3)
