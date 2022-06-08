from Criticalidades import Criticalidades
from Rede.Rede import Rede 
from funcGrafo import *

def ler_grupo(g):
    nome_arquivo =  f'Grupo{g}.txt'
    grupo = []
    with open(nome_arquivo) as arquivo:
        for linha in arquivo:
            grupo.append(int(linha.replace('\n',''))) 
    return set(grupo)

grupo1=ler_grupo(1)
grupo2=ler_grupo(2)
grupo3=ler_grupo(3)

med_plan = Criticalidades('Caso118b333mCO1.csv')
med_plan1= Criticalidades('medplan1_114m.csv')
med_plan2= Criticalidades('medplan2_120m.csv')
med_plan3= Criticalidades('medplan3_127m.csv')

nao_encontradas = med_plan.C1 - med_plan1.C1 -med_plan2.C1 -med_plan3.C1
print(f'Ck1: {len(nao_encontradas)}')#\n{nao_encontradas}')
nao_encontradas = med_plan.C2 - med_plan1.C2 -med_plan2.C2 -med_plan3.C2
print(f'Ck2: {len(nao_encontradas)}')#\n{nao_encontradas}')
nao_encontradas = med_plan.C3 - med_plan1.C3 -med_plan2.C3 -med_plan3.C3
print(f'Ck3: {len(nao_encontradas)}')#\n{nao_encontradas}')
nao_encontradas = med_plan.C4 - med_plan1.C4 -med_plan2.C4 -med_plan3.C4
print(f'Ck4: {len(nao_encontradas)}')#\n{nao_encontradas}')
nao_encontradas = med_plan.C5 - med_plan1.C5 -med_plan2.C5 -med_plan3.C5
print(f'Ck5: {len(nao_encontradas)}#\n{nao_encontradas}')

rede = Rede(118)

G = montar_grafo_da_rede(rede)
Criticalidades = med_plan.C5 - med_plan1.C5 -med_plan2.C5 -med_plan3.C5
G_crit = montar_grafo_criticalidades(Criticalidades)


for node in G:
    if node in grupo1:
        G.nodes[node]['grupo'] = 1
    if node in grupo2:  
        G.nodes[node]['grupo'] = 2    
    if node in grupo3:  
        G.nodes[node]['grupo'] = 3 

exibir_grafo_de_criticalidades(G,G_crit,rede.coordenadas)

print()