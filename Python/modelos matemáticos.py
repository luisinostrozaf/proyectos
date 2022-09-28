#AUTOR: LUIS INOSTROZA FLORES
import numpy as np
import matplotlib.pyplot as plt
valores_finales = []
iteraciones_finales = []
#funciones de primera linea f y g

def f(x): # a = 3
    y= (x**3)/3 + (x**2)/2 + 2*x - 15 - 9/2
    return y
def f_prima(x):
    y= x**2 + x + 2
    return y
def f_prima_prima(x):
    y= 2*x + 1
    return y

#apartado punto fijo
def g(x):
    y = (4*x**4+ 2*x**3+ x**2+1.0)/3.0 #-3*x 
    return y

def g_prima(x):
    y= (16*x**3+6*x**2+2*x)/3.0
    return y

#algoritmos previos a punto fijo
def biseccion(a,b,valor_cifras_significativas): #tarea chica que ira despues a evaluacion 
    an = a
    bn = b
    pn_ant=0
    P_sub_n = float((an+bn)/2)
    i=0

    while (error_absoluto(P_sub_n,pn_ant) > valor_cifras_significativas ):
        if (f(an) * f(P_sub_n) > 0):
            an=P_sub_n
        elif( f(bn) * f(P_sub_n) > 0):
            bn = P_sub_n
        pn_ant = P_sub_n
        i+=1
        P_sub_n = float((an+bn)/2)
    global valores_finales
    valores_finales.append(P_sub_n)
    global iteraciones_finales
    iteraciones_finales.append(i)
    return {"valor biseccion":P_sub_n,"iteracion":i,"cifras_significativas":valor_cifras_significativas}

def falsa_posicion(a,b,valor_cifras_significativas): 
    an = a
    bn = b
    pn_ant = 0
    P_sub_n = bn - ((f(bn)*(bn - an)) / ( f(bn) -  f(an)))
    i=0

    while (error_absoluto(P_sub_n,pn_ant) > valor_cifras_significativas ):
        if (f(an) * f(P_sub_n) > 0):
            an=P_sub_n
        elif( f(bn) * f(P_sub_n) > 0):
            bn = P_sub_n
        pn_ant = P_sub_n
        i+=1
        P_sub_n = bn - ((f(bn)*(bn - an)) / ( f(bn) -  f(an)))
    global valores_finales
    valores_finales.append(P_sub_n)
    global iteraciones_finales
    iteraciones_finales.append(i)
    return {"valor falsa posicion":P_sub_n,"iteracion":i,"cifras_significativas":valor_cifras_significativas}


def punto_fijo_1condicion(a,b):#teorema de biseccion
    g_a= g(a)
    g_b= g(b)
    if( a< g_b  and  g_b < b ) and ( a< g_a  and  g_a < b):
        print("cumple primera condicion")
        return 1
    else:
        print("no cumple primera condicion")
        return 0

def punto_fijo_2condicion(a,b,tamanio_de_pasos):#continuidad con la derivada
    for h in (a,b,tamanio_de_pasos):
        
        if(g_prima(h)== np.nan or g_prima(h)==None):
            print("No cumple con segunda condicion")
            return 0
    print("cumple con segunda condicion")
    return 1 

def punto_fijo(a,b,tamanio_de_pasos):
    condicion_1=punto_fijo_1condicion(a,b)
    condicion_2=punto_fijo_2condicion(a,b,tamanio_de_pasos)
    x=a
    for i in range(0,100):
        print(x,g(x),abs(x-g(x)))
        x=g(x)

    return "FIN"

#metodo iterativos
def Newton_raphson(P_sub_0, valor_cifras_significativas):
    P_sub_n=P_sub_0
    pn_ant = 0
    i=0
    while (error_absoluto(P_sub_n,pn_ant) > valor_cifras_significativas ):
        pn_ant = P_sub_n
        P_sub_n=(P_sub_n- (1/f_prima(P_sub_n) )*f(P_sub_n) )
        i+=1
    global valores_finales
    valores_finales.append(P_sub_n)
    global iteraciones_finales
    iteraciones_finales.append(i)
    return {"valor newton raphson":P_sub_n,"iteracion":i,"cifras_significativas":valor_cifras_significativas}

def Secante(P_sub_0,P_sub_1,num_iteraciones):
    P_sub_n1=P_sub_0
    P_sub_n2=P_sub_1
    for i in range(0,num_iteraciones):
        if(((f(P_sub_n2)-f(P_sub_n1)))* f(P_sub_n1) != 0.0):
            print(P_sub_n1,P_sub_n2, P_sub_n1- ((P_sub_n2-P_sub_n1)/(f(P_sub_n2)-f(P_sub_n1)))* f(P_sub_n1))
            aux=P_sub_n2
            P_sub_n2=P_sub_n1- ((P_sub_n2-P_sub_n1)/(f(P_sub_n2)-f(P_sub_n1)))* f(P_sub_n1)
            P_sub_n1=aux

