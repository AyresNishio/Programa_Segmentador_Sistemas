from Criticalidades import Criticalidades
from Rede.Rede import Rede 
from funcGrafo import *


med_plan = Criticalidades('Caso118b333m.csv')
med_plan1= Criticalidades('medplan1_112m.csv')
med_plan2= Criticalidades('medplan2_105m.csv')
med_plan3= Criticalidades('medplan3_132m.csv')

print(med_plan.C1 - med_plan1.C1 -med_plan2.C1 -med_plan3.C1)
print(med_plan.C2 - med_plan1.C2 -med_plan2.C2 -med_plan3.C2)
print(med_plan.C3 - med_plan1.C3 -med_plan2.C3 -med_plan3.C3)
print(med_plan.C4 - med_plan1.C4 -med_plan2.C4 -med_plan3.C4)
print(med_plan.C5 - med_plan1.C5 -med_plan2.C5 -med_plan3.C5)

rede = Rede(118)

  


G = montar_grafo_da_rede(rede)

G_crit = montar_grafo_criticalidades(med_plan.C5 - med_plan1.C5 -med_plan2.C5 -med_plan3.C5)

exibir_grafo_de_criticalidades(G,G_crit,rede.coordenadas)

print()