import numpy as np

#plano de medição
#Coluna - função
# 0 - de
# 1 - para
# 2 - Unidade de Medição
# 3 - Circuito
# 4 - Tipo
# 5 - de (redundante)
# 6 - ligado ou desligado

def monta_Jacobiana(A,medidas):
    n_med=int(sum(medidas[:,6]))
    n=A.shape[0]
    H=np.zeros([n_med,n])#nao precisa de ref pois possui medida fasorial
    Haux= np.zeros([n_med,n-1])
    ind=0
    med=0
    existe_medida_fasorial = False
    while (med<n_med):

        if (medidas[ind,6]==1):#indica se a medida esta ligada ou desligada

            de=int(medidas[ind,1])-1
            para=int(medidas[ind,2])-1

            if (de!=para): #serve para medida de fluxo de potencia e de corrente
                H[med,de]=1
                H[med,para]=-1

            if (de==para)and(medidas[ind,4]==3):#medida de angulo
                 H[med,de]=1
                 existe_medida_fasorial =True

            if (de==para)and(medidas[ind,4]==2):#medida de injecao de Potencia
                nbc=int(sum(A[de,:]))
                for l in range(n-1):
                    if (l==de):
                        H[med,l]=nbc
                    else:
                        H[med,l]=-1*(A[de,l])    
            med=med+1
        ind=ind+1


    if (existe_medida_fasorial):
        return H
    else:
        Haux=H[:,1:n-1]
        return Haux




def monta_matriz_de_Ganho(H):
    G=np.matmul(np.transpose(H),H)
    return G

def monta_matriz_de_Covariância(G,H):
    I=np.eye(H.shape[0])
    if (teste_observabilidade(G,1.E-10)):
        aux = np.matmul(H,np.linalg.inv(G))
        E= I - np.matmul(aux,np.transpose(H))
    else :
        E=np.zeros(H.shape[0])
    return E  

def teste_observabilidade(G,tol):
    if(np.linalg.det(G)>=tol): 
        return True  
    if(np.linalg.det(G)<tol): 
        #print('Não observável')
        return False 

def calcula_redundancia(m, num_barras,max_med):
    return (m-(num_barras-1))/(max_med-(num_barras-1))

#TODO mudar o nome esta salvando o caso inteiro
def salva_Caso(rede,grupo =''):
    nome_arq = 'Caso' + str(rede.num_barras) +'b'+str(rede.num_medidas)+'m'+grupo+'.txt'
    dados_caso = [rede.num_medidas]

    f = open(nome_arq,'a')
    np.savetxt(f, dados_caso,delimiter=' ',  fmt ='%i')
    np.savetxt(f,rede.plano_med, delimiter=' ',fmt = '%i')
    np.savetxt(f,rede.E, delimiter=' ')
    
    f.close()