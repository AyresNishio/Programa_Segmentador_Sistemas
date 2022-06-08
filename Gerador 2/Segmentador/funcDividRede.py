
import networkx as nx
import random as rd


def dividir_rede(G):
    
    # Vertices de maior excentricidade são aqueles mais distântes do centro do grafo
    max_exc = listar_maiores_exc(G)

    #Vertices precisam estar distântes entre si para o agrupamento
    folhas = identificar_vertices_distantes(G, max_exc)

    G = agrupar_barras(G,folhas)

    G = balancear_grafo(G)

    return G

def listar_maiores_exc(G):
    exc = nx.eccentricity(G)
    diametro =max(exc.items())[1]
    max_exc = []
    for ex in exc.items():
        if(ex[1]==diametro): max_exc.append(ex[0])

    return max_exc

def identificar_vertices_distantes(G,max_exc):
    diametro = nx.diameter(G)
    folhas = rd.sample(max_exc, 2)
    while(nx.shortest_path_length(G,folhas[0],folhas[1])!=diametro) : folhas[0],folhas[1] = rd.sample(max_exc, 2)
    return folhas

def agrupar_barras(G, folhas):
    for barra in G.nodes():
        if(nx.shortest_path_length(G,folhas[0],barra) < nx.shortest_path_length(G,folhas[1],barra)): 
            G.nodes[barra]['grupo'] = 0
        else:
            G.nodes[barra]['grupo'] = 1
    return G


def balancear_grafo(G):

    for i in range(10):
        
        maior_grupo, menor_grupo = identifica_maior_e_menor_grupo(G)
        
        barra_trocada = escolher_barra_para_mudar_de_grupo(G,maior_grupo)
        
        Gnovo= G.copy()
        Gnovo.nodes[barra_trocada]['grupo'] = menor_grupo

        conexo = testar_conectividade_do_grupo(Gnovo,maior_grupo)
        if(conexo): 
            viavel = testar_melhoria_da_troca(G, Gnovo)
        else: viavel = False

        if(viavel): G.nodes[barra_trocada]['grupo'] = menor_grupo

    return G




def identifica_maior_e_menor_grupo(G):

    pesos = calcular_pesos(G)

    if( pesos[0] < pesos[1]):
        grupo_menor = 0
        grupo_maior = 1
    else:
        grupo_menor = 1
        grupo_maior = 0

    return grupo_maior, grupo_menor

def calcular_pesos(G):
    peso_grupo = [0,0]
    for barra in G.nodes:   
        if(G.nodes[barra]['grupo'] == 0): peso_grupo[0] = peso_grupo[0]+G.nodes[barra]['medidas']
        if(G.nodes[barra]['grupo'] == 1): peso_grupo[1] = peso_grupo[1]+G.nodes[barra]['medidas']

    return peso_grupo

def escolher_barra_para_mudar_de_grupo(G,grupo):
    barras_de_fronteira = []
    for barra in G.nodes:
        fronteira = False
        for vizinho in G.neighbors(barra):
            if(G.nodes[barra]['grupo'] == grupo and G.nodes[vizinho]['grupo'] != G.nodes[barra]['grupo']): 
                fronteira = True
        if (fronteira) : barras_de_fronteira.append(barra)

    barra_trocada = rd.choice(barras_de_fronteira)
    return barra_trocada

def testar_conectividade_do_grupo(G,grupo):
    Gmaior = G.copy()
    for barra in G.nodes:
        if(G.nodes[barra]['grupo'] != grupo):
            Gmaior.remove_node(barra)
    
    return nx.is_connected(Gmaior)

def testar_melhoria_da_troca(G_antigo, G_novo):
    #peso representa o número de medidas em um grupo
    peso_antigo = calcular_pesos(G_antigo) #armazenar antes da troca TODO melhorar isso
    peso_novo = calcular_pesos(G_novo)

    #objetivo da minimização
    dif_peso_antigo = abs(peso_antigo[0] - peso_antigo[1])
    dif_peso_novo = abs(peso_novo[0] - peso_novo[1])

    return dif_peso_novo < dif_peso_antigo

        
