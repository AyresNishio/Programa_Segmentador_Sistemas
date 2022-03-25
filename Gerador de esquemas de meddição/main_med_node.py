import numpy as np

from Rede.Rede import *

from Grafo.funcGrafo import*

from Segmentador.funcSegmentaRede import*
from Segmentador.funcSegSaida import*
from Segmentador.funcReagrupar import *

import os
import shutil

num_barras = 6
redun_min = .20
nome_top = 'ieee-'+str(num_barras) + '-bus.txt'

rede = Rede(num_barras)

barras_preferidas = []
barras_excluidas = []

gera_plano_concentrado(rede,redun_min, barras_preferidas,barras_excluidas)
print(rede.num_medidas)


G=montar_grafo_da_topologia(rede)
exibir_grafo_de_peso_de_medidas(G,rede.coordenadas)
rede.plano_med=remove_medidas_desativaddas(rede)
print(rede.plano_med)
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



print('fim')