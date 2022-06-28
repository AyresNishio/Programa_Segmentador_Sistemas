
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
barras_excluidas  = []
#barras_excluidas = [2,3,4,6,7,8,11, 117,14, 13, 33, 16, 18,19, 20, 29, 31, 10, 27, 13, 114,26, 25,22 ]
#barras_excluidas = [113, 17,15, 20, 23, 72, 39, 40, 33, 35, 34, 43, 38, 70, 75, 66, 116, 47, 45, 48, 50, 53, 56, 59]

gera_plano_concentrado(rede,redun_min, barras_preferidas,barras_excluidas)
print(calcula_redundancia(rede.num_medidas,rede.num_barras,rede.max_med))


#G=montar_multigrafo_do_plano_medidas(rede)
G=montar_grafo_da_topologia(rede)
G.coordenadas = rede.coordenadas
exibir_grafo_de_peso_de_medidas(G)

rede.plano_med = remove_medidas_desativaddas(rede)

salva_Caso(rede)
n_grupos = 3
n_iter =5

G = segmentar_rede_em_n_grupos_m_vezes(G,n_grupos,n_iter)
G.coordenadas = rede.coordenadas
exibir_grafo_de_grupos(G,salvar = True)
salva_grupos_em_txt(G,n_grupos)

grupos     = cria_lista_de_grupos(G,n_grupos)
sub_planos = salva_sub_plano_med(rede.plano_med,grupos)
salva_sub_covariancia(rede.E,sub_planos)

# Arruma diretórios
dir_origem = os.path.dirname(__file__)
caso= f'Caso{rede.num_barras}barras{rede.num_medidas}medidas'
dir_destino = dir_origem + '/' +caso
if not os.path.exists(dir_destino):
    os.makedirs(dir_destino)
arquivos_na_pasta = os.listdir(dir_origem)
for arquivo in arquivos_na_pasta:
    if arquivo.endswith('.txt') or arquivo.endswith('.png'):
        shutil.move(os.path.join(dir_origem,arquivo), os.path.join(dir_destino,dir_destino))



print('')




