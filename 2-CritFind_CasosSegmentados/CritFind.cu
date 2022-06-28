#include <stdio.h>
#include <iostream>

#include<omp.h>
#include<math.h>


//#include "AnalisCrit.h"

//#pragma warning(disable:4996)

#include<string>
#include <fstream>
#include<time.h>
using namespace std;

#define min(a, b) (((a) < (b)) ? (a) : (b))


//Parametros da GPU
#define threadspblock 1024

//Arquivos de entrada
string nomeEntrada = "Caso.txt";

//Arquivos de Saida
string nomeSaida = "Saida.csv";


//Parametros do Sitema
// int nbar;
// int nmed;
// int kmax;
int solSize = 10000;

//Estutura da matriz de resultados de combinações (Cn)
string nomeCnfile = "combs1000em5.txt";
const int rowsCn=1000;
const int colsCn=5;

//Variaveis de percentual
bool p25 = 0;
bool p50 = 0;
bool p75 = 0;


__device__ int critics=0; //  versao de nSols na GPU

//Etapas 
//Enumera Combinacoes 
__global__ void enumerar(int* combs, int card, long long int combsIdini, long long int combsInWave, long long int* Cn, int kmax, int nmed);

//Encontra Combinacoes criticas
__global__ void findcrit(double *E, int *combs, int *isCrit,int card, long long int combsInwave,int kmax, int nmed);

//Confirma Combinacoes criticas
__global__ void removcrit(int *combs, int* conjSol, int* isCrit, int sol, long long int combsInwave,int card, int kmax, int nmed);

//Atualiza Conjunto solucao
__global__ void preScan(int * confirmadosOut,int* confirmados, int* sum, long long int combsInWave);

__global__ void preScanSum(int* confirmados, long long int combsInWave);

__global__ void addScan(int *Aux,int *SUMS, long long int combsInWave);

__global__ void compact(int *combs, int *conjSol, int *isCrit,long long int combsInWave, int  *scaned, int kmax, int nmed);

//// Etapas da Analise de criticalidade
__device__ void d_covarAux(double *Ei, double* E, int* combs, int card, int indc, int kmax, int nmed);

__device__ bool d_isinvertible(double *mat, int m);

__global__ void scan(int *g_odata, int *g_idata, int n, int *sums);
__global__ void scanSum( int *g_idata, int n);




