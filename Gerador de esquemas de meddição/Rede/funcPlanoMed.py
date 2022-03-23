import numpy as np
from random import seed
from random import sample
import os


from .funcObservabilidade import*





def gerar_plano_med(Rede,redundancia,semente = 5):

        seed(semente)

        #inicializa plano de medição "cheio" com todas medidas desativadas
        Rede.plano_med = gera_plano_vazio(Rede.Y_barra,Rede.max_med)
        Rede.num_medidas = 0
        Rede.observavel = False
        redundancia_atual = 0

        medidas_nao_sorteadas = [i for i in range(1,Rede.max_med+1)]

        while(not Rede.observavel and redundancia_atual < redundancia):
            #TODO Diminuir esta parte
            med_sorteada = sample(medidas_nao_sorteadas, 1)
            medidas_nao_sorteadas = [barra for barra in medidas_nao_sorteadas if barra not in med_sorteada]

            Rede.num_medidas += adiciona_medida(Rede.plano_med,med_sorteada[0])
            redundancia_atual =  calcula_redundancia(Rede.num_medidas,Rede.num_barras,Rede.max_med)

            H = monta_Jacobiana(Rede.Y_barra,Rede.plano_med)
            G = monta_matriz_de_Ganho(H)
            Rede.observavel = teste_observabilidade(G,1.E-10)
        
        return Rede.plano_med

def gera_plano_vazio(A, max_med):
    med_plan = np.zeros([max_med,7],np.int32)
    medida = 0

    num_barras = len(A)
    #medidas de fluxo
    for linha in range(num_barras):
        for col in range(num_barras):
            if(A[linha][col] == 1):
                de = linha+1
                para = col+1
                med_plan[medida][0] = medida+1
                med_plan[medida][1] = de
                med_plan[medida][2] = para
                med_plan[medida][3] = 1
                med_plan[medida][4] = 1
                med_plan[medida][5] = de
                med_plan[medida][6] = 0
                
                medida = medida + 1

    #medidas de injeção
    for linha in range(num_barras):
        barra = linha+1
        med_plan[medida][0] = medida + 1
        med_plan[medida][1] = barra
        med_plan[medida][2] = barra
        med_plan[medida][3] = 1
        med_plan[medida][4] = 2
        med_plan[medida][5] = barra
        med_plan[medida][6] = 0
        
        medida = medida + 1

    return med_plan

def adiciona_medida(med_plan, medida):
       

    if med_plan[medida-1,6] == 0 : 
        med_plan[medida-1,6] = 1 
        return 1
    else :
        return 0

def gera_plano_UM_completa(Rede,redundancia,semente = 5):

    seed(semente)

    #inicializa plano de medição "cheio" com todas medidas desativadas
    Rede.plano_med = gera_plano_vazio(Rede.Y_barra,Rede.max_med)
    Rede.num_medidas = 0
    Rede.observavel = False
    redundancia_atual = 0

    barras_nao_sorteadas = [i for i in range(1,Rede.num_barras+1)]

    while(not Rede.observavel and redundancia_atual < redundancia):
            #TODO Diminuir esta parte
            barra_sorteada = sample(barras_nao_sorteadas, 1)
            barras_nao_sorteadas = [barra for barra in barras_nao_sorteadas if barra not in barra_sorteada]

            Rede.num_medidas += adiciona_UM(Rede.plano_med,barra_sorteada[0])
            redundancia_atual =  calcula_redundancia(Rede.num_medidas,Rede.num_barras,Rede.max_med)

            H = monta_Jacobiana(Rede.Y_barra,Rede.plano_med)
            G = monta_matriz_de_Ganho(H)
            Rede.observavel = teste_observabilidade(G,1.E-10)
        
    return Rede.plano_med

def adiciona_UM(med_plan, num_barr):
    medidas_adicionadas = 0
    for linha in med_plan:
        if(linha[1] ==num_barr ):#or linha[2] == num_barr): 
            if linha[6] == 0 : 
                medidas_adicionadas=medidas_adicionadas + 1
                linha[6] = 1 
    return medidas_adicionadas

def remove_medidas_desativaddas(Rede): #arquivo apenas com as medidas ativadas
    medidas_desativadas = []
    num_medidas_desativadas = 0
    cont = 0
    for line in Rede.plano_med:
        if line[6] == 0:
            medidas_desativadas.append(cont)
            num_medidas_desativadas += 1
        cont = cont + 1

    #Deleta medidas da lista
    Rede.plan_med = np.delete(Rede.plano_med,medidas_desativadas, axis=0)
    #Corrige contagem inicial
    for i in range(Rede.plan_med.shape[0]):
        Rede.plan_med[i,0] = i + 1
    return Rede.plan_med

