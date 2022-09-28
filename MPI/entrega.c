#include "mpi.h"
#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#define DIM 20

int main (int argc, char **argv)
{
	int nproc; /* Número de procesos */
	int yo; /* Mi dirección: 0<=yo<=(nproc-1) */
	int dato[10], dato_recibido[10], i, j,k,  flag=0, arr_buf[100], contador;
	MPI_Status st, st2;
	MPI_Request mpirq;
	int N_DATOS;
    float K;
	float **BD;


	MPI_Init(&argc, &argv);
	MPI_Comm_size(MPI_COMM_WORLD, &nproc);
	MPI_Comm_rank(MPI_COMM_WORLD, &yo);
	if (yo == 0)
	{
		scanf("%d", &N_DATOS);
		scanf("%f", &K);

		BD = (float **)malloc(sizeof(float *)*N_DATOS);
		for (i=0; i < N_DATOS; i++)
			BD[i] = (float *)malloc(sizeof(float)*DIM);

		for (i=0; i < N_DATOS; i++)
			for (j=0; j < DIM; j++)
				scanf("%f", &(BD[i][j]));
		printf("Nodo[%d] :: N_DATOS = %d, K = %f, Vectores:\n", yo, N_DATOS, K);
		//imprime primera lista
		/*for (i=0; i < N_DATOS; i++)
		{
			for (j=0; j < DIM; j++)
				printf("%.3f ", BD[i][j]);
			printf("\n");
			printf("\n");
		}*/
	}
	MPI_Barrier(MPI_COMM_WORLD);

	if (yo == 0)
	{
		//Se envia la Base de Datos a cada nodo
		for (i=1; i < nproc; i++)
		{
			MPI_Send(&N_DATOS, 1, MPI_INT, i, 100, MPI_COMM_WORLD);
            MPI_Send(&K, 1, MPI_FLOAT, i, 100, MPI_COMM_WORLD);
			for (j=0; j < N_DATOS; j++)
				MPI_Send(BD[j], DIM, MPI_FLOAT, i, 100, MPI_COMM_WORLD);
		}
	}
	else
	{
        float **BD2;
        float M, p0;
        int N_DATOS3;


        MPI_Recv(&N_DATOS3, 1, MPI_INT, 0, 100, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        MPI_Recv(&M, 1, MPI_FLOAT, 0, 100, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        
		BD2 = (float **)malloc(sizeof(float *)*N_DATOS3);

		for (i=0; i < N_DATOS3; i++){
			BD2[i] = (float *)malloc(sizeof(float)*DIM); 
			}

		for (i=0; i < N_DATOS3; i++){
			MPI_Recv(BD2[i], DIM, MPI_FLOAT, 0, 100, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
		}
		//lista recibida
		float num[DIM], eucli, resul;

        for (i=0; i < N_DATOS3; i++)
		{

			for (j=0; j < DIM; j++)
			{
				//distancia euclidiana
				eucli = 0;
				resul = 0;
				
				for(k=0; k<DIM; k++)
				{
					eucli += ((BD2[i][k]-BD2[0][k])*(BD2[i][k]-BD2[0][k]));
				}
		
			}
		resul = sqrt(eucli);
		printf("%.3f", resul);
		printf("\n");
			// el primer pivote
				//num[j]=BD2[0][j];
			//printf("%.3f\n", p0);
			//printf("\n");
			//printf("\n");
		}
		//for (i=0; i<DIM ; i++){
			//printf("p0 es: %f ", num[i]);*/
		//}
    }
	MPI_Finalize();
	return 0;
}

//Compilacion: mpicc prog.c
//Ejecucion: mpirun -np 8 a.out
//
//
//
//
//
