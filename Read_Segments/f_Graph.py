import networkx as nx
import matplotlib.pyplot as plt
from itertools import count

def build_measurement_dist_graph(bus_sys,meas_plan):

    Dg = nx.Graph()
    Dg.coordinates = bus_sys.coordinates
    #Dicionario que relaciona as barras com a qtde de meas_plan associadas a ela
    n_meas_in_bus = {}
    for i in range(bus_sys.n_bus):
        n_meas_in_bus[i+1] = 0

    for meas in meas_plan:
        n_meas_in_bus[meas[1]] += meas[6] 

    #Nós do Grafo
    for bus in range(1,bus_sys.n_bus+1):
        Dg.add_node(bus,group = 0,n_meas = n_meas_in_bus[bus])

    #Arestas dos grafos
    for i in range(1,bus_sys.n_bus+1):
        for j in range(1,bus_sys.n_bus+1):
            if (i>j)  and (bus_sys.Ybus[i-1, j-1]) == 1:
               Dg.add_edge(i,j)

    return Dg 

 

def show_measurement_dist_graph(Dg, save=0):
    coordinates = Dg.coordinates
    list_bus_numbers =  {x: x for x in Dg.nodes}
    list_meas_per_bus = []
    for bus in list_bus_numbers: list_meas_per_bus.append(Dg.nodes[bus]['n_meas'])

    max_color = max(list_meas_per_bus)
    min_color = min(list_meas_per_bus)
    for bus in Dg.nodes: # define a cor pelo grau do nó 
        if list_meas_per_bus[bus-1] - min_color > ((max_color-min_color) / 2):
            nx.draw_networkx_labels(Dg, coordinates,{bus : bus}, font_size=7, font_color='w')
        else:
            nx.draw_networkx_labels(Dg, coordinates, {bus : bus}, font_size=7, font_color='k')

    nx.draw_networkx(Dg,coordinates, node_size = 150 ,with_labels = False, labels = list_bus_numbers , node_color = list_meas_per_bus,node_shape ='o', width = 0.5, font_size = 0.5, cmap = plt.get_cmap('Oranges'), vmin = min_color, vmax = max_color)

    sm = plt.cm.ScalarMappable(cmap=plt.get_cmap('Oranges'),norm=plt.Normalize(vmin = min_color, vmax = max_color))
    sm._A = []
    sm.set_array(list(range(min_color, max_color + 1)))
    plt.colorbar(sm, ticks = range(min_color, max_color + 1))
    plt.gca().set_facecolor('paleturquoise')
    # plt.colorbar(sm)
    if save : plt.savefig('Distribution Graph '+str(len(Dg.nodes))+'b'+str(sum(list_meas_per_bus))+'m.png')
    plt.show() # display

def show_groups(Graph, save=False):
    coordinates = Graph.coordinates
    bus_numbers = {x: x for x in Graph.nodes}

    #Cria grupo com elementos únicos
    groups = set(nx.get_node_attributes(Graph,'group').values())
    mapping = dict(zip(sorted(groups),count()))
    #Cria Listas de Cores para cada grupo
    colors = [mapping[Graph.nodes[n]['group']] for n in Graph.nodes]

    nx.draw_networkx_labels(Graph, coordinates, bus_numbers, font_size=11, font_color='w', font_family = "Tahoma", font_weight = "normal")
    nx.draw_networkx_nodes(Graph, coordinates, node_size = 300, node_color=colors, alpha=1, node_shape='o')
    nx.draw_networkx_edges(Graph, coordinates, edge_color = 'black')

    if save:
        plt.savefig('fig grupos.png')

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
        return distances

def get_measurements_in_group(G):
    groups=set(nx.get_node_attributes(G,'group').values())
    n_meas_in_group = {}   
    for group in groups: n_meas_in_group[group] = 0
    for bus in G.nodes:
        grupo = G.nodes[bus]['group']
        n_meas_in_group[grupo] = n_meas_in_group[grupo]+G.nodes[bus]['n_meas']

    return n_meas_in_group

# def get_obj_func(n_meas_in_group):
#     objective = 0 
#     total_meas = sum(n_meas_in_group)
#     n_groups = len(n_meas_in_group)
#     avg_n_meas = total_meas/n_groups
#     for n_meas in n_meas_in_group:
#         objective = objective + abs(n_meas-avg_n_meas)

#     return objective   

