// Integrantes: Mario Gonzalez Galdames - Luis Inostroza Flores
#include "omp.h"
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#define T 8
#define DIM 20


float euclidiana(float * valores, float * valores2){ //Funcion que calcula la distancia euclidiana entre 2 vectores
    int i = 0;
    float x = 0;
    float resultado;
    for (i = 0; i < DIM; i++){
        x = x + pow(valores[i] - valores2[i], 2);
    }
    resultado = sqrt(x);
    return resultado;
}

int main (int argc, char **argv){//Declarancion de variables a utilizar durante el programa
    int cant_datos, i, j, matriz_distancias;
    float **bd1;
    float **bd_consultas;
    float **bd_pivotes;
    int num_consultas;
    int num_pivotes;
    float radio;
    float **bd_consultas2;
    float **bd_matrizdistancias;
    int flag_descarte;

//-------------Lectura de datos ----------------------

    scanf("%d", &cant_datos);
    bd1 = (float **)malloc(sizeof(float *)*cant_datos);
    for (i=0; i < cant_datos; i++){
        bd1[i] = (float *)malloc(sizeof(float)*DIM);
    }
    for (i=0; i < cant_datos; i++){
        for (j = 0; j < DIM; j++)
            scanf("%f", &(bd1[i][j]));
    }
    /*for (i=0; i < cant_datos; i++){
        for (j = 0; j < DIM; j++)
            printf("%.3f", bd1[i][j]);
            printf("\n");
			printf("\n");
    }*/
    scanf("%d", &num_pivotes);
    matriz_distancias = num_pivotes * cant_datos;
    float Bd_dist[matriz_distancias];
    for (i=0; i < matriz_distancias; i++){
        scanf("%f", &Bd_dist[i]);
        /*printf("%.3f ", Bd_dist[i]);
        cont = cont + 1;
        if (cont % 20 == 0){
        printf("\n");
        }*/
        
    }
    bd_pivotes = (float **)malloc(sizeof(float *)*num_pivotes);
    for (i=0; i < num_pivotes; i++){
        bd_pivotes[i] = (float *)malloc(sizeof(float)* DIM);
    }

    for (i=0; i < num_pivotes; i++){
        for (j=0; j < DIM; j++){
            scanf("%f", &bd_pivotes[i][j]);
            //printf("%f ", bd_pivotes[i][j]);
        }
    }

    scanf("%d", &num_consultas);

    bd_consultas = (float **)malloc(sizeof(float *)*num_consultas);
    for (i=0; i < num_consultas; i++){
        bd_consultas[i] = (float * )malloc(sizeof(float)*(DIM+1));
    }

    bd_consultas2 = (float **)malloc(sizeof(float *)*num_consultas);
    for (i=0; i < num_consultas; i++){
        bd_consultas2[i] = (float * )malloc(sizeof(float)*(DIM));
    }

    for (i=0; i < num_consultas; i++){
        for (j=0; j < (DIM+1); j++){

            scanf("%f", &bd_consultas[i][j]);
            //printf("%.3f ", bd_consultas[i][j]);
        }
        //printf("\n");
    }



    for (i=0; i < num_consultas; i++){ //Limpiamos el radio de los vectores consultas
        for (j=0; j < DIM; j++){
            bd_consultas2[i][j] = bd_consultas[i][j+1];
            //printf("%.3f ", bd_consultas2[i][j]);
        }
    }

    bd_matrizdistancias = (float **)malloc(sizeof(float *)*num_consultas);
    for (i=0; i < num_consultas; i++){
        bd_matrizdistancias[i] = (float * )malloc(sizeof(float)*(num_pivotes));
    }

    //DISTRIBUCION
    omp_set_num_threads(T);


    #pragma omp parallel shared(bd_matrizdistancias)
    {
        #pragma omp for schedule(dynamic)//Se distribuyen los calculos de forma arbitraria por la directiva
            //PUNTO 1
            for (int k=0; k < num_consultas; k++){//Construccion de matriz de distancia entre vectores consultas y pivotes
                for (int l=0; l < num_pivotes; l++){
                    bd_matrizdistancias[k][l] = euclidiana(bd_consultas2[k], bd_pivotes[l]);
                    //printf("%.3f ", bd_matrizdistancias[i][j]);
                }
                //printf("\n");
            }
        
        #pragma omp barrier
    }

    /*for (int m=0; m < num_consultas; m++){
        printf("c%d: ", m);
        for (int n=0; j < (num_pivotes); j++){
            printf("%.3f ", bd_matrizdistancias[i][j]);
        }
        printf("\n");
    }
    */
    // PUNTO 2
    radio = bd_consultas[0][0];
    #pragma omp parallel shared(bd_matrizdistancias)
    {
        int descartados_totales = 0;
        int totales = 0;
        int cont2 = 0;
        #pragma omp for schedule(dynamic)//Se distribuyen los calculos de forma arbitraria por la directiva

        for(int i = 0; i < num_consultas; i++){//Implementacion del algoritmo 1
            int elem_descartados = 0, elementos = 0;
            for(int j = 0; j < cant_datos; j++){
                int flag_descarte = 0;
                for(int k = 0; k < num_pivotes; k++){
                    cont2++;
                    if (bd_matrizdistancias[i][k] + radio < euclidiana(bd1[j], bd_pivotes[k]) || bd_matrizdistancias[i][k] - radio > euclidiana(bd1[j], bd_pivotes[k])){
                        flag_descarte = 1;
                        elem_descartados++;
                        break;
                    }
                }
                if (flag_descarte ==1){
                    continue;
                }
                

                if (euclidiana(bd_consultas2[i], bd1[j]) < radio){
                    elementos++;
                }
            }
            printf("Consulta N°:%d, Cantidad de elementos resultantes: %d\n", i, elementos);
            descartados_totales = descartados_totales + elem_descartados;
            totales = totales + elementos;
            
        }
        #pragma omp master
        {
            printf("\nElementos descartados en total: %d\n", descartados_totales);
        }
    }
}