def gera_plano_concentrado(Rede,redundancia, barras_preferidas,barras_excluidas, semente = 5):
    np.random.seed(semente)

    #inicializa plano de medição "cheio" com todas medidas desativadas
    Rede.plano_med = gera_plano_vazio(Rede.Y_barra,Rede.max_med)
    Rede.num_medidas = 0
    Rede.observavel = False
    redundancia_atual = 0

    medidas = range (1,Rede.max_med+1)
    
    pesos = monta_lista_pesos(Rede.plano_med, barras_preferidas,barras_excluidas)

    

    while(not Rede.observavel or redundancia_atual < redundancia):
        #TODO Diminuir esta parte
        med_sorteada = np.random.choice(medidas, 1, p=pesos)
        #medidas_nao_sorteadas = [barra for barra in medidas_nao_sorteadas if barra not in med_sorteada]
        #print(Rede.plano_med[med_sorteada[0]-1])
        Rede.num_medidas += adiciona_medida(Rede.plano_med,med_sorteada[0])
        redundancia_atual =  calcula_redundancia(Rede.num_medidas,Rede.num_barras,Rede.max_med)

        H = monta_Jacobiana(Rede.Y_barra,Rede.plano_med)
        G = monta_matriz_de_Ganho(H)
        Rede.observavel = teste_observabilidade(G,1.E-10)

    Rede.E = monta_matriz_de_Covariância(G,H)    
    return Rede.plano_med


def monta_lista_pesos(plano_med,barras_preferidas,barras_exlucidas):

    extra = 10

    num_med_preferidas = 0
    num_med_excluidas = 0
    for medida  in plano_med:
        if(medida[1] in  barras_preferidas): 
            num_med_preferidas +=1
        elif(medida[1] in barras_exlucidas):
            num_med_excluidas +=1
    
    num_med = len(plano_med)
    peso_unitario = 1/(num_med + num_med_preferidas*(extra-1)-num_med_excluidas)

    pesos = [peso_unitario]*num_med
    i = 0
    for medida  in plano_med:
        if(medida[1] in  barras_preferidas): 
            pesos[i] = pesos[i]*extra
        elif(medida[1] in barras_exlucidas):
            pesos[i] = 0
        i+=1

    return pesos


def salva_txt_planomed(Rede):
    nome_arquivo ='med'+ str(Rede.num_barras)+'b'+str(Rede.num_medidas)+'m.txt'
    dados_caso = [Rede.num_medidas]
    f=open(nome_arquivo,'a')
    np.savetxt(f, dados_caso,delimiter=' ',  fmt ='%i')
    np.savetxt(nome_arquivo,Rede.plano_med,delimiter=' ',fmt = '%i')

    f.close()

def complementar_plano_med(Rede,semente = 5):

        seed(semente)

        #inicializa plano de medição "cheio" com todas medidas desativadas
        #Rede.plano_med = gera_plano_vazio(Rede.Y_barra,Rede.max_med)
        #Rede.num_medidas = 0
        Rede.observavel = False
        

        medidas_nao_sorteadas = [i for i in range(1,Rede.max_med+1)]

        while(not Rede.observavel):
            #TODO Diminuir esta parte
            med_sorteada = sample(medidas_nao_sorteadas, 1)
            medidas_nao_sorteadas = [barra for barra in medidas_nao_sorteadas if barra not in med_sorteada]

            Rede.num_medidas += adiciona_medida(Rede.plano_med,med_sorteada[0])
            
            H = monta_Jacobiana(Rede.Y_barra,Rede.plano_med)
            G = monta_matriz_de_Ganho(H)
            Rede.observavel = teste_observabilidade(G,1.E-10)
            
        Rede.E = monta_matriz_de_Covariância(G,H)
        return Rede.plano_med

def completar_plano_UM_completa(Rede,semente = 5):

    seed(semente)

    Rede.observavel = False
    redundancia_atual = 0

    barras_nao_sorteadas = [i for i in range(1,Rede.num_barras+1)]

    while(not Rede.observavel ):
            #TODO Diminuir esta parte
            barra_sorteada = sample(barras_nao_sorteadas, 1)
            barras_nao_sorteadas = [barra for barra in barras_nao_sorteadas if barra not in barra_sorteada]

            Rede.num_medidas += adiciona_UM(Rede.plano_med,barra_sorteada[0])
            
            H = monta_Jacobiana(Rede.Y_barra,Rede.plano_med)
            G = monta_matriz_de_Ganho(H)
            Rede.observavel = teste_observabilidade(G,1.E-10)

    Rede.E = monta_matriz_de_Covariância(G,H)    
    return Rede.plano_med