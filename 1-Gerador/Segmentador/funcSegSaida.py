import numpy as np



def salva_sub_plano_med(rede, grupos):

    sub_planos = []

    for i in range(len(grupos)):
        
        sub_med_plan = monta_sub_med_plan(rede,grupos[i])
        n_med= len(sub_med_plan)
        dados_caso = [n_med]

        nome_arquivo=f'medplan{i+1}_{n_med}m.txt'
        f=open(nome_arquivo,'a')
        np.savetxt(f, dados_caso,delimiter=' ',  fmt ='%i')
        np.savetxt(f,sub_med_plan, delimiter=' ', fmt='%i')
        sub_planos.append(sub_med_plan)
        f.close()

    return sub_planos

def monta_sub_med_plan(rede,grupo):
    med = rede.plano_med
    sub_med_plan =  []

    
    for medida in med:
        if medida[1] in grupo or medida[2] in grupo:
            sub_med_plan.append(medida)


    

    
    return sub_med_plan

def salva_sub_covariancia(E,planos_med):
    n_grupos = len(planos_med)

    for i in range(n_grupos):
        n_med =  len(planos_med[i])
        Eg = monta_Sub_Covax(planos_med[i],E)

        
        nome_arquivo=f'medplan{i+1}_{n_med}m.txt'
        f = open(nome_arquivo,'a')
        
        np.savetxt(f,Eg,delimiter=' ')
        f.close()

#Monta Matriz de Covariância do Subsistemas de medição
def monta_Sub_Covax ( med, E):

    # Constroi Matrizes E dos subsistemas
    #array =  np.arange(len(med)*len(med)).reshape(len(med),len(med))
    Eg = np.zeros((len(med),len(med)),np.float64)
    lin = 0
    for medi in med:
        col = 0
        for medj in med :
            de   = medi[0]-1 
            para = medj[0]-1
            Eg[lin,col] =  E[de,para]
            col = col + 1
        lin = lin + 1
    
    return Eg;