def division_sintetica(grado,pn):
    #4*x**4+ 2*x**3+ x**2+3*x+1.0
    coef= [4.0,2.0,1.0,3.0,1.0]# ESTOS SON LOS COEF ORDENADOS PARA EL METODO DE HORNE
    coef_segundos=[0]
    coef_nuevos=[]
    for i in range(0,len(coef)):
        coef_nuevos.append((coef[i] + coef_segundos[len(coef_segundos)-1]))
        coef_segundos.append(coef_nuevos[len(coef_nuevos)-1]*pn)

    #print(coef)
    #print(coef_segundos)
    #print("---------------------------!!!",pn)
    #print(coef_nuevos)
    return coef_nuevos

def horner(P0,num_iteraciones):
    pn=float(P0)
    grado=4
    print(pn)
    for i in range(0,num_iteraciones):
        div_sintetica=[]
        div_sintetica = division_sintetica(grado,pn)
        Q = div_sintetica[0:len(div_sintetica)-1]
        resto = div_sintetica[len(div_sintetica)-1]+ 0.0
        resultado_Q = 0.0
        for i in range(0, len(Q)):
            resultado_Q = Q[i]*(pn**(len(Q)-i-1))+ resultado_Q 
        #print("b0:",resto)
        pn = pn - (resto / resultado_Q)
        print(pn)
    return pn

def horner_1(P0,valor_cifras_significativas):
    pn=float(P0)
    grado=4
    pn_anterior=0
    i=0
    """Para verificar el valor absoluto en vez de hacer una cantidad n de iteraciones"""
    while (error_absoluto(pn,pn_anterior) > valor_cifras_significativas ):
        
        div_sintetica=[]
        div_sintetica = division_sintetica(grado,pn)
        Q = div_sintetica[0:len(div_sintetica)-1]
        resto = div_sintetica[len(div_sintetica)-1]+ 0.0
        resultado_Q = 0.0
        for i in range(0, len(Q)):
            resultado_Q = Q[i]*(pn**(len(Q)-i-1))+ resultado_Q 
        #print("b0:",resto)
        """Agregue una var auxiliar para el valor absoluto"""
        pn_anterior=pn
        pn = pn - (resto / resultado_Q)
        i+=1
    global valores_finales
    valores_finales.append(pn)
    global iteraciones_finales
    iteraciones_finales.append(i)
    return {"valor horner_1":pn,"iteracion":i,"cifras_significativas":valor_cifras_significativas}

def N_R_mejorado(P0,valor_cifras_significativas):
    pn_anterior = 0
    i=0
    pn=P0
    while (error_absoluto(pn,pn_anterior) > valor_cifras_significativas ):
        pn_anterior = pn
        pn= pn -  (f(pn)*f_prima(pn))/ ( f_prima(pn)**2  - f(pn)*f_prima_prima(pn))
        i+=1
    global valores_finales
    valores_finales.append(pn)
    global iteraciones_finales
    iteraciones_finales.append(i)
    return {"valor n_r mejorado":pn,"iteracion":i,"cifras_significativas":valor_cifras_significativas}

def steffesen(P0):
    x0=P0
    for i in range(0,5):
        print(  x0 - (x0-g(x0))**2 / (g(g(x0)) - 2*g(x0) + x0)   )
        x0=  x0 - (x0-g(x0))**2 / (g(g(x0)) - 2*g(x0) + x0) 

def error_absoluto(valor_real, valor_cifras_significativas):
    #| real - punto flotante|
    return np.absolute((valor_real-valor_cifras_significativas))

#graficos

def mostrar_grafica(datos):
    fig, axs = plt.subplots(1, 1, figsize=(8, 4))
    axs.plot(['Bisección','Falsa Posición','Newton Raphson','Horner','N_R Mejorado'],datos,marker="o", color="red")
    plt.show()

def mostrar_grafica2(datos):
    fig, axs = plt.subplots(1, 1, figsize=(8, 4))
    axs.plot(['Bisección','Falsa Posición','Newton Raphson','Horner','N_R Mejorado'],datos,marker="o", color="blue")
    plt.show()



az = biseccion(-2,0,0.000001)
print(az)
fp=falsa_posicion(-5,5,0.000001)
print(fp)
#steffesen(1)
#N_R_mejorado(1)
#P_sub_0 = -1.2
#P_sub_1 = -1.0
#print("Newton rapshon")
print(Newton_raphson(-1.2,0.000001))
#print("secante")
#print(Secante(P_sub_0,P_sub_1,10))
#print("steffesen")
#steffesen(P_sub_0)
#print("steffesen")
print(N_R_mejorado(-1.2,0.000001))
print(horner_1(-1,0.000001))
print(valores_finales)
print(iteraciones_finales)
mostrar_grafica(valores_finales)
mostrar_grafica2(iteraciones_finales)