int main()
{
    
    //int nbar = 300;
    int nmed;
    int kmax = 4;

    // Variaveis iniciais
    const long long int wave_size = (int)pow(2, 20);


    //SolStack
    int nSols=0;
    int* Sols;

  
    // Combinacoes pre calculadas (Cn)
    long long int Cn[(rowsCn + 1) * (colsCn + 1)] = { 0 };
    ifstream Cnfile(nomeCnfile.c_str());
	for (int i = 0; i < rowsCn+1; i++)
	{
		for (int j = 0; j < colsCn+1; j++)
		{
			Cnfile >> Cn[i * (colsCn +1) + j];
            //printf("%lld ",Cn[i * (colsCn +1) + j]);
		}
        //printf("\n");
	}
	Cnfile.close();

    //Entrada programa
    ifstream arqEntrada(nomeEntrada);
    //arqEntrada >> nbar;
    arqEntrada >> nmed;
    //arqEntrada >> kmax;

    
    int* med_plan;
    med_plan = (int*)malloc(nmed * 7 *sizeof(int));
    for (int i = 0; i < nmed; i++)
	{
		for (int j = 0; j < 7; j++)
		{
			arqEntrada >> med_plan[i * 7 + j];
            //printf("%d ",med_plan[i * 7 + j]);
		}
        //printf("\n");

	}

    // Matriz Covariancia E
    double* E;
    E = (double*)malloc(nmed * nmed * sizeof(double));
    //lerE(E, nomeEfile, nmed);
    for (int i = 0; i < nmed; i++)
	{
		for (int j = 0; j < nmed; j++)
		{
			arqEntrada >> E[i * nmed + j];
            //printf("%f ",E[i * nmed + j]);
		}
        //printf("\n");
	}

    // Conjunto Solucao
    Sols = (int*)malloc(kmax * solSize * sizeof(int));

    //-----------Alocalcoes na GPU-------------------------------------------------------------
    int* combs; //Combinacoes enumeradas por ondas
    combs = (int*)malloc((size_t)wave_size * kmax * sizeof(int));

    int* isCrit;// Vetor booleano  1: Combinacao critica 0: Combinacao nao 
    isCrit = (int*)malloc(wave_size * sizeof(int));

    //Alocacoes na GPU
	double *d_E;// Matrix de Covariancia
	cudaMalloc(&d_E,nmed*nmed * sizeof(double));
	cudaMemcpy(d_E,E,nmed*nmed * sizeof(double),cudaMemcpyHostToDevice);

	int *d_combs;//Matriz com combinacoes enumeradas
    cudaMalloc(&d_combs,wave_size*kmax * sizeof(int));


	int *d_isCrit;//Matris que indica combinacoes criticas
	cudaMalloc(&d_isCrit,wave_size* sizeof(int));
	//cudaMemset( d_isCrit,0,wave_size* sizeof(int));

	int *d_conjSol;//conjunto solucao
    cudaMalloc(&d_conjSol,solSize*kmax*sizeof(int));
    //cudaMemset((void*)&d_conjSol,1,solSize*nmed*sizeof(int));
    
    long long int *d_Cn;//Combinacoes pré calculadas
    cudaMalloc(&d_Cn,(rowsCn+1)*(colsCn+1)*sizeof( long long int));
    cudaMemcpy(d_Cn,Cn,(rowsCn+1)*(colsCn+1)* sizeof(long long int),cudaMemcpyHostToDevice);

    int* d_SUMS;//Somatórios dos blocos Scan 
    cudaMalloc(&d_SUMS, (wave_size/threadspblock)*sizeof(int));
    
    int* d_Scaned;//Somatórios do Scan 
    cudaMalloc(&d_Scaned, (wave_size)*sizeof(int));

    for (int card = 1; card <=kmax ;card++)
        {
            cout << "cardinalidade " << card;
            cout << ": iniciado...\n";
            long long int totalwaves = 0; // Combinacoes vizitadas em todas as ondas
            //int combsId = 0;    // Identificador de combinacoes :  (1 = 0011) (2 = 0101) ... (6 = 1100) 
            
            while (totalwaves < Cn[nmed * (colsCn + 1) + card])
            {
                long long int combsInWave = min(wave_size, Cn[nmed * (colsCn + 1) + card] - totalwaves); // Combinacoes Visitada em onda
                
                //1-Enumeracao---------------------------
                enumerar<<<wave_size/threadspblock,threadspblock>>>(d_combs, card,totalwaves+1, combsInWave, d_Cn,kmax,nmed);
                
                //2-Procura-------------------------------
                findcrit<<<wave_size/threadspblock,threadspblock>>>(d_E, d_combs, d_isCrit,card,combsInWave,kmax,nmed);

                for (int sol = 0; sol < nSols; sol++) 
                {
                    removcrit<<<wave_size/threadspblock,threadspblock>>>( d_combs, d_conjSol, d_isCrit, sol, combsInWave,card,kmax,nmed);
                }

                //4-Atualizacao do Conjunto Solucao-------
                scan<<<wave_size/threadspblock,threadspblock>>>(d_Scaned,d_isCrit,threadspblock,d_SUMS);
                scanSum<<<1,threadspblock>>>(d_SUMS,threadspblock);
                addScan<<<wave_size/threadspblock,threadspblock>>>(d_Scaned,d_SUMS, combsInWave); 
                compact<<<wave_size/threadspblock,threadspblock>>>(d_combs,d_conjSol, d_isCrit, combsInWave, d_Scaned, kmax, nmed);
            
                totalwaves += wave_size;
                //Printa percentuais para acompanhar andamento da analise de criticalidades
                if (totalwaves > Cn[nmed * (colsCn + 1) + card]/4 && !p25)
                {
                    printf("25%% ->");
                    p25 = 1;
                }
                if (totalwaves > Cn[nmed * (colsCn + 1) + card] / 2 && !p50)
                {
                    printf("50%% ->");
                    p50 = 1;
                }
                if (totalwaves > Cn[nmed * (colsCn + 1) + card] * 3 / 4 && !p75)
                {
                    printf("75%%");
                    p75 = 1;
                }

        }
        printf(" Finalizado\n");
        cudaMemcpyFromSymbol(&nSols, critics, sizeof(int), 0, cudaMemcpyDeviceToHost);
        //Reseta cardinalidades para proxima cardinalidade
        p25 = 0; p50 = 0; p75 = 0;
        //cout <<"\ncrit found "<<conjSol.nSols<< " finalizado.\n" << endl;
        

    }

    cudaMemcpy(Sols,d_conjSol,solSize*kmax* sizeof(int),cudaMemcpyDeviceToHost);
    free(combs);
    free(isCrit);

    //Print Resultados ----------------------------------------------------------------------------------------------
    printf("RESULTADOS:\n");
    printf("Conjunto solucao: %i\n", nSols);
    int ncrits[colsCn];
    for (int i = 0; i < kmax; i++)
        ncrits[i] = 0;
    int card;
    for (int i = 0; i < nSols; i++) {
        card = 0; 
        for (int j = 0; j < kmax; j++) {
            if(Sols[i * kmax + j] !=-1) card++;
        }
        ncrits[card - 1] += 1;
    }
    printf("Cardinalidade -> numero de tuplas criticas\n");
    for (int i = 0; i < kmax; i++)
        printf("%i -> %i\n", i + 1, ncrits[i]);




    printf("total de tuplas criticas : %i\n", nSols);

    //Print Tempos e CSV----------------------------------------------------------------------------------------------

    //asctime(localtime(&timetoday))+
    FILE* Output_file;
    Output_file = fopen(nomeSaida.c_str(), "w");
    fprintf(Output_file ,"Cardinalidade;numero de Cks\n");
    for (int i = 0; i < kmax; i++) {
        fprintf(Output_file ,"%i;%i\n", i + 1, ncrits[i]);
    }
    fprintf(Output_file ," total de tuplas criticas : %i\n", nSols + 1);

    fprintf(Output_file, "numero de combinacoes analisadas por cardinalidade\n");
    for (int i = 1; i <= kmax; i++)
        fprintf(Output_file, "%i; %lld\n", i, Cn[nmed * (colsCn + 1) + i]);

    for (int i =0; i < nSols; i++)
    {
        int k = 0;
        for (int j =0; j < kmax; j++)
        {
            int medida = Sols[i* kmax + j];
            if(medida != -1)
            {
                if(med_plan[medida*7 + 4] == 1) fprintf(Output_file,"F(%i-%i) ",med_plan[medida*7 + 1],med_plan[medida*7 + 2]);
                if(med_plan[medida*7 + 4] == 2) fprintf(Output_file,"I(%i) ",med_plan[medida*7 + 2]);
                if(med_plan[medida*7 + 4] == 3) fprintf(Output_file,"A(%i) ",med_plan[medida*7 + 2]);
            }
            else
            {
                k++;
            }
            
        }
        fprintf(Output_file,";");
        for (int j =0; j < kmax; j++)
        {
            int medida = Sols[i* kmax + j];
            if(medida != -1) fprintf(Output_file,"%i;",med_plan[medida*7]);
            else fprintf(Output_file,"-;");
            
        }
        fprintf(Output_file,"%i \n",kmax - k);
    }
    fclose(Output_file);


    cudaFree(d_conjSol);
	cudaFree(d_isCrit);
	cudaFree(d_E);
    cudaFree(d_combs);
    cudaFree(d_Cn);
    cudaFree(d_SUMS);
    cudaFree(d_Scaned);


}

