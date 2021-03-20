import numpy as np 
import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio 
import random
import time 

#Generador de numeros aleatorios randu de 0 a 1
def randu(N):
    
    x = 3 #semilla
    a = 2**16 + 3
    c = 0
    m = 2**31
    random_num = np.zeros(N)
    for i in range(N):
        x_new = (a*x + c) % m
        random_num[i] = x_new
        x = x_new
    return random_num/np.max(random_num)

#Funcion para guardar los titulos de manera aleatoria 
# en el vector de cajones con un generador twister o "LSG propio"
def secuencia_random(titulos, generator = "twister", ifi_selection = False):
    indices_pasados = list()
    titulos_copy = titulos.copy() #creando una copia de los titulos
    cajones = list() #Lista donde seran guardados los titulos
    count_randu = 0
    if generator == "randu":
        randu_list = randu(2000) #Creamos una secuencia de 2000 con el generador lsg

    while len(titulos_copy) > 0: 
        #Salir de la rutina si un estudiante IFI ya selecciono un 
        #maximo de 98 cajones 
        if len(cajones) == 98 and ifi_selection == True:
            break
        #Eligiendo el generador de numeros aleatorios ... 
        if generator == "twister":
            #Checar que el indice_random  no sea igual a la longitud del vector titulos
            indice_random = len(titulos)
            while indice_random >= len(titulos):
                #Generando un indice random y redondeando con los funcion floor
                indice_random = np.floor(np.random.rand()* len(titulos)).astype('int32')
        elif generator == "randu":
            #Si el usuario elige la opcion de randu, entonces ...
            indice_random = len(titulos)
            while indice_random >= len(titulos):
                indice_random = np.floor(randu_list[count_randu]*len(titulos)).astype('int32')
                count_randu += 1

        #En la primera iteracion cualquier indice random es aceptado para guardar un titulo en el cajon i 
        if len(cajones) == 0:
            cajones.append(titulos[indice_random])
            indices_pasados.append(indice_random)
            titulos_copy = np.delete(titulos_copy,indice_random)
        else:
            #Checando que el nuevo indice random no haya sido generado previamente 
            try:
                indices_pasados.index(indice_random) #El indice_random esta dentro de la lista ?
            except:

                #Si el indice random no esta en la lista de indices pasados,
                #entonces se ejecutara el siguiete codigo
                cajones.append(titulos[indice_random])    
                indices_pasados.append(indice_random)
                #Borrando el elemento del vector titulos_copy....
                index_to_delete = np.nonzero(titulos_copy == titulos[indice_random])
                titulos_copy = np.delete(titulos_copy,index_to_delete)
    return np.array(cajones)

#ifis -> Vector que guarda el estado del IFI numero n
N = 100 #Cantidad de ifis
exitos_B = 0
N_exp = 100 #Repeticiones de los experimentos
ifis = np.linspace(1,N,N, dtype=bool)
ifis[0:] = False #Todos los IFIs tienen un estado False, ya que aun no tienen su titulo 

etiquetas_ifi = np.linspace(0,N-1,N).astype('int32') #Titulos y etiquetas de los ifis enumerados del 0-99 
print("Titulos con etiquetas del 0 al 99 --> \n",etiquetas_ifi,"\n")  
cajones = secuencia_random(etiquetas_ifi) #Titulos guardados en los cajones de manera aleatoria 
print("Cajones con los titulos guardados aleatoriamente --> \n",cajones) 

#......................Primer esquema, cada IFI abririra 98 cajones..................
#Repitiendo el experimento N_exp veces 
def esquema_a(mode = "twister"):

    exitos_A = 0  #numero de exitos
    start_1 = time.time()
    cajones_1 = cajones.copy()

    for i in range(N_exp):
        #los indices de los cajones van de 0 a 99
        for ifi_number in range(N):
            #ifi_selection=True da una secuencia aleatoria para abrir 98 cajones 
            if mode == "randu":
                indices_cajones_abiertos = secuencia_random(etiquetas_ifi, generator = mode, ifi_selection = True) 
            else:
                indices_cajones_abiertos = random.sample(range(N),98)  #secuencia random de los 98 cajones que se abriran  
            #ABRIENDO CAJONES...
            titulos_encontrados = cajones_1[indices_cajones_abiertos]
            #Revisaremos si en alguno de los cajones abiertos el IFI logro encontrar su titulo ...
            etiqueta_del_titulo_encontrado = np.nonzero(titulos_encontrados == ifi_number)
            #Si el titulo del ifi fue encontrado, entonces asignaremos un estado de True al ifi ...
            if len(etiqueta_del_titulo_encontrado[0]) != 0:
                ifis[ifi_number] = True

        checando_exp = np.nonzero(ifis == True)
        #Si todos los ifis encontraron su titulo sumaremos 1 a nuestros exitos
        if len(checando_exp[0]) == N:
            exitos_A += 1
            
        ifis[0:] = False #Reiniciando el experimento
        cajones_1 = secuencia_random(etiquetas_ifi)

    final_1 = time.time() #tomado el tiempo de ejecuccion

    print("\n # Exitos del experimento_A = ",exitos_A)
    print("Tiempo de ejecucion del experimento_A = ", final_1 - start_1," s")
    return exitos_A
    
exitos_A = esquema_a()


#........Segundo esquema, cada IFI abrira 50 canjones ..................
N_caj = 50 #Cajones permitidos 
cajones_2 = cajones.copy()

#midiendo tiempo de ejecucion del experimento 2
start_2 = time.time()

for i in range(N_exp):
    #Abrir el cajón asignado al número de ifi correspondiente
    for ifi_number in range(N):
        #Abrir el cajón asignado al número de ifi correspondiente
        titulo_encontrado = cajones_2[ifi_number] #primer cajon abierto
        for j in range(N_caj):
            #Revisamos si el titulo encontrado es el correcto
            if titulo_encontrado == ifi_number:
                #Cambiamos el estado del ifi a True
                ifis[ifi_number] = True
                break #El ifi puede dejar de buscar
            else:
                #En caso de no encontrar el titulo, se abrira el cajon
                #que corresponde al numero de titulo encontrado
                titulo_encontrado = cajones_2[titulo_encontrado]

    #Revisamos si el experimento fue exitoso
    checando_exp_b = np.nonzero(ifis == True)
    if len(checando_exp_b[0]) == N:
        exitos_B += 1

    ifis[0:] = False #Reiniciamos el experimento 
    cajones_2 = secuencia_random(etiquetas_ifi)

final_2 = time.time()
print("\n # Exitos del experimento B = ",exitos_B)   
print("Tiempo de ejecucion de experimento_B = ", final_2 - start_2,"s")

#Calculando las probabilidades de exito
print("\n------------------Probabilidades de exito de los experimentos----------------------------------")
print("\nProbabilidad de exito del experimento_A_twister =", 100*exitos_A/N_exp)
print("Probabilidad de exito del experimento_B =", 100*exitos_B/N_exp, "% \n")

print("--------------------------Corriendo el experimento A corriendo con un generador Randu... -------------------- \n")
exitos_a_randu = exitos_A = esquema_a(mode = 'randu')
print("Probabilidad de exito del experimento_A_randu =", 100*exitos_a_randu/N_exp, "% \n")