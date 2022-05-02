import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from networkx import *
import numpy as np

from sklearn import cluster
from collections import defaultdict

def Grafo_para_matriz(Grafo):
    # Initialize edge matrix with zeros
    edge_mat = np.zeros((len(Grafo), len(Grafo)), dtype=int)

    # Loop to set 0 or 1 (diagonal elements are set to 1)
    for node in Grafo:
        for neighbor in Grafo.neighbors(node):
            edge_mat[node-1][neighbor-1] = 1
        edge_mat[node-1][node-1] = 1
    return edge_mat

def clusteriza_kmeans(Grafo,coord,n_grupos):
    edge_mat = Grafo_para_matriz(Grafo)
    print(edge_mat)
    k_clusters = n_grupos
    resultados = []
    algoritmos = {}

    #K-Means
    algoritmos['kmeans'] = cluster.KMeans(
        n_clusters=k_clusters,n_init= 100,
        precompute_distances = True, 
        n_jobs = -1, 
        algorithm = "auto")

    for modelo in algoritmos.values():
        modelo.fit(edge_mat)
        resultados.append(list(modelo.labels_))
        print("Models Fitted")

    grupos = []

    nx.draw(Grafo,
        coord,
        with_labels = True, 
        node_color=list(algoritmos['kmeans'].labels_))

    for no in Grafo.nodes:
        Grafo.nodes[no]['grupo'] = resultados[0][no-1] 
    plt.title("kmeans_test")
    plt.savefig('fig resultado kmeans.png')
    plt.show() 

def clusteriza_agglomerative(Grafo,coord,n_grupos):
    edge_mat = Grafo_para_matriz(Grafo)
    k_clusters = n_grupos
    resultados = []
    algoritmos = {}

    # #Agglomerative Clustering
    algoritmos['agglom'] = cluster.AgglomerativeClustering(
        n_clusters=k_clusters, 
        linkage="ward")


    for modelo in algoritmos.values():
        modelo.fit(edge_mat)
        resultados.append(list(modelo.labels_))
        print("Models Fitted")

    grupos = []

    nx.draw(Grafo,
        coord,
        with_labels = True, 
        node_color=list(algoritmos['agglom'].labels_))

    for no in Grafo.nodes:
        Grafo.nodes[no]['grupo'] = resultados[0][no-1] 

    plt.title("kmeans_test")
    plt.savefig('fig resultado aglomerativo.png')
    plt.show()    

def clusteriza_spectral(Grafo,coord,n_grupos):
    edge_mat = Grafo_para_matriz(Grafo)
    k_clusters = n_grupos
    resultados = []
    algoritmos = {}

    # #Spectral Clustering
    algoritmos['spectral'] = cluster.SpectralClustering(
        n_clusters=k_clusters, 
        affinity="precomputed", 
        n_init=14, 
        assign_labels="discretize")



    for modelo in algoritmos.values():
        modelo.fit(edge_mat)
        resultados.append(list(modelo.labels_))
        print("Models Fitted")

    grupos = []

    nx.draw(Grafo,
        coord,
        with_labels = True, 
        node_color=list(algoritmos['spectral'].labels_))

    for no in Grafo.nodes:
        Grafo.nodes[no]['grupo'] = resultados[0][no-1] 

    plt.title("spectral_test")
    plt.savefig('fig resultado spectral.png')
    plt.show()   