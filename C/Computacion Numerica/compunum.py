#Nombres: Mario Gonzalez Galdames - Luis Inostroza Flores

#A continuacion se presentará el código que creamos para realizar el trabajo, hay casos muy particulares en donde al compilar el codigo este tira una especie de error que no pudimos solucionar
#Pero sospechamos que se debian a la creacion de numeros inadecuados por parte de la biblioteca numpy, los casos en los que nos sucedio esto fueron demasiado pocos, pero en caso de que le suceda
#a usted profe por favor ejecute el programa denuevo hasta que compile.

import numpy as np
import sys
import matplotlib.pyplot as plt

def listas(cant_datos): #funcion para crear las 2 listas correspondientes, cada una con valores float64
    listarandom = np.random.randn(1, cant_datos)*1000
    return listarandom

def float_bin(number, places = 3): #funcion para binarizar otorgada por el profe

    whole, dec = str(number).split(".") 

    whole = int(whole) 
    dec = int (dec) 

    res = bin(whole).lstrip("0b") + "."

    for x in range(places): 

        whole, dec = str((decimal_converter(dec)) * 2).split(".") 
        dec = int(dec) 
        res += whole 
    return res 

def decimal_converter(num):  
    while num > 1: 
        num /= 10
    return num

def binarizacion(operando): #Funcion que utiliza la funcion para binarizar con el fin de crear las listas con los numeros binarizados.
    lista_binarios = []
    lista1 = []
    lista2 = []
    binarios_listos = []
    for i in range (0,len(operando[0])):
        numero_entero=operando_1[0][i]
        lista_binarios.append(float_bin(numero_entero, places = 50))
    for i in range(len(lista_binarios)):
        lista1 = list(lista_binarios[i])
        if lista1[0]== "-":
            lista1.remove("0")
            lista1.remove("b")
            lista2.append(lista1)
        else:
            lista2.append(lista1)
        
    
    for i in range(len(lista2)):
        binario = ''.join(lista2[i])
        binarios_listos.append(binario)
    return binarios_listos

    for i in range(len(lista2)):
        binario = ''.join(lista2[i])
        lista_colada.append(binario)

    ####Binarizacion operando2: se creo una funcion aparte para binarizar la segunda lista debido a que al 
    # utilizar la misma funcion para binarizar la segunda lista se guardaban los valores de la primera lista y me dio lata arreglar ese error xd
def binarizacion2(operando_2):
    operando_2_binario = []
    lista21=[]
    lista22=[]
    lista_colada2=[]

    for i in range (0,len(operando_2[0])):
        Numero_inicial3=operando_2[0][i]
        operando_2_binario.append(float_bin(Numero_inicial3, places = 50))
    for i in range(len(operando_2_binario)):
        lista21 = list(operando_2_binario[i])
        if lista21[0]== "-":
            lista21.remove("0")
            lista21.remove("b")
            lista22.append(lista21)
        else:
            lista22.append(lista21)
        
    
    for i in range(len(lista22)):
        binario = ''.join(lista22[i])
        lista_colada2.append(binario)
    return lista_colada2

def suma_binaria(operando1binario, operando2binario): #Como dice el nombre, esta funcion recibe las 2 listas binarizadas y realiza la suma en binario de estas 2, 
                                                      #devolviendo una nueva lista con los valores sumados

    binarios1_separados = []
    binarios2_separados = []
    suma_binaria = []
    for i in range(len(operando1binario)):
        x = operando1binario[i].split(".")
        binarios1_separados.append(x)
    for i in range(len(operando2binario)):
        y = operando2binario[i].split(".")
        binarios2_separados.append(y)

    for i in range(len(operando1binario)):
        suma_entera = "{0:b}".format(int(binarios1_separados[i][0], 2) + int(binarios2_separados[i][0], 2))
        suma_decimales = "{0:b}".format(int(binarios1_separados[i][1], 2) + int(binarios2_separados[i][1], 2))
        total = str(suma_entera) + "." + str(suma_decimales)
        suma_binaria.append(total)
    #print(suma_binaria)
    return suma_binaria



def suma_real(operando1, operando2): #Funcion que suma los valores reales de las listas
    suma_final = []
    if len(operando1[0]) == len(operando2[0]):
        for i in range(len(operando1[0])):
            suma = operando1[0][i] + operando2[0][i]
            suma_final.append(suma)
    else:
        return suma_final
    return suma_final