//Etapas
__global__ void enumerar(int* combs, int card, long long int combsIdinicial,long long int combsInWave, long long int* Cn,int kmax , int nmed)
{
    int linha = threadIdx.x + blockDim.x*blockIdx.x;
    if(linha<combsInWave)
    {
        int nZ = nmed - card;
        int nO = card;
        long long int n = linha + combsIdinicial;
        for (long long int i = 0; i < nmed; i++)
        {
            nZ--;
            long long int zcomb = Cn[(nmed - 1 - i) * (colsCn + 1) +  min(nZ, nO)];
            if (zcomb < n)
            {
                combs[linha * kmax + (card-nO)] = i;
                nO--;
                nZ++;
                n = n - zcomb;
            }
        }
        for(int j=card; j<kmax;j++) {
            combs[linha * kmax + j] = -1;
        }
        
    }   
    
    //printf("\n");

    
    
}
__global__ void findcrit(double *E, int *combs,int *isCrit, int card1, long long int combsInwave,int kmax,int nmed)
{
    int ind = threadIdx.x + blockDim.x*blockIdx.x;
    
    if(ind<combsInwave){
		
        double Ei[colsCn*colsCn];
    		
        d_covarAux(Ei, E, combs, card1, ind,kmax,nmed);
        
        if (!(d_isinvertible(Ei, card1))) {
            isCrit[ind] = 1;
        }
        else {
            isCrit[ind] = 0;
		}
		
		
        free(Ei);
       
    }
}
__global__ void removcrit(int *combs, int* conjSol, int* isCrit, int sol, long long int combsInwave, int card, int kmax, int nmed)
{
    int crit = threadIdx.x + blockDim.x*blockIdx.x;
   
    if(isCrit[crit]==1)
    {
        int is = 0;
        int i = 0;
        int j = 0;
        while(conjSol[sol * kmax + i]!=-1 && i<card)
        {
            for (j = 0; j < card; j++)
            {
                if (conjSol[sol * kmax + i]==combs[crit*kmax+j])
                    break;
            }


            if (j == card)
                is = 1;
            i++;
        }
        isCrit[crit] = is;
    }
}



