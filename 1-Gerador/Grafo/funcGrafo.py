
import numpy  as np
import matplotlib.pyplot as plt
import networkx as nx

from itertools import count

from sklearn import neighbors

def montar_multigrafo_do_plano_medidas(rede):
    Grafo_da_rede = nx.MultiGraph()

    #Dicionario que relaciona as barras com a qtde de medidas associadas a ela
    num_meds_na_barra = {}
    for i in range(rede.num_barras):
        num_meds_na_barra[i+1] = 0

    for med in rede.plano_med:
        num_meds_na_barra[med[1]] += med[6] 

    #Nós do Grafo
    for barra in range(1,rede.num_barras+1):
        Grafo_da_rede.add_node(barra,grupo = 0,medidas = num_meds_na_barra[barra])

    for row in rede.plano_med:
        From = row[1]
        To = row[2]
        # From = row[0]
        # To = row[1]
        if row[6] == 1:
            if From != To and rede.Y_barra[From - 1, To - 1] == 1:
                Grafo_da_rede.add_edge(From, To, weight = 1, label = 'P' + str(From) + '-' + str(To))

    for row in rede.plano_med:
        From = row[1]
        To = row[2]
        Type = row[4]

        if row[6] == 1:
            if To == From and Type == 2:
                for Col in range(rede.num_barras):
                    if (From - 1) != Col and rede.Y_barra[From - 1][Col] == 1:
                        Grafo_da_rede.add_edge(From, Col + 1, weight = 1, label = 'P' + str(From))

    return Grafo_da_rede

def montar_grafo_da_topologia(rede):

    Grafo_da_rede = nx.Graph()

    #Dicionario que relaciona as barras com a qtde de medidas associadas a ela
    num_meds_na_barra = {}
    for i in range(rede.num_barras):
        num_meds_na_barra[i+1] = 0

    for med in rede.plano_med:
        num_meds_na_barra[med[1]] += med[6] 

    #Nós do Grafo
    for barra in range(1,rede.num_barras+1):
        Grafo_da_rede.add_node(barra,grupo = 0,medidas = num_meds_na_barra[barra],fronteira = 0)

    #Arestas dos grafos
    for i in range(1,rede.num_barras+1):
        for j in range(1,rede.num_barras+1):
            if (i>j)  and (rede.Y_barra[i-1, j-1]) == 1:
               Grafo_da_rede.add_edge(i,j)

    return Grafo_da_rede  

def exibir_multigrafo_de_peso_de_medidas(Grafo, coordenadas):
    
    lista_num_barras =  {x: x for x in Grafo.nodes}
    lista_num_med = []
    for barra in lista_num_barras: lista_num_med.append(Grafo.nodes[barra]['medidas'])

    maior_cor = max(lista_num_med)
    menor_cor = min(lista_num_med)
    for barra in Grafo.nodes: # define a cor pelo grau do nó 
        nx.draw_networkx_labels(Grafo, coordenadas, {barra : barra}, font_size=7, font_color='k')

    nx.draw_networkx(Grafo,coordenadas, node_size = 150 ,with_labels = False, labels = lista_num_barras , node_color = 'w',node_shape ='o', width = 0.5, font_size = 0.5, cmap = plt.get_cmap('Oranges'), vmin = menor_cor, vmax = maior_cor)

    # sm = plt.cm.ScalarMappable(cmap=plt.get_cmap('Oranges'),norm=plt.Normalize(vmin = menor_cor, vmax = maior_cor))
    # sm._A = []
    # sm.set_array(list(range(menor_cor, maior_cor + 1)))
    # plt.colorbar(sm, ticks = range(menor_cor, maior_cor + 1))
    plt.gca().set_facecolor('paleturquoise')

    ax = plt.gca()

    med_lin = dict()
    for e in Grafo.edges:
            
            key = str(e[0]) + '-' +str(e[1])
            med_lin[key] = 0


    curvatura = [0,.1,-.1,.2,-.2,.3,-.3,.4,-.4]

    for e in Grafo.edges:
        if(e[0]<e[1]):
            key = str(e[0]) +'-' + str(e[1])
        elif ((e[0]>e[1])):
            key = str(e[1]) +'-' + str(e[0])
        
        ax.annotate("",
                    xy=coordenadas[e[0]], xycoords='data',
                    xytext=coordenadas[e[1]], textcoords='data',
                    arrowprops=dict(arrowstyle="-", color="0.5",
                                    shrinkA=5, shrinkB=5,
                                    patchA=None, patchB=None,
                                    connectionstyle=f'arc3,rad={curvatura[med_lin[key]]}'),
                    )
        #nx.draw_networkx_edges(Zm,coord,edgelist=[(e[0],e[1])], connectionstyle=f"arc3,rad={curvatura[med_lin[key]]}")
        med_lin[key] = 1 + med_lin[key]

    plt.savefig('fig '+str(len(Grafo.nodes))+'b'+str(sum(lista_num_med))+'m.png')
    plt.show()

