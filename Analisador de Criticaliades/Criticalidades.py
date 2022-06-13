
class Criticalidades :
    def __init__(self, nome_arquivo):
        self.C1,self.C2,self.C3,self.C4,self.C5=ler_arquivo_criticalidade(nome_arquivo)

def ler_criticalidades(arquivo,k,n_criticalidades):
    criticalidades = ['']*n_criticalidades
    #numero_medidas = [[0]*k]*n_criticalidades
    for i in range(n_criticalidades):
        Aux = arquivo.readline().replace('\n','')
        Aux = Aux.split(';')
        criticalidades[i] = Aux[0]
        # for j in range(k):
        #     numero_medidas[i].append(int(Aux[1+i]))

    #return criticalidades,numero_medidas
    return set(criticalidades)




def ler_arquivo_criticalidade(nome_arquivo):
    with open(nome_arquivo) as arquivo:

        arquivo.readline()

        n_criticalidades = [0]*5
        lista =[] 
        for i in range(5): 
            Aux = arquivo.readline().replace('\n','')
            lista.append([int(i) for i in Aux.split(';')])
            n_criticalidades[i] = lista[i][1]

        arquivo.readline()
        arquivo.readline()
        
        n_combs = [0]*5
        lista =[] 
        for i in range(5): 
            Aux = arquivo.readline().replace('\n','')
            lista.append([int(i) for i in Aux.split(';')])
            n_combs[i] = lista[i][1]
        

        C1 = ler_criticalidades(arquivo,1,n_criticalidades[0])
        C2 = ler_criticalidades(arquivo,2,n_criticalidades[1])
        C3 = ler_criticalidades(arquivo,3,n_criticalidades[2])
        C4 = ler_criticalidades(arquivo,4,n_criticalidades[3])
        C5 = ler_criticalidades(arquivo,5,n_criticalidades[4])

    return  C1,C2,C3,C4,C5   
        
    