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

med_plan = Criticalidades('Caso118b333mCO2.csv')
med_plan1= Criticalidades('medplan1_115m.csv')
med_plan2= Criticalidades('medplan2_123m.csv')
med_plan3= Criticalidades('medplan3_128m.csv')



c1_nao_encontradas = med_plan.C1 - med_plan1.C1 -med_plan2.C1 -med_plan3.C1
c2_nao_encontradas = med_plan.C2 - med_plan1.C2 -med_plan2.C2 -med_plan3.C2
c3_nao_encontradas = med_plan.C3 - med_plan1.C3 -med_plan2.C3 -med_plan3.C3
c4_nao_encontradas = med_plan.C4 - med_plan1.C4 -med_plan2.C4 -med_plan3.C4
c5_nao_encontradas = med_plan.C5 - med_plan1.C5 -med_plan2.C5 -med_plan3.C5

print(f'Ck1: {len(c1_nao_encontradas)}')
print(f'Ck2: {len(c2_nao_encontradas)}')
print(f'Ck3: {len(c3_nao_encontradas)}')
print(f'Ck4: {len(c4_nao_encontradas)}')
print(f'Ck5: {len(c5_nao_encontradas)}')

print(f'Ck1: {c1_nao_encontradas}')
print(f'Ck2: {c2_nao_encontradas}')
print(f'Ck3: {c3_nao_encontradas}')
print(f'Ck4: {c4_nao_encontradas}')
print(f'Ck5: {c5_nao_encontradas}')

with open('Resultados.txt','w') as f:
    f.write(f'Ck1: {len(c1_nao_encontradas)}\n')
    f.write(f'Ck2: {len(c2_nao_encontradas)}\n')
    f.write(f'Ck3: {len(c3_nao_encontradas)}\n')
    f.write(f'Ck4: {len(c4_nao_encontradas)}\n')
    f.write(f'Ck5: {len(c5_nao_encontradas)}\n')

    f.write(f'Ck1: {c1_nao_encontradas}\n')
    f.write(f'Ck2: {c2_nao_encontradas}\n')
    f.write(f'Ck3: {c3_nao_encontradas}\n')
    f.write(f'Ck4: {c4_nao_encontradas}\n')
    f.write(f'Ck5: {c5_nao_encontradas}\n')

rede = Rede(118)

G = montar_grafo_da_rede(rede)
Nf_ck = med_plan.C3 - med_plan1.C3 -med_plan2.C3 -med_plan3.C3
G_crit = montar_grafo_criticalidades(Nf_ck)


for node in G:
    if node in grupo1:
        G.nodes[node]['grupo'] = 1
    if node in grupo2:  
        G.nodes[node]['grupo'] = 2    
    if node in grupo3:  
        G.nodes[node]['grupo'] = 3 

exibir_grafo_de_criticalidades(G,G_crit,rede.coordenadas)

print()