def exibir_grafo_de_peso_de_medidas(Grafo):
    coordenadas = Grafo.coordenadas
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

def exibir_grafo_de_grupos(Grafo,salvar =False):
    coordenadas = Grafo.coordenadas
    numeros_das_barras = {x: x for x in Grafo.nodes}

    #Cria grupo com elementos únicos
    grupos = set(nx.get_node_attributes(Grafo,'grupo').values())
    mapping = dict(zip(sorted(grupos),count()))
    #Cria Listas de Cores para cada grupo
    cores = [mapping[Grafo.nodes[n]['grupo']] for n in Grafo.nodes]

    nx.draw_networkx_labels(Grafo, coordenadas, numeros_das_barras, font_size=11, font_color='w', font_family = "Tahoma", font_weight = "normal")
    nx.draw_networkx_nodes(Grafo, coordenadas, node_size = 300, node_color=cores, alpha=1, node_shape='o')
    nx.draw_networkx_edges(Grafo, coordenadas, edge_color = 'black')


    if(salvar):
        plt.savefig('fig grupos.png')
    plt.show()
def exibir_grafo_de_fronteiras(Grafo,salvar =False):
    coordenadas = Grafo.coordenadas
    numeros_das_barras = {x: x for x in Grafo.nodes}

    fronteiras = set(nx.get_node_attributes(Grafo,'fronteira').values())
    mapping = dict(zip(sorted(fronteiras),count()))
    cores = [mapping[Grafo.nodes[n]['fronteira']] for n in Grafo.nodes]

    nx.draw_networkx_labels(Grafo, coordenadas, numeros_das_barras, font_size=11, font_color='w', font_family = "Tahoma", font_weight = "normal")
    nx.draw_networkx_nodes(Grafo, coordenadas, node_size = 300, node_color=cores, alpha=1, node_shape='o')
    nx.draw_networkx_edges(Grafo, coordenadas, edge_color = 'black')

    

    

    if(salvar):
        plt.savefig('fig fronteiras.png')
    plt.show()
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

def cria_lista_de_grupos_sobrepostos(G,n_grupos):

    grupos =  [[] for _ in range(n_grupos)]
    for no in G.nodes:
        grupo = G.nodes[no]['grupo']  
        grupos[grupo].append(int(no))
        for viz in G.neighbors(no):
            grupo_v = G.nodes[viz]['grupo']
            if(grupo!= grupo_v): 
                grupos[grupo].append(int(viz))
                G.nodes[no]['fronteira']=max(grupo,grupo_v)*10 + min(grupo,grupo_v)
            else:
                G.nodes[no]['fronteira']=grupo
        
    return grupos

def find_border(G):
    border = []
    for node in G.nodes():
        group_from = G.nodes[node]['grupo']
        for neigh in G.neighbors(node):
            group_to = G.nodes[neigh]['grupo']
            if(group_from!= group_to): border.append({node,neigh})

    return border
        

def monta_grafo_med_nodes(rede):
    Grafo = nx.Graph()

    for medida in rede.plano_med:
        
        if(medida[4] == 2):#Injeção
            Grafo.add_node(medida[0],grupo = 0,medida = f'I{medida[1]}',medidas = 1)
        if(medida[4] == 1):#Fluxo
            Grafo.add_node(medida[0],grupo = 0,medida=f'F{medida[1]},{medida[2]}',medidas =1)

    for no in Grafo.nodes:
        barra_med1 = rede.plano_med[no-1][1] 
        tipo = rede.plano_med[no-1][4]
        for med in rede.plano_med:
            de   = med[1]
            para = med[2]
            #print(no,de,para)
            if(barra_med1 == de or barra_med1 == para):
                if(no != med[0]): Grafo.add_edge(no,med[0])
            if(tipo == 2):
                if (rede.Y_barra[barra_med1-1][de-1]==1 or rede.Y_barra[barra_med1-1][para-1]==1):
                    if(no != med[0]): Grafo.add_edge(no,med[0])    
    return Grafo

def exibir_grafo(Grafo,coordenadas):
    numero_das_barras =  {x: Grafo.nodes[x]['medida'] for x in Grafo.nodes}

    nx.draw_networkx_labels(Grafo, coordenadas, numero_das_barras, font_size=11, font_color='r', font_family = "Tahoma", font_weight = "normal")
    nx.draw_networkx_nodes(Grafo, coordenadas, node_size = 300, node_color='b', alpha=1, node_shape='o')
    nx.draw_networkx_edges(Grafo, coordenadas, edge_color = 'black')
    
    plt.title(f'Grafo {len(Grafo.nodes)} medidas')
    plt.show()

def shortest_path_BFS(G,start):
        visited = {i:False for i in G.nodes}
        distances  ={i:0 for i in G.nodes}
        next = []
        next.append(start)
        visited[start] = True
        while(next):
                n=next[0]
                next.pop(0)
                for v in G.neighbors(n):
                        if(not visited[v]): 
                                visited[v] = True
                                next.append(v)
                                distances[v] = distances[n] + 1
        #print(distances)
        return distances
    