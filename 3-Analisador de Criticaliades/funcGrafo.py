
import numpy  as np
import matplotlib.pyplot as plt
import networkx as nx

from itertools import count


def montar_grafo_da_rede(rede):

    Grafo_da_rede = nx.Graph()

    #Dicionario que relaciona as barras com a qtde de medidas associadas a ela
    num_meds_na_barra = {}
    for i in range(rede.num_barras):
        num_meds_na_barra[i+1] = 0

    for med in rede.plano_med:
        num_meds_na_barra[med[1]] += med[6] 

    #Nós do Grafo
    for barra in range(1,rede.num_barras+1):
        Grafo_da_rede.add_node(barra,grupo = 0,medidas = num_meds_na_barra[barra])

    #Arestas dos grafos
    for i in range(1,rede.num_barras+1):
        for j in range(1,rede.num_barras+1):
            if (i>j)  and (rede.Y_barra[i-1, j-1]) == 1:
               Grafo_da_rede.add_edge(i,j)

    return Grafo_da_rede  

def exibir_grafo_de_grupos(Grafo,coordenadas):

    numeros_das_barras = {x: x for x in Grafo.nodes}

    #Cria grupo com elementos únicos
    grupos = set(nx.get_node_attributes(Grafo,'grupo').values())
    mapping = dict(zip(sorted(grupos),count()))
    #Cria Listas de Cores para cada grupo
    cores = [mapping[Grafo.nodes[n]['grupo']] for n in Grafo.nodes]

    nx.draw_networkx_labels(Grafo, coordenadas, numeros_das_barras, font_size=11, font_color='w', font_family = "Tahoma", font_weight = "normal")
    nx.draw_networkx_nodes(Grafo, coordenadas, node_size = 300, node_color=cores, alpha=1, node_shape='o')
    nx.draw_networkx_edges(Grafo, coordenadas, edge_color = 'black')

    plt.savefig('fig grupos '+str(len(Grafo.nodes))+'b'+str(sum(Grafo.pesos))+str(Grafo.pesos)+'m.png')
    plt.show()

def exibir_grafo_de_peso_de_medidas(Grafo,coordenadas):

    lista_num_barras =  {x: x for x in Grafo.nodes}
    lista_num_med = []
    for barra in lista_num_barras: lista_num_med.append(Grafo.nodes[barra]['medidas'])

    maior_cor = max(lista_num_med)
    menor_cor = min(lista_num_med)
    for barra in Grafo.nodes: # define a cor pelo grau do nó 
        if lista_num_med[barra-1] - menor_cor > ((maior_cor-menor_cor) / 2):
            nx.draw_networkx_labels(Grafo, coordenadas,{barra : barra}, font_size=7, font_color='w')
        else:
            nx.draw_networkx_labels(Grafo, coordenadas, {barra : barra}, font_size=7, font_color='k')

    nx.draw_networkx(Grafo,coordenadas, node_size = 150 ,with_labels = False, labels = lista_num_barras , node_color = lista_num_med,node_shape ='o', width = 0.5, font_size = 0.5, cmap = plt.get_cmap('Oranges'), vmin = menor_cor, vmax = maior_cor)

    sm = plt.cm.ScalarMappable(cmap=plt.get_cmap('Oranges'),norm=plt.Normalize(vmin = menor_cor, vmax = maior_cor))
    sm._A = []
    sm.set_array(list(range(menor_cor, maior_cor + 1)))
    plt.colorbar(sm, ticks = range(menor_cor, maior_cor + 1))
    plt.gca().set_facecolor('paleturquoise')
    # plt.colorbar(sm)
    plt.savefig('fig '+str(len(Grafo.nodes))+'b'+str(sum(lista_num_med))+'m.png')
    plt.show() # display
    

def salva_grupos_em_txt(G,n_grupos):

    grupos = cria_lista_de_grupos(G,n_grupos)
    num_barras = len(G.nodes)
    dif = int(G.dif)
    num_medidas = sum(G.pesos)

    for i in range(n_grupos):
        nome_arquivo = f'{num_barras}b{num_medidas}m{dif}d_Grupo{i+1}.txt'
        textfile = open(nome_arquivo, "w")
    
        for elemento in grupos[i]:  
            textfile.write(f'{elemento}\n')

        textfile.close()


def cria_lista_de_grupos(G,n_grupos):

    grupos =  [[] for _ in range(n_grupos)]
    for no in G.nodes:
        grupo = G.nodes[no]['grupo']  
        grupos[grupo].append(int(no))

    return grupos

def montar_grafo_criticalidades(Ckset):

    Grafo_criticalidades = nx.Graph()

    for i in Ckset:
        meds = i.split(' ')[0:-2]
        for med in meds:
            if(med[0] == 'F'):
                #print('Medida de Fluxo')
                med = str(med).replace('F','')
                med = str(med).replace('(','')
                med = str(med).replace(')','') 
                med = str(med).split('-')
                med = [int(i) for i in med]
                Grafo_criticalidades.add_edge(med[0],med[1],tipo ='F')
            elif(med[0] == 'I'):
                #print('Medida de Injeção')
                med = str(med).replace('I','')
                med = str(med).replace('(','')
                med = str(med).replace(')','')
                med=int(med)
                Grafo_criticalidades.add_node(med,tipo = "I") 
    
    return Grafo_criticalidades


def exibir_grafo_de_criticalidades(Grafo,Criticalidades,coordenadas):
    numeros_das_barras = {x: x for x in Grafo.nodes} 

    #Cria grupo com elementos únicos
    grupos = set(nx.get_node_attributes(Grafo,'grupo').values())
    mapping = dict(zip(sorted(grupos),count()))
    #Cria Listas de Cores para cada grupo
    cores = [mapping[Grafo.nodes[n]['grupo']] for n in Grafo.nodes]

    nx.draw_networkx_labels(Grafo, coordenadas, numeros_das_barras, font_size=11, font_color='w', font_family = "Tahoma", font_weight = "normal")
    nx.draw_networkx_nodes(Grafo, coordenadas, node_size = 300, node_color=cores, alpha=1, node_shape='o')
    nx.draw_networkx_edges(Grafo, coordenadas, edge_color = 'black')

    
    nx.draw_networkx_labels(Criticalidades, coordenadas, numeros_das_barras, font_size=11, font_color='w', font_family = "Tahoma", font_weight = "normal")
    nx.draw_networkx_nodes (Criticalidades, coordenadas, node_size = 300, node_color='blue', alpha=1, node_shape='o')
    nx.draw_networkx_edges (Criticalidades, coordenadas, edge_color = 'red')

    plt.show()