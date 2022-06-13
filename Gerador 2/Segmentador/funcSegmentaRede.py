
import networkx as nx
import random as rd

from numpy import Inf

from Grafo.funcGrafo import exibir_grafo_de_grupos

semente = 5


def segmentar_rede_em_n_grupos_m_vezes(G,n_grupos,vezes):
    menor_dif = Inf
    print('Inicia Segmentação')
    #melhor_G=nx.Graph()
    for i in range(vezes):
        global semente 
        rd.seed(semente+i)
        G = segmentar_rede(G,n_grupos)
        pesos=calcular_pesos(G,n_grupos)
        dif_pesos=calcular_dif_dos_grupos(pesos)
        print(f'[{pesos}] -> {dif_pesos}')
        if(dif_pesos<menor_dif):
            menor_dif = dif_pesos
            melhor_G = G.copy()
            melhores_pesos =pesos
    print(f'Melhor caso selecionado:{menor_dif}')
    print(f'Pesos por grupos:{melhores_pesos}')
    melhor_G.dif = menor_dif
    melhor_G.pesos = melhores_pesos
    return melhor_G

def segmentar_rede(G,n_grupos):
    
    # Vertices de maior excentricidade são aqueles mais distântes do centro do grafo
    #Vertices precisam estar distântes entre si para o agrupamento
    folhas = identificar_n_folhas_distantes(G,n_grupos)
    print(f'folhas: {folhas}')
    G = agrupar_n_barras(G,folhas)
    exibir_grafo_de_grupos(G)
    G = balancear_grafo(G,n_grupos)
    exibir_grafo_de_grupos(G)
    
    return G

def identificar_n_folhas_distantes(G,n_grupos):
    arvore_geradora = nx.minimum_spanning_tree(G)
    lista_de_folhas = listar_folhas(arvore_geradora)

    diametro = nx.diameter(G)
    folhas = rd.sample(lista_de_folhas, n_grupos)
    proximas = True
    while(proximas):
        proximas = False
        for f1 in folhas:
            for f2 in folhas:
                if(f1!=f2 and nx.shortest_path_length(G,f1,f2)<diametro/2):
                    proximas = True
        if(proximas):
            folhas = rd.sample(lista_de_folhas, n_grupos)      
    
    return folhas

def listar_folhas(T):
    lista_de_folhas = []
    graus = nx.degree(T)
    for no in graus:
        if(no[1]==1):lista_de_folhas.append(no[0])

    return lista_de_folhas

def agrupar_n_barras(G, folhas):
    menor_distancia = [Inf]*len(G.nodes)
    for folha in folhas:
        lista_de_distancias = nx.shortest_path_length(G,folha)
        for barra in G.nodes:
            if lista_de_distancias[barra]<menor_distancia[barra-1]:
                    G.nodes[barra]['grupo'] = folhas.index(folha)
                    menor_distancia[barra-1] = lista_de_distancias[barra]
        
    return G


def balancear_grafo(G,n_grupos):
    barras_escolhidas= []
    for i in range(100):
        global semente
        rd.seed(semente + i)
        pesos = calcular_pesos(G,n_grupos)
        
        
        menor_grupo = pesos.index(min(pesos))
        
        #[numero da barra, grupo da barra]
        barra_trocada,grupo_barra_trocada = escolher_barra_para_adicionar_ao_grupo(G,menor_grupo,barras_escolhidas)
        barras_escolhidas.append(barra_trocada)
        Gnovo= G.copy()
        Gnovo.nodes[barra_trocada]['grupo'] = menor_grupo

        conexo = testar_conectividade_do_grupo(Gnovo,grupo_barra_trocada)
        if(conexo): 
            viavel = testar_melhoria_da_troca(G, Gnovo, n_grupos)
        else: 
            viavel = False

        if(viavel):
            print(f'Barra trocada {barra_trocada}->grupo {menor_grupo}')
            G.nodes[barra_trocada]['grupo'] = menor_grupo
            
    return G

def calcular_pesos(G,n_grupos):
    peso_grupo = [0]*n_grupos   
    
    for barra in G.nodes:
        grupo = G.nodes[barra]['grupo']
        peso_grupo[grupo] = peso_grupo[grupo]+G.nodes[barra]['medidas']

    return peso_grupo

def escolher_barra_para_adicionar_ao_grupo(G,grupo,barras_trocadas):
    barras_de_fronteira = []
    for barra in G.nodes:
        #if (barra not in barras_trocadas):
            for vizinho in G.neighbors(barra):
                if(G.nodes[barra]['grupo'] == grupo and G.nodes[vizinho]['grupo'] != G.nodes[barra]['grupo']): 
                    barras_de_fronteira.append([vizinho,G.nodes[vizinho]['grupo']])

    barra_trocada_e_grupo = rd.choice(barras_de_fronteira)
    return barra_trocada_e_grupo

def testar_conectividade_do_grupo(G,grupo):
    Gmaior = G.copy()
    for barra in G.nodes:
        if(G.nodes[barra]['grupo'] != grupo):
            Gmaior.remove_node(barra)
    
    return nx.is_connected(Gmaior)

def testar_melhoria_da_troca(G_antigo, G_novo,n_grupos):
    #peso representa o número de medidas em um grupo
    peso_antigo = calcular_pesos(G_antigo,n_grupos) #armazenar antes da troca TODO melhorar isso
    peso_novo = calcular_pesos(G_novo,n_grupos)

    #objetivo da minimização
    dif_peso_antigo = calcular_dif_dos_grupos(peso_antigo)
    dif_peso_novo = calcular_dif_dos_grupos(peso_novo)

    return dif_peso_novo < dif_peso_antigo

def calcular_dif_dos_grupos(pesos):
    dif = 0 
    n_medidas = sum(pesos)
    n_grupos = len(pesos)
    media_medidas = n_medidas/n_grupos
    for peso in pesos:
        dif = dif + abs(peso-media_medidas)
    
    return dif      



