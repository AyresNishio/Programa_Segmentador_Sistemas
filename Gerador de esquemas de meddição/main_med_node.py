import numpy as np

from Rede.Rede import *

from Grafo.funcGrafo import*

from Segmentador.funcSegmentaRede import*
from Segmentador.funcSegSaida import*
from Segmentador.funcReagrupar import *

import os
import shutil

num_barras = 118
redun_min = .60
nome_top = 'ieee-'+str(num_barras) + '-bus.txt'

rede = Rede(num_barras)

barras_preferidas = []
barras_excluidas = []

def save_Casos_grupos(grupos,rede):
    np.savetxt(f'Grupos{rede.num_barras}b_{rede.num_medidas}m.txt',grupos,fmt='%i')
    i = 1
    for grupo in grupos:
        nmedg = [len(grupo)]
        medg = monta_sub_plano(rede.plano_med,grupo)
        Eg = monta_Sub_Cov_mednum(rede.E,grupo)
        nome_arquivo=f'medplan{i}_{len(grupo)}m.txt'
        with open(nome_arquivo,'a') as f:
            np.savetxt(f,nmedg,fmt='%i')
            np.savetxt(f,medg,delimiter=' ',fmt = '%i')
            np.savetxt(f,Eg  ,delimiter=' ')
        i=i+1
def monta_sub_plano(med_plan,num_das_medidas):
    tam = len(num_das_medidas)
    sub_med_plan = []
    for m in num_das_medidas:
         sub_med_plan.append(med_plan[m-1])
    return sub_med_plan        
def monta_Sub_Cov_mednum(E,num_das_medidas):
    tam = len(num_das_medidas)
    Eg = np.zeros((tam,tam),np.float64)
    lin =0
    for num_i in num_das_medidas:
        col = 0
        for num_j in num_das_medidas:
            Eg[lin,col] = E[num_i-1,num_j-1]
            col = col+1
        lin = lin+1
    return Eg    

gera_plano_concentrado(rede,redun_min, barras_preferidas,barras_excluidas)
print(rede.num_medidas)

G=montar_grafo_da_topologia(rede)
exibir_grafo_de_peso_de_medidas(G,rede.coordenadas)
rede.plano_med=remove_medidas_desativaddas(rede)
Gmed= monta_grafo_med_nodes(rede)
coordenadas = nx.circular_layout(Gmed)
# for y in range(2):
#             for x in range(4):
#                 chave = y*4+x+1
#                 coordenadas[chave] = np.array([x,y])
exibir_grafo(Gmed,coordenadas)

segmentar_rede_em_n_grupos_m_vezes(Gmed,2,5)

exibir_grafo_de_grupos(Gmed,coordenadas)

#salva_grupos_em_txt(Gmed,2)
grupos =cria_lista_de_grupos(Gmed,2)
save_Casos_grupos(grupos,rede)

dir_origem = os.path.dirname(__file__)
caso= f'Caso{rede.num_barras}barras{rede.num_medidas}medidas'
dir_destino = dir_origem + '/' +caso
if not os.path.exists(dir_destino):
    os.makedirs(dir_destino)
arquivos_na_pasta = os.listdir(dir_origem)
for arquivo in arquivos_na_pasta:
    if arquivo.endswith('.txt') or arquivo.endswith('.png'):
        shutil.move(os.path.join(dir_origem,arquivo), os.path.join(dir_destino,dir_destino))


print('fim')