import numpy as np

def build_jacobian_matrix(A,meas_plan):
    n_med=int(sum(meas_plan[:,6]))
    n=A.shape[0]
    H=np.zeros([n_med,n])#nao precisa de ref pois possui medida fasorial
    Haux= np.zeros([n_med,n-1])
    ind=0
    med=0
    existe_medida_fasorial = False
    while (med<n_med):

        if (meas_plan[ind,6]==1):#indica se a medida esta ligada ou desligada

            de=int(meas_plan[ind,1])-1
            para=int(meas_plan[ind,2])-1

            if (de!=para): #serve para medida de fluxo de potencia e de corrente
                H[med,de]=1
                H[med,para]=-1

            if (de==para)and(meas_plan[ind,4]==3):#medida de angulo
                 H[med,de]=1
                 existe_medida_fasorial =True

            if (de==para)and(meas_plan[ind,4]==2):#medida de injecao de Potencia
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

def build_gain_matrix(H):
    G=np.matmul(np.transpose(H),H)
    return G

def build_covariance_matrix(G,H):
    I=np.eye(H.shape[0])
    if (test_observability(G,1.E-10)):
        aux = np.matmul(H,np.linalg.inv(G))
        E= I - np.matmul(aux,np.transpose(H))
    else :
        E=np.zeros(H.shape[0])
    return E  

def test_observability(G,tol):
    if(np.linalg.det(G)>=tol): 
        return True  
    if(np.linalg.det(G)<tol): 
        print('UNOBSERVABLE SYSTEM')
        return False 

def calculate_redundancy(m, nb,max_meas):
    return (m-(nb-1))/(max_meas-(nb-1))