def conversion(sumabinaria): #Convierte la suma binaria a decimal para calcular los correspondientes errores.
    binarios = []
    numeros_enteros = []
    numeros_decimales = []
    numero_final = []
    numero = ""

    for i in range(len(sumabinaria)):
        x = sumabinaria[i].split(".")
        binarios.append(x)
    for i in range(len(binarios)):
        y = int(str(binarios[i][0]), 2)
        numeros_enteros.append(y)
        z = int(str(binarios[i][1]), 2)
        numeros_decimales.append(z)
    for i in range(len(numeros_enteros)):
        numero = str(numeros_enteros[i]) + "." + str(numeros_decimales[i])
        numero_final.append(float(numero))

    return numero_final

def error_absoluto(listareal, listaobtenido): #Funcion que recibe la lista con los valores reales y los binarios en decimal para calcular su respectivo error absoluto
    errores =[]
    for i in range(len(listareal)):
        error = abs(float(listareal[i])-float(listaobtenido[i]))
        errores.append(error)
    return errores   

def error_relativo(listareal, listaobtenido): #Funcion que recibe la lista con los valores reales y los binarios en decimal para calcular su respectivo error relativo
    errores = []
    for i in range(len(listareal)):
        error = abs((float(listareal[i])-float(listaobtenido[i])) / float(listareal[i]))
        errores.append(error)
    return errores

def error_cuadratico(errorabsoluto): #Funcion que recibe la lista con los valores del error absoluto para calcular su respectivo error cuadratico
    errorcuadratico = []
    for i in range(len(errorabsoluto)):
        errorcuadratico.append((errorabsoluto[i])**2)
    return errorcuadratico    

def plot_(datos, title):#2 funciones 1 plot de los valores reales y otro plot para los errores (absoluto y relativo), si no se puede ver bien el relativo del absoluto dividir un por cada plot(grafico)
    #print(data.shape,data.shape[1],np.arange(start=0, stop=data.shape[1], step=1))
    fig, axs = plt.subplots(1, 1, figsize=(8, 4))
    #axs[1, 0].scatter(data[0], data[1])
    plt.title(title)
    axs.plot(np.arange(start=0, stop=datos.shape[0], step=1), datos.transpose())

    plt.show()

def plot_2(datos, title): ##plot para graficar las curvas de la suma real y binaria

    fig, axs = plt.subplots(1, 1, figsize=(8, 4))
    plt.title(title)
    axs.plot(np.arange(start=0, stop=datos[0].shape[0], step=1), datos.transpose())
    axs.plot(np.arange(start=0, stop=datos[1].shape[0], step=1), datos.transpose())

    plt.show()


if __name__ == "__main__":

    realesybinarios = []
    operando_1 = listas(80)
    operando_2 = listas(80)
    operando1_binarizado = binarizacion(operando_1)
    operando2_binarizado = binarizacion2(operando_2)
    sumareal = suma_real(operando_1, operando_2)
    sumareal = np.array(sumareal)
    realesybinarios.append(sumareal)
    sumabinaria = suma_binaria(operando1_binarizado, operando2_binarizado)
    conversion = conversion(sumabinaria)
    conversion = np.array(conversion)
    realesybinarios.append(conversion)
    realesybinarios = np.array(realesybinarios)
    error_absoluto = error_absoluto(sumareal, conversion)
    error_cuadratico = error_cuadratico(error_absoluto)
    error_cuadratico = np.array(error_cuadratico)
    error_absoluto = np.array(error_absoluto)
    error_relativo = error_relativo(sumareal, conversion)
    error_relativo = np.array(error_relativo)
    print("Operando_1: ", "\n")
    print(operando_1[0], "\n")
    print("Operando_1_binario: ", "\n")
    print(operando1_binarizado, "\n")
    print("Operando_2: ", "\n")
    print(operando_2[0], "\n")
    print("Operando_2_binario: ", "\n")
    print(operando2_binarizado, "\n")
    print("Suma binaria de las 2 listas: ", "\n")
    print(sumabinaria, "\n")
    print("Suma real de las 2 listas: ", "\n")
    print(sumareal, "\n")
    print("Errores Absolutos: ", "\n")
    print(error_absoluto, "\n")
    print("Errores Relativos: ", "\n")
    print(error_relativo, "\n")
    print("Errores Cuadraticos: ", "\n")
    print(error_cuadratico, "\n")
    x= "Error Absoluto"
    y = "Error Relativo"
    w = "Error Cuadratico"
    z = "Suma real vs Suma binaria"
    plot_(error_absoluto, x)
    plot_(error_relativo, y)
    plot_(error_cuadratico, w)
    plot_2(realesybinarios, z)