//Analise de Criticalidade
__device__ bool d_isinvertible(double *mat, int m) 
{

	bool inv;
	double pivo = 0.;
	for (int i = 0; i < m; i++) {

        //pivotiamento 
		int indmaior = i;
		double maior = mat[i * colsCn + i];
		for (int j = i; j < m; j++)
		{
			if (abs(maior) < abs(mat[j * colsCn + i]))
			{
				maior = mat[j * colsCn + i];
				indmaior = j;
			}
		}
		for (int j = 0; j < m; j++)
		{
			double swap = mat[i * colsCn + j];
			mat[i * colsCn + j] = mat[indmaior * colsCn + j];
			mat[indmaior * colsCn + j] = swap;
		}
		
		pivo = mat[i*colsCn + i];

		if (abs(pivo) < 0.0000000001) {
			inv = 0;
			return inv;
		}

		for (int j = 0; j < m; j++) {
			mat[i*colsCn + j] = mat[i*colsCn + j] / pivo;

		}


		for (int j = 0; j < m; j++) {
			if (j != i) {
				pivo = mat[j*colsCn + i];
				for (int l = 0; l < m; l++) {
					mat[j*colsCn + l] = mat[j*colsCn + l] - pivo * mat[i*colsCn + l];
				}
			}
		}

	}

	inv = 1;
	return inv;
}
__device__ void d_covarAux(double *Ei, double* E, int* combs, int card, int indc, int kmax, int nmed) 
{

    for (int i = 0; i < card; i++)
	{
		for (int j = 0; j < card; j++)
		{
			int m = combs[indc * kmax + i];
			int n = combs[indc * kmax + j];

			
			Ei[i * colsCn + j] = E[m * nmed + n];
		}
		
	}

}

