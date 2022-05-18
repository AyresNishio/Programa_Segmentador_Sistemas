import numpy as np

from Rede.Rede import *

from Grafo.funcGrafo import*

from Segmentador.funcSegmentaRede import*
from Segmentador.funcSegSaida import*
from Segmentador.funcReagrupar import *

import os
import shutil

num_barras = 57
redun_min = .30
nome_top = 'ieee-'+str(num_barras) + '-bus.txt'

rede = Rede(num_barras)
rede.plano_med = gera_plano_vazio(rede.Y_barra,rede.max_med)
ums_alocadas = [1, 4, 9, 20, 23, 27, 29, 30, 32, 36, 38, 41, 45, 46, 50, 54, 57]
for um in ums_alocadas:
    rede.num_medidas += adiciona_UM(rede.plano_med,um)

print(calcula_redundancia(rede.num_medidas,rede.num_barras,rede.max_med))

complementar_plano_med(rede)

print(calcula_redundancia(rede.num_medidas,rede.num_barras,rede.max_med))

remove_medidas_desativaddas(rede)

G=montar_grafo_da_topologia(rede)
exibir_grafo_de_peso_de_medidas(G,rede.coordenadas)

rede.plano_med = remove_medidas_desativaddas(rede)

salva_Caso(rede)