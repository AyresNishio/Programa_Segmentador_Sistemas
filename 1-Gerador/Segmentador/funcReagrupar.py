from pickle import FALSE, TRUE
import networkx as nx
import random as rd

from numpy import Inf
from sympy import false

from .funcSegmentaRede import agrupar_n_barras

semente = 5

def reagrupar(Grafo, grupos):
    n_grupos = len(grupos)

    barras_de_fronteira =dic_barras_fronteiras(Grafo, n_grupos)
    i =0
    for fronteira in barras_de_fronteira:
        
        for barra in barras_de_fronteira[fronteira]:
            Grafo.nodes[barra]['grupo'] = 4+i
        i=i+1    
    # barras_folha=[] 
    # i=0
    # rd.seed(semente)
    # for i in range(n_grupos):
    #     barras_folha.append(rd.sample(barras_de_fronteira[i],1)[0]) 


    # Grafo = agrupar_n_barras(Grafo,barras_folha)

    
    return Grafo

def dic_barras_fronteiras(Grafo,n_grupos):
    chaves = []
    for grupo in range(0,n_grupos):
        for grupo2 in range(grupo+1,n_grupos):
            chaves.append(f'{grupo}-{grupo2}')

    barras_de_fronteira = {chave:[] for chave in chaves} 

    for barra in Grafo.nodes():
        
        grupo_barra = Grafo.nodes[barra]['grupo']
        for vizinho in Grafo.neighbors(barra):
            grupo_vizinho = Grafo.nodes[vizinho]['grupo'] 
            if grupo_barra < grupo_vizinho :
                chave = f'{grupo_barra}-{grupo_vizinho}'
                barras_de_fronteira[chave].append(barra)    
                barras_de_fronteira[chave].append(vizinho)    

    return barras_de_fronteira   

def lista_barras_fronteiras(Grafo, n_grupos):
    barras_de_fronteira = [[] for _ in range(n_grupos)]
    
    for barra in Grafo.nodes():
        fronteira =  FALSE
        grupo_barra = Grafo.nodes[barra]['grupo']
        for vizinho in Grafo.neighbors(barra):
            grupo_vizinho = Grafo.nodes[vizinho]['grupo'] 
            if grupo_barra != grupo_vizinho :
                fronteira =  TRUE

        if fronteira==TRUE:
            barras_de_fronteira[grupo_barra].append(barra)

    return barras_de_fronteira


def reagrupar_n_barras(G, folhas):
    for barra in G.nodes():
        folha_proxima = -1
        menor_distancia = nx.diameter(G)+1
        for folha in folhas:
            distancia = nx.shortest_path_length(G,folha,barra)
            if(distancia < menor_distancia):
                folha_proxima = folha
                menor_distancia = distancia

        G.nodes[barra]['grupo'] = folhas.index(folha_proxima)
         
    return G