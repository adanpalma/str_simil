import textdistance as txtdist

from nltk.translate import bleu
from nltk.translate.bleu_score import SmoothingFunction


# nltk it is a translate package that can be used as a string comparison
def compara_similutes(ptext1, ptext2):
	smoothie = SmoothingFunction().method4
	disbleu = bleu([ptext1], ptext2, smoothing_function=smoothie)
	disjaccard = txtdist.jaccard(ptext1, ptext2)
	dissorensen = txtdist.sorensen(ptext1, ptext2)
	dissorensen_dice = txtdist.sorensen_dice(ptext1, ptext2)
	
	print(f"\n {ptext1} - {ptext2} \n")
	print("   Bleu          Jaccard          Sorensen       Sorensen_Dice")
	print(
			f"  {(disbleu * 100).__round__(2)}%           {(disjaccard * 100).__round__(2)}% "
			f"           {(dissorensen * 100).__round__(2)}%        "
			f" {(dissorensen_dice * 100).__round__(2)} "
			f"               Promedio"
			f" "
			f"{(((disjaccard + dissorensen) / 2) * 100).__round__(2)}   %"
			)
	print("*" * 70)


text1: str = 'ADAN MANUEL PALMA DE LEON'
text2: str = 'DE LEON MANUEL ADAN'
text3: str = 'Farmacias Arrocha'

compara_similutes(text1.upper(), text2.upper())
compara_similutes(text1.upper(), text3.upper())
print("\n" * 5)

text1: str = 'Proyecto las Acacias No1'
text2: str = 'Las Acacias'
text3: str = 'Farmacias Arrocha'

compara_similutes(text1.upper(), text2.upper())
compara_similutes(text1.upper(), text3.upper())
