import textdistance as txtdist
import csv

from nltk.translate import bleu
from nltk.translate.bleu_score import SmoothingFunction


# nltk it is a translate package that can be used as a string comparison
def compara_similutes(ptext1, ptext2) -> float:
    smoothie = SmoothingFunction().method4
    disbleu = bleu([ptext1], ptext2, smoothing_function=smoothie)
    disjaccard = txtdist.jaccard(ptext1, ptext2)
    dissorensen = txtdist.sorensen(ptext1, ptext2)
    dissorensen_dice = txtdist.sorensen_dice(ptext1, ptext2)

    return ((((disbleu + disjaccard + dissorensen) / 3) * 100).__round__(2))


registros = 1

#TODO: TRATA DE USAR UN HASH O JSON PARA QUE MUESTRES EL CODIGO DE LAS EMPRESAS PARECIDAS

empresa = list(csv.reader(open("inputs\\nombre_empresas.csv")))
empresa1 = []

try:
    for nombre in empresa:
        empresa1.append( nombre[0].split("-")[0])
except:
    pass

empresa2 = empresa1.copy()

for idx, nombre_empresa in enumerate(empresa1[1:]):

    for idx1, nombre_empresa2 in enumerate(empresa2[1:]):
        try:
            avg = compara_similutes(nombre_empresa, nombre_empresa2)

            if avg > 88.00 and avg < 100.00:
                print(nombre_empresa, nombre_empresa2, avg)
        except:
            pass