__global__ void scan(int *g_odata, int *g_idata, int n, int *sums) 
{   
    __shared__ int temp[2*threadspblock]; 
    // allocated on invocation    
    int thid = threadIdx.x; 
    int blid = blockIdx.x;  
    int pout = 0, pin = 1;   
    // Load input into shared memory.    
    // This is exclusive scan, so shift right by one    
    // and set first element to 0   
    temp[pout*n + thid] = g_idata[thid+blid*blockDim.x] ; 
    temp[pin*n + thid] = 0;//g_idata[thid+blid*blockDim.x] ;   
    __syncthreads();
        
    for (int offset = 1; offset < n; offset *= 2)   
    {     
        pout = 1 - pout; 
        // swap double buffer indices     
        pin = 1 - pout;     
        if (thid >= offset)       
            temp[pout*n+thid] = temp[pin*n+thid - offset]+temp[pin*n+thid];     
        else       
            temp[pout*n+thid] = temp[pin*n+thid];     
        
        //if(blid==1&&thid<10) printf ("%i::%i ",thid, temp[pout*n + thid]); 
        __syncthreads();
        //if(blid==1&&thid==0)printf("\n");   
    }   
        g_odata[thid+blid*blockDim.x] = temp[pout*n+thid]; 
        // write output 
    if (thid==0)
    {
        sums[blid]=temp[n-1];
    }
    
}
__global__ void scanSum( int *g_idata, int n) 
{   
    __shared__ int temps[2*threadspblock]; 
    // allocated on invocation    
    int thid = threadIdx.x; 
    int pout = 0, pin = 1;   
    // Load input into shared memory.    
    // This is exclusive scan, so shift right by one    
    // and set first element to 0   
    temps[pout*n + thid] = g_idata[thid] ; 
    temps[pin*n + thid] = 0;  
    __syncthreads();   
    for (int offset = 1; offset < n; offset *= 2)   
    {     
        pout = 1 - pout; 
        // swap double buffer indices     
        pin = 1 - pout;     
        if (thid >= offset)       
            temps[pout*n+thid] = temps[pin*n+thid - offset]+temps[pin*n+thid];     
        else       
            temps[pout*n+thid] = temps[pin*n+thid];     
        
        __syncthreads();   
    }   
        g_idata[thid] = temps[pout*n+thid]; 
       
        
}

//Atualiza Conjunto solucao 
__global__ void preScan(int * confirmadosOut,int* confirmados, int* sum, long long int combsInWave)
{
    int tid = threadIdx.x;
    int bid= blockIdx.x;
    
    int id = tid+blockDim.x*bid;
   
    __shared__ int temp[threadspblock];
    //if (id<combsInWave){
        temp[tid]=confirmados[id];
        
        __syncthreads();  

        for (int offset = 1; offset < threadspblock; offset *= 2)   
        { 
            
            if(tid>=offset)
                temp[tid]+=temp[tid-offset];
        

            __syncthreads();  
        }
        //__syncthreads(); 
        
        if(tid==0){
            //sum[0]=0;
            //temp[0]=0;
            sum[bid]=temp[threadspblock-1];
            //printf("::%i - %i\n",sum[bid],bid);
        }
        confirmadosOut[id]=temp[tid];
    //}   

}
__global__ void preScanSum(int* confirmados, long long int combsInWave)
{
    int tid = threadIdx.x;
    int bid= blockIdx.x;
    
    int id = tid+blockDim.x*bid;
   
    __shared__ int temp[threadspblock]; 
    if (id<combsInWave){
        temp[tid]=confirmados[id];
        
        __syncthreads();  

        for (int offset = 1; offset < threadspblock; offset *= 2)   
        { 
            
            if(tid>=offset)
                temp[tid]+=temp[tid-offset];
        

            __syncthreads();  
        }
        
        confirmados[id]=temp[tid];
    }   
}

__global__ void addScan(int *Aux,int *SUMS, long long int combsInWave)
{
    int thid= threadIdx.x;
    int bid = blockIdx.x;
    int id = thid + bid*blockDim.x;
    if(id<combsInWave ){
    
        Aux[id]+=critics;
        if( bid>0)
            Aux[id]+=SUMS[bid-1];
        
    }
}

__global__ void compact(int *combs, int *conjSol, int *isCrit,long long int combsInWave, int  *scaned, int kmax, int nmed)
{
    int index =threadIdx.x + blockDim.x*blockIdx.x;
    
    if(index<combsInWave)
    {
        //printf("ev=%i",isCrit[index]);
        if(isCrit[index]==1)
        {
            int idSol=scaned[index]-1;
            for(int i = 0; i<kmax;i++){
                conjSol[idSol*kmax+i]=combs[index*kmax+i];
                
            }
            atomicAdd(&critics, 1);
            
            
        }
    }
